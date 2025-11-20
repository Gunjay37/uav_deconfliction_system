from src.query.deconfliction_api import check_mission_conflicts
from src.visualization.plotter_2d import plot_2d_static, animate_2d
from src.data.loader import load_missions, load_simulated_flights

missions = load_missions("data/sample_missions.json")
flights = load_simulated_flights("data/simulated_flights.json")

result = check_mission_conflicts(
    missions_path="data/sample_missions.json",
    flights_path="data/simulated_flights.json",
    mission_id="mission_2"
)

mission = next(m for m in missions if m.mission_id == "mission_2")

plot_2d_static(mission, flights, conflicts=result["conflicts"])
animate_2d(mission, flights, conflicts=result["conflicts"])
