# Magnetics SME Agent + MCP Server

A sample project demonstrating an AI agent with domain expertise in electromagnetics and magnetics, powered by a custom MCP (Model Context Protocol) server that provides physics computation tools.

## Project Overview

This project showcases a **Senior Magnetics Engineer** AI agent that leverages the Anthropic SDK and a custom MCP server to perform expert-level analysis and calculations in electromagnetics. The agent understands Maxwell's equations, magnetic circuit design, material properties, and can reason through complex physics problems using real equations and precise numerical computations.

Key features:
- **Hand-rolled agentic loop** (no framework dependencies) for transparent agent reasoning
- **Custom MCP server** as a separate subprocess communicating via stdio (not mocked functions)
- **Real physics equations** with SI unit constants (e.g., μ₀ = 4π×10⁻⁷ H/m)
- **8 specialized physics tools** for field calculations, circuit analysis, and unit conversions
- **SME system prompt** that guides Claude's reasoning toward rigorous engineering principles
- **Comprehensive test suite** validating all tools and calculations

## Architecture

```
┌─────────────────────────────────┐
│   Agent (Anthropic SDK)         │
│   - Agentic loop                │
│   - Tool orchestration          │
│   - SME system prompt           │
└──────────────┬──────────────────┘
               │
        stdio (JSON-RPC)
               │
┌──────────────▼──────────────────┐
│   MCP Server (subprocess)       │
│   - Tool discovery & dispatch   │
│   - stdio transport             │
└──────────────┬──────────────────┘
               │
     ┌─────────┴──────────┬──────────────┬──────────┐
     │                    │              │          │
┌────▼────┐  ┌─────────┐ ┌────────────┐ ┌────────┐ │
│ Fields  │  │Circuits │ │ Materials  │ │Convert │ │
│ Tools   │  │ Tools   │ │ Lookup     │ │ Units  │ │
└─────────┘  └─────────┘ └────────────┘ └────────┘ │
```

## Project Structure

```
magnetics-sme/
├── mcp_server/
│   ├── server.py              # MCP server (stdio transport)
│   ├── __init__.py
│   └── tools/
│       ├── fields.py          # B/H field calculations (solenoid, wire, flux, energy)
│       ├── circuits.py        # Reluctance, MMF calculations
│       ├── materials.py       # Material property lookup (6 common materials)
│       ├── converters.py      # Unit conversions (T↔Gauss, Wb↔Maxwell, etc.)
│       └── __init__.py
├── agent/
│   ├── agent.py               # SME agent with agentic loop
│   └── __init__.py
├── tests/
│   ├── test_fields.py         # Field calculation tests
│   ├── test_circuits.py       # Circuit calculation tests
│   ├── test_materials.py      # Material lookup tests
│   ├── test_converters.py     # Conversion tests
│   └── __init__.py
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- `pip` package manager
- An Anthropic API key

### Step 1: Clone or Download the Project

```bash
cd magnetics-sme
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Your Anthropic API Key

```bash
export ANTHROPIC_API_KEY="sk-ant-..."  # On Windows: set ANTHROPIC_API_KEY=sk-ant-...
```

Or, for persistent setup, add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## Running the Agent

### Interactive Agent with Example Queries

```bash
python agent/agent.py
```

This will:
1. Start the MCP server as a subprocess
2. Discover all available tools via MCP
3. Run three example queries demonstrating the agent's capabilities:
   - Solenoid field calculation
   - Magnetic circuit reluctance
   - Energy storage in a magnetic field

**Example Output:**
```
Starting MCP server...
✓ MCP server started with 8 tools

======================================================================
User: What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?
======================================================================

Agent: I'll calculate the magnetic field at the center of the solenoid using the formula B = μ₀ · n · I...

🔧 Calling tool: solenoid_field
   Input: {
     "turns": 500,
     "length_m": 0.2,
     "current_A": 2.0
   }
   Result: {
     "B_tesla": 0.006283185307179586,
     "turns": 500,
     "length_m": 0.2,
     "current_A": 2.0,
     "turns_per_meter": 2500,
     "equation": "B = μ₀ · n · I"
   }

Agent: The magnetic field at the center of the solenoid is approximately **6.28 mT** (millitesla)...
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests for a Specific Module

```bash
pytest tests/test_fields.py -v       # Field calculations
pytest tests/test_circuits.py -v     # Circuit calculations
pytest tests/test_materials.py -v    # Material lookups
pytest tests/test_converters.py -v   # Unit conversions
```

### Run Tests with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=mcp_server --cov=agent
```

## Available Tools

### Field Calculations

#### **`solenoid_field`**
Compute magnetic field at the center of a solenoid.

