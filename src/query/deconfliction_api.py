"""
High-level Query API for UAV Deconfliction System.
"""

from typing import Dict, List
from src.utils.logger import get_logger
from src.utils.config import get_config

from src.core.conflict_resolver import resolve_conflicts_for_mission
from src.data.models import Mission, FlightSchedule
from src.data.loader import load_missions, load_simulated_flights, load_test_scenarios

logger = get_logger(__name__)


def get_mission_by_id(missions: List[Mission], mission_id: str) -> Mission:
    for m in missions:
        if m.mission_id == mission_id:
            return m
    raise ValueError(f"Mission with ID '{mission_id}' not found")


def check_mission_conflicts(
    missions_path: str,
    flights_path: str,
    mission_id: str,
) -> Dict:
    """
    Public API: Check conflicts for a single mission.
    """
    config = get_config()

    missions = load_missions(missions_path)
    flights = load_simulated_flights(flights_path)

    mission = get_mission_by_id(missions, mission_id)

    return resolve_conflicts_for_mission(
        mission=mission,
        schedule=flights,
        safety_buffer=config.SAFETY_BUFFER_DISTANCE,
        num_samples=config.NUM_SAMPLES,
    )


def run_scenario(
    missions_path: str,
    flights_path: str,
    scenarios_path: str,
    scenario_id: str,
) -> Dict:
    """
    Public API: Run a scenario defined in scenarios.json.
    """
    scenarios = load_test_scenarios(scenarios_path)

    scenario = None
    for s in scenarios:
        if s.id == scenario_id:
            scenario = s
            break

    if scenario is None:
        raise ValueError(f"Scenario '{scenario_id}' not found")

    result = check_mission_conflicts(
        missions_path,
        flights_path,
        scenario.primary_mission_id,
    )

    return {
        "scenario_id": scenario.id,
        "scenario_name": scenario.name,
        "expected_status": scenario.expected_result,
        "actual_status": result["status"],
        "match": scenario.expected_result == result["status"],
        "raw_output": result
    }
