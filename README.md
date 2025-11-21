# UAV Deconfliction System  
*A Modular, Visual, and Scalable Airspace Conflict Detection Engine*

## 🚀 Overview
This project implements a **UAV Deconfliction System** capable of detecting **spatial**, **temporal**, and **spatiotemporal** conflicts between unmanned aerial vehicles (UAVs) operating in the same airspace. It includes:

- Dynamic airspace simulation with random drone flights  
- Spatial, temporal, and combined conflict detection  
- 2D (static + animated), 3D static, and 4D (3D + time) visualization  
- Scenario evaluation engine  
- Modular architecture suitable for scaling to larger UTM systems  

The system is built with clean structuring, testability, and clarity in mind.

---

## ⭐ Features

### ✔ **Spatial Conflict Detection**
Computes minimum distances between flight paths, safety buffer infringements, and trajectory intersection events.

### ✔ **Temporal Conflict Detection**
Interpolates drone positions over time to identify overlaps in time windows.

### ✔ **Spatiotemporal Analysis**
Samples full mission timelines using configurable time steps to identify real collision risks.

### ✔ **Dynamic Random Airspace**
Generates 5+ random drone flights every run for stress-testing.

### ✔ **Multi-Layer Visualization**
- **2D Static Plot:** Top-down paths + conflict markers  
- **2D Animation:** Real-time movement  
- **3D Static Plot:** Altitude representation  
- **4D Animation:** Full 3D + time visualization  

### ✔ **Scenario Evaluation**
Runs predefined UTM conflict scenarios with expected and actual outcomes.

### ✔ **Clean Architecture**
Modular structure under `src/` for clarity, reuse, and extensibility.

---

## 📂 Project Structure

```
uav-deconfliction-system/
├── src/
│   ├── data/                # Models + JSON loaders
│   ├── core/                # Spatial, temporal, spatiotemporal logic
│   ├── visualization/       # 2D, 3D, 4D plots + animations
│   ├── query/               # API for scenario/mission checks
│   └── utils/               # Config, logging, random flights
├── data/                    # sample_missions, simulated_flights, scenarios
├── examples/                # example runner scripts
├── docs/                    # Stage 10 documentation
├── tests/                   # pytest suite
└── main.py                  # unified runner
```

---

## 🛠 Installation

```bash
git clone <your-repo-url>
cd uav-deconfliction-system
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## ▶️ How to Run

### **Mission Mode**
```
python main.py --mission mission_2 --visualize_all
```

### **Scenario Mode**
```
python main.py --scenario scenario_2 --visualize_all
```

### **Dynamic Random Airspace (recommended demo)**
```
python main.py --dynamic --visualize_all
```

### **Only 2D visualization**
```
python main.py --mission mission_2 --visualize
```

---

## 📸 Visualizations Included

- 2D static “dashboard”
- 2D animation of UAVs over time  
- 3D static trajectories (altitude included)  
- 4D time-based animation in 3D space  

---

## 👨‍💻 Author
**Gunjay Chitr Suhalka**  
Robotics & Automation Engineer  

---

