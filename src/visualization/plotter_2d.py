"""
2D visualization utilities for UAV missions and simulated flights.
"""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from typing import List, Dict
from src.data.models import Mission, FlightSchedule


def plot_2d_static(
    mission: Mission,
    schedule: FlightSchedule,
    conflicts: List[Dict] = None,
    save_path: str = None,
):
    """
    Create a static 2D plot showing:
    - Primary mission path
    - Other drone paths
    - Conflict points (if any)
    """

    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # Plot mission
    mx = [wp.x for wp in mission.drone.waypoints]
    my = [wp.y for wp in mission.drone.waypoints]
    ax.plot(mx, my, '-o', label=f"Primary Mission: {mission.mission_id}", linewidth=2)

    # Plot other drones
    for drone in schedule.drones:
        ox = [wp.x for wp in drone.waypoints]
        oy = [wp.y for wp in drone.waypoints]
        ax.plot(ox, oy, '--o', label=f"{drone.drone_id}")

    # Plot conflicts if present
    if conflicts:
        for c in conflicts:
            x = c["location"]["x"]
            y = c["location"]["y"]
            ax.scatter(x, y, color='red', s=120, marker='x')
            ax.text(x, y, f"  {c['other_drone_id']}\n  t~{c['conflict_time']:.1f}",
                    color='red', fontsize=8)

    ax.set_title("2D UAV Trajectories (Top-Down View)")
    ax.set_xlabel("X (meters)")
    ax.set_ylabel("Y (meters)")
    ax.legend()
    ax.grid(True)

    if save_path:
        plt.savefig(save_path, dpi=120)

    plt.show()


def animate_2d(
    mission: Mission,
    schedule: FlightSchedule,
    conflicts: List[Dict] = None,
    save_path: str = None,
    fps: int = 10,
):
    """
    Animate UAV movements over time.

    Shows:
    - Mission trajectory animation
    - Other drone animations
    - Dynamic playback for demo video
    """

    # Gather all timestamps to find animation range
    all_times = []
    all_times.extend([wp.t for wp in mission.drone.waypoints])
    for drone in schedule.drones:
        all_times.extend([wp.t for wp in drone.waypoints])

    t_min = min(all_times)
    t_max = max(all_times)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Static trajectories in background
    mx = [wp.x for wp in mission.drone.waypoints]
    my = [wp.y for wp in mission.drone.waypoints]
    ax.plot(mx, my, 'k--', alpha=0.4)

    for drone in schedule.drones:
        ox = [wp.x for wp in drone.waypoints]
        oy = [wp.y for wp in drone.waypoints]
        ax.plot(ox, oy, 'k:', alpha=0.3)

    # Dynamic points
    mission_point, = ax.plot([], [], 'bo', label="Mission Drone")
    other_points = [
        ax.plot([], [], 'ro')[0]
        for _ in schedule.drones
    ]

    # conflict markers
    conflict_markers = []
    if conflicts:
        for c in conflicts:
            cx = c["location"]["x"]; cy = c["location"]["y"]
            marker = ax.scatter(cx, cy, color='red', s=120, marker='x')
            conflict_markers.append(marker)

    ax.set_xlim(min(mx)-20, max(mx)+20)
    ax.set_ylim(min(my)-20, max(my)+20)
    ax.set_title("2D UAV Animation")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    def interp_path(drone, t):
        """Interpolate position at time t."""
        for wp1, wp2 in zip(drone.waypoints[:-1], drone.waypoints[1:]):
            if wp1.t <= t <= wp2.t:
                alpha = (t - wp1.t) / (wp2.t - wp1.t)
                x = wp1.x + alpha * (wp2.x - wp1.x)
                y = wp1.y + alpha * (wp2.y - wp1.y)
                return x, y
        return drone.waypoints[-1].x, drone.waypoints[-1].y

    def update(frame_time):
        # Update mission
        mx, my = interp_path(mission.drone, frame_time)
        mission_point.set_data(mx, my)

        # Update each drone
        for i, drone in enumerate(schedule.drones):
            ox, oy = interp_path(drone, frame_time)
            other_points[i].set_data(ox, oy)

        return [mission_point] + other_points + conflict_markers

    frames = np.linspace(t_min, t_max, int((t_max - t_min) * fps))

    ani = FuncAnimation(fig, update, frames=frames, interval=1000/fps, blit=True)

    if save_path:
        ani.save(save_path, writer="ffmpeg", fps=fps)

    plt.show()
