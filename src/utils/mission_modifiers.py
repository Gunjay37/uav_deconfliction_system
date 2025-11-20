"""
Utilities to modify mission altitude profiles.
Allows slanted, wavy, or randomized altitude paths
for better 3D visualization while keeping 2D identical.
"""

import numpy as np


def slope_mission_altitude(mission, start_z=10.0, end_z=40.0):
    """
    Makes the mission's altitude gradually increase (slanted path).
    Keeps X and Y unchanged.
    """
    waypoints = mission.drone.waypoints
    n = len(waypoints)

    for i, wp in enumerate(waypoints):
        alpha = i / max(1, (n - 1))
        wp.z = start_z + alpha * (end_z - start_z)

    return mission


def wave_mission_altitude(mission, amplitude=10, base=20):
    """
    Gives the mission a wavy sinusoidal altitude profile.
    """
    waypoints = mission.drone.waypoints
    n = len(waypoints)

    for i, wp in enumerate(waypoints):
        wp.z = base + amplitude * np.sin((i / max(1, (n - 1))) * np.pi)

    return mission


def randomize_mission_altitude(mission, min_z=10, max_z=40):
    """
    Assigns random altitude values to the mission's waypoints.
    """
    for wp in mission.drone.waypoints:
        wp.z = np.random.uniform(min_z, max_z)

    return mission
