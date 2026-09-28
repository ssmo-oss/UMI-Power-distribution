# UMI D6 — engineering and prototype test notes

## The three boards

**MAIN_POWER** is a passive 12 V distribution board. **POE_POWER** is the separate protected 53.5 V boost board. **USB_POWER** supplies two current-limited USB-A charging sockets from its fused 12 V feed.

D6 is prepared for ten of each of the three boards. Final D6 native checks pass on all three boards: zero DRC violations, unconnected items, schematic parity issues and ERC violations. See each board’s verification folder. These are untested prototype designs.

MAIN is68×100.263962mm, POE106×100mm and USB80×50mm. MAIN preserves four mounting-hole centers at(18,18),(70,18),(18,102.263962),(70,102.263962) in design coordinates. Use each board's Edge.Cuts and mechanical drawing for enclosure design; the separate POE board has its own mounting pattern.

## Electrical design envelope

| Item | Design basis |
|---|---|
| External source | Mean Well RSP-320-12, nominal 12 V, 26.7 A; mains wiring is external to these PCBs |
| Enclosure ambient | Maximum 40 °C, as specified by the user |
| Jetson branch | 12 V, 5 A allowance |
| SG4A branch | 12 V, 4 A allowance |
| Fan branch | 12 V, 0.14 A nominal |
| Switch branch | 53.5 V, 1.31 A, approximately 70.1 W |
| USB board | Two charge-only USB-A outputs, 3 A electrical-load design target per socket |
| Interboard harness | Provisional maximum 1 m one-way, AWG16 copper pair; actual length was not supplied |
| Environment | Dry indoor enclosure; no claim of automotive, outdoor or medical qualification |

**The PoE switch and SENSING GMSL configurations are mutually exclusive.** This is a manual wiring/configuration rule, not a hardware interlock. Do not populate both loads and assume the revised budget covers them.

At an assumed 90% converter efficiency, common loads are 60 W Jetson,1.68W fan and 33.9759 W USB input. Adding PoE requires 77.8987 W, giving **173.5546W /14.4629A at 12 V**. The alternative GMSL configuration with a provisional 4 A allowance totals 143.6559 W /11.9713A. Take the larger configuration, not their sum. GMSL's3A label has not been verified against a manufacturer aggregate-current specification;4A remains a design allowance, not a measured requirement.

At the boost's upper static output tolerance, the PoE configuration becomes174.4875W /14.5406A. This is not a full worst case: efficiency, USB output tolerance, startup, cable losses and auxiliaries remain. Input minimum voltage has not been specified; no10.8V operating guarantee is implied. Retain 20 A continuous supply-path design/test capability as margin. Do not raise the 12 V source to compensate cable loss without checking every device.

The USB feedback divider targets 5.096 V. Reference and resistor tolerances give an estimated static regulator range of 5.012–5.181 V before ripple, bias-current error and transients. The current-limit switches and connector/cable resistances reduce loaded voltage. A 3 A electrical capacity does not establish that a connected headset will negotiate or draw 3 A. These sockets use charging identification, not USB Power Delivery, and have no data connection. Actual Meta Quest compatibility remains to be tested because the exact model was not specified.

Five 47 µF ceramic output capacitors are used at the USB buck. Their nominal sum is 235 µF; effective capacitance at bias is lower. TI's three-capacitor example states about 78 µF at 5 V and 25 °C; proportional scaling gives about 130 µF typical for five. This is not a guaranteed minimum over tolerance and temperature. Validate startup and load-step response on the prototype. No feedforward network is populated; TI describes it as optional near the minimum capacitance and its table/example guidance must not be applied without considering the series resistor and zero frequency.

## Retained D4 electrical selections

D4_COMPONENT_CHANGES_RETAINED.json records the inherited component substitutions; its original MAIN converter references now belong to POE_POWER. POE Q1–Q3 are Infineon BSC040N08NS5: same 80 V package/pinout, lower on-resistance but increased gate/output charge. The driver-current budget was reviewed; switching-node ringing, gate waveform and 40 °C thermal tests remain required. L2 changes to Coilcraft XAL4020-102MEC (packaging suffix), D2 to onsemi NRVB1H100SFT3G (same family/pinout), and the 4 mΩ shunt R2 to Ever Ohms MA251230FR004MZ. R2 uses the manufacturer-recommended 2.60 × 3.68 mm pads with a 2.55 mm inner gap; Kelvin sense continuity must be preserved.

