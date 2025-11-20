"""
Main entry point for the UAV Deconfliction System.
"""
import sys
from src.utils.logger import get_logger
from src.query.deconfliction_api import check_mission_conflicts, run_scenario

logger = get_logger(__name__)


def main():
    """Main system help message."""
    logger.info("UAV Deconfliction System initialized")
    print("\nUAV Deconfliction System")
    print("Usage:")
    print("  python main.py --test-load")
    print("  python main.py --check <mission_id>")
    print("  python main.py --scenario <scenario_id>")
    print("Example:")
    print("  python main.py --check mission_1")
    print("  python main.py --scenario scenario_2\n")


# ------------ Existing Stage 2 Loader Test ------------
def test_stage_2_loading():
    """Temporary data loading test."""
    from src.data.loader import (
        load_missions,
        load_simulated_flights,
        load_test_scenarios
    )

    missions = load_missions("data/sample_missions.json")
    flights = load_simulated_flights("data/simulated_flights.json")
    scenarios = load_test_scenarios("data/scenarios.json")

    print("\n--- Missions Loaded ---")
    for m in missions:
        print(m)

    print("\n--- Simulated Flights Loaded ---")
    for d in flights.drones:
        print(d)

    print("\n--- Scenarios Loaded ---")
    for s in scenarios:
        print(s)

    print("\n--- Segments (from first mission) ---")
    print(missions[0].drone.to_segments())


# ------------ New Stage 6 Handlers ------------
def handle_args():
    """Parse CLI arguments for Stage 6."""
    args = sys.argv

    # Keep Stage 2 test-load
    if "--test-load" in args:
        test_stage_2_loading()
        return

    # Mission check
    if "--check" in args:
        idx = args.index("--check")
        mission_id = args[idx + 1]
        result = check_mission_conflicts(
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            mission_id=mission_id,
        )
        print("\n--- Deconfliction Result ---")
        print(result)
        return

    # Scenario execution
    if "--scenario" in args:
        idx = args.index("--scenario")
        scenario_id = args[idx + 1]
        result = run_scenario(
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            scenarios_path="data/scenarios.json",
            scenario_id=scenario_id,
        )
        print("\n--- Scenario Result ---")
        print(result)
        return

    # Default help
    main()


if __name__ == "__main__":
    handle_args()
