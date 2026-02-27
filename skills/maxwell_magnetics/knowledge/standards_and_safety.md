# Magnetic Standards, Regulations & Safety

## Electromagnetic Safety Standards

### Magnetic Field Exposure Limits (IEC 62366)

| Frequency | Limit | Context |
|-----------|-------|---------|
| Static (DC) | 8 T (general public), 2 T (occupational with warning) | MRI systems operate at 1.5-3 T |
| 50 Hz / 60 Hz | 200 μT | Typical high-voltage line: 10-20 μT at fence |
| High frequency (>100 kHz) | Specific Absorption Rate (SAR) limits | Wireless charging, medical implants |

**Practical implications**:
- Large neodymium magnets (>1 T) shouldn't be near people with pacemakers
- Electromagnets creating >8 T fields require access restriction
- Industrial high-frequency induction heating has strict SAR limits near workers

### Magnetic Shielding for Medical Devices

**Requirement**: Reduce stray magnetic field from electromagnets/transformers.

**Standards**:
- IEC 60601 (medical devices): Defines EMC (electromagnetic compatibility)
- Transformer shielding: Reduce field to <10 μT at 30cm distance
- Common solution: Mu-metal enclosure (expensive but highly effective)

**Cost-benefit**:
- No shielding: Possible interference with patient monitors
- Basic shielding (steel can): 20-50% field reduction
- Professional mu-metal shield: 99.9% field reduction, $500-2000

---

## Transformer Efficiency Standards

### EU 2014/61 (European Efficiency Regulation)

Defines minimum efficiency for distribution transformers:

| Capacity | Phase | Efficiency Minimum |
|----------|-------|-------------------|
| 25 kVA | 3-phase | 96.5% |
| 100 kVA | 3-phase | 97.2% |
| 250 kVA | 3-phase | 97.6% |
| 1 MVA | 3-phase | 97.9% |

**Designer impact**: Must use silicon steel cores and optimize design for <3% losses.

### U.S. NEMA Standards (TP-1, TP-2, TP-3)

Three efficiency classes for transformers:
- **TP-1**: Standard efficiency (94-95%)
- **TP-2**: High efficiency (96-97%)
- **TP-3**: Premium efficiency (97-98%)

**Economic driving factor**: Operating losses over 30-year lifespan exceed transformer purchase price. Premium efficiency becomes economical for continuously-operated transformers.

---

## Motor Efficiency Standards (IE3 / NEMA Premium)

### Global Harmonization

Minimum efficiency at 75% load:

| Power | IE3 / NEMA Premium |
|-------|-------------------|
| 1 kW | 91.0% |
| 10 kW | 93.0% |
| 100 kW | 95.0% |

**Magnetic design impact**:
- Requires thicker windings (lower losses)
- Better core material (grain-oriented steel)
- Results in heavier, larger motor (premium cost)
- Payback period: 2-3 years from energy savings

---

## Permanent Magnet Safety Regulations

### CPSC 16 CFR 1250 (U.S. Consumer Product Safety Commission)

Restricts high-power neodymium magnets in consumer products after child injuries:

**Definition of prohibited magnets**:
- Individual magnet with flux index >50 kG² (killiGauss squared)
- Sets available as multiple magnets totaling flux index >50 kG²

**Impact**:
- Consumer magnets must be weaker or encapsulated
- Professional/industrial magnets not restricted
- Manufacturer liability for injuries involving strong magnets

### EU Safety Directive (2014/35/EU)

Electromagnet-containing products must demonstrate electrical safety:
- Insulation coordination (voltage rating vs. insulation class)
- Temperature rise limits (Class B: 130°C maximum)
- Short-circuit protection
- Overcurrent protection

**Designer responsibility**:
- Create technical file documenting safety analysis
- Perform temperature testing at rated conditions
- Provide protection/shutdown mechanisms if failure possible

---

## Industry-Specific Standards

### Automotive Magnets (ISO 16750)

