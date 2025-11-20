"""
Spatiotemporal conflict resolution.

Combines:
- temporal overlap between segments
- interpolated positions over time
- spatial distance and safety buffer

Outputs detailed conflict events for a given primary mission
against a schedule of other flights.
"""

from typing import Dict, List, Tuple, Optional

import numpy as np

from src.core.temporal_checker import (
    get_segments_time_overlap,
    interpolate_segment_position,
)
from src.data.models import Mission, FlightSchedule, Drone


def evaluate_segment_pair_spatiotemporal(
    seg_a: Tuple[Tuple[float, float, float], Tuple[float, float, float], float, float],
    seg_b: Tuple[Tuple[float, float, float], Tuple[float, float, float], float, float],
    safety_buffer: float,
    num_samples: int = 50,
) -> Dict:
    """
    Evaluate spatiotemporal conflict between two segments.

    Each segment has form:
        (start_xyz, end_xyz, t_start, t_end)

    Steps:
    - Find overlapping time interval between the segments.
    - Sample positions along both segments in that overlap.
    - Compute minimum distance and the time at which it occurs.
    - Decide conflict if min_distance < safety_buffer.

    Returns dict with:
        {
            "conflict": bool,
            "min_distance": float,
            "conflict_time": Optional[float],
            "position_a": Optional[Tuple[float,float,float]],
            "position_b": Optional[Tuple[float,float,float]]
        }
    """
    start_a, end_a, t_a_start, t_a_end = seg_a
    start_b, end_b, t_b_start, t_b_end = seg_b

    overlap = get_segments_time_overlap(seg_a, seg_b)
    if overlap is None:
        return {
            "conflict": False,
            "min_distance": float("inf"),
            "conflict_time": None,
            "position_a": None,
            "position_b": None,
        }

    t_overlap_start, t_overlap_end = overlap

    if t_overlap_end <= t_overlap_start:
        return {
            "conflict": False,
            "min_distance": float("inf"),
            "conflict_time": None,
            "position_a": None,
            "position_b": None,
        }

    # Sample times in the overlap
    times = np.linspace(t_overlap_start, t_overlap_end, num_samples)

    min_dist = float("inf")
    best_time: Optional[float] = None
    best_pos_a: Optional[Tuple[float, float, float]] = None
    best_pos_b: Optional[Tuple[float, float, float]] = None

    for t in times:
        pos_a = interpolate_segment_position(start_a, end_a, t_a_start, t_a_end, t)
        pos_b = interpolate_segment_position(start_b, end_b, t_b_start, t_b_end, t)

        dist = np.linalg.norm(np.array(pos_a) - np.array(pos_b))
        if dist < min_dist:
            min_dist = dist
            best_time = float(t)
            best_pos_a = pos_a
            best_pos_b = pos_b

    conflict = min_dist < safety_buffer

    return {
        "conflict": conflict,
        "min_distance": float(min_dist),
        "conflict_time": best_time,
        "position_a": best_pos_a,
        "position_b": best_pos_b,
    }


def resolve_conflicts_for_mission(
    mission: Mission,
    schedule: FlightSchedule,
    safety_buffer: float,
    num_samples: int = 50,
) -> Dict:
    """
    Check a single primary mission against all other flights.

    Returns summary dict:
        {
          "mission_id": str,
          "status": "clear" or "conflict_detected",
          "total_conflicts": int,
          "conflicts": [
            {
              "other_drone_id": str,
              "min_distance": float,
              "conflict_time": float,
              "location": {"x": float, "y": float, "z": float},
            },
            ...
          ]
        }
    """
    mission_segments = mission.drone.to_segments()
    conflicts: List[Dict] = []

    for other_drone in schedule.drones:
        other_segments = other_drone.to_segments()

        for seg_a in mission_segments:
            for seg_b in other_segments:
                result = evaluate_segment_pair_spatiotemporal(
                    seg_a, seg_b, safety_buffer, num_samples=num_samples
                )

                if result["conflict"]:
                    # we use the position of mission's drone as the "conflict location"
                    pos_a = result["position_a"]
                    conflicts.append(
                        {
                            "other_drone_id": other_drone.drone_id,
                            "min_distance": result["min_distance"],
                            "conflict_time": result["conflict_time"],
                            "location": {
                                "x": pos_a[0],
                                "y": pos_a[1],
                                "z": pos_a[2],
                            },
                        }
                    )

    status = "clear" if len(conflicts) == 0 else "conflict_detected"

    return {
        "mission_id": mission.mission_id,
        "status": status,
        "total_conflicts": len(conflicts),
        "conflicts": conflicts,
    }
