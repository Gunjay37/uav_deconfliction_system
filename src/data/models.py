from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class Waypoint:
    id: int
    x: float
    y: float
    z: float
    t: float  # timestamp


@dataclass
class Drone:
    """
    Represents ANY drone flight (simulated or mission).
    """
    drone_id: str
    name: str
    description: str
    waypoints: List[Waypoint]

    def to_segments(self) -> List[Tuple[Tuple[float, float, float],
                                       Tuple[float, float, float],
                                       float, float]]:
        """
        Converts waypoints to straight-line time-parameterized segments.
        Returns list of:
        (start_xyz, end_xyz, start_time, end_time)
        """
        segments = []
        if len(self.waypoints) < 2:
            return segments

        for wp1, wp2 in zip(self.waypoints[:-1], self.waypoints[1:]):
            if wp2.t <= wp1.t:
                # Invalid segment (non-increasing time)
                continue

            start = (wp1.x, wp1.y, wp1.z)
            end = (wp2.x, wp2.y, wp2.z)
            segments.append((start, end, wp1.t, wp2.t))

        return segments


@dataclass
class Mission:
    mission_id: str
    name: str
    description: str
    time_window: Tuple[float, float]
    drone: Drone


@dataclass
class FlightSchedule:
    """
    Represents all simulated drone flights.
    """
    drones: List[Drone]


@dataclass
class TestScenario:
    id: str
    name: str
    description: str
    primary_mission_id: str
    expected_result: str
    expected_conflicts: int
    conflict_details: Optional[dict] = None
