"""
Dynamic Airspace Scenario:
- Main mission = mission_2 (fixed)
- 5 random flights generated each run
- Run conflict detection between mission_2 and random schedule
- Visualize in unified 2D plot
"""

from src.data.loader import load_missions
from src.utils.random_flights import generate_random_flight_schedule
from src.core.conflict_resolver import resolve_conflicts_for_mission
from src.utils.config import get_config
from src.visualization.plotter_2d import plot_2d_static


def main():
    # ----------------------------------------
    # 1) Load main mission (fixed)
    # ----------------------------------------
    MAIN_MISSION_ID = "mission_2"

    missions = load_missions("data/sample_missions.json")
    main_mission = next(m for m in missions if m.mission_id == MAIN_MISSION_ID)

    print(f"\nLoaded main mission: {MAIN_MISSION_ID}")

    # ----------------------------------------
    # 2) Generate random airspace flights
    # ----------------------------------------
    # Use same time window as mission for overlap
    t_start, t_end = main_mission.time_window
    schedule = generate_random_flight_schedule(
        num_drones=5,
        area_size=150.0,
        t_min=t_start,
        t_max=t_end,
    )

    print("Generated 5 random flights in the airspace.")

    # ----------------------------------------
    # 3) Run conflict detection
    # ----------------------------------------
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
            f"- Conflict with {c['other_drone_id']} at "
            f"(x={c['location']['x']:.1f}, y={c['location']['y']:.1f}, z={c['location']['z']:.1f}), "
            f"t≈{c['conflict_time']:.1f}, d≈{c['min_distance']:.1f}m"
        )

    # ----------------------------------------
    # 4) Visualize
    # ----------------------------------------
    plot_2d_static(
        mission=main_mission,
        schedule=schedule,
        conflicts=result["conflicts"],
    )


if __name__ == "__main__":
    main()
