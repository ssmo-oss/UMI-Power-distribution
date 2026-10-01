# MAIN D8-2L — mechanical-outline adaptation candidate

Created 2026-09-30 from the D7-2L two-layer MAIN board after the owner supplied the corrected mechanical DXF. The editable KiCad project is `MAIN_POWER/MAIN_POWER.kicad_pro`. The D7-2L source project remains unchanged.

## Mechanical input

Latest source: `source/10052938_AA-UMI POWER PCB OUTLINE V3.dxf` (SHA-256 `10ADAB7113C99765CFB8C23128E78733F5ECCF2D0ECE246013FCFE98C07AA364`). DXF `$INSUNITS` is millimetres. V3 has 32 unique contour segments, bounds 121.8 × 60.5 mm, and six 3.5 mm diameter mounting holes. Compared with V2_1 it moves the upper inner pair from DXF X=±19 mm to ±16 mm and revises the contour. V3 is applied to both D8 MAIN options without scaling; earlier outline files are retained for history.

The DXF contour origin was mapped to the existing MAIN project coordinates as `x = 139.6 mm + DXF X` and `y = 97.131981 mm − DXF Y`. This keeps the board in the D7 project coordinate area. The DXF is mechanical geometry, not a source of electrical or assembly instructions.

## Layout adaptation

D8 starts from the D7-2L electrical design, rotates the component layout to fit the landscape profile, replaces the old four mounting holes with the six DXF holes, and refills the two copper zones. After the owner adjusted placement, the five fuse centers were aligned on one row, the five output connector centers on another, and each fuse/connector pair was centered on the same vertical line. The five fuse-holder footprints are on B.Cu (underside); all other components stay on F.Cu (top). All board text is on F.SilkS, with the fuse ratings and connector names centered on their corresponding columns. F3/J4 was shifted 1.5 mm left to clear mounting hole H2. The MAIN copper was rerouted: five fused outputs, a shared 12 V input bus routed around the DXF notch and mounting holes, and ground zones. On 2026-09-30, J1 was changed from the oversized Phoenix screw terminal to two 8 × 8 mm flat top-copper solder pads, labelled +12V and GND, sized for 10 AWG leads. Sixteen 1.0/0.5 mm ground stitching vias tie the GND pad to the B.Cu return plane. Lay the leads along the board and strain-relieve them to the enclosure or harness; do not use the solder joints as cable support. J1 has no connector part number. The circuit and other components are unchanged. `tools/create_d8_main.py` records the initial conversion from the original D7-2L board and DXF.

## Current validation and limits

KiCad 10.0.6 DRC with zone refill reports 0 violations, 0 unconnected items, and 0 schematic-parity issues. The board is an editable routing candidate, not released for manufacture. Electrical voltage-drop, thermal and enclosure validation remain outstanding; in particular, the 10 AWG input connection and copper path still need thermal qualification at the maximum intended current.

The top-view review is `MAIN_POWER/review/MAIN_POWER_D8.svg`; the underside view is `MAIN_POWER/review/MAIN_POWER_D8_bottom.svg`. The DRC data is `MAIN_POWER/verification/D8_DRC.json`.


## STEP assembly — 2026-10-01

`MAIN_POWER/MAIN_POWER_D8.step` includes the board, solder-mask surfaces, and all 10 modeled components (J2–J6 and F1–F5). J1 is the two flat input pads; input wires are not modeled. The JST VH and Littelfuse FLR bodies use project-local dimensioned envelope STEP models because those vendor models are absent from the installed KiCad model library. These simplified volumes preserve the specified connector/fuse identities and overall envelopes, but omit detail; use the STEP for arrangement and preliminary clearance review, then verify with vendor CAD before release. Raw tracks, pads, and zones are excluded from STEP export. Run `tools/export_d8_main_steps.ps1` to regenerate both D8 MAIN STEP assemblies.
