"""
Main entry point for UAV Deconfliction System
"""
import logging
logging.getLogger("PIL").setLevel(logging.WARNING)  # silence pillow
logging.getLogger("matplotlib").setLevel(logging.CRITICAL)  # silence mpl
logging.getLogger("matplotlib.font_manager").setLevel(logging.CRITICAL)  # silence font scans
import argparse
from src.data.loader import (
    load_missions,
    load_simulated_flights,
    load_test_scenarios
)
from src.query.deconfliction_api import (
    check_mission_conflicts,
    run_scenario
)
from src.visualization.plotter_2d import plot_2d_static, animate_2d
from src.visualization.plotter_3d import plot_3d_static, animate_3d

from src.utils.random_flights import generate_random_flight_schedule
from src.core.conflict_resolver import resolve_conflicts_for_mission
from src.utils.config import get_config

# NEW: altitude modification utilities
from src.utils.mission_modifiers import slope_mission_altitude



# =====================================================
# Dynamic Airspace Generator
# =====================================================

def run_dynamic_airspace(visualize_all=False):
    """
    Run dynamic scenario:
    - Main mission fixed (MISSION_2)
    - Five random drones generated
    - Full visualization pipeline if visualize_all=True
    """

    MAIN_MISSION_ID = "mission_2"

    missions = load_missions("data/sample_missions.json")
    main_mission = next(m for m in missions if m.mission_id == MAIN_MISSION_ID)

    # Apply altitude slope (NEW)
    main_mission = slope_mission_altitude(main_mission, start_z=10, end_z=40)

    print(f"\nLoaded main mission: {MAIN_MISSION_ID}")

    # Generate 5 random flights
    t_start, t_end = main_mission.time_window
    schedule = generate_random_flight_schedule(
        num_drones=5,
        area_size=150.0,
        t_min=t_start,
        t_max=t_end
    )

    print("Generated 5 random flights in the airspace.")

    # Conflict detection
    config = get_config()
    result = resolve_conflicts_for_mission(
        mission=main_mission,
        schedule=schedule,
        safety_buffer=config.SAFETY_BUFFER_DISTANCE,
        num_samples=config.NUM_SAMPLES,
    )

    print("\n--- Dynamic Airspace Conflict Check ---")
    print("Status         :", result["status"])
    print("Total Conflicts:", result["total_conflicts"])
    for c in result["conflicts"]:
        print(
            f"- Conflict w/ {c['other_drone_id']} at "
            f"(x={c['location']['x']:.1f}, y={c['location']['y']:.1f}, z={c['location']['z']:.1f}), "
            f"t≈{c['conflict_time']:.1f}, d≈{c['min_distance']:.1f}m"
        )

    # Run full visualization pipeline
    print("\n\n=== Running 2D Static Visualization ===")
    plot_2d_static(main_mission, schedule, conflicts=result["conflicts"])

    if visualize_all:
        print("\n=== Running 2D Animation ===")
        animate_2d(main_mission, schedule, conflicts=result["conflicts"])

        print("\n=== Running 3D Static Visualization ===")
        plot_3d_static(main_mission, schedule, conflicts=result["conflicts"])

        print("\n=== Running 4D (3D Animated) Visualization ===")
        animate_3d(main_mission, schedule, conflicts=result["conflicts"])



# =====================================================
# Main
# =====================================================

def main():

    parser = argparse.ArgumentParser(description="UAV Deconfliction System")

    parser.add_argument("--mission", type=str, help="Run conflict check for a mission ID")
    parser.add_argument("--scenario", type=str, help="Run predefined scenario from scenarios.json")
    parser.add_argument("--dynamic", action="store_true", help="Run dynamic random airspace mode")
    parser.add_argument("--visualize", action="store_true", help="Run only 2D visualization")
    parser.add_argument("--visualize_all", action="store_true", help="Run 2D, 3D, and 4D visualizations in sequence")

    args = parser.parse_args()

    # =====================================================
    # Dynamic Airspace Mode
    # =====================================================
    if args.dynamic:
        run_dynamic_airspace(visualize_all=args.visualize_all)
        return

    # =====================================================
    # Scenario Mode
    # =====================================================
    if args.scenario:
        result = run_scenario(
            scenarios_path="data/scenarios.json",
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            scenario_id=args.scenario
        )

        print("\n--- Scenario Result ---")
        print(result)

        missions = load_missions("data/sample_missions.json")
        flights = load_simulated_flights("data/simulated_flights.json")
        mission_id = result["raw_output"]["mission_id"]
        mission = next(m for m in missions if m.mission_id == mission_id)

        # Apply altitude slope (NEW)
        mission = slope_mission_altitude(mission, start_z=10, end_z=40)

        # Always 2D static
        plot_2d_static(mission, flights, conflicts=result["raw_output"]["conflicts"])

        if args.visualize_all:
            animate_2d(mission, flights, conflicts=result["raw_output"]["conflicts"])
            plot_3d_static(mission, flights, conflicts=result["raw_output"]["conflicts"])
            animate_3d(mission, flights, conflicts=result["raw_output"]["conflicts"])

        return

    # =====================================================
    # Mission Mode
    # =====================================================
    if args.mission:

        missions = load_missions("data/sample_missions.json")
        flights = load_simulated_flights("data/simulated_flights.json")

        result = check_mission_conflicts(
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            mission_id=args.mission
        )

        print("\n--- Mission Check Result ---")
        print(result)

        mission = next(m for m in missions if m.mission_id == args.mission)

        # Apply altitude slope (NEW)
        mission = slope_mission_altitude(mission, start_z=10, end_z=40)

        # Always 2D static
        plot_2d_static(mission, flights, conflicts=result["conflicts"])

        if args.visualize_all:
            animate_2d(mission, flights, conflicts=result["conflicts"])
            plot_3d_static(mission, flights, conflicts=result["conflicts"])
            animate_3d(mission, flights, conflicts=result["conflicts"])

        return

    # Usage help
    print("Usage examples:")
    print("  python main.py --scenario scenario_2 --visualize_all")
    print("  python main.py --mission mission_2 --visualize_all")
    print("  python main.py --dynamic --visualize_all")


if __name__ == "__main__":
    main()
