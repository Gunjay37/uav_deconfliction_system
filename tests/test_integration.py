from src.query.deconfliction_api import check_mission_conflicts
from src.data.loader import load_missions, load_simulated_flights


def test_full_pipeline():
    missions = load_missions("data/sample_missions.json")
    flights = load_simulated_flights("data/simulated_flights.json")

    # Pick mission 2 (which conflicts)
    result = check_mission_conflicts(
        missions_path="data/sample_missions.json",
        flights_path="data/simulated_flights.json",
        mission_id="mission_2"
    )

    assert result["status"] in ["clear", "conflict_detected"]
    assert isinstance(result["total_conflicts"], int)
    assert "conflicts" in result