R20 changes from 931 Ω to 953 Ω, with R19 84.5 kΩ and R18 1.96 kΩ, all 0.1%. The nominal boost target is **53.518163 V**. The calculated static tolerance interval is **52.879495–54.159133 V**, excluding ripple, bias effects and transients. A switch adapter label of 53.5 V is not evidence of its maximum acceptable input; verify the actual switch input range and startup behavior before connection.

Selected capacitors/resistors use the equivalents listed in the substitution manifest. No branch current ratings or fuse ratings were increased. USB input capacitors use the complete TDK order code CNA6P1X7R1H106KT000A. MAIN J1 retains exact Phoenix 1709681, sourced loose from DigiKey. POE R1 changes to stocked Yageo RC2010JK-077R5L, JLC C4169838: same 7.5 ohm, 5%, 0.75 W, 2010 size. Estimated snubber dissipation is 0.301 W nominal and 0.356 W with illustrative capacitor/frequency margins. This resolves the original preorder minimum; it does not establish measured pulse endurance. See verification/d6_electrical_resolution.md.

## Wiring and assembly

- Fit the exact through-hole connectors and fuse holders from the manual BOM. Fit fuse **inserts** separately; a holder's BOM entry does not include a fuse.
- MAIN_POWER J1 is the 12 V input. Check the finished board's pin labels against the pin schedule before wiring.
- MAIN_POWER J2/J3/J4/J5/J6 are the Jetson, GMSL, fan, USB and POE12V feeds respectively. Each two-pin output uses pin 1 positive and pin 2 return; verify against the final pin schedule.
- POE_POWER J1 receives fused 12 V from MAIN J6. The53.5V switch output is POE J6, a distinct three-position connector. Use only the populated supply/return positions documented in the final pin schedule. Never connect this output to a 12 V device.
- USB_POWER J1: pin 1 +12 V, pin 2 GND. J2/J3 are the two USB-A sockets; their shields connect to board GND.
- Use appropriately crimped JST contacts and verify retention. Do not tin wire before crimping it. The proposed AWG16 contact is JST SVH-41T-P1.1; thinner wire needs a compatible contact selected from the manufacturer's range.
- Use an adequately rated supply-input pair and upstream protection for the cable from the PSU to the board. Its fuse rating must match the final wire gauge and installation; the individual branch fuses do not protect an upstream input cable short.
- USB and POE via-in-pad holes must be resin-filled and copper-capped by the PCB fabricator, not left open under the module's solder pads. An ordinary stencil process over open holes is not an equivalent assembly process.
- The heavy Coilcraft SMT inductor may require an assembly support fixture. Confirm this with the assembler. The user's permission to fit through-hole components does not mean the large SMT inductor is to be hand fitted.

## Prototype bring-up record

Use a current-limited bench supply for initial tests. Disconnect the actual Jetson, switch and headset until unloaded voltage, polarity and control behavior have been checked. Record board revision, supply setting, load, ambient, waveforms and temperatures for each result.

1. **Unpowered inspection:** inspect component identities, polarities, solder joints and filled/capped thermal pads; check no hard shorts between each supply and GND. Verify the 53.5 V output connector separately.
2. **USB alone:** start from 12 V with a low current limit, no output load. Confirm approximately 5.1 V and no sustained oscillation. Increase input current allowance before applying loads. Test each output independently, then both at 3 A with electronic loads. Record voltage at board pads and at the cable-end load separately.
3. **USB transient response:** step each load from low load to 3 A and back, including simultaneous steps. Scope the regulator output and each port. Confirm no sustained oscillation and no damaging overshoot; use a short probe ground connection. Test cable insertion, removal and restart after a port overload.
4. **Main distribution:** with MAIN F5 removed, confirm polarity and nominal 12 V on each fused branch. Apply each specified load and record supply/input/connector voltage drop.
5. **Boost without switch:** fit MAIN F5 and POE F6, start unloaded and current limited. Confirm approximately 53.5 V, then increase an electronic load gradually to 1.31 A. Record input current, switching-node ringing, output ripple, startup overshoot and input-protection power-good timing. Use probes rated for the voltage and switching transients.
6. **Protection tests:** use controlled electronic-load overloads first. Verify individual USB-port current limiting and boost eFuse latch-off/recovery behavior. Test a hard output short only with a suitably rated switching fixture and current-limited source; record eFuse input/output excursions and diode current paths. Fuse ratings alone do not establish semiconductor short-circuit survival.
7. **Combined load and temperature:** test Jetson,fan,USB and the selected PoE-or-GMSL load simultaneously in the intended enclosure at 40 °C ambient until temperatures stabilize. Check the buck, current-limit switches, boost MOSFETs, inductor, eFuse, fuses, connectors and PCB. Stay within each component's recommended operating limits; TPSM63610 recommended maximum junction temperature is 125 °C, not its 150 °C absolute maximum. Package surface temperature is not identical to junction temperature.
8. **Real devices:** after the electrical tests, connect actual devices individually, then test each permitted configuration; never combine the PoE and GMSL loads. Check boot cycles, USB charging behavior, full load and cable hot-plugging. The switch's startup load and input capacitance were not specified.
9. **ESD and EMC:** evaluate the finished enclosure/cabling and USB protection on the prototype. Close ESD placement and clean DRC are not an IEC test result. Do not claim certified compliance from these design files.

