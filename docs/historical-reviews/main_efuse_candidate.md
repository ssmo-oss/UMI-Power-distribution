# Boost input eFuse integration candidate — engineering hold

Use TPS259824ONRGER (letter O, circuit breaker), between F5 and all boost circuitry. Existing fuse remains upstream. Source: https://www.ti.com/lit/ds/symlink/tps25982.pdf (Rev D, May 2026).

Pin schedule: 1/2/3/16 and exposed Pad 1 = FUSED_12V; 17–24 = BOOST_IN; 4/5/14 and exposed Pad 2 = GND; 6 = EFUSE_EN; 7 = ITIMER (unconnected initially); 8 = ILIM via 182 ohm 0.1% to GND; 9 = IMON via 511 ohm to GND and test point; 10 RETRY_DLY = GND for latch-off; 11 NRETRY = unconnected; 12 LDSTRT = GND; 13 PG = existing LM5122 UVLO net; 15 dVdt = 6.8 nF / 50 V C0G to GND. Exposed pads are DIFFERENT nets; generic single-ground-EP QFN is invalid.

Engineering choices/calculations:

- EN divider: 100k top from FUSED_12V, 13.7k bottom to GND, both 0.1%. Nominal threshold 9.959 V. Threshold-only extrema 9.793–10.208 V; resistor tolerance and leakage add approximately 0.03 V. 12 V gives 1.446 V EN, well below 6 V recommended limit.
- Tie PG directly to LM5122 UVLO to hold the boost disabled until eFuse fully enhances. The existing 49.9k/8.45k divider supplies the PG pull-up safely (1.738 V at 12 V). Check this joint net against both datasheets before implementation. Do not add a 12 V PG pull-up.
- 182 ohm gives nominal 8.132 A threshold, characterized range 7.23–9.07 A before resistor tolerance. Nominal full switch load at 90% efficiency is 6.49 A at 12 V; at 10 V it becomes 7.79 A and can trip. Therefore this setting supports nominal 12 V, not a guaranteed full-load 10 V operating range.
- 6.8 nF gives approximately 0.676 V/ms and 17.74 ms full 12 V ramp. With boost disabled, local boost input plus output capacitors charge through L1/Q1 body diode. Local nominal capacitance is about 127 uF, giving only 86 mA ramp current. Switch input capacitance adds to this and is unknown. 1 mF additional capacitance would add 0.676 A. Powering an active switch load before boost starts must be tested.
- ITIMER initially open avoids deliberately passing sustained overcurrent. Provide DNP capacitor pads so transient blanking can be characterized later; do not short ITIMER to ground.
- At 6.49 A and maximum 4.5 milliohm on-resistance, eFuse loss is 0.190 W. This is a useful low-loss candidate; thermal vias and actual board copper still matter.

Transient network candidate:

- Littelfuse SMBJ15A from FUSED_12V cathode to GND anode, immediately at eFuse. 15 V stand-off, 24.4 V clamp at 24.6 A (10/1000 us). This is below 30 V IC absolute maximum at the stated waveform; wiring inductance, pulse shape and temperature still require validation. Source: https://m.littelfuse.com/~/media/electronics/datasheets/tvs_diodes/littelfuse_tvs_diode_smbj_datasheet.pdf.pdf
- Input bypass 1 uF/50 V X7R + 100 nF/50 V directly across eFuse IN/GND, with upstream bulk available. Keep paths short.
- Diodes Inc B540C-13-F, cathode BOOST_IN/anode GND, candidate negative transient catch diode. Source: https://www.diodes.com/datasheet/download/B540C.pdf . Rating 40 V, 5 A average, 100 A surge; verify current manufacturing status because the family page lists an EOL PCN whose affected codes were not yet inspected. At interruption it must carry boost-inductor current; verify forward drop at worst transient current against eFuse OUT -0.8 V limit. This part is not approved solely from its 5 A average rating.

Remaining release blockers: custom split-pad footprint, clamp and layout parasitics, proof of negative voltage bound, actual switch capacitance/load startup, short-circuit interruption waveforms, thermal test, and fuse coordination. This candidate is suitable for capture and review, not an assertion of validated protection.