Requirements for components in vehicles:
- Operating temperature: -40 to +125°C
- Thermal cycling: 100+ cycles, no failure allowed
- Vibration: Survive 20 Hz to 500 Hz sweep
- Salt spray: 500+ hours without corrosion (neodymium must be coated)

**Cost impact**: Automotive-grade components cost 2-3× consumer-grade.

### Aerospace Magnets (AS9100C)

Most stringent requirements in industry:
- Traceability: Complete material history required
- Testing: 100% of batch tested (not sampling)
- Documentation: Extensive records for each component
- Environmental: Extreme temperature ranges (-60 to +250°C possible)
- Redundancy: Critical systems require backup magnet systems

**Cost impact**: Aerospace magnets can cost 10-50× consumer equivalents.

### Medical Device Magnets (ISO 13485)

Quality management system for medical devices:
- Biocompatibility testing: Magnets must not off-gas or corrode into patient
- Neodymium requirement: Encapsulated (not exposed)
- Design history file: Document all design decisions
- Risk analysis: FMEA (Failure Mode and Effects Analysis) required

**Typical timeline**: 18-24 months certification, $100k+ in testing.

---

## EMC (Electromagnetic Compatibility)

### What is EMC?

Equipment must:
1. **Not emit** unacceptable electromagnetic interference
2. **Tolerate** external electromagnetic interference within safe limits

### Relevant Frequency Bands

| Equipment | EMI Emission Limit | ESD Immunity |
|-----------|-------------------|--------------|
| Consumer (Class B) | -40 dBμV/m at 10m | ±4 kV contact, ±8 kV air |
| Industrial (Class A) | -30 dBμV/m at 10m | ±6 kV contact, ±15 kV air |

### Testing & Certification

- **EMI Emission**: Measure radiated and conducted interference
- **ESD Immunity**: Simulate electrostatic discharge contact/air gap
- **RF Immunity**: Simulate radio frequency fields (10 MHz - 1 GHz)
- **Cost**: $5,000-50,000 for full testing
- **Time**: 2-4 weeks in testing lab

---

## Environmental Regulations

### Restriction of Hazardous Substances (RoHS 2011/65/EU)

Restricts use of:
- Lead (Pb): Eliminated from solder in transformers/electromagnets
- Cadmium (Cd): Banned completely
- Chromium VI (CrVI): Banned

**Impact on magnetics**:
- Ferrite magnets OK (ceramic material, no heavy metals)
- Neodymium magnets OK (trace elements acceptable if <0.1%)
- Coatings must be RoHS compliant (no lead paint)

### WEEE (Waste Electrical and Electronic Equipment)

Manufacturers responsible for recycling discarded products:
- Magnets must be declared in technical documentation
- Ferromagnetic iron can be recycled (high scrap value)
- Neodymium magnets: Rare earth elements recoverable, but economics poor
- Current recycling rate: <5% for small permanent magnets

---

## When to Hire a Standards Consultant

**Hire an expert if**:
- Product will be sold internationally (IEC standards complex)
- Safety is critical (liability + legal liability)
- Aerospace/medical application (strict requirements)
- Unsure about certification path (can save $100k+ by avoiding wrong approach)

**DIY is OK for**:
- Hobby/personal projects (no certification needed)
- Industrial internal use (fewer regulations)
- Well-understood applications with off-the-shelf components

---

## Quick Checklist: Is My Design Compliant?

- [ ] Identified all applicable standards (IEC, NEMA, CPSC, etc.)
- [ ] Designed for duty cycle and temperature rise (thermal management)
- [ ] Verified insulation coordination and safety margins
- [ ] Checked for EMC issues (especially if powered electronics involved)
- [ ] Confirmed magnet materials are RoHS compliant
- [ ] Reviewed environmental exposure (salt spray, humidity, temperature extremes)
- [ ] Documented design decisions and test results
- [ ] Confirmed supplier components have appropriate certifications
