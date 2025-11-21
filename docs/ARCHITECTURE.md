# UAV Deconfliction System — Architecture

This document explains the internal structure and data flow of the UAV Deconfliction System. The system is designed using a **modular, layered architecture** inspired by professional UTM (Unmanned Traffic Management) pipelines.

---

# 🔧 High-Level Architecture

```
JSON → Models → Checkers → Resolver → API → Visualization
```

### 1. **Input Layer**
Reads mission and drone flight data from JSON.

### 2. **Data Modeling Layer**
Converts raw JSON into:
- Waypoint  
- Drone  
- Mission  
- FlightSchedule  

### 3. **Core Logic Layer**
Handles the entire conflict detection process:
- Spatial Checker  
- Temporal Checker  
- Spatiotemporal Conflict Resolver  

### 4. **Query API Layer**
Provides simple, high-level functions:
- `check_mission_conflicts()`
- `run_scenario()`

### 5. **Visualization Layer**
Generates:
- 2D static + animated plots  
- 3D static  
- 4D animated  

---

# 📁 Module Breakdown

## 1. `src/data/`
### `models.py`
Defines core data classes:
- `Waypoint`
- `Drone`
- `Mission`
- `FlightSchedule`

### `loader.py`
Loads missions, simulated flights, scenarios from JSON.  
Ensures validation and correct formatting.

---

## 2. `src/core/`
This layer performs all conflict calculations.

### `spatial_checker.py`
- Computes distances between trajectory segments  
- Evaluates safety buffer  
- Detects path intersections  

### `temporal_checker.py`
- Interpolates drone positions using timestamps  
- Detects timing overlaps  
- Calculates closest approach times  

### `conflict_resolver.py`
- Runs spatial + temporal checks together  
- Samples time steps  
- Reports:
  - conflict time  
  - location (x,y,z)  
  - min distance  
  - conflicting drone ID  

---

## 3. `src/query/deconfliction_api.py`
High-level user-facing API:
- Loads data  
- Calls conflict resolver  
- Formats output  
- Used by `main.py`

---

## 4. `src/utils/`
### `config.py`
Defines system-wide settings such as:
- Safety buffer  
- Time step  
- Debug level  

### `logger.py`
Handles unified logging.

### `random_flights.py`
Generates randomized flights for dynamic airspace simulations.

---

## 5. `src/visualization/`
### `plotter_2d.py`
- Static 2D plot  
- Animated 2D visualization  

### `plotter_3d.py`
- Static 3D  
- Animated 3D (4D)  

---

# 🔄 Data Flow Diagram

```
load_missions()           load_simulated_flights()
       │                               │
       ▼                               ▼
    Mission ---------------------> FlightSchedule
       │                               │
       └──────► conflict_resolver ◄────┘
                       │
                       ▼
                Conflict Reports
                       │
                       ▼
         (2D/3D/4D Visualization Modules)
```

---

## 🧩 Why This Architecture Works Well
- **Clear separation of responsibilities**  
- **Each module can be replaced/extended independently**  
- **Easy debugging and testing**  
- **Scalable for larger airspace**  
- **Professional structure used in robotics/UTM systems**

---