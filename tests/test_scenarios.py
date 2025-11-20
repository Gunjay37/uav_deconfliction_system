from src.query.deconfliction_api import run_scenario
from src.data.loader import load_test_scenarios


def test_all_scenarios_run():
    scenarios = load_test_scenarios("data/scenarios.json")

    for s in scenarios:
        result = run_scenario(
            missions_path="data/sample_missions.json",
            flights_path="data/simulated_flights.json",
            scenarios_path="data/scenarios.json",
            scenario_id=s.id
        )

        assert "actual_status" in result
        assert "expected_status" in result
        assert "match" in result
        assert result["match"] in [True, False]  # at least valid
