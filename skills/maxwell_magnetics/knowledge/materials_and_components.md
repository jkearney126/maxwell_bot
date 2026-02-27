# Magnetic Materials & Components: Real-World Data

## Magnetic Core Materials Comparison

### Soft Magnetic Materials (Used in Electromagnets, Transformers, Inductors)

| Material | μᵣ | Bsat (T) | Loss @1kHz (W/kg) | Cost/kg | Best For |
|----------|-----|----------|-------------------|---------|----------|
| Pure Iron | 5000 | 2.15 | 2-4 | $1 | Electromagnets, rough tolerances |
| Silicon Steel (2% Si) | 4000 | 2.00 | 0.5-1.5 | $1.50 | Transformers, motors |
| Grain-Oriented Si-Steel | 6000 | 1.95 | 0.3-0.8 | $2.50 | Distribution transformers (optimized grain direction) |
| Cold-Rolled Steel | 2000 | 1.8 | 3-6 | $0.80 | Budget applications (high loss) |
| Ferrite (Mn-Zn) | 2000 | 0.40 | 0.2-0.5 | $8-12 | High-frequency inductors, switching supplies |
| Ferrite (Ni-Zn) | 800 | 0.25 | 0.1-0.3 | $10-15 | Very high frequency (>10 MHz) |
| Amorphous (Fe-Si-B) | 3000 | 1.56 | 0.1-0.3 | $15-20 | Ultra-low loss transformers (premium cost) |
| Permalloy (80% Ni-Fe) | 10000 | 0.80 | 2-4 | $5 | Audio transformers, precision shielding |
| Mu-Metal (Ni-Fe-Mo) | 80000 | 0.80 | 5-10 | $20+ | Magnetic shielding, scientific instruments |

### Permanent Magnets (Used in Motors, Speakers, Bearings)

| Material | Br (T) | Hc (kA/m) | Curie Temp (°C) | Cost/kg | Applications |
|----------|--------|-----------|-----------------|---------|--------------|
| Ferrite (hard) | 0.4 | 300 | 450 | $2-3 | Budget motors, cheap speakers |
| Alnico | 1.3 | 50 | 860 | $10-15 | Vintage motors, quality speakers |
| Samarium-Cobalt | 1.1 | 720 | 750 | $50-100 | High-temp aerospace, premium |
| Neodymium (N45) | 1.32 | 950 | 80 | $5-10 | Modern motors, consumers, speakers |
| Neodymium (N52) | 1.48 | 955 | 80 | $8-15 | Maximum strength, popular |
| Neodymium (N35SH) | 1.2 | 1000 | 150 | $15-25 | High-temp version (140°C safe) |

**Key Notes**:
- Ferrite: Heavy, weak, cheap - acceptable for consumer products
- Neodymium: Light, strong, easy to use - standard for modern designs
- Samarium-Cobalt: Rare, expensive, very high Tc - aerospace only
- **Temperature matters**: Standard neodymium loses 0.1-0.15%/°C above 20°C

---

## Copper Wire for Coils

### AWG vs. Resistance & Current Capacity

| AWG | Diameter (mm) | Resistance/m (Ω/m) | Max Current (A) | Turns/inch | Use Case |
|-----|---------------|-------------------|-----------------|-----------|----------|
| 28 | 0.32 | 0.21 | 0.5 | 50 | Very small coils, high-impedance circuits |
| 24 | 0.51 | 0.083 | 1.5 | 32 | Small electromagnets, precision work |
| 22 | 0.64 | 0.052 | 2.5 | 23 | Hobby coils, small relays |
| 20 | 0.81 | 0.033 | 4 | 17 | Standard electromagnets |
| 18 | 1.02 | 0.021 | 6 | 12 | Larger coils, higher current |
| 16 | 1.29 | 0.013 | 10 | 9 | Heavy-duty electromagnets |
| 14 | 1.63 | 0.0083 | 15 | 6 | Very large coils |

**Insulation Types**:
- Bare copper: No insulation, adjacent turns must not touch
- Enamel coated (Class A/B/C): Thin insulation, allows tight packing
- Single build: Thinner enamel, highest wire packing
- Double build: Thicker enamel, temperature margin
- Cloth covered: Mechanical protection, vintage style

