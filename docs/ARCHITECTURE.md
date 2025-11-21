# System Architecture  
### UAV Deconfliction System — Engineering Architecture Specification  
**Version:** 1.0  
**Author:** Gunjay Chitr Suhalka

---

## 1. Introduction

This document describes the full architecture of the **UAV Deconfliction System**, including module responsibilities, data flow, subsystem interactions, and the underlying engineering principles.

The system is designed following **modular, layered, and testable software engineering practices**, commonly used in aerospace autonomy and UTM software.

---

## 2. High-Level Architecture

The system is composed of **five primary subsystems**:

1. **Data Layer** – models for UAVs, missions, and waypoints  
2. **Core Conflict Detection Layer** – spatial, temporal, and fused logic  
3. **Query / Interface Layer** – user-facing API  
4. **Visualization Layer** – 2D/3D/4D representation of results  
5. **Utility Layer** – logging, configuration, random traffic generation  

---

## 3. Architecture Diagram

pgsql
Copy code
            ┌─────────────────────────────┐
            │        JSON Data Files       │
            │ missions / flights / scenarios│
            └───────────────┬─────────────┘
                            │
                    Data Loaders
                            │
                            ▼
            ┌─────────────────────────────┐
            │        Data Models           │
            │ Waypoint, Drone, Mission     │
            └───────────────┬─────────────┘
                            │
                    Core Conflict Engine
                            │
    ┌────────────────────────┼────────────────────────┐
    ▼                        ▼                        ▼
Spatial Checker      Temporal Checker     Spatiotemporal Resolver
(d(x,y,z))          (t, interpolation)      (fusion engine)
└────────────────────────┼────────────────────────┘
                         │
                         ▼
         ┌─────────────────────────────┐
         │ Query API Layer │
         │ check_mission_conflicts() │
         └─────────────────────────────┘
                         │
                         ▼
               Visualization Layer
(2D, 2D Animation, 3D Static, 4D Animated Visualization)

## 4. Subsystem Details

### 4.1 Data Layer (src/data)
Models:

- **Waypoint**: (x, y, z, t)
- **Drone**: drone_id, waypoints
- **Mission**: mission_id, drone, time_window

Loaders:

- `load_missions()`
- `load_simulated_flights()`
- `load_test_scenarios()`

---

### 4.2 Spatial Checker (src/core/spatial_checker.py)
Responsibilities:

- Compute Euclidean distance between moving UAVs  
- Compute segment-to-segment minimum approach  
- Enforce **safety buffer rule**  
- Return instantaneous spatial conflicts

Complexity: *O(N·M)* where N, M are number of segments.

---

### 4.3 Temporal Checker (src/core/temporal_checker.py)
Responsibilities:

- Evaluate mission time windows  
- Identify overlapping intervals  
- Perform interpolation across timestamps  
- Produce time-indexed trajectories

---

### 4.4 Spatiotemporal Conflict Resolver  
Combines:

- Spatial separation constraints  
- Temporal overlap  
- Minimum-distance sampling  

Provides:

- Conflict list  
- Closest approach metrics  
- Conflict timing  
- Conflict severity

---

### 4.5 Visualization Layer  
Modules:

- **2D static plotter**
- **2D animated trajectory**
- **3D static visualization**
- **4D animated visualization (3D + time)**

Responsibilities:

- Render conflicts  
- Show multi-drone interaction  
- Provide interpretable view of conflict evolution

---

### 4.6 Query Layer  
Single entrypoint:

check_mission_conflicts()

Provides a clean interface for:

- Loading missions  
- Running conflict detection  
- Returning structured outputs  

---

## 5. Testing Architecture

Tests include:

- Spatial checker unit tests  
- Temporal checker unit tests  
- Fusion / resolver tests  
- End-to-end integration tests  
- Scenario validation tests  

Testing framework: **pytest**

---

## 6. Engineering Principles Used

- Separation of concerns  
- Pure functions for core logic  
- Deterministic outputs for scenario testing  
- High-cohesion, low-coupling module design  
- Configurable safety parameters  
- Extensible visualization layer  

---

## 7. Conclusion

The system architecture is robust, extensible, and aligned with aerospace-grade modularity. It enables accurate detection of multi-UAV conflicts and supports future extensions such as ROS2 integration, probabilistic trajectories, and large-scale UTM simulations.
