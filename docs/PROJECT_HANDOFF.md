# Project handoff â€” 2026-09-28

## Accepted requirements and decisions

- Original two-board proposal evolved into three boards for independent replacement/modification of the PoE supply. D6 is the latest delivered revision.
- Board expansion was subsequently authorized; earlier size requests (including the initial 30 Ã— 60 mm USB target) are superseded by the delivered dimensions. Use actual Edge.Cuts and mounting-hole geometry for mechanics.
- Ten of each board; user fits through-hole connectors/holders and fuse inserts. JLC is the intended SMT assembler. Keep all parts on one combined sourcing list.
- External supply basis: Mean Well RSP-320-12, nominal 12 V / 26.7 A. Mains wiring is outside these PCBs.
- Maximum enclosure ambient 40 Â°C. PoE and GMSL loads are mutually exclusive; budget the larger configuration.
- All six fuses retained: MAIN F1 Jetson 7.5 A, F2 GMSL 7.5 A, F3 fan 1 A, F4 USB 5 A, F5 PoE feed 10 A; POE F6 output 3 A / 80 V DC. F5 protects the interboard cable at its source, so no duplicate local PoE input fuse is fitted.
- Jetson 7.5 A is a provisional protection rating, not its normal consumption. Validate startup, ambient derating and the weakest harness section before reducing it. USB port current-limit devices protect each output independently; a charging-only socket still requires overload protection.

## Completed evidence

Use design/D6/README.md and verification/FINAL_AUDIT.json for final D6 results. Schematics, local symbols/footprints, boards, Gerbers, drills, SMT BOMs, normalized placement files, manual BOMs, fabrication drawings, placement reviews and test records are included. D6 corrected the snubber resistor sourcing, inner-layer identities, five narrow PoE traces, selected text sizes and via-treatment metadata. The manufacturing source files are preserved without edits in this transfer.

Six simplified STEP files were generated and reimported through Open CASCADE. Their geometry reports pass; component heights remain approximate. No manufacturing change resulted from STEP generation.

## Remaining work before manufacture and system release

**First priority â€” corrected board outlines:** On 2026-09-28 the owner confirmed that the existing outlines are out of date. Correct replacement geometry is pending; no outline changes have been guessed or applied. Obtain the authoritative mechanical files/dimensions for the affected boards, including mounting holes and connector constraints. Rework layout/routing as needed, validate clearances and regenerate manufacturing and STEP outputs as a new revision. Current D6 files are historical design evidence, not approved final mechanics.

1. Obtain supplier acceptance of the explicit 4-layer copper/thickness combinations, selective epoxy fill/copper cap treatment and heavy-inductor fixture. QUOTE_REQUEST.md is prepared but has not been sent to JLC. Review placement/polarity previews and exact assembly attrition before purchasing.
2. Recheck and reserve stock at ordering time. Prior observations include tight C1 and L1 stock and the obsolete Littelfuse 166.7000.4302 output fuse; these are not live stock guarantees.
3. Confirm the exact Ethernet switch model/input-voltage tolerance and USB-powered device model. The supplied switch requirement was 53.5 V / 1.31 A; that alone does not verify maximum input tolerance. USB-A outputs do not provide USB PD or data; device charging compatibility remains untested.
4. Finalize cable lengths, device-end plugs, wire/pigtail ratings and upstream input-cable protection. AWG16 and at most 1 m one-way are provisional interboard assumptions, not confirmed installation measurements.
5. Perform the test plan: polarity, unloaded startup, load steps, regulation/ripple, boost ringing/snubber, eFuse and per-port faults, fuse behavior, thermal rise at 40 Â°C, real-device boot/charging and enclosure EMC/ESD as applicable. No physical results have been claimed.
6. Replace estimated STEP bodies with verified mechanical envelopes before final enclosure signoff; include mating plugs and cable bends.

## Tooling notes

Earlier KiCad bundled Python and CLI invocations produced application-crash dialogs. Later native checks used an isolated wrapper and API-based workflows. Historical scripts contain machine-specific paths and some mutate designs. Do not execute the legacy directory as an automated pipeline. The saved D6 projects and validated outputs are the authoritative handoff.

The original knowledge-base pointer is https://sklvc.atlassian.net/wiki/spaces/LMP/pages/2171306022/UMI+Pack (access may require authentication). This transfer does not publish a dump of the private knowledge base, account credentials or browser sessions. Public manufacturer references are retained in the engineering documents.

The user's previous permission question about sending files to JLC remains unanswered. This GitHub transfer is explicitly authorized; it does not constitute permission to place orders, make payments or contact JLC.

## Latest update — 2026-09-29

MAIN schematic presentation is now D6S1 in design/D6S1/MAIN_POWER. It uses visible supply/return rails and fused branches instead of disconnected-looking blocks. All 22 electrical pin/net assignments match D6; ERC and DRC/parity checks pass. The physical MAIN PCB is byte-identical to D6; PoE and USB remain D6. Corrected mechanical outlines are still pending: the user said on September 28 that they did not have the DXF yet. Do not infer that a replacement arrived merely because the planned day has passed.

## MAIN user-layout repair — D6L1, 2026-09-29

Use design/D6L1/MAIN_POWER for the latest MAIN PCB and accompanying D6S1 schematic. The user rearranged components in KiCad; five branches were rerouted and four planes refilled without changing any footprint or board graphics. Final DRC/parity reports zero violations and zero unconnected items. D6 and D6S1 remain historical copies. MAIN Gerbers, STEP files and position-based documentation from those revisions are stale and need regeneration after mechanical confirmation. PoE and USB remain D6. User-open source files were preserved; continue from the delivered D6L1 copy.

MAIN D6L1 text update: all printed board notes are now on F.SilkS; six former B.SilkS notes were unmirrored and placed below the outputs. Copper and component placement unchanged; DRC/parity remains clean.
