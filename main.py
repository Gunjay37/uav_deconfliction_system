"""
Main entry point for UAV Deconfliction System
"""

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
from src.visualization.plotter_2d import plot_2d_static
# from src.visualization.plotter_2d import animate_2d  # If you want animation


def main():

    parser = argparse.ArgumentParser(description="UAV Deconfliction System")
    parser.add_argument("--mission", type=str, help="Run conflict check for a mission ID")
    parser.add_argument("--scenario", type=str, help="Run a scenario from scenarios.json")
    parser.add_argument("--visualize", action="store_true", help="Show 2D visualization")
    parser.add_argument("--animate", action="store_true", help="Run animation")
    args = parser.parse_args()

    # =========================================================
    # 1️⃣ RUN SCENARIO MODE
    # =========================================================
    if args.scenario:
        result = run_scenario(
            scenarios_path="data/scenarios.json",
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            scenario_id=args.scenario
        )

        print("\n--- Scenario Result ---")
        print(result)

        # Visualization
        if args.visualize:
            missions = load_missions("data/sample_missions.json")
            flights = load_simulated_flights("data/simulated_flights.json")

            mission_id = result["raw_output"]["mission_id"]
            mission = next(m for m in missions if m.mission_id == mission_id)

            plot_2d_static(mission, flights, conflicts=result["raw_output"]["conflicts"])

        return

    # =========================================================
    # 2️⃣ RUN MISSION MODE
    # =========================================================
    if args.mission:
        # Load mission & flights
        missions = load_missions("data/sample_missions.json")
        flights = load_simulated_flights("data/simulated_flights.json")

        result = check_mission_conflicts(
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            mission_id=args.mission
        )

        print("\n--- Mission Check Result ---")
        print(result)

        # Visualization
        if args.visualize:
            mission = next(m for m in missions if m.mission_id == args.mission)
            plot_2d_static(mission, flights, conflicts=result["conflicts"])

        return

    # If no args passed
    print("Run with:")
    print("  python main.py --scenario scenario_2 --visualize")
    print("  python main.py --mission mission_2 --visualize")


if __name__ == "__main__":
    main()
