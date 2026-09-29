# MAIN D6L1 — reconnected user layout

2026-09-29. Repaired the layout saved by the user in the extracted D6S1 package. All 15 footprint placements, rotations, footprint contents, mounting holes, outline and board graphics are preserved. Removed old tracks and rebuilt the five fused branch connections on both outer layers: 3 mm branch tracks except the 1 mm fan branch, with 2 mm fuse terminal links. Refilled all four zones: F.Cu/In1.Cu 12V_IN, In2.Cu/B.Cu GND. No vias are required; through-hole pads connect the layers.

Final native DRC including schematic parity: 0 violations, 0 unconnected items, 0 parity issues. Initial saved layout: 421 reported violations and 28 unconnected items, including stale copper fill. See MAIN_POWER/verification/REPAIR_AUDIT.json and DRC.json. Initial reports are retained as before-repair evidence only.

Open MAIN_POWER/MAIN_POWER.kicad_pro or MAIN_POWER.kicad_pcb. This is a separate saved copy; the user's open source board was not overwritten. Its silkscreen still reads D6, as part of preserving the user's graphics. D6L1 is the package identifier. The schematic is the D6S1 redraw.

The previous D6 Gerbers, STEP models and placement-dependent drawings do not describe this new layout. They have not been reissued here. Outline confirmation and hardware qualification remain pending. Do not manufacture from the old outputs. Inspect the saved repair, then continue editing this copy to avoid accidentally replacing it with the still-open older board.

## Top-side text update

All six back-side silkscreen notes were moved to F.SilkS, unmirrored and arranged below the output connectors. Text formerly outside the outline is now inside the board. Copper, components and outline are unchanged. Native DRC/parity passes. See verification/TOP_TEXT_AUDIT.json. This supersedes the earlier statement about preserving all board graphics.
