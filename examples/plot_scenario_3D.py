from src.query.deconfliction_api import check_mission_conflicts
from src.visualization.plotter_3d import plot_3d_static, animate_3d
from src.data.loader import load_missions, load_simulated_flights


missions = load_missions("data/sample_missions.json")
flights = load_simulated_flights("data/simulated_flights.json")

# Choose a mission that actually conflicts
mission_id = "mission_2"

result = check_mission_conflicts(
    missions_path="data/sample_missions.json",
    flights_path="data/simulated_flights.json",
    mission_id=mission_id
)

mission = next(m for m in missions if m.mission_id == mission_id)

plot_3d_static(mission, flights, conflicts=result["conflicts"])
animate_3d(mission, flights, conflicts=result["conflicts"])