**Equation:** B = μ₀ · n · I

**Inputs:**
- `turns` (int): Number of turns
- `length_m` (float): Length in meters
- `current_A` (float): Current in amperes

**Example:**
```
Input: 500 turns, 0.2m long, 2A
Output: B = 6.28 mT
```

---

#### **`biot_savart_wire`**
Compute magnetic field around an infinite straight current-carrying wire.

**Equation:** B = μ₀I / (2πr)

**Inputs:**
- `current_A` (float): Current in amperes
- `distance_m` (float): Distance from wire in meters

**Example:**
```
Input: 10A at 0.1m
Output: B = 20 μT
```

---

#### **`magnetic_flux`**
Compute magnetic flux through a surface.

**Equation:** Φ = B · A · cos(θ)

**Inputs:**
- `B_tesla` (float): Flux density in Tesla
- `area_m2` (float): Area in square meters
- `angle_deg` (float, default 0): Angle in degrees

**Example:**
```
Input: 0.1T, 0.01m², 0° angle
Output: Φ = 0.001 Wb (1 mWb)
```

---

#### **`energy_stored`**
Compute energy stored in a magnetic field.

**Equation:** W = (B² / (2μ₀)) · Volume

**Inputs:**
- `B_tesla` (float): Flux density in Tesla
- `volume_m3` (float): Volume in cubic meters

**Example:**
```
Input: 50mT in 0.5L (0.0005m³)
Output: W ≈ 0.99 Joules
```

---

### Magnetic Circuit Tools

#### **`reluctance`**
Compute reluctance of a magnetic circuit path.

**Equation:** R = l / (μ₀ · μᵣ · A)

**Inputs:**
- `length_m` (float): Path length in meters
- `area_m2` (float): Cross-sectional area in square meters
- `relative_permeability` (float): Material's μᵣ

**Example:**
```
Input: Iron core (μᵣ=5000), 0.1m long, 2cm² area
Output: R ≈ 79,600 H⁻¹
```

---

#### **`mmf_required`**
Compute magnetomotive force (MMF) for a magnetic path.

**Equation:** MMF = H · l

**Inputs:**
- `H_field` (float): Field strength in A/m
- `path_length_m` (float): Path length in meters

**Example:**
```
Input: H = 1000 A/m, l = 0.1m
Output: MMF = 100 AT (Ampere-turns)
```

---

### Material Properties

#### **`material_lookup`**
Return properties of a magnetic material.

**Inputs:**
- `material` (string): Material name (case-insensitive)

**Available Materials:**
- `air` — Vacuum/air (μᵣ = 1)
- `iron` — Pure iron, soft magnetic (μᵣ = 5000, Bsat = 2.15 T)
- `silicon_steel` — Transformer core (μᵣ = 4000, Bsat = 2.0 T)
- `ferrite` — Hard magnetic (μᵣ = 2000, Bsat = 0.4 T)
- `neodymium` — NdFeB permanent magnet (μᵣ = 1.05, Bsat = 1.4 T)
- `mu_metal` — Shielding material (μᵣ = 80000, Bsat = 0.8 T)

**Example:**
```
Input: "neodymium"
Output: {
  "relative_permeability": 1.05,
  "saturation_flux_density_T": 1.4,
  "coercivity_A_per_m": 955000.0
}
```

---

### Unit Conversions

#### **`unit_convert`**
Convert between magnetic units.

**Supported Conversions:**
- Tesla ↔ Gauss (1 T = 10,000 Gauss)
- Weber ↔ Maxwell (1 Wb = 10⁸ Maxwell)
- A/m ↔ Oersted (1 A/m ≈ 0.0126 Oersted)
- Henry ↔ milliHenry ↔ microHenry (H ↔ mH ↔ uH)

**Inputs:**
- `value` (float): Value to convert
- `from_unit` (string): Source unit
- `to_unit` (string): Target unit

**Example:**
```
Input: 1.2 T → Gauss
Output: 12000 Gauss
```

---

## Example Interactions

### Query 1: Solenoid Design

**User:** "What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?"

**Agent:**
1. Identifies: Use solenoid field equation B = μ₀ · n · I
2. Calls `solenoid_field` tool
3. Returns: **B ≈ 6.28 mT**
4. Explains: The field is uniform along the axis (ideal assumption) and proportional to turn density and current.

---

### Query 2: Magnetic Circuit Design

**User:** "I'm designing a magnetic circuit with a 10cm iron core (μr=5000), 2cm² cross-section. What is the reluctance?"