No physical tests in this list have been performed by the software agent. A clean KiCad report verifies the configured schematic/layout rules and connectivity; it does not measure stability, heat, transient protection or compatibility.

## Ordering status

Read the D6 README and procurement records before ordering. The requested batch is ten of each of the three boards. Live catalogue inventory is not reserved inventory and does not establish assembly acceptance. MAIN J1 has an exact stocked loose-part source; POE R1 now uses the stocked Yageo part. POE C1 and L1 have limited stock headroom; assembler attrition must be included. The selected loose F6 source showed 378 pieces; the plan buys 20 for ten fitted plus ten spares. Manufacturer obsolescence is confirmed, so this resolves the current batch rather than future lifetime supply.

JLC parts-library components are for PCBA orders and cannot simply be shipped loose. The selected arrangement is JLC SMT assembly plus user fitting of separately purchased exact loose parts from LCSC/DigiKey; catalogue matches do not complete the harness procurement. Confirm copper/thickness, filled/capped vias, placement orientation and the heavy-inductor fixture in the quote. No physical test, order, payment or external upload is established by these documents.

Sources: [TI TPSM63610](https://www.ti.com/lit/ds/symlink/tpsm63610.pdf), [TI PMP21274](https://www.ti.com/tool/PMP21274), [TI TPS25982](https://www.ti.com/lit/ds/symlink/tps25982.pdf), [JST VH](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), [Würth USB-A connector](https://www.we-online.com/components/products/datasheet/614004190021.pdf). See the accompanying review records for calculations and unresolved procurement evidence.

## Fuse and wiring decisions

All six system fuses remain. MAIN F1/F2/F3/F4/F5 are7.5A Jetson,7.5A GMSL,1A fan,5A USB and10A POE feed. F5 is at the cable source so it also protects the cable to POE J1; no duplicate local input fuse is fitted. POE F6 is3A80V on the53.5V output. Input eFuse protection does not establish that this output fuse is redundant.

Jetson7.5A is provisional, not the only possible value. A5A supply allowance is not a measured load or inrush specification. A5A fuse carrying5A has no demonstrated enclosure/startup margin; the manufacturer typical table permits6A loading on7.5A at65°C. Verify actual startup and the weakest harness segment before considering a lower rating.

All12V connectors use pin 1 positive, pin 2GND. POE J6 uses pin 1+53.5V, pin 2unused, pin 3GND. Identify the board name before interpreting J6: MAIN J6 is12V, POE J6 is53.5V. Label the completed harness accordingly.

MAIN is passive: parallel12V power planes on F.Cu/In1.Cu, GND on In2.Cu/B.Cu, solid connections and dual-outer3mm fused branch tracks (1mm fan). No MAIN via-in-pad fabrication is required. POE and USB retain filled/capped vias. This geometry is not measured thermal qualification.


D6 fabrication detail: the five narrow POE OPT traces are now 0.16 mm; configured clearance remains 0.20 mm. MAIN visible small board legends are enlarged to 1 mm. Individual via filling/capping flags and the per-board VIA_TREATMENT.csv schedules identify selective epoxy fill and copper capping; 0.635 mm POE vias remain ordinary. See FABRICATION_NOTES.md.
