# MAIN D8-2L — mechanical-outline adaptation candidate

Created 2026-09-30 from the D7-2L two-layer MAIN board after the owner supplied the corrected mechanical DXF. The editable KiCad project is `MAIN_POWER/MAIN_POWER.kicad_pro`. The D7-2L source project remains unchanged.

## Mechanical input

Latest source: `source/10052907_AA-UMI POWER PCB OUTLINE V2_1.dxf` (SHA-256 `0877C00FB9349EF65E27D2A11B6E98D88A92D332F4D000D3EFB83654D1033AA7`). The earlier V2 file is retained for history. DXF `$INSUNITS` is millimetres. Both versions have the same 30-segment closed contour with bounds 121.8 × 60.5 mm and six 3.5 mm diameter mounting holes; V2_1 relocates every hole by 1.33–1.41 mm. The V2_1 hole centers are applied to the six NPTH footprints. No scaling was applied.

The DXF contour origin was mapped to the existing MAIN project coordinates as `x = 139.6 mm + DXF X` and `y = 97.131981 mm − DXF Y`. This keeps the board in the D7 project coordinate area. The DXF is mechanical geometry, not a source of electrical or assembly instructions.

## Layout adaptation

D8 starts from the D7-2L electrical design, rotates the component layout to fit the landscape profile, replaces the old four mounting holes with the six DXF holes, and refills the two copper zones. After the owner adjusted placement, the five fuse centers were aligned on one row, the five output connector centers on another, and each fuse/connector pair was centered on the same vertical line. The five fuse-holder footprints are on B.Cu (underside); all other components stay on F.Cu (top). All board text is on F.SilkS, with the fuse ratings and connector names centered on their corresponding columns. F3/J4 was shifted 1.5 mm left to clear mounting hole H2. The MAIN copper was rerouted: five fused outputs, a shared 12 V input bus routed around the DXF notch and mounting holes, and ground zones. On 2026-09-30, J1 was changed from the oversized Phoenix screw terminal to two 8 × 8 mm flat top-copper solder pads, labelled +12V and GND, sized for 10 AWG leads. Sixteen 1.0/0.5 mm ground stitching vias tie the GND pad to the B.Cu return plane. Lay the leads along the board and strain-relieve them to the enclosure or harness; do not use the solder joints as cable support. J1 has no connector part number. The circuit and other components are unchanged. `tools/create_d8_main.py` records the initial conversion from the original D7-2L board and DXF.

## Current validation and limits

KiCad 10.0.6 DRC with zone refill after the flat-pad change reports 0 violations and 0 unconnected items. Fourteen schematic-parity warnings remain for the mechanical holes and footprint fields. The board is an editable routing candidate, not released for manufacture. The six mechanical holes still need matching schematic records. D8 has no manufacturing exports. Electrical voltage-drop, thermal and enclosure validation remain outstanding; in particular, the 10 AWG input connection and copper path still need thermal qualification at the maximum intended current.

The top-view review is `MAIN_POWER/review/MAIN_POWER_D8.svg`; the underside view is `MAIN_POWER/review/MAIN_POWER_D8_bottom.svg`. The DRC data is `MAIN_POWER/verification/D8_DRC.json`.


## STEP assembly — 2026-09-30

`MAIN_POWER/MAIN_POWER_D8.step` includes the D8 board body and the 10 remaining mounted component volumes (J2–J6 and F1–F5). The tall J1 terminal proxy has been removed to reflect the flat solder-pad input; the pads, solder and user-routed 10 AWG leads are not modeled as STEP solids. The other component volumes use scaled KiCad STEP proxies for JST VH connectors and blade-fuse holders, not exact vendor geometry. Use the file for arrangement/space review only; confirm enclosure clearances with vendor CAD before release. A copy of the prior STEP with the terminal proxy is retained in `MAIN_POWER/verification/MAIN_POWER_D8_with_previous_J1_terminal.step` for reference only.
