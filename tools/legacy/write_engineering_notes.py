from pathlib import Path
import json
root=Path('outputs/UMI_D2');root.mkdir(exist_ok=True)
notes='''# UMI two-board system — engineering and prototype test notes

## The two boards

**MAIN_POWER** distributes the external 12 V supply to the Jetson, SG4A unit, fan and USB board. Its protected boost converter supplies the Ethernet switch at approximately 53.5 V. **USB_POWER** converts its fused 12 V feed to approximately 5.1 V and supplies two current-limited USB-A charging sockets. D1 and D2 were revision names, not the names of the two different functions.

The latest authorized enclosure assumption is that either board may be enlarged. The USB board is 80 × 50 mm. The main board retains the original four mounting-hole locations while enlarging the outline; use its final Edge.Cuts and mechanical drawing for the exact dimensions. Do not design the enclosure from old D1 or UMI_USB_D2 files.

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

At an intentionally conservative 90% efficiency for each converter, the simultaneous nominal demand is about 221 W / 18.4 A at 12 V: 60 W Jetson + 48 W SG4A + 1.68 W fan + 33.3 W USB input + 77.9 W switch input. This is a design budget, not a measurement. It excludes unknown startup peaks and enclosure auxiliaries. Do not increase the supply voltage to compensate cable loss without reviewing every connected device.

The USB feedback divider targets 5.096 V. Reference and resistor tolerances give an estimated static regulator range of 5.012–5.181 V before ripple, bias-current error and transients. The current-limit switches and connector/cable resistances reduce loaded voltage. A 3 A electrical capacity does not establish that a connected headset will negotiate or draw 3 A. These sockets use charging identification, not USB Power Delivery, and have no data connection. Actual Meta Quest compatibility remains to be tested because the exact model was not specified.

Five 47 µF ceramic output capacitors are used at the USB buck. Their nominal sum is 235 µF; effective capacitance at bias is lower. TI's three-capacitor example states about 78 µF at 5 V and 25 °C; proportional scaling gives about 130 µF typical for five. This is not a guaranteed minimum over tolerance and temperature. Validate startup and load-step response on the prototype. No feedforward network is populated; TI describes it as optional near the minimum capacitance and its table/example guidance must not be applied without considering the series resistor and zero frequency.

## Wiring and assembly

- Fit the exact through-hole connectors and fuse holders from the manual BOM. Fit fuse **inserts** separately; a holder's BOM entry does not include a fuse.
- MAIN_POWER J1 is the 12 V input. Check the finished board's pin labels against the pin schedule before wiring.
- MAIN_POWER J2/J3/J4/J5 are the Jetson, SG4A, fan and USB feeds respectively. Each two-pin output uses pin 1 positive and pin 2 return; verify against the final pin schedule.
- The 53.5 V switch output uses a distinct three-position connector. Use only the populated supply/return positions documented in the final pin schedule. Never connect this output to a 12 V device.
- USB_POWER J1: pin 1 +12 V, pin 2 GND. J2/J3 are the two USB-A sockets; their shields connect to board GND.
- Use appropriately crimped JST contacts and verify retention. Do not tin wire before crimping it. The proposed AWG16 contact is JST SVH-41T-P1.1; thinner wire needs a compatible contact selected from the manufacturer's range.
- Use an adequately rated supply-input pair and upstream protection for the cable from the PSU to the board. Its fuse rating must match the final wire gauge and installation; the individual branch fuses do not protect an upstream input cable short.
- USB via-in-pad holes must be resin-filled and copper-capped by the PCB fabricator, not left open under the module's solder pads. An ordinary stencil process over open holes is not an equivalent assembly process.
- The heavy Coilcraft SMT inductor may require an assembly support fixture. Confirm this with the assembler. The user's permission to fit through-hole components does not mean the large SMT inductor is to be hand fitted.

## Prototype bring-up record

Use a current-limited bench supply for initial tests. Disconnect the actual Jetson, switch and headset until unloaded voltage, polarity and control behavior have been checked. Record board revision, supply setting, load, ambient, waveforms and temperatures for each result.

1. **Unpowered inspection:** inspect component identities, polarities, solder joints and filled/capped thermal pads; check no hard shorts between each supply and GND. Verify the 53.5 V output connector separately.
2. **USB alone:** start from 12 V with a low current limit, no output load. Confirm approximately 5.1 V and no sustained oscillation. Increase input current allowance before applying loads. Test each output independently, then both at 3 A with electronic loads. Record voltage at board pads and at the cable-end load separately.
3. **USB transient response:** step each load from low load to 3 A and back, including simultaneous steps. Scope the regulator output and each port. Confirm no sustained oscillation and no damaging overshoot; use a short probe ground connection. Test cable insertion, removal and restart after a port overload.
4. **Main distribution:** with the boost branch fuse removed, confirm polarity and nominal 12 V on each fused branch. Apply each specified load and record supply/input/connector voltage drop.
5. **Boost without switch:** fit the specified boost input/output fuses, start unloaded and current limited. Confirm approximately 53.5 V, then increase an electronic load gradually to 1.31 A. Record input current, switching-node ringing, output ripple, startup overshoot and input-protection power-good timing. Use probes rated for the voltage and switching transients.
6. **Protection tests:** use controlled electronic-load overloads first. Verify individual USB-port current limiting and boost eFuse latch-off/recovery behavior. Test a hard output short only with a suitably rated switching fixture and current-limited source; record eFuse input/output excursions and diode current paths. Fuse ratings alone do not establish semiconductor short-circuit survival.
7. **Combined load and temperature:** test all specified loads simultaneously in the intended enclosure at 40 °C ambient until temperatures stabilize. Check the buck, current-limit switches, boost MOSFETs, inductor, eFuse, fuses, connectors and PCB. Stay within each component's recommended operating limits; TPSM63610 recommended maximum junction temperature is 125 °C, not its 150 °C absolute maximum. Package surface temperature is not identical to junction temperature.
8. **Real devices:** after the electrical tests, connect the actual Ethernet switch, Jetson, SG4A unit and headset individually, then together. Check boot cycles, USB charging behavior, full load and cable hot-plugging. The switch's startup load and input capacitance were not specified.
9. **ESD and EMC:** evaluate the finished enclosure/cabling and USB protection on the prototype. Close ESD placement and clean DRC are not an IEC test result. Do not claim certified compliance from these design files.

No physical tests in this list have been performed by the software agent. A clean KiCad report verifies the configured schematic/layout rules and connectivity; it does not measure stability, heat, transient protection or compatibility.

## Ordering status

Read the final release-status file before ordering. Exact MPNs are provided where selected; blank catalog codes in BOM_JLC_DRAFT.csv are unresolved assembler sourcing, not permission for substitution. Confirm all sourcing, copper thickness, board thickness, via-in-pad processing, assembly orientation and the heavy-inductor fixture in the quote. No order, payment or external upload has been made.

Sources: [TI TPSM63610](https://www.ti.com/lit/ds/symlink/tpsm63610.pdf), [TI PMP21274](https://www.ti.com/tool/PMP21274), [TI TPS25982](https://www.ti.com/lit/ds/symlink/tps25982.pdf), [JST VH](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), [Würth USB-A connector](https://www.we-online.com/components/products/datasheet/614004190021.pdf). See the accompanying review records for calculations and unresolved procurement evidence.
'''
(root/'ENGINEERING_AND_TEST_NOTES.md').write_text(notes,encoding='utf-8')
print(root/'ENGINEERING_AND_TEST_NOTES.md')
