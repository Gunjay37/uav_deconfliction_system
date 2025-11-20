import json
from pathlib import Path
from typing import List

from .models import (
    Waypoint,
    Drone,
    Mission,
    FlightSchedule,
    TestScenario
)

# ---------------- Validation ----------------

def validate_waypoint(wp: dict):
    required = ["id", "x", "y", "timestamp"]
    for key in required:
        if key not in wp:
            raise ValueError(f"Waypoint missing required field: '{key}'")

    # numerical checks
    float(wp["x"])
    float(wp["y"])
    float(wp["timestamp"])
    if "z" in wp:
        float(wp["z"])


def load_waypoints(raw_wps: List[dict]) -> List[Waypoint]:
    waypoints = []
    for wp in raw_wps:
        validate_waypoint(wp)
        waypoints.append(
            Waypoint(
                id=int(wp["id"]),
                x=float(wp["x"]),
                y=float(wp["y"]),
                z=float(wp.get("z", 0.0)),
                t=float(wp["timestamp"])
            )
        )
    return waypoints


# ---------------- Mission Loader ----------------

def load_missions(path: str | Path) -> List[Mission]:
    data = json.loads(Path(path).read_text())

    missions = []
    for m in data["missions"]:
        mission_id = m["id"]
        name = m["name"]
        desc = m["description"]
        tw = m["time_window"]

        wp = load_waypoints(m["waypoints"])

        drone = Drone(
            drone_id=mission_id,
            name=name,
            description=desc,
            waypoints=wp
        )

        missions.append(
            Mission(
                mission_id=mission_id,
                name=name,
                description=desc,
                time_window=(tw["start_time"], tw["end_time"]),
                drone=drone
            )
        )

    return missions


# ---------------- Other Flights Loader ----------------

def load_simulated_flights(path: str | Path) -> FlightSchedule:
    data = json.loads(Path(path).read_text())

    drones = []
    for f in data["flights"]:
        drone_id = f["id"]
        name = f["name"]
        desc = f["description"]
        wp = load_waypoints(f["waypoints"])

        drones.append(
            Drone(
                drone_id=drone_id,
                name=name,
                description=desc,
                waypoints=wp
            )
        )

    return FlightSchedule(drones=drones)


# ---------------- Scenario Loader ----------------

def load_test_scenarios(path: str | Path) -> List[TestScenario]:
    data = json.loads(Path(path).read_text())

    scenarios = []
    for s in data["test_scenarios"]:
        scenarios.append(
            TestScenario(
                id=s["id"],
                name=s["name"],
                description=s["description"],
                primary_mission_id=s["primary_mission_id"],
                expected_result=s["expected_result"],
                expected_conflicts=s["expected_conflicts"],
                conflict_details=s.get("conflict_details", None)
            )
        )

    return scenarios
