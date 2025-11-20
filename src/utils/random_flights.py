import random
from typing import List

from src.data.models import Waypoint, Drone, FlightSchedule


def generate_random_drone(
    drone_id: str,
    area_size: float = 150.0,
    t_min: float = 0.0,
    t_max: float = 100.0,
    min_waypoints: int = 2,
    max_waypoints: int = 5,
) -> Drone:
    """
    Generate a random drone flight with waypoints inside a square [0, area_size].
    Times are within [t_min, t_max] and strictly increasing.
    """

    num_wps = random.randint(min_waypoints, max_waypoints)

    # Generate strictly increasing times within [t_min, t_max]
    times = sorted(random.uniform(t_min, t_max) for _ in range(num_wps))

    waypoints: List[Waypoint] = []
    for idx, t in enumerate(times):
        x = random.uniform(0, area_size)
        y = random.uniform(0, area_size)
        z = random.uniform(10.0, 40.0)  # altitude in meters

        waypoints.append(
            Waypoint(
                id=idx,          # ✅ your dataclass uses `id`, not `waypoint_id`
                x=x,
                y=y,
                z=z,
                t=t,
            )
        )

    return Drone(
        drone_id=drone_id,
        name=f"Random {drone_id}",
        description="Randomly generated flight path in dynamic airspace",
        waypoints=waypoints,
    )


def generate_random_flight_schedule(
    num_drones: int = 5,
    area_size: float = 150.0,
    t_min: float = 0.0,
    t_max: float = 100.0,
) -> FlightSchedule:
    """
    Create a FlightSchedule containing N randomly-generated drones.
    """

    drones: List[Drone] = []
    for i in range(num_drones):
        d = generate_random_drone(
            drone_id=f"random_drone_{i+1}",
            area_size=area_size,
            t_min=t_min,
            t_max=t_max,
        )
        drones.append(d)

    return FlightSchedule(drones=drones)
