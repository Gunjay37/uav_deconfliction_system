"""
Temporal conflict detection utilities.

This module handles:
- Time interval overlap between segments
- Position interpolation along a segment at a given time
"""

from typing import Tuple, Optional


def get_time_overlap(
    interval_a: Tuple[float, float],
    interval_b: Tuple[float, float],
) -> Optional[Tuple[float, float]]:
    """
    Compute the overlap between two time intervals [a_start, a_end] and [b_start, b_end].

    Returns:
        (overlap_start, overlap_end) if there is an overlap and overlap_start < overlap_end,
        otherwise None.
    """
    a_start, a_end = interval_a
    b_start, b_end = interval_b

    # Normalize so start <= end
    if a_end < a_start:
        a_start, a_end = a_end, a_start
    if b_end < b_start:
        b_start, b_end = b_end, b_start

    start = max(a_start, b_start)
    end = min(a_end, b_end)

    if start < end:
        return (start, end)
    else:
        return None


def interpolate_segment_position(
    start_xyz: Tuple[float, float, float],
    end_xyz: Tuple[float, float, float],
    t_start: float,
    t_end: float,
    t: float,
) -> Tuple[float, float, float]:
    """
    Linearly interpolate position along a segment at time t.

    - If t < t_start, returns position at t_start.
    - If t > t_end, returns position at t_end.
    - Otherwise returns position at the corresponding fraction along the segment.

    Assumes straight-line motion with constant velocity between start and end.
    """
    if t_end <= t_start:
        # Degenerate segment: no time duration, just return start
        return start_xyz

    # Clamp t into [t_start, t_end]
    if t <= t_start:
        return start_xyz
    if t >= t_end:
        return end_xyz

    alpha = (t - t_start) / (t_end - t_start)

    x0, y0, z0 = start_xyz
    x1, y1, z1 = end_xyz

    x = x0 + alpha * (x1 - x0)
    y = y0 + alpha * (y1 - y0)
    z = z0 + alpha * (z1 - z0)

    return (x, y, z)


def get_segment_time_interval(
    segment: Tuple[Tuple[float, float, float], Tuple[float, float, float], float, float]
) -> Tuple[float, float]:
    """
    Helper to extract the (t_start, t_end) from a segment of the form:
        (start_xyz, end_xyz, t_start, t_end)
    """
    _, _, t_start, t_end = segment
    return (t_start, t_end)


def get_segments_time_overlap(
    seg_a: Tuple[Tuple[float, float, float], Tuple[float, float, float], float, float],
    seg_b: Tuple[Tuple[float, float, float], Tuple[float, float, float], float, float],
) -> Optional[Tuple[float, float]]:
    """
    Convenience function:
    Given two segments (as produced by Drone.to_segments),
    compute their overlapping time interval, if any.
    """
    interval_a = get_segment_time_interval(seg_a)
    interval_b = get_segment_time_interval(seg_b)
    return get_time_overlap(interval_a, interval_b)
