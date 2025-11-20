"""
Main entry point for the UAV Deconfliction System.
"""
import sys
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main function."""
    logger.info("UAV Deconfliction System initialized")
    print("System ready. Run tests or examples to verify setup.")


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


if __name__ == "__main__":
    if "--test-load" in sys.argv:
        test_stage_2_loading()
    else:
        main()

