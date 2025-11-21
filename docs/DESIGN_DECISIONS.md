# UAV Deconfliction System — Design Decisions

This document describes the key design choices behind the system, along with reasoning for each decision.

---

# 🎯 1. Modular Architecture

### **Decision:**  
Split the system into separate layers (data → core → query → visualization).

### **Reasoning:**  
- Mirrors real UTM and robotics software  
- Easier maintenance  
- Allows independent upgrades (e.g., replace spatial checker)  
- Visualization does not affect computation logic  

---

# 📄 2. JSON as Input Format

### **Decision:**  
Use JSON for missions, simulated flights, and scenarios.

### **Reasoning:**  
- Human-readable  
- Easily modifiable  
- Integrates well with simulation/testing  
- Supports nested data cleanly  

---

# 📏 3. Waypoint-Based Trajectories

### **Decision:**  
Represent all drone paths using waypoints with timestamps.

### **Reasoning:**  
- Standard in drone mission planning  
- Matches real autopilot systems (PX4/ArduPilot)  
- Makes interpolation mathematically simple  

---

# 🧮 4. Linear Interpolation Between Waypoints

### **Decision:**  
Use linear interpolation for time-based position calculation.

### **Reasoning:**  
- Fast  
- Predictable  
- Suitable for fixed-wing and multirotor motion planning  
- Good trade-off between accuracy and compute time  

---

# 🚦 5. Safety Buffer Distance

### **Decision:**  
Default = **50 meters** (configurable).

### **Reasoning:**  
- Avoids near-miss events  
- Matches typical UTM minimum separation  
- Easily adjustable in `config.py`  

---

# 🔎 6. Sampling for Spatiotemporal Checking

### **Decision:**  
Iterate over time samples instead of continuous functions.

### **Reasoning:**  
- Much simpler implementation  
- Still accurate at small time steps  
- Allows real-time processing  
- Works well for many drones  

---

# 🎥 7. Multi-Layer Visualization

### **Decision:**  
Provide 2D, 3D, and 4D visualizations.

### **Reasoning:**  
- Stronger demonstration value  
- Helps debugging complex cases  
- Shows altitude/time effects clearly  
- Useful for demo videos  

---

# 🧪 8. Scenario Testing Framework

### **Decision:**  
Use scenarios.json with expected outputs.

### **Reasoning:**  
- Easy regression testing  
- Clear pass/fail for each scenario  
- Allows extension into larger test suites  

---

