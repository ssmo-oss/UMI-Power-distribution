# MAIN D7-2L — two-layer prototype option

Created 2026-09-29 from the user's repaired D6L1 placement. Open MAIN_POWER/MAIN_POWER.kicad_pro in KiCad 10. This package is separate from the preserved four-layer option.

## What changed

MAIN now has only F.Cu and B.Cu. F.Cu carries the 12 V supply plane and fused branch tracks; B.Cu carries the ground plane and matching branch tracks. Both sides specify 0.070 mm copper (nominal 2 oz). Finished thickness stays 1.2 mm: nominal 1.04 mm FR4 core, two 0.07 mm copper layers and two 0.01 mm soldermask layers. The fabricator must implement the finished specification with its available stackup and tolerances.

All component positions, rotations, footprints, holes and outline are unchanged. The 110 existing outer-layer track segments are retained, including parallel 3 mm branch paths (1 mm for fan) and 2 mm fuse-terminal ties. Both remaining zones are solid-connected and refilled. No vias or selective via filling/capping are needed on MAIN. Top text positions are retained; revision legends now identify D7-2L. The schematic circuit is unchanged. PoE and USB are not changed by this revision and remain separate four-layer designs.

## Verification and limits

Native ERC passes. Native PCB DRC including schematic parity reports zero violations, zero unconnected items and zero parity issues. The audit checks exactly two copper layers, 1.2 mm stack thickness, preserved placements/outline/outer tracks, and a two-layer Gerber job. See MAIN_POWER/verification/TWO_LAYER_AUDIT.json.

The existing outer tracks already provide the five local branch paths; the removed inner layers were parallel supply and ground planes. Their removal reduces current-sharing and thermal margin. Ideal local branch-trace resistance calculations are included (roughly 0.42–0.43 milliohm for the paired 3 mm paths at 40 C). These estimates exclude fuse/connector resistance, pad entry constrictions, through-hole barrel resistance, shared plane losses, unequal sharing and self-heating. They are NOT a complete board voltage-drop, thermal or 20 A ampacity validation.

Retain the documented approximately 14.5 A operating-budget basis and 20 A input-path design/test target, but do not treat them as proven ratings. Measure complete-board voltage drop and temperature rise with both allowed configurations at 40 C enclosure ambient, including input pad/connector and fuse terminals. Final mechanical geometry is still unconfirmed. This is a candidate for prototype evaluation, not a production-qualified release.

## Fabrication and assembly

Use MAIN_POWER/MAIN_POWER_2L_GERBERS.zip only for this two-layer variant. Do not combine it with D6/D6L1 four-layer outputs. Two layers, 2 oz finished copper each side, 1.2 mm finished thickness, existing finish ENIG. Copper clearances/pads and hole geometry are unchanged. MAIN is through-hole/manual assembly; no SMT placement operation or stencil is required. Fuse inserts are separate from holders. Component sourcing remains the combined D6 list because part selection has not changed.

Matching Gerber/drill outputs, schematic PDF and top-copper preview are included. Older MAIN STEP models predate the user's rearranged placement and are not updated by this package. Existing wiring, fuse, PoE/GMSL exclusivity and qualification notes from D6 remain applicable.
