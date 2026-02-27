# Common Design Mistakes & Troubleshooting Guide

## Electromagnetic Coil Design Failures

### Problem 1: Coil Overheating (Burnout)

**Symptoms**: Coil smoke, melted insulation, open circuit after brief operation.

**Root Causes**:
- Excessive current: Duty cycle mismatch (continuous applied to intermittent-rated coil)
- Poor thermal contact: Potting compound traps heat, doesn't conduct it away
- Wrong wire gauge: Designer used 22 AWG where 18 AWG was needed
- Calculation mistake: Used peak current instead of RMS in power calculations

**Prevention**:
- Validate duty cycle: Is it continuous, intermittent (10s on/off), or pulsed (milliseconds)?
- Design for derating: Run at 60-70% rated current for reliability
- Thermal path: Plan how heat leaves the coil (convection, conduction to frame, active cooling)
- FEA simulation: Model temperature rise before prototype (saves expensive iteration)

**Example Failure**:
A designer specified a 24V solenoid for continuous use. They calculated:
- P = V×I = 24×1 = 24 watts
- Assumed coil could handle this continuously
- Reality: Coil was rated for 2-minute intermittent duty (max 4 cycles/minute)
- In continuous use: Thermal runaway → burnout in minutes

**Lesson**: Always validate duty cycle from supplier datasheet, not assumed.

---

### Problem 2: Insufficient Holding Force

**Symptoms**: Electromagnet releases under load that should be held (vibration, mechanical shock, thermal drift).

**Root Causes**:
- Air gap grew: Mechanical tolerance stack-up created 0.5mm gap instead of planned 0.2mm
- Temperature rise: Coil heated up, permeability dropped, field weakened
- Saturation calculation was wrong: Designer assumed linear B-H curve at actual operating point
- Forgot to account for flux leakage: Assumed 100% flux coupling, actual is 85-90%

**Prevention**:
- Mechanical tolerance analysis: Sum all gaps, add safety margin
- Thermal derating: Model temperature rise, recalculate force at hot condition
- B-H curve study: Plot actual curve, identify saturation knee, design below it
- Prototype testing: Measure actual force, compare to calculated
- Safety margin: Design for 1.5-2× required force, not just nominal

**Example Failure**:
Magnetic latch design:
- Calculated holding force: 50 N (assuming 1.8 T in iron, linear curve)
- Prototype test: Actual force was 35 N
- Investigation: At 1.7 T, permeability dropped 40% (curved B-H)
- Fix: Redesign with larger core (+15% cost) to operate at 1.4 T (linear region)

---

### Problem 3: Unexpected Vibration or Noise

**Symptoms**: Humming, buzzing, mechanical vibration in electromagnet.

**Root Causes**:
- Magnetic attraction to unintended objects: Designer didn't shield field
- Lamination resonance: Iron core oscillates at power frequency (50/60 Hz)
- Core saturation oscillation: As flux increases, saturation reduces field, causing oscillation
- Loose mechanical parts: Iron attracted to nearby ferrous objects

**Prevention**:
- Shielding design: Model field distribution, identify stray flux regions
- Lamination: Use laminated cores (stacked thin sheets, not solid block)
- Frequency analysis: Calculate natural frequencies, avoid 50/60 Hz
- Mechanical constraint: Secure all iron parts, prevent rattling

---

## Air Gap Trap (The Most Common Mistake)

**The Problem**: Engineers underestimate how much reluctance an air gap adds.

**Quick Reference**:
| Air Gap | Effect on Reluctance | Effect on MMF Required |
|---------|----------------------|------------------------|
| 0.1 mm  | x2 | Double coil needed |
| 0.5 mm  | x10 | 10× coil turns or current |
| 1.0 mm  | x20 | Completely impractical |

**Real Example**: Magnetic circuit design
- Iron core reluctance: 100 units
- 0.2 mm air gap reluctance: 1,000 units
- Total: 1,100 units (iron is only 9% of total!)
- Designer thought: "small gap, negligible effect"
- Reality: Air gap dominates everything

**Lesson**: Every 0.1 mm air gap costs you enormously. Measure twice, design once.

---

## Thermal Drift Issues

**Problem**: Electromagnet force decreases over time during operation.

**Physical Cause**: As temperature rises:
1. Coil resistance increases (~0.4% per °C for copper)
2. Current decreases (V=IR, fixed voltage source)
3. Permeability drops (iron ~0.2% per °C)
4. Force drops by ~0.5-0.8% per °C

**Example**: 10°C temperature rise
- Current drops 4%
- Permeability drops 2%
- Force drops 6% (compounded effect)
- Visible as control system hunting for equilibrium

**Solutions**:
1. **Constant current source**: Instead of fixed voltage, provide fixed current (more costly)
2. **Active compensation**: Temperature sensor + feedback control (complex)
3. **Over-design**: Build for cold condition only, accept some drift (simplest)
4. **Cooling**: Forced air or liquid cooling (adds cost/complexity)

---

## Saturation Blindness

**The Mistake**: Designer calculates assuming linear B-H relationship everywhere.

**Reality**: At high fields, B-H curve bends severely:
- Below 1.0 T: Nearly linear for iron (μᵣ ~ 5000)
- 1.2-1.6 T: Permeability drops 20-40%
- 1.8+ T: Severe nonlinearity, cannot reliably increase field further
- 2.0+ T: Essentially flat (saturated)

**Why It Matters**:
- Linear assumption: "Need 2.0 T? Use design for 2.0 T field"
- Nonlinear reality: "Can't reach 2.0 T reliably; saturated at 1.6 T"
- Mistake cost: Redesign whole magnetic circuit (expensive late discovery)

**Prevention**:
- Always plot B-H curve for your material
- Design to stay below 80% of saturation
- Verify with FEA before building prototype

---

## Material Selection Gotchas

### Ferrite vs. Iron at High Frequency

**Common Mistake**: Using iron core for high-frequency inductor.
- Iron core at 1 MHz: Severe eddy current losses, core gets hot
- Ferrite core at 1 MHz: Minimal losses, efficient
- Cost difference: Ferrite costs 2-3× more, but iron fails completely

**Rule**: Use ferrite for f > 100 kHz, use iron/steel for DC and low frequency.

### Neodymium Corrosion

**Common Mistake**: Exposing neodymium magnets to moisture.
- Neodymium is reactive with oxygen and water
- Uncoated magnets rust in weeks
- Corrosion flakes off, damaging magnet and nearby components
- Solution: Always specify coated neodymium (nickel, epoxy, or aluminum)

### Cost Optimization Gone Wrong

**Mistake**: Substituting material to save 5% in cost.
- Designer: "Use cheaper ferrite instead of iron"
- Reality: Ferrite has 40% lower saturation, new core size is 3× larger
- Final cost: 200% more expensive due to size penalties

**Lesson**: Never optimize materials in isolation; optimize the whole system.

---

## Testing & Validation Red Flags

**If you observe these, stop and investigate**:
1. Measured force is <80% of calculated - Air gap or saturation issue
2. Coil gets warm during short test - Thermal design problem
3. Performance varies with temperature - Thermal drift or saturation
4. Intermittent failures - Usually thermal (transient overheating)
5. Works in lab, fails in field - Environmental factors (temperature, vibration, humidity)
