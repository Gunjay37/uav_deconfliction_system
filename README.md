# UAV Strategic Deconfliction System

A Python-based system for detecting and analyzing conflicts between drone missions in shared airspace.

## Quick Start

### Prerequisites
- Python 3.9+
- pip/conda
- Git

### Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/yourusername/uav-deconfliction-system.git
   cd uav-deconfliction-system
   \`\`\`

2. Create virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   \`\`\`

3. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Run tests:
   \`\`\`bash
   pytest tests/ -v
   \`\`\`

5. Run example scenarios:
   \`\`\`bash
   python examples/scenario_1_conflict_free.py
   \`\`\`

## Usage

Basic query:
\`\`\`python
from src.query.deconfliction_api import DeconflictionService

service = DeconflictionService()
result = service.check_mission(primary_mission, simulated_flights)
print(result)
\`\`\`

## Project Structure

See ARCHITECTURE.md for detailed system design.

## Documentation

- ARCHITECTURE.md - System design and components
- DESIGN_DECISIONS.md - Rationale for architectural choices
- SCALABILITY.md - Discussion of real-world deployment

## Testing

Run tests with coverage:
\`\`\`bash
pytest tests/ --cov=src --cov-report=html
\`\`\`

## Features

- ✅ Spatial conflict detection
- ✅ Temporal conflict detection
- ✅ Detailed conflict reporting
- ✅ 2D visualization
- ✅ 3D/4D visualization (extra credit)
- 🚧 Scalability for 10k+ drones
