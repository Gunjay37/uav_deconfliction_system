from src.core.temporal_checker import (
    get_time_overlap,
    interpolate_segment_position,
    get_segments_time_overlap,
)


def test_time_overlap_partial():
    a = (0.0, 10.0)
    b = (5.0, 15.0)
    overlap = get_time_overlap(a, b)
    assert overlap == (5.0, 10.0)


def test_time_overlap_none():
    a = (0.0, 4.0)
    b = (5.0, 10.0)
    overlap = get_time_overlap(a, b)
    assert overlap is None


def test_time_overlap_nested():
    a = (0.0, 10.0)
    b = (2.0, 5.0)
    overlap = get_time_overlap(a, b)
    assert overlap == (2.0, 5.0)


def test_interpolation_start_mid_end():
    start = (0.0, 0.0, 0.0)
    end = (10.0, 0.0, 10.0)
    t_start, t_end = 0.0, 10.0

    # At start
    p0 = interpolate_segment_position(start, end, t_start, t_end, 0.0)
    assert p0 == start

    # At end
    p1 = interpolate_segment_position(start, end, t_start, t_end, 10.0)
    assert p1 == end

    # Midpoint
    pmid = interpolate_segment_position(start, end, t_start, t_end, 5.0)
    assert pmid == (5.0, 0.0, 5.0)


def test_interpolation_clamping_before_after():
    start = (0.0, 0.0, 0.0)
    end = (10.0, 0.0, 0.0)
    t_start, t_end = 0.0, 10.0

    p_before = interpolate_segment_position(start, end, t_start, t_end, -5.0)
    p_after = interpolate_segment_position(start, end, t_start, t_end, 20.0)

    assert p_before == start
    assert p_after == end


def test_segments_time_overlap_helper():
    seg_a = ((0, 0, 0), (10, 0, 0), 0.0, 10.0)
    seg_b = ((0, 10, 0), (10, 10, 0), 5.0, 15.0)

    overlap = get_segments_time_overlap(seg_a, seg_b)
    assert overlap == (5.0, 10.0)
