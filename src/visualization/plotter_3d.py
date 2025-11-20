"""
3D / 4D visualization utilities for UAV trajectories.

Provides:
- 3D static plot
- 4D animation (3D position over time)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List, Dict
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from src.data.models import Mission, FlightSchedule


# ---------------------------------------------------
# 3D STATIC PLOT
# ---------------------------------------------------

def plot_3d_static(
    mission: Mission,
    schedule: FlightSchedule,
    conflicts: List[Dict] = None,
    save_path: str = None
):
    """
    Creates a 3D static plot showing:
    - Primary mission trajectory
    - Other drone trajectories
    - Conflict points in 3D
    """

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Plot primary mission
    mx = [wp.x for wp in mission.drone.waypoints]
    my = [wp.y for wp in mission.drone.waypoints]
    mz = [wp.z for wp in mission.drone.waypoints]
    ax.plot(mx, my, mz, '-o', linewidth=2, label=f"Primary Mission: {mission.mission_id}")

    # Plot other drones
    for drone in schedule.drones:
        ox = [wp.x for wp in drone.waypoints]
        oy = [wp.y for wp in drone.waypoints]
        oz = [wp.z for wp in drone.waypoints]
        ax.plot(ox, oy, oz, '--o', alpha=0.7, label=drone.drone_id)

    # Conflicts
    if conflicts:
        for c in conflicts:
            cx = c['location']['x']
            cy = c['location']['y']
            cz = c['location']['z']
            ax.scatter(cx, cy, cz, color="red", s=80, marker='x')
            ax.text(cx, cy, cz, f"{c['other_drone_id']}", color='red')

    ax.set_title("3D UAV Trajectories")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Altitude (Z)")
    ax.legend()
    ax.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=120)

    plt.show()


# ---------------------------------------------------
# 4D ANIMATION
# ---------------------------------------------------

def animate_3d(
    mission: Mission,
    schedule: FlightSchedule,
    conflicts: List[Dict] = None,
    fps: int = 12,
    save_path: str = None,
):
    """
    Animate UAV movement in 3D over time (4D visualization).
    """

    # Get all timestamps
    times = []
    times.extend([wp.t for wp in mission.drone.waypoints])
    for drone in schedule.drones:
        times.extend([wp.t for wp in drone.waypoints])

    t_min, t_max = min(times), max(times)
    frames = np.linspace(t_min, t_max, int((t_max - t_min) * fps))

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection="3d")

    # Background path lines
    for drone in [mission.drone] + schedule.drones:
        xs = [wp.x for wp in drone.waypoints]
        ys = [wp.y for wp in drone.waypoints]
        zs = [wp.z for wp in drone.waypoints]
        ax.plot(xs, ys, zs, 'k--', alpha=0.3)

    # Dynamic points
    mission_point, = ax.plot([], [], [], 'bo', markersize=8)
    other_points = [
        ax.plot([], [], [], 'ro')[0]
        for _ in schedule.drones
    ]

    # Conflict markers
    conflict_markers = []
    if conflicts:
        for c in conflicts:
            marker = ax.scatter(
                c["location"]["x"],
                c["location"]["y"],
                c["location"]["z"],
                s=120, color='red', marker='x'
            )
            conflict_markers.append(marker)

    # Helper function: linear interpolation
    def interp(drone, t):
        for wp1, wp2 in zip(drone.waypoints[:-1], drone.waypoints[1:]):
            if wp1.t <= t <= wp2.t:
                alpha = (t - wp1.t) / (wp2.t - wp1.t)
                return (
                    wp1.x + alpha * (wp2.x - wp1.x),
                    wp1.y + alpha * (wp2.y - wp1.y),
                    wp1.z + alpha * (wp2.z - wp1.z)
                )
        last = drone.waypoints[-1]
        return (last.x, last.y, last.z)

    # Update frame
    def update(frame_time):
        # Mission drone
        mx, my, mz = interp(mission.drone, frame_time)
        mission_point.set_data(mx, my)
        mission_point.set_3d_properties(mz)

        # Other drones
        for i, drone in enumerate(schedule.drones):
            x, y, z = interp(drone, frame_time)
            other_points[i].set_data(x, y)
            other_points[i].set_3d_properties(z)

        ax.view_init(elev=30, azim=40 + frame_time * 2)  # orbit camera slowly

        return [mission_point] + other_points + conflict_markers

    ani = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=False)

    if save_path:
        ani.save(save_path, writer="ffmpeg", fps=fps)

    plt.show()
