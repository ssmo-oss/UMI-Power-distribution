# D8 MAIN — FASTON 250 input alternative

This separate MAIN-board variant is based on D8-2L. It uses the owner-supplied V3 outline and keeps the fuse and connector arrangement, routing, copper zones, and output connectors. J1 is changed to two TE Connectivity 63951-4 FASTON 250 PCB tabs, each with two plated mounting holes (four holes total) on the tab axis, with both blade axes pointing toward the board's top edge in the top view. The flat solder-pad version remains in `design/D8-2L/MAIN_POWER/`.

The FASTON pair is centered on the board's 139.6 mm X centerline. Its footprint courtyard sits 2.5 mm in from the straight lower board edge.

## Input connector

- PCB terminals: TE Connectivity **63951-4**, quantity 2; FASTON 250, 6.35 × 0.8 mm tabs. Each tab uses two 1.4 mm plated holes at 5.08 mm pitch.
- Mating 10 AWG receptacle option: TE Connectivity **62998-2**, quantity 2, for 10–8 AWG wire. The mating receptacles and wires are off-board, not fitted to the PCB.
- TE lists 8.89 mm profile height from PCB for 63951-4, leaving 1.11 mm nominal margin under 10 mm. The same product page recommends 1.57 mm board thickness. This variant still uses 1.2 mm board thickness; confirm fit/retention with TE or update the stackup before ordering.
- The 10 mm clearance also needs checking with the selected female receptacles and wires installed. The TE 63951-4 summary does not state a current rating, so qualify the complete connection thermally at the intended maximum current. Terminals have no wire-insulation support; add harness strain relief.

## Files

- `MAIN_POWER/MAIN_POWER.kicad_pcb` — updated PCB; copper zones refilled.
- `MAIN_POWER/MAIN_POWER.kicad_sch` — J1 value, footprint, MPN and BOM status updated.
- `MAIN_POWER/UMI_D2.pretty/Input_FASTON_250_PAIR.kicad_mod` — pair footprint with four 1.4 mm plated holes (two per tab, 5.08 mm pitch) and top-view tab orientation shown on F.Fab.
- `MAIN_POWER/verification/D8_FASTON_DRC.json` — KiCad 10.0.6 check after V3 outline and zone refill: 0 rule violations, 0 unconnected items, and 0 schematic-parity warnings. The six DXF-derived 3.5 mm mounting holes have matching schematic records.
- `MAIN_POWER/review/MAIN_POWER_D8_FASTON.svg` — top-view preview.
- `MAIN_POWER/MAIN_POWER_D8_FASTON.step` — refreshed 2026-10-01; board, solder-mask surfaces, and all 11 modeled components (J1–J6 and F1–F5); raw tracks, pads, and zones are excluded.
- `MAIN_POWER/review/MAIN_POWER_D8_FASTON_3D.png` — 3D assembly preview showing the input blades extending toward the board top and the fuse-holder envelopes aligned over their backside pad patterns.

The STEP uses dimensioned envelope models for the TE 63951-4 terminal pair, the JST VH output headers, and the Littelfuse FLR fuse holders. They are simplified solid envelopes, not detailed vendor CAD. The FASTON pair uses a 6.35 × 0.8 mm blade, 8.89 mm profile height, four tails aligned to the four 1.4 mm holes, and a right-angle bend; the two blades point toward the board top, parallel to the fuse row. The B.Cu fuseholder envelopes are mirrored to match the pad patterns. TE recommends a 1.57 mm board; this candidate is still 1.2 mm. Confirm the terminal fit, 10 mm enclosure clearance, current capacity, and mating connector with exact vendor CAD before release. This remains a prototype layout candidate, not a manufacturing release.
