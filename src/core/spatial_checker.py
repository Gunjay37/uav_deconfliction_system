"""
Spatial conflict detection module.
Computes minimum distance between two 3D line segments.
"""

import numpy as np
from typing import Tuple, Dict


def segment_to_vector(seg_start, seg_end):
    return np.array(seg_start), np.array(seg_end - seg_start)


def compute_min_distance_segment_segment(
    A0: Tuple[float, float, float],
    A1: Tuple[float, float, float],
    B0: Tuple[float, float, float],
    B1: Tuple[float, float, float],
) -> Dict:
    """
    Compute minimum 3D distance between line segment A and segment B.
    Returns:
        {
            "distance": float,
            "point_on_A": np.array,
            "point_on_B": np.array
        }
    """

    A0 = np.array(A0, dtype=float)
    A1 = np.array(A1, dtype=float)
    B0 = np.array(B0, dtype=float)
    B1 = np.array(B1, dtype=float)

    u = A1 - A0
    v = B1 - B0
    w0 = A0 - B0

    a = np.dot(u, u)  # always >= 0
    b = np.dot(u, v)
    c = np.dot(v, v)  # always >= 0
    d = np.dot(u, w0)
    e = np.dot(v, w0)

    D = a * c - b * b  # denom

    # parameters on each segment (0 to 1)
    if D < 1e-8:  
        # Segments are almost parallel
        s = 0.0
        t = (e / c) if c != 0 else 0.0
    else:
        s = (b * e - c * d) / D
        t = (a * e - b * d) / D

    # Clamp to segment range [0,1]
    s = min(max(s, 0.0), 1.0)
    t = min(max(t, 0.0), 1.0)

    closest_A = A0 + s * u
    closest_B = B0 + t * v

    distance = np.linalg.norm(closest_A - closest_B)

    return {
        "distance": float(distance),
        "point_on_A": closest_A,
        "point_on_B": closest_B
    }


def check_spatial_conflict(
    A0, A1, B0, B1, safety_buffer: float
) -> Dict:
    """
    Returns:
        {
            "conflict": bool,
            "distance": float,
            "closest_point_A": np.array,
            "closest_point_B": np.array
        }
    """
    result = compute_min_distance_segment_segment(A0, A1, B0, B1)

    return {
        "conflict": result["distance"] < safety_buffer,
        "distance": result["distance"],
        "closest_point_A": result["point_on_A"],
        "closest_point_B": result["point_on_B"],
    }
