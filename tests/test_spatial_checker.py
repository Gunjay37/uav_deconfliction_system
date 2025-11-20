import numpy as np
from src.core.spatial_checker import (
    compute_min_distance_segment_segment,
    check_spatial_conflict
)


def test_parallel_segments_no_conflict():
    A0, A1 = (0,0,0), (10,0,0)
    B0, B1 = (0,5,0), (10,5,0)

    res = check_spatial_conflict(A0, A1, B0, B1, safety_buffer=2.0)
    assert res["conflict"] is False
    assert res["distance"] == 5


def test_crossing_segments_conflict():
    A0, A1 = (0,0,0), (10,10,0)
    B0, B1 = (0,10,0), (10,0,0)

    res = check_spatial_conflict(A0, A1, B0, B1, safety_buffer=1.0)
    assert res["conflict"] is True
    assert abs(res["distance"]) < 1e-6  # crossing


def test_segments_with_altitude_separation():
    A0, A1 = (0,0,0), (10,0,0)
    B0, B1 = (0,0,10), (10,0,10)

    res = check_spatial_conflict(A0, A1, B0, B1, safety_buffer=5.0)
    assert res["conflict"] is False
    assert res["distance"] == 10
