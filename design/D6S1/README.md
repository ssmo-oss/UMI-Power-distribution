# D6S1 — MAIN schematic presentation revision

2026-09-29. MAIN schematic redrawn on one A4 landscape page: visible input supply rail, five fuse symbols and branch connectors, common return wiring, mechanical-only mounting symbols, and configuration notes. All component references, UUIDs, values, footprints and 22 electrical pin/net assignments are retained. Native ERC and PCB DRC including schematic parity pass with zero reported violations, unconnected items or parity issues. See MAIN_POWER/verification/REDRAW_AUDIT.json.

Open MAIN_POWER/MAIN_POWER.kicad_pro in KiCad 10. For a quick review, use MAIN_POWER/review/MAIN_POWER_schematic.pdf or MAIN_POWER.png.

The PCB file is byte-identical to D6. This is a schematic presentation update, not a physical board revision. The PCB title therefore still says D6. PoE and USB remain at D6. D6 manufacturing files remain in ../D6; they have not been regenerated or released by this update. All existing electrical qualifications and sourcing caveats still apply.

OUTLINE HOLD: corrected DXF/mechanical geometry has not been supplied. No mounting or board-outline change is included. Do not order from this package before the mechanics and supplier requirements are resolved. The original D6 schematic remains archived in ../D6.
