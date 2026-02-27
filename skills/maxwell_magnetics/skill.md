# Magnetics SME Agent Skill Definition

**Purpose:** Enable AI agents to solve electromagnetics and magnetic circuit design problems with expert-level physics reasoning and precise calculations.

**Domain:** Electromagnetics, magnetism, magnetic circuit design, material properties

---

## Use Case Decision Table

| Problem Type | Tool(s) to Use | Notes |
|---|---|---|
| Solenoid/coil field strength | `solenoid_field` | Use when you have turns, length, and current. Returns field in Tesla. |
| Field around a wire | `biot_savart_wire` | For infinite straight wires. Specify distance and current. |
| Magnetic flux through surface | `magnetic_flux` | Need B field, area, and angle. Calculates flux in Webers. |
| Magnetic circuit reluctance | `reluctance` | Use for circuit design. Need path length, area, and material μᵣ. |
| Magnetomotive force (MMF) | `mmf_required` | For circuit analysis. Multiply H-field by path length. |
| Energy in magnetic field | `energy_stored` | Calculate stored energy from B field and volume. |
| Material properties | `material_lookup` | Get μᵣ, saturation, coercivity for 6 materials (iron, ferrite, etc). |
| Unit conversions | `unit_convert` | Convert between magnetic units (Tesla, Gauss, Weber, etc). |

---

## Tool Reference

### solenoid_field
```
Input: { turns: int, length_m: float, current_A: float }
Output: { B_tesla: float, equation: "B = μ₀ · n · I" }
```
**Use Case:** Calculate uniform magnetic field inside a solenoid.
**Assumptions:** Ideal solenoid, uniform field along axis, no fringing effects.
**Equation:** B = μ₀ · (N/L) · I where μ₀ = 4π×10⁻⁷ H/m

---

### biot_savart_wire
```
Input: { current_A: float, distance_m: float }
Output: { B_tesla: float, equation: "B = μ₀I / (2πr)" }
```
**Use Case:** Magnetic field at distance from an infinite straight wire.
**Assumptions:** Infinite wire, uniform current, point measurement.
**Equation:** B = μ₀I / (2πr)

---

### magnetic_flux
```
Input: { B_tesla: float, area_m2: float, angle_deg: float (default: 0) }
Output: { flux_Wb: float, equation: "Φ = B · A · cos(θ)" }
```
**Use Case:** Calculate magnetic flux through a surface.
**Assumptions:** Uniform field, flat surface.
**Equation:** Φ = B · A · cos(θ) where θ is angle between B and surface normal.

---

### reluctance
```
Input: { length_m: float, area_m2: float, relative_permeability: float }
Output: { reluctance_H_inv: float, equation: "R = l / (μ₀·μᵣ·A)" }
```
**Use Case:** Magnetic circuit design. Analogous to electrical resistance.
**Assumptions:** Linear material, uniform cross-section.
**Equation:** R = l / (μ₀ · μᵣ · A)

---

### mmf_required
```
Input: { H_field: float, path_length_m: float }
Output: { mmf_AT: float, equation: "MMF = H · l" }
```
**Use Case:** Magnetomotive force in a magnetic circuit path.
**Assumptions:** Uniform field along path.
**Equation:** MMF = H · l (in Ampere-turns)

---

### energy_stored
```
Input: { B_tesla: float, volume_m3: float }
Output: { energy_J: float, equation: "W = (B²/(2μ₀))·Volume" }
```
**Use Case:** Energy stored in a magnetic field region.
**Assumptions:** Uniform field, non-ferromagnetic medium.
**Equation:** W = (B² / (2μ₀)) · V in Joules

---

### material_lookup
```
Input: { material: string }
Output: {
  relative_permeability: float,
  saturation_flux_density_T: float,
  coercivity_A_per_m: float
}
```
**Available Materials:**
- `iron` - Soft magnetic, high permeability (μᵣ ≈ 5000)
- `silicon_steel` - Transformer cores, low loss
- `ferrite` - Hard magnetic, high coercivity
- `neodymium` - Permanent magnet (NdFeB)
- `mu_metal` - Shielding, very high permeability
- `air` - Reference, μᵣ = 1

---

