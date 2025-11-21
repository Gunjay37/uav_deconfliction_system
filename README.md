# UAV Deconfliction System  
### Multi-Drone Spatiotemporal Conflict Detection, Resolution & Visualization Suite  
**Author:** Gunjay Chitr Suhalka  
**Domain:** UAV Traffic Management (UTM), Airspace Safety, Autonomous Robotics  
**Version:** 1.0 – 2025

---

## 1. Overview

The **UAV Deconfliction System** is a complete, modular, and scalable framework for detecting and visualizing **spatial**, **temporal**, and **spatiotemporal** conflicts between multiple unmanned aerial vehicles operating within shared airspace.  

The system integrates:

- High-fidelity geometric modeling of UAV trajectories  
- Time-indexed interpolation for continuous position estimation  
- Spatial + temporal rule-based conflict evaluation  
- Dynamic airspace simulation with randomized drone traffic  
- Multi-layer visualization:
  - **2D static analysis**
  - **2D continuous-time animation**
  - **3D static trajectory visualization**
  - **4D (3D + time) animated visualization**
- Scenario-based validation and mission-based conflict assessment  
- Clean architecture aligned with professional aerospace software practices

This project demonstrates engineering rigor, modular design thinking, and real-world UTM applicability.

---

## 2. Key Features

### ✔ Spatial Conflict Detection  
- Computes continuous minimum distance between UAV trajectory segments  
- Supports configurable safety buffer (default 50m)

### ✔ Temporal Conflict Detection  
- Time-window analysis using mission timestamps  
- Linear interpolation to estimate UAV position at sub-second resolution

### ✔ Spatiotemporal Conflict Fusion  
- Combines spatial and temporal constraints  
- Produces interpretable conflict reports:
  - Closest approach location (x, y, z)
  - Time of violation
  - Minimum separation

### ✔ Dynamic Airspace Simulation  
- Automatically generates randomized drone trajectories  
- Produces non-deterministic, realistic airspace encounters  
- Helps test robustness under varying densities

### ✔ Multi-Layer Visualization Suite  
- **2D Top-Down Static View**
- **2D Animated Trajectories**
- **3D Spatial Visualization**
- **4D Animated Temporal-Spatial Evolution**

### ✔ Scenario Evaluator  
- Reads scenarios from `scenarios.json`  
- Validates expected vs. actual outcomes  
- Outputs conflict summaries

---

## 3. Architecture Summary

uav-deconfliction-system/
│
├── src/
│ ├── data/ # Data models & loaders
│ ├── core/ # Spatial, temporal & fusion logic
│ ├── query/ # API-level interface
│ ├── visualization/ # 2D, 3D, 4D visualization modules
│ ├── utils/ # Config, logger, random generators
│ └── tests/ # Unit & integration tests
│
├── data/ # Mission, flights, scenario JSON files
├── examples/ # Scenario scripts & demos
└── main.py # Entrypoint for all modes

## 4. Installation

git clone https://github.com/<your-repo>/uav-deconfliction-system
cd uav-deconfliction-system
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

## 5. Usage
### 1. Run a mission conflict check
- python main.py --mission mission_2 --visualize_all
### 2. Run a predefined scenario
- python main.py --scenario scenario_2 --visualize_all
### 3. Dynamic airspace simulation
- python main.py --dynamic --visualize_all

## 6. Requirements

Python 3.9+

NumPy

Matplotlib

Pillow

## 7. Author

Gunjay Chitr Suhalka
Robotics & Automation Engineer
Specialization in autonomous systems, CV pipelines, UAV trajectory modeling, and ROS-based navigation.