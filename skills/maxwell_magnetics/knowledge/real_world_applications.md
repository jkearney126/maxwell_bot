# Real-World Magnetic Applications & Case Studies

## Medical Imaging: MRI Systems

**Application**: Magnetic Resonance Imaging (MRI) creates detailed body scans without radiation.

**Key Challenges**:
- Field strength: 1.5-3.0 Tesla (clinical), up to 10.5 Tesla (research)
- Uniformity requirement: Better than 1 ppm over imaging volume
- Cryogenic cooling: Superconducting magnets at 4.2 K (-269°C)
- Heat dissipation: 10-15 kW cooling required continuously

**Material Choices**:
- Superconducting wire (Nb-Ti): Zero resistance, carries 100+ A per mm²
- Shielding: Multiple layers of mu-metal and ferrite to prevent external interference
- Gradient coils: Copper windings create small field variations for spatial encoding

**Design Tradeoff**: Cost vs. field strength
- 1.5 T: $1-2M, good for routine imaging
- 3.0 T: $3-5M, better resolution, more heating
- 7.0 T: $10M+, research only, severe heating/safety issues

## Power Transformers: Grid-Scale Energy Transfer

**Application**: Convert grid voltage (120kV) down to household use (120V) with >99% efficiency.

**Core Design**:
- Material: Grain-oriented silicon steel (very low loss)
- Size: 500 kg+ for typical distribution transformer
- Operating point: ~1.8 T (close to saturation, minimizes size)
- Cooling: Oil-based, with radiator fins

**Loss Breakdown**:
- Core loss (hysteresis + eddy current): 0.2-0.5% of power
- Copper loss (I²R): 1-2% of power
- Total efficiency: 96-99%

**Economic Reality**:
- Material cost: ~40% of transformer cost
- Design is optimized for lifetime losses, not initial price
- A 0.1% efficiency improvement saves millions in operating costs over 30+ year lifetime

## Electric Motors: Rotating Magnetic Fields

**Application**: Convert electrical power to mechanical motion in pumps, fans, compressors.

**Magnetic Design**:
- Stator: Multi-phase coils create rotating field pattern
- Rotor: Iron core with conductive bars (induction) or permanent magnets (BLDC)
- Air gap: 0.5-2mm, critical to efficiency
- Flux density in iron: 1.2-1.6 T (designed to avoid saturation)

**Efficiency Considerations**:
- Modern BLDC motors: 90-95% efficient
- Induction motors: 85-92% efficient
- Loss sources: Copper resistance, core eddy currents, friction

**Cost-Performance Tradeoff**:
- Premium motor (BLDC, neodymium): +30% cost, +5-10% efficiency, longer life
- Budget motor (induction, aluminum): Baseline cost, adequate for non-critical applications
- Payback period: 2-3 years for high-duty applications

## Magnetic Relays: Electromagnetic Switching

**Application**: Control high-power circuits with low-power signals (24V coil controls 480V load).

**Design Challenge**: Fast, reliable switching
- Armature acceleration: Must be <100ms for audio relays
- Contact bounce: Mechanical vibration causes multiple on/off cycles
- Arc suppression: Prevent electrical arcs at contacts

**Material Stack**:
- Coil: Copper wire on plastic bobbin (low cost)
- Core: Silicon steel or iron for high flux density
- Contacts: Silver alloy for low resistance and arc resistance
- Spring: Beryllium copper or stainless steel

**Failure Modes**:
- Sticking: Flux pulls contacts closed permanently (saturation)
- Bouncing: Multiple false on/off cycles damage logic
- Contact erosion: Arc vaporizes contact material over time

## Speakers: Audio Magnetic Actuation

**Application**: Convert electrical signals to mechanical vibration to produce sound.

**Design Parameters**:
- Magnet: Neodymium (modern) or ferrite (budget), flux density 0.3-1.0 T
- Coil: Light aluminum or copper, suspended in magnetic field
- Cone: Paper, plastic, or composite - driven by coil motion
- Acoustic impedance: Tuned via cabinet design

**Performance Trade-offs**:
- Bass response: Larger magnet + cone, lower frequency response
- Treble response: Smaller magnet, lighter cone
- Efficiency: 1-3% of electrical power → acoustic power (rest is heat)
- Nonlinearities: Magnet field distorts with coil position (nonlinear behavior)

## Magnetic Resonance: Quantum Applications

**Application**: Measuring atomic/nuclear properties at near-zero fields.

**Challenge**: Detecting extremely weak signals (picotesla range).

**Solution**: Atomic magnetometers
- Element choice: Potassium, rubidium (alkali metals have unpaired electrons)
- Laser polarization: Align nuclear spins to same direction
- Detection: Measure light absorption shift as field changes
- Sensitivity: Better than superconducting sensors for many applications
- Cost: 1/10th the price of SQUID sensors

## Lessons Across Applications

1. **Saturation limits design**: Can't exceed ~2 T easily, forces larger/heavier cores
2. **Thermal is critical**: Most failures are thermal, not magnetic
3. **Efficiency matters long-term**: Premium materials pay for themselves in operating costs
4. **Standards drive design**: IEEE, IEC standards set acceptable loss limits
5. **Air gaps kill efficiency**: Every mm of air gap is equivalent to centimeters of iron
