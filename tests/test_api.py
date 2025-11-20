from src.query.deconfliction_api import check_mission_conflicts, run_scenario


def test_check_mission_conflicts_basic():
    """
    Ensure API runs without crashing and returns expected keys.
    """
    result = check_mission_conflicts(
        missions_path="data/sample_missions.json",
        flights_path="data/simulated_flights.json",
        mission_id="mission_1"
    )

    assert "status" in result
    assert "total_conflicts" in result
    assert "conflicts" in result


def test_run_scenario_2():
    """
    Scenario 2 has exactly one conflict.
    """
    scenario_result = run_scenario(
        missions_path="data/sample_missions.json",
        flights_path="data/simulated_flights.json",
        scenarios_path="data/scenarios.json",
        scenario_id="scenario_2"
    )

    assert scenario_result["expected_status"] == "conflict_detected"
    assert scenario_result["actual_status"] == "conflict_detected"
    assert scenario_result["match"] is True
