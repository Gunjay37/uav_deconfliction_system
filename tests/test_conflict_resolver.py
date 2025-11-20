from src.data.models import Waypoint, Drone, Mission, FlightSchedule
from src.core.conflict_resolver import (
    resolve_conflicts_for_mission,
    evaluate_segment_pair_spatiotemporal,
)


def _make_waypoint(id, x, y, z, t):
    return Waypoint(id=id, x=x, y=y, z=z, t=t)


def test_no_conflict_simple():
    """
    Two horizontal segments far apart in Y → no conflict.
    """
    # Mission: from (0,0,10) to (10,0,10), t 0→10
    wps_m = [
        _make_waypoint(0, 0.0, 0.0, 10.0, 0.0),
        _make_waypoint(1, 10.0, 0.0, 10.0, 10.0),
    ]
    mission_drone = Drone(
        drone_id="mission_drone",
        name="Mission Drone",
        description="Test mission",
        waypoints=wps_m,
    )
    mission = Mission(
        mission_id="mission_test",
        name="Test Mission",
        description="No conflict scenario",
        time_window=(0.0, 10.0),
        drone=mission_drone,
    )

    # Other drone: same timing but y=100
    wps_o = [
        _make_waypoint(0, 0.0, 100.0, 10.0, 0.0),
        _make_waypoint(1, 10.0, 100.0, 10.0, 10.0),
    ]
    other_drone = Drone(
        drone_id="other_drone",
        name="Other Drone",
        description="Far away",
        waypoints=wps_o,
    )
    schedule = FlightSchedule(drones=[other_drone])

    result = resolve_conflicts_for_mission(
        mission, schedule, safety_buffer=20.0, num_samples=50
    )

    assert result["status"] == "clear"
    assert result["total_conflicts"] == 0


def test_single_conflict_crossing_paths():
    """
    Mission goes east, other drone goes north,
    they cross at the same (x,y,z,t) → conflict.
    """
    # Mission: (0,0,10) -> (10,0,10), t 0→10
    wps_m = [
        _make_waypoint(0, 0.0, 0.0, 10.0, 0.0),
        _make_waypoint(1, 10.0, 0.0, 10.0, 10.0),
    ]
    mission_drone = Drone(
        drone_id="mission_drone",
        name="Mission Drone",
        description="Crossing mission",
        waypoints=wps_m,
    )
    mission = Mission(
        mission_id="mission_cross",
        name="Crossing Mission",
        description="Should conflict",
        time_window=(0.0, 10.0),
        drone=mission_drone,
    )

    # Other drone: (5,-5,10) -> (5,5,10), t 0→10
    wps_o = [
        _make_waypoint(0, 5.0, -5.0, 10.0, 0.0),
        _make_waypoint(1, 5.0, 5.0, 10.0, 10.0),
    ]
    other_drone = Drone(
        drone_id="other_drone",
        name="Other Drone",
        description="Crossing",
        waypoints=wps_o,
    )
    schedule = FlightSchedule(drones=[other_drone])

    result = resolve_conflicts_for_mission(
        mission, schedule, safety_buffer=2.0, num_samples=100
    )

    assert result["status"] == "conflict_detected"
    assert result["total_conflicts"] >= 1

    conflict = result["conflicts"][0]
    # The crossing should be around x=5,y=0,z=10 at t~5
    assert abs(conflict["location"]["x"] - 5.0) < 1.0
    assert abs(conflict["location"]["y"] - 0.0) < 1.0
    assert abs(conflict["location"]["z"] - 10.0) < 1.0
    assert abs(conflict["conflict_time"] - 5.0) < 1.0
    assert conflict["min_distance"] < 2.0


def test_segment_pair_spatiotemporal_no_overlap_time():
    """
    Segments that don't overlap in time should report no conflict,
    even if they are geometrically close.
    """
    # Same spatial segment, but non-overlapping times
    seg_a = ((0.0, 0.0, 0.0), (10.0, 0.0, 0.0), 0.0, 10.0)
    seg_b = ((0.0, 0.0, 0.0), (10.0, 0.0, 0.0), 20.0, 30.0)

    result = evaluate_segment_pair_spatiotemporal(
        seg_a, seg_b, safety_buffer=1.0, num_samples=50
    )

    assert result["conflict"] is False
    assert result["min_distance"] == float("inf")
    assert result["conflict_time"] is None
