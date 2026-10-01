LATEST MAIN MECHANICAL CANDIDATE (2026-10-01): both `design/D8-2L/MAIN_POWER/` (flat solder-pad input) and `design/D8-2L-FASTON/MAIN_POWER/` (two TE 63951-4 input tabs) use the owner-supplied V3 outline. Both pass KiCad 10.0.6 DRC with 0 violations, 0 unconnected items, and 0 schematic-parity issues. Matching STEP assemblies are saved in each MAIN_POWER folder. They include board/copper and mounted component volumes, with simplified proxies for connector and fuse-holder geometry. FASTON uses a dimension-based tab proxy rather than the gated manufacturer model. Confirm the terminal fit, 10 mm enclosure clearance, current capacity, and mating connector with exact vendor CAD; TE recommends a 1.57 mm board while these candidates remain 1.2 mm. Read both D8 README files before further work. The V3 update applies to MAIN only; POE and USB remain at their prior D6 mechanical revisions. D7-2L remains unchanged as the electrical baseline.

## Cart update — 29 September 2026

Ten-board MAIN D7-2L carts are now saved at JLCPCB and DigiKey. No payment/order submission. See [cart status](procurement/MAIN_D7_2L_UK_10/ONLINE_CART_STATUS.md). Earlier basket-failure notes are superseded. Mechanical and thermal holds remain.

# Resume on another computer

LATEST PROCUREMENT (2026-09-29): `procurement/MAIN_D7_2L_UK_10/` contains the MAIN-only ten-board UK purchasing list, DigiKey basket import files, matching two-layer JLCPCB Gerber ZIP and order settings. It includes the latest 3 mm FAN tracks. No online basket/order was completed; DigiKey Bulk Add returned a server error. The existing mechanical and physical-validation holds remain. For MAIN, use `design/D7-2L/MAIN_POWER/MAIN_POWER.kicad_pro`; the older D6 MAIN instructions below are historical.

NEWEST OPTION: MAIN D7-2L is the requested two-layer prototype in design/D7-2L/MAIN_POWER, preserving the D6L1 component layout. Read its README and the latest handoff entry. D6L1 remains the four-layer fallback. Neither is production-qualified.

LATEST UPDATE: MAIN layout is now D6L1 (design/D6L1/MAIN_POWER), reconnected after user placement edits; its schematic is the D6S1 redraw. Read the latest entry in docs/PROJECT_HANDOFF.md. D6/D6S1 MAIN manufacturing and STEP outputs are stale for this layout. The older state described below is superseded for MAIN PCB selection.

Repository: https://github.com/ssmo-oss/UMI-Power-distribution

Download or clone this repository on the new computer. In a desktop agent with local folder access, open the repository folder as the project. For a cloud/chat agent, connect the repository if available, or upload the downloaded files; a URL alone does not guarantee the agent can edit the repository. Authentication and KiCad installation belong to the new machine and are not included in this repository. See [OpenAI project guidance](https://learn.chatgpt.com/docs/projects).

Read README.md, docs/PROJECT_HANDOFF.md, design/D6S1/README.md and design/D6/ENGINEERING_AND_TEST_NOTES.md. The latest MAIN schematic is D6S1; its PCB is still D6. PoE and USB remain D6. The corrected outline is applied to MAIN in D8-2L. POE/USB mechanics and all manufacturing outputs remain on hold. Past checks passed but hardware tests are unperformed.

Paste this into the next agent:

> Continue the UMI power-distribution project from https://github.com/ssmo-oss/UMI-Power-distribution. Read START_HERE.md, README.md, docs/PROJECT_HANDOFF.md and design/D6S1/README.md before editing. Confirm which files you can actually access. The MAIN schematic redraw is D6S1, while its copper and the other two boards remain D6. The owner supplied a revised MAIN-only outline, now applied in design/D8-2L/MAIN_POWER. POE/USB replacement mechanics remain pending. Continue from D8 for MAIN, validate connectivity and clearance, and regenerate matching manufacturing and mechanical files only after remaining review items and mechanics are resolved. Keep one combined sourcing list, preserve the three-board architecture and PoE-or-GMSL configuration rule. Record changes and remaining issues in the repository so work can continue from any computer. Do not submit orders or claim physical qualification.

For KiCad editing, open design/D6S1/MAIN_POWER/MAIN_POWER.kicad_pro (MAIN) or the corresponding project under design/D6 for POE and USB. Local symbol and footprint libraries are included. The old development scripts under tools/legacy contain machine-specific paths and are not a turnkey build pipeline. Earlier KiCad bundled Python/CLI invocations caused application-error dialogs; do not blindly rerun those scripts. Verify the available tools on the new computer first.

This is a durable project handoff, not a transfer of the old chat transcript, open editor windows, credentials or installed plugins. Update docs/PROJECT_HANDOFF.md and push completed changes before switching computers again.
