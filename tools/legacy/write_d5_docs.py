from pathlib import Path
src=Path('outputs/UMI_D4');dst=Path('outputs/UMI_D5');dst.mkdir(exist_ok=True)
s=(src/'ENGINEERING_AND_TEST_NOTES.md').read_text(encoding='utf8')
s=s.replace('UMI D4','UMI D5').replace('D4 is a procurement revision for ten MAIN_POWER and ten USB_POWER prototypes.','D5 separates distribution, boost conversion and USB conversion into ten MAIN_POWER, ten POE_POWER and ten USB_POWER prototypes.')
a=s.index('**MAIN_POWER**');b=s.index('## Electrical design envelope')
s=s[:a]+'''**MAIN_POWER** is a passive12V distribution board. **POE_POWER** is the separate protected53.5V boost board. **USB_POWER** supplies two current-limited USB-A charging sockets from its fused12V feed.

D5 is prepared for ten of each board. Native verification is pending in this document; only final D5 reports may establish a pass. These are untested prototype designs.

MAIN is68×100.263962mm, POE106×100mm and USB80×50mm. MAIN preserves four mounting-hole centers at(18,18),(70,18),(18,102.263962),(70,102.263962) in design coordinates. Use each board's Edge.Cuts and mechanical drawing for enclosure design; the separate POE board has its own mounting pattern.

'''+s[b:]
a=s.index('At an intentionally conservative');b=s.index('The USB feedback divider')
s=s[:a]+'''**The PoE switch and SENSING GMSL configurations are mutually exclusive.** This is a manual wiring/configuration rule, not a hardware interlock. Do not populate both loads and assume the revised budget covers them.

At an assumed90% converter efficiency, common loads are60W Jetson,1.68W fan and33.9759W USB input. Adding PoE requires77.8987W, giving **173.5546W /14.4629A at12V**. The alternative GMSL configuration with a provisional4A allowance totals143.6559W /11.9713A. Take the larger configuration, not their sum. GMSL's3A label has not been verified against a manufacturer aggregate-current specification;4A remains a design allowance, not a measured requirement.

At the boost's upper static output tolerance, the PoE configuration becomes174.4875W /14.5406A. This is not a full worst case: efficiency, USB output tolerance, startup, cable losses and auxiliaries remain. Input minimum voltage has not been specified; no10.8V operating guarantee is implied. Retain20A continuous supply-path design/test capability as margin. Do not raise the12V source to compensate cable loss without checking every device.

'''+s[b:]
s=s.replace('## D4 component changes','## Retained D4 electrical selections').replace('Main Q1–Q3','POE Q1–Q3').replace('Main J1 and R1 retain','MAIN J1 and POE R1 retain')
s=s.replace('MAIN_POWER J2/J3/J4/J5 are the Jetson, SG4A, fan and USB feeds respectively.','MAIN_POWER J2/J3/J4/J5/J6 are the Jetson, GMSL, fan, USB and POE12V feeds respectively.').replace('The 53.5 V switch output uses a distinct three-position connector.','POE_POWER J1 receives fused12V from MAIN J6. The53.5V switch output is POE J6, a distinct three-position connector.')
s=s.replace('USB via-in-pad holes','USB and POE via-in-pad holes')
s=s.replace('with the boost branch fuse removed','with MAIN F5 removed').replace('fit the specified boost input/output fuses','fit MAIN F5 and POE F6')
s=s.replace('test all specified loads simultaneously','test Jetson,fan,USB and the selected PoE-or-GMSL load simultaneously')
s=s.replace('connect the actual Ethernet switch, Jetson, SG4A unit and headset individually, then together','connect actual devices individually, then test each permitted configuration; never combine the PoE and GMSL loads')
s=s.replace('D4 README','D5 README').replace('ten of each board','ten of each of the three boards').replace('Main J1 and R1 remain','MAIN J1 and POE R1 remain').replace('Main C1 and L1','POE C1 and L1')
a=s.index('## Final mechanical and wiring details')
s=s[:a]+'''## Fuse and wiring decisions

All six system fuses remain. MAIN F1/F2/F3/F4/F5 are7.5A Jetson,7.5A GMSL,1A fan,5A USB and10A POE feed. F5 is at the cable source so it also protects the cable to POE J1; no duplicate local input fuse is fitted. POE F6 is3A80V on the53.5V output. Input eFuse protection does not establish that this output fuse is redundant.

Jetson7.5A is provisional, not the only possible value. A5A supply allowance is not a measured load or inrush specification. A5A fuse carrying5A has no demonstrated enclosure/startup margin; the manufacturer typical table permits6A loading on7.5A at65°C. Verify actual startup and the weakest harness segment before considering a lower rating.

All12V connectors use pin1 positive, pin2GND. POE J6 uses pin1+53.5V, pin2unused, pin3GND. Identify the board name before interpreting J6: MAIN J6 is12V, POE J6 is53.5V. Label the completed harness accordingly.

MAIN is passive: parallel12V power planes on F.Cu/In1.Cu, GND on In2.Cu/B.Cu, solid connections and dual-outer3mm fused branch tracks (1mm fan). No MAIN via-in-pad fabrication is required. POE and USB retain filled/capped vias. This geometry is not measured thermal qualification.
'''
(dst/'ENGINEERING_AND_TEST_NOTES.md').write_text(s,encoding='utf8')
(dst/'MANUFACTURING_SPECIFICATION.md').write_text('''# D5 fabrication and assembly specification — prototype

Prepare ten of each of three boards. Use only matched D5 source, Gerbers, drills, paste and placement files. Native checks are pending here; final D5 verification records establish actual pass status. No hardware qualification or approved manufacturing quote is claimed.

| Setting | MAIN_POWER | POE_POWER | USB_POWER |
|---|---|---|---|
|Outline|68×100.263962mm|106×100mm|80×50mm|
|Layers|4|4|4|
|Finished thickness|1.2mm|1.2mm|1.6mm|
|Outer copper|2oz|2oz|2oz|
|Inner copper|1oz|1oz|1oz|
|Finish|ENIG|ENIG|ENIG|
|Mask/legend|Green/white|Green/white|Green/white|
|SMT parts|0|53,top only|31,top only|
|Through-hole parts|11|3|3|
|Filled/capped vias|Not required|Required under solder pads|Required under solder pads|

Four copper layers are F.Cu,In1.Cu,In2.Cu,B.Cu. FR-4 Tg≥150°C requested; exact standard dielectric construction may be quoted provided total thickness and copper weights are retained. Do not silently substitute0.5oz inner copper. MAIN and POE thickness remains below the fuse holder's1.5mm PCB limit. USB requires a separate1.6mm build setting.

MAIN contains six connectors (Phoenix input plus five two-pin JST outputs) and five fuse holders, with no SMT. Its F.Cu/In1.Cu carry12V and In2.Cu/B.Cu GND, with solid connections. Fused branches use dual-outer3mm tracks except1mm fan. MAIN needs no VIPPO service. POE has SMT conversion/protection circuitry and three manual parts: J1input,F6holder,J6output. USB has31SMT and three manual connectors.

POE and USB solder-pad vias must be resin-filled and copper-capped. Tenting or soldermask plugging is not equivalent. Confirm stencil/thermal-pad treatment and the heavy Coilcraft inductor support fixture with the assembler. Reference the actual final drill files and board drawing; do not copy D4 geometry into the three-board build.

MAIN retains mounting centers(18,18),(70,18),(18,102.263962),(70,102.263962). POE has a separate mounting pattern defined by its delivered board/mechanical drawing. Manufacturing must use outline centerlines, not graphic stroke bounding boxes.

## Assembly handoff

Use per-board BOM_by_reference.csv, grouped BOM and the matching normalized supplier CPL. MAIN has no SMT placement operation. Raw KiCad local-footprint rotations are not substitutes for normalized CPL. Verify supplier preview against pin1/polarity and reference drawings. Preserve D4 component choices, including POE R2's manufacturer lands and MOSFET substitution qualifications; do not use D4 paste/position files after the split.

Installed procurement totals131parts per three-board set including manual items, as tracked by the consolidated procurement files; quantities for ten sets must include separately agreed spare/attrition allowance. MAIN J1 and POE R1 retain exact MPNs needing procurement/preorder confirmation. Visible stock is not reserved stock. POE C1/L1 have limited stock headroom; F6 has exactly ten observed inserts and no spares.

JLC library parts are PCBA-only and cannot simply ship loose. Agree supply/installation of hand-fitted headers, holders, inserts and cable-side parts, or buy them separately. The manual/harness arrangement remains pending. No external order or physical testing is established by these documents. Follow ENGINEERING_AND_TEST_NOTES.md before device connection.
''',encoding='utf8')
s=(src/'MANUAL_ASSEMBLY.md').read_text(encoding='utf8').replace('# D4','# D5').replace('ten MAIN_POWER and ten USB_POWER boards','ten MAIN_POWER, ten POE_POWER and ten USB_POWER boards').replace('Main F6','POE F6').replace('All six holders','All six system holders').replace('Main board thickness remains1.2','MAIN and POE board thickness remains1.2')
s=s.replace('Main board thickness remains 1.2 mm','MAIN and POE thickness remains1.2mm').replace('Main switch connector uses','POE switch connector uses')
s=s.replace('fifty housings for ten systems','seventy housings for ten systems').replace('main J2–J5 and USB J1','MAIN J2–J6, POE J1 and USB J1')
s += '''

## Three-board wiring and configuration

MAIN J1 is the source12V input. MAIN J2Jetson,J3GMSL,J4fan,J5USB andJ6POE each use pin1positive,pin2GND. MAIN F5 protects the cable feeding POE J1. No duplicate POE input fuse is fitted. POE J6 is the53.5V output: pin1positive,pin2empty,pin3GND. MAIN J6 and POE J6 have different voltages: label by board name and voltage.

PoE switch and GMSL must never be used in the same configuration. This is a manual configuration constraint, not interlocked hardware. Test the two permitted configurations separately. All six fuses remain; no removal is approved based on the lower combined power budget.

Each complete three-board set now has seven two-position cable housings (five MAIN outputs plus POE/USB inputs), one three-position POE output housing, and sixteen populated JST contacts if all connections use this scheme. For ten sets this is70two-position housings,10three-position housings and160contacts before spares. Select contact sizes for actual wires and reconcile the final consolidated harness BOM; device-end connectors remain installation-specific.
'''
(dst/'MANUAL_ASSEMBLY.md').write_text(s,encoding='utf8')
print('D5 documents prepared')