### unit_convert
```
Input: { value: float, from_unit: string, to_unit: string }
Output: { converted_value: float }
```
**Supported Conversions:**
- Magnetic flux density: Tesla ↔ Gauss (1 T = 10,000 Gauss)
- Magnetic flux: Weber ↔ Maxwell (1 Wb = 10⁸ Maxwell)
- Magnetic field: A/m ↔ Oersted
- Inductance: H ↔ mH ↔ μH

---

## Boundaries & Constraints

### What Agents CAN Do
✅ Calculate fields, flux, reluctance, MMF with given parameters
✅ Look up material properties and compare them
✅ Convert between magnetic units
✅ Chain multiple tool calls (e.g., reluctance → MMF)
✅ Explain physics reasoning (equations, assumptions)

### What Agents CANNOT Do
❌ Design PCBs or semiconductor devices (use EDA tools instead)
❌ Simulate dynamic/time-varying fields (use FEA software)
❌ Model non-linear magnetic saturation effects
❌ Handle 3D field geometry (tools assume simple 1D/uniform fields)
❌ Calculate losses, temperature effects, or eddy currents

---

## Gotchas & Common Mistakes

### Mistake 1: Wrong Unit Expectations
**Problem:** Passing current in kA when tools expect amperes.
**Solution:** Always check input descriptions. All tools use SI base units (meters, amperes, Tesla).

**Example:**
```
❌ reluctance(length_m=100, area_m2=0.5, μᵣ=5000)  # Wrong: 100 meters is huge
✅ reluctance(length_m=0.1, area_m2=0.0002, μᵣ=5000)  # Right: 10cm, 2cm²
```

### Mistake 2: Mixing CGS and SI Units
**Problem:** Getting confusing results from unit mismatches.
**Solution:** All calculations use SI. Convert from CGS using `unit_convert` before/after.

**Example:**
```
❌ B_gauss = 5000; use directly in solenoid_field() → Wrong by factor of 10,000
✅ B_tesla = 5000 / 10000 = 0.5; then use in tools
```

### Mistake 3: Ignoring Assumptions
**Problem:** Using tools outside their valid range.
**Solution:** Read the "Assumptions" field for each tool. Solenoid assumes ideal long coil, wire assumes infinite length.

### Mistake 4: Material Lookup Typos
**Problem:** Calling with misspelled material name.
**Solution:** Material names are case-insensitive but must match exactly (e.g., `silicon_steel` not `silicon-steel`).

---

## Physics Foundations

### Constants
- **Permeability of free space:** μ₀ = 4π × 10⁻⁷ H/m ≈ 1.257 × 10⁻⁶ H/m
- **Relative permeability (μᵣ):** Material property, dimensionless
- **Absolute permeability:** μ = μ₀ · μᵣ

### Key Equations
| Concept | Equation | Units |
|---|---|---|
| Magnetic field (solenoid) | B = μ₀·n·I | Tesla (T) |
| Magnetic field (wire) | B = μ₀I/(2πr) | Tesla (T) |
| Magnetic flux | Φ = B·A·cos(θ) | Weber (Wb) |
| Reluctance | R = l/(μ₀·μᵣ·A) | H⁻¹ (Ampere-turns/Weber) |
| MMF | MMF = H·l | Ampere-turns (AT) |
| Energy density | u = B²/(2μ₀) | J/m³ |

---

## Recommended Workflow

When solving a magnetics problem:

1. **Identify** - What physical principle applies? (Faraday, Ampere, etc.)
2. **Look up** - Do you need material properties? Use `material_lookup`
3. **Calculate** - Use the appropriate tool with SI units
4. **Convert** - If output needs different units, use `unit_convert`
5. **Explain** - Mention the equation, assumptions, and physical interpretation
6. **Validate** - Are the results reasonable? (Check orders of magnitude)

---

## Integration

**Language:** Python 3.9+
**API Client:** Anthropic SDK (`claude-sonnet-4-6`)
**CLI Entry Point:** `python cli.py` (interactive chat)
**Programmatic Entry Point:** `from agent.agent import MagneticsSMEAgent`

---

## Related Documentation

- Maxwell's Equations: https://en.wikipedia.org/wiki/Maxwell%27s_equations
- Magnetic Circuits: Griffiths, "Introduction to Electrodynamics"
- SI Units: https://www.nist.gov/pml/general-tables-units-measurement
- Tool Source Code: See `mcp_server/tools/` directory
