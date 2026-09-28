# D3 visual and assembly recommendations

Read-only review of D2 delivered layouts. Clean native DRC is not a substitute for these improvements.

## Main
- Keep the compact TI switching/gate/sense placement. Do not spread it just to fill the board.
- Organize the distribution section as four aligned branch cells with consistent holder-to-connector spacing. Existing row alignment is a useful starting point.
- Restore visible F1–F6 and J1–J6 references, connector functions, polarity and fuse ratings. Many references disappeared when crowded silkscreen was moved wholesale to fabrication layer.
- Use the empty lower-middle region for a clear title/revision and a compact connector/fuse key, or a ref-only assembly legend.
- Clean the long output path into a deliberate edge corridor with consistent 45-degree transitions and a short fuse approach. Avoid cosmetic trace changes in Kelvin-sense and gate loops.
- Current fabrication page overlaps values and references severely. Produce a ref-only assembly view, with enlarged boost detail if needed; BOM supplies values.

## USB
- Label the two sockets PORT1 / PORT2 and 5V / 3A; ensure J2/J3 are visible.
- Align mounting columns: H3 x13.5 differs from H1 x14; right column is already consistent.
- Centre the added C13/C14 row under the main output capacitor bank, subject to tight low-impedance routing.
- Use consistent horizontal ref text; restore crowded/absent C1, U1, R7, R9 and C10 references. C13 vertical text currently breaks the pattern.
- Review whether input bulk C12 can sit nearer the input/buck path rather than visually isolated top-right. Electrical placement takes priority.
- Preserve the matched port-channel placement and ESD devices immediately behind each socket.

## Shared finish
Use one reference font/size, larger functional connector legends, and a restrained title/revision. Do not print long part values on the board. Use real footprint rotation metadata where practical, or retain a rigorously normalized physical-angle CPL, so visual cleanup does not reintroduce assembly orientation errors. Review actual board, copper plots and ref-only assembly drawing separately.
