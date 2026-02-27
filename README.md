# Maxwell Bot: Skill-Agnostic AI Agent Framework

A sample project demonstrating a skill-agnostic AI agent that dynamically loads domain expertise from markdown skill definitions, with an example magnetics/electromagnetics SME skill.

## Project Overview

This project showcases a generic agent framework that can work with any domain expertise by loading tool definitions and system prompts from skill.md files. The magnetics example demonstrates how to build an expert-level AI agent for electromagnetics and magnetic circuit design using real equations and precise numerical computations.

Key features:
- **Skill-agnostic architecture** - works with any domain by loading from skill.md files
- **Hand-rolled agentic loop** (no framework dependencies) for transparent agent reasoning
- **Dynamic tool discovery** - parses tool schemas directly from skill.md markdown
- **Retrieval-augmented generation (RAG)** - Chroma vector database with semantic search over domain knowledge
- **Real physics equations** with SI unit constants (e.g., μ₀ = 4π×10⁻⁷ H/m)
- **8 specialized magnetics tools** for field calculations, circuit analysis, and unit conversions
- **Configuration-driven design** - change agent behavior by editing skill.md, no code changes needed
- **Comprehensive test suite** validating all tools and calculations

## Architecture

```
┌──────────────────────────────────────┐
│   CLI (cli.py)                       │
│   - Skill selection & discovery      │
│   - Interactive chat interface       │
└────────────────┬─────────────────────┘
                 │
┌────────────────▼─────────────────────┐
│   SkillAgent (Anthropic SDK)         │
│   - Agentic loop                     │
│   - Tool orchestration               │
│   - skill.md parsing & loading       │
└────────────────┬─────────────────────┘
                 │
        ┌────────▼─────────┐
        │  Skills/         │
        │  <skill-name>/   │
        │  - skill.md      │
        │  - tool configs  │
        └────────┬─────────┘
                 │
     ┌───────────┴───────────┬──────────────┐
     │                       │              │
┌────▼─────┐  ┌─────────┐ ┌─┴──────────┐ ┌─┴──────┐
│ Fields   │  │Circuits │ │ Materials  │ │Convert │
│ (fields) │  │(circuits)│ │ (materials)│ │(units) │
└──────────┘  └─────────┘ └────────────┘ └────────┘
```

## Project Structure

```
maxwell_bot/
├── agent/
│   ├── agent.py               # SkillAgent: generic, skill-agnostic framework
│   └── __init__.py
├── mcp_server/
│   ├── tools/
│   │   ├── fields.py          # B/H field calculations (solenoid, wire, flux, energy)
│   │   ├── circuits.py        # Reluctance, MMF calculations
│   │   ├── materials.py       # Material property lookup (6 materials)
│   │   ├── converters.py      # Unit conversions (T↔Gauss, Wb↔Maxwell, etc.)
│   │   └── __init__.py
│   └── __init__.py
├── skills/
│   └── maxwell_magnetics/
│       └── skill.md           # Skill definition: tool reference, use cases, boundaries
├── tests/
│   ├── test_fields.py         # Field calculation tests
│   ├── test_circuits.py       # Circuit calculation tests
│   ├── test_materials.py      # Material lookup tests
│   ├── test_converters.py     # Conversion tests
│   └── __init__.py
├── cli.py                     # Interactive CLI entry point
├── requirements.txt           # Python dependencies
├── .gitignore
└── README.md                  # This file
```

## Installation & Setup

### Prerequisites
- Python 3.9+
- `pip` package manager
- An Anthropic API key

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/jkearney126/maxwell_bot.git
cd maxwell_bot
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

### Interactive Chat Interface

```bash
python cli.py
```

This launches an interactive chat where you can:
- Select from available skills (if multiple exist)
- Choose from 5 example prompts (by number 1-5)
- Type your own custom questions
- See animated thinking spinner while Claude responds
- Type `quit` or `exit` to exit

The agent auto-discovers skills from the `skills/` directory and loads tool definitions and expertise from each skill's `skill.md` file.

## Skill Definition Files (skill.md)

Each skill lives in `skills/<skill-name>/` with a `skill.md` file that defines:

- **Use Case Decision Table**: Maps problem types to appropriate tools
- **Tool Reference**: Complete tool specifications with:
  - Input/output schemas (parsed automatically by the agent)
  - Use cases and assumptions
  - Physics equations and constants
