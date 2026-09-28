# D6 fabrication and assembly specification — prototype

Prepare ten of each of three boards. Use only matched D6 source, Gerbers, drills, paste and placement files. Final D6 DRC and ERC checks pass on all three boards; the per-board verification reports and source hashes record the checked versions. No hardware qualification or approved manufacturing quote is claimed.

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

Use per-board BOM_by_reference.csv, grouped BOM and the matching normalized supplier CPL. MAIN has no SMT placement operation. Raw KiCad local-footprint rotations are not substitutes for normalized CPL. Verify supplier preview against pin 1/polarity and reference drawings. Preserve D4 component choices, including POE R2's manufacturer lands and MOSFET substitution qualifications; do not use D4 paste/position files after the split.

Installed procurement totals131parts per three-board set including manual items, as tracked by the consolidated procurement files; quantities for ten sets must include separately agreed spare/attrition allowance. MAIN J1 uses its original exact MPN via loose procurement; POE R1 uses stocked Yageo RC2010JK-077R5L. Visible stock is not reserved stock. POE C1/L1 have limited stock headroom; F6 is sourced loose, with a purchase plan of twenty including ten spares.

JLC library parts are PCBA-only and cannot simply ship loose. Buy the exact loose manual parts from the suppliers in the consolidated list and fit them after JLC SMT assembly. Device-end plugs, final cable lengths and tooling remain installation-specific. No external order or physical testing is established by these documents. Follow ENGINEERING_AND_TEST_NOTES.md before device connection.


D6 fabrication detail: the five narrow POE OPT traces are now 0.16 mm; configured clearance remains 0.20 mm. MAIN visible small board legends are enlarged to 1 mm. Individual via filling/capping flags and the per-board VIA_TREATMENT.csv schedules identify selective epoxy fill and copper capping; 0.635 mm POE vias remain ordinary. See FABRICATION_NOTES.md.