**Designer Trade-off**:
- Fine wire (AWG 28-24): More turns in small space, higher resistance
- Coarse wire (AWG 16-14): Fewer turns, lower resistance, requires larger bobbin

---

## Wire Heating Power Loss

**Critical for duty cycle design:**

P = I²R = I² × ρ × (length/area)

**Example: 20m of 22 AWG copper at 2A continuous**:
- Resistance: 20 × 0.052 = 1.04 Ω
- Power loss: 2² × 1.04 = 4.16 watts (converted to heat!)
- Temperature rise: 10-20°C depending on cooling

**Rule of thumb**: 1 watt loss per cm³ of copper raises temperature by ~1°C

---

## Magnetic Component Datasheets: What to Look For

### Electromagnet Specifications Example
```
Part: 24VDC Solenoid, 200N Pull

Electrical:
- Voltage: 24V DC
- Current: 1.5A continuous, 3.0A surge (100ms)
- Coil resistance: 16Ω ±10%
- Duty cycle: Intermittent (2 min on, 3 min off max)
- Temperature rise: 40°C at continuous rating
- Ambient: -20 to +70°C

Mechanical:
- Pull force: 200N @ gap 0
- Force at 2mm: 180N (80% - don't rely on force at distance!)
- Operating time: <50ms to 90% force
- Release: <20ms after de-energized

Reliability:
- Mechanical life: 1,000,000 cycles
- Electrical life: 100,000 switching cycles
- Contact rating: No switching contacts (just coil)
```

**What designers often miss**:
- "Pull force" is at zero air gap - actual force drops rapidly with distance
- "Intermittent duty" means you can't run it continuously
- Operating time 50ms means there's 50ms lag before full force
- Mechanical life is different from electrical life

---

## Common Component Costs (2024 Estimates)

### Electromagnets (small, 24V)
- Basic solenoid (200N): $5-8
- Stronger solenoid (500N): $15-25
- Proportional solenoid (adjustable): $50-100

### Permanent Magnets
- Small neodymium disk (1cm): $0.50-1.00
- Medium magnet assembly: $2-5
- Magnet with keeper plate: $3-8

### Transformer Cores
- Small ferrite EE core: $1-2
- Silicon steel C-core (500VA): $10-30
- Toroid core (1kVA): $20-50

### Specialty Materials
- Mu-metal sheet (100×100mm): $50-100
- Ferrite bar antenna core: $2-5
- Superconducting wire (per meter): $10-50 (very specialized)

**Note**: Costs vary with quantity (1 piece vs. 1000 pieces) and supplier.

---

## Thermal Management in Magnetic Systems

### Cooling Methods & Effectiveness

| Method | Temperature Reduction | Cost | Complexity |
|--------|----------------------|------|------------|
| Natural convection | Baseline (100%) | None | None |
| Increased surface area (fins) | +20-30% | $1-2 | Low |
| Forced air (fan) | +50-100% | $5-20 | Medium |
| Oil bath cooling | +30-50% | $10-30 | Medium |
| Liquid cooling (water) | +100-200% | $50-500 | High |

**Design approach**:
1. Calculate power loss first (I²R for coils)
2. Estimate temperature rise (loss / surface area)
3. If too hot, add cooling incrementally
4. Avoid over-designing initially (adds cost/complexity)

---

## Performance vs. Cost Trade-offs

### Budget Electromagnet ($5-10)
- Material: Cold-rolled steel, basic coil
- Performance: Functional, slow response, limited force
- Reliability: Medium (thermal issues possible)
- Use: Industrial controls, non-critical switching

### Quality Electromagnet ($20-40)
- Material: Silicon steel, precision-wound coil
- Performance: Good force, faster response, thermal rated
- Reliability: High (tested to duty cycle)
- Use: Automotive, HVAC, appliances

### Premium Electromagnet ($100+)
- Material: Grain-oriented steel, custom winding
- Performance: Optimized for specific application
- Reliability: Excellent (over-designed for safety margin)
- Use: Aerospace, medical, critical control systems

**Designer question**: Do you need a $5 component or a $100 component?
- Answer: Design for your requirements, not your budget preference
- Example: Using a $5 solenoid that fails after 10,000 cycles costs less than designing a $20 solenoid rated for 1,000,000 cycles for a one-time use application