- **Boundaries & Constraints**: What the agent can/cannot do
- **Gotchas & Common Mistakes**: User guidance for typical errors
- **Physics Foundations**: Key equations and reference constants
- **Recommended Workflow**: Step-by-step reasoning guide

### Key Design Pattern

The agent is **completely skill-agnostic**:
- Tool definitions are **parsed from skill.md** (not hardcoded)
- System prompts are **loaded from skill.md**
- To add a new skill: create `skills/<name>/skill.md` with proper format
- To modify behavior: edit skill.md, no code changes needed

This separation of "what" (skill definition) from "how" (agent implementation) makes the framework flexible and reusable.

## Knowledge Base & Retrieval-Augmented Generation (RAG)

Each skill can include a knowledge base of domain documents to augment agent responses with relevant context.

### How It Works

1. **Vector Database**: Uses Chroma with semantic embeddings (all-MiniLM-L6-v2)
2. **Automatic Indexing**: Markdown files in `skills/<skill>/knowledge/` are indexed on first load
3. **Semantic Search**: When user queries, top-3 most relevant document chunks are retrieved
4. **Context Injection**: Retrieved knowledge is appended to system prompt before Claude API call

### Adding Knowledge Documents

Create markdown files in `skills/<skill-name>/knowledge/`:

```
skills/
└── maxwell_magnetics/
    ├── skill.md
    └── knowledge/
        ├── real_world_applications.md
        ├── design_mistakes_troubleshooting.md
        ├── materials_and_components.md
        └── standards_and_safety.md
```

**Document Format**:
- Use `## Section Title` headers for automatic chunking
- Each chunk becomes searchable (improves relevance ranking)
- Include practical, complementary information (not just duplicating skill.md)

### Example: Magnetics Knowledge Base

The included magnetics skill has 4 knowledge documents covering:

- **Real-World Applications** - MRI systems, transformers, motors, relays, speakers
- **Design Mistakes & Troubleshooting** - Common failures, thermal drift, saturation issues
- **Materials & Components** - Real costs, specifications, performance tradeoffs
- **Standards & Safety** - Regulatory requirements, compliance paths, EMC/RoHS

Result: 33 semantic chunks indexed, ~80% relevance for domain-specific queries

### Storage & Persistence

- Vector database stored in `skills/<skill>/.chroma_db/`
- Automatic persistence: survives process restarts
- One collection per skill, allowing multi-skill deployments

### Example Output:
```
✓ Agent initialized with skill: maxwell_magnetics
✓ Loaded 8 tools

======================================================================
SKILL AGENT - MAXWELL_MAGNETICS
======================================================================

Example prompts you can use:
  1. What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?
  2. I'm designing a magnetic circuit with a 10cm iron core (μr=5000), 2cm² cross-section. What is the reluctance?
  3. How much energy is stored in a 50mT field occupying 0.5 liters?
  4. Compare the permeability of silicon steel vs ferrite.
  5. Convert 1.2 Tesla to Gauss.

======================================================================
User: What is the magnetic field at the center of a solenoid with 500 turns, 20cm long, carrying 2A?
======================================================================

🧠 Thinking...

Agent: I'll calculate the magnetic field at the center of the solenoid using the formula B = μ₀ · n · I...

🔧 Calling tool: solenoid_field
   Input: {
     "turns": 500,
     "length_m": 0.2,
     "current_A": 2.0
   }
   Result: {
     "B_tesla": 0.006283185307179586,
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
python cli.py
```

### "No skills found in skills/ directory"
Ensure your skill is properly structured:
```
skills/
└── <skill-name>/
    └── skill.md
```

The agent auto-discovers skills by looking for `skill.md` files in subdirectories of `skills/`.


## Dependencies

| Package | Purpose |
|---------|---------|
| `anthropic>=0.25.0` | Anthropic Python SDK (Claude API) |
| `chromadb>=0.4.0` | Vector database for RAG (Chroma) |
| `sentence-transformers>=3.0.0` | Semantic embeddings for retrieval |
| `pytest>=7.4.0` | Test framework |
| `pytest-asyncio>=0.21.0` | Async test support |

---

## Further Reading

- **Maxwell's Equations**: https://en.wikipedia.org/wiki/Maxwell%27s_equations
- **Magnetic Circuit Design**: Textbooks on electromagnetics (Griffiths, Jackson)
- **MCP Specification**: https://modelcontextprotocol.io
- **Anthropic SDK**: https://github.com/anthropics/anthropic-sdk-python