**Agent:**
1. Identifies: Need to find reluctance R = l / (μ₀ · μᵣ · A)
2. Calls `material_lookup("iron")` to verify μᵣ
3. Calls `reluctance` with core parameters
4. Returns: **R ≈ 79,577 H⁻¹** (Ampere-turns per Weber)

---

### Query 3: Energy in a Magnetic Field

**User:** "How much energy is stored in a 50mT field occupying 0.5 liters?"

**Agent:**
1. Identifies: Use energy density equation W = (B² / (2μ₀)) · Volume
2. Converts 0.5 L → 0.0005 m³
3. Calls `energy_stored` tool
4. Returns: **W ≈ 0.99 Joules**
5. Context: About the energy in a small magnet or inductor.

---

## Design Decisions

### 1. **No Agent Framework**
The agentic loop is implemented manually (not using LangChain, AutoGen, etc.) to demonstrate:
- Clear understanding of the agent pattern
- Transparent message flow and tool execution
- Direct control over system prompts and tool definitions

### 2. **MCP Server as Separate Process**
The MCP server runs as a **real subprocess**, not a mock:
- Tools communicate via stdio JSON-RPC (standard MCP)
- Clear separation of concerns: agent reasoning vs. computation
- Demonstrates production-ready architecture
- Easy to swap tools or extend with FEA, simulation, etc.

### 3. **Real Physics Equations**
Tools use actual constants and equations:
- μ₀ = 4π × 10⁻⁷ H/m (permeability of free space)
- Proper unit handling and validation
- Realistic material properties from engineering literature

### 4. **SME Persona**
The system prompt is not decorative—it actively shapes Claude's reasoning:
- Emphasizes physical principles before calculations
- Asks for assumptions and limitations
- Ensures units are included in answers
- Guides tool selection and multi-step problem solving

---

## Extension Ideas

### 1. **Add FEA Integration**
Integrate a finite element analysis tool (e.g., COMSOL API, Ansys):
- `magnetic_fea_simulation` tool for 3D field visualization
- Non-linear material models

### 2. **Multi-Agent Routing**
Use a router agent to dispatch questions:
- Fields & circuits → magnetics SME
- Thermal analysis → thermal engineer SME
- Mechanical design → mechanical engineer SME

### 3. **Interactive REPL**
Replace hardcoded example queries with an interactive prompt:
```bash
python -m agent.interactive
> Ask me about magnetics...
> What is the reluctance of...?
```

### 4. **Web Interface**
Build a simple Flask/FastAPI frontend:
- Chat interface to the agent
- Real-time tool call visualization
- Export results to PDF reports

### 5. **Domain-Specific Language (DSL)**
Parse structured design specs:
```
solenoid {
  turns: 1000
  wire_gauge: 24
  length_mm: 50
  core: iron
  frequency_hz: 60
}
→ Estimate DC resistance, inductance, power loss
```

---

## Testing

This project includes comprehensive tests covering:
- **Unit tests** for each tool (solenoid, wire, flux, energy, reluctance, MMF)
- **Material property lookups** (all 6 materials)
- **Unit conversions** (bidirectional, edge cases)
- **Error handling** (invalid inputs, missing materials, unsupported conversions)

Run all tests:
```bash
pytest tests/ -v --tb=short
```

---

## Troubleshooting

### "ANTHROPIC_API_KEY not found"
Ensure your API key is set:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
python agent/agent.py
```

### "MCP server failed to start"
Check that Python is in your PATH and `mcp_server/server.py` is readable:
```bash
python mcp_server/server.py
# Should run without errors and accept stdin
```

### Tests fail with import errors
Ensure dependencies are installed and PYTHONPATH includes the project root:
```bash
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

### Slow agent response
The agent makes real API calls to Anthropic. If responses are slow:
- Check your internet connection
- Verify `ANTHROPIC_API_KEY` is valid
- Reduce the number of example queries in `agent.py`

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `anthropic>=0.25.0` | Anthropic Python SDK (Claude API) |
| `mcp>=1.0.0` | Model Context Protocol SDK |
| `pytest>=7.4.0` | Test framework |
| `pytest-asyncio>=0.21.0` | Async test support |

---

## License

This is a portfolio project. Use, modify, and extend as needed.

---

## Further Reading

- **Maxwell's Equations**: https://en.wikipedia.org/wiki/Maxwell%27s_equations
- **Magnetic Circuit Design**: Textbooks on electromagnetics (Griffiths, Jackson)
- **MCP Specification**: https://modelcontextprotocol.io
- **Anthropic SDK**: https://github.com/anthropics/anthropic-sdk-python

---

## Contact & Support

For questions or improvements, consider:
1. Reviewing the code and docstrings
2. Running the test suite to verify functionality
3. Extending with your own physics tools or domains
