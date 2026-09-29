# Resume on another computer

Repository: https://github.com/ssmo-oss/UMI-Power-distribution

Download or clone this repository on the new computer. In a desktop agent with local folder access, open the repository folder as the project. For a cloud/chat agent, connect the repository if available, or upload the downloaded files; a URL alone does not guarantee the agent can edit the repository. Authentication and KiCad installation belong to the new machine and are not included in this repository. See [OpenAI project guidance](https://learn.chatgpt.com/docs/projects).

Read README.md, docs/PROJECT_HANDOFF.md, design/D6S1/README.md and design/D6/ENGINEERING_AND_TEST_NOTES.md. The latest MAIN schematic is D6S1; its PCB is still D6. PoE and USB remain D6. The corrected outlines/DXF are still missing. All manufacturing outputs remain on hold. Past checks passed but hardware tests are unperformed.

Paste this into the next agent:

> Continue the UMI power-distribution project from https://github.com/ssmo-oss/UMI-Power-distribution. Read START_HERE.md, README.md, docs/PROJECT_HANDOFF.md and design/D6S1/README.md before editing. Confirm which files you can actually access. The MAIN schematic redraw is D6S1, while its copper and the other two boards remain D6. Correct board outlines have not been supplied yet; wait for my mechanical files before changing geometry. Then apply the supplied outlines and mounting/connector constraints, adapt layout and routing, validate connectivity and regenerate matching manufacturing and mechanical files. Keep one combined sourcing list, preserve the three-board architecture and PoE-or-GMSL configuration rule. Record changes and remaining issues in the repository so work can continue from any computer. Do not submit orders or claim physical qualification.

For KiCad editing, open design/D6S1/MAIN_POWER/MAIN_POWER.kicad_pro (MAIN) or the corresponding project under design/D6 for POE and USB. Local symbol and footprint libraries are included. The old development scripts under tools/legacy contain machine-specific paths and are not a turnkey build pipeline. Earlier KiCad bundled Python/CLI invocations caused application-error dialogs; do not blindly rerun those scripts. Verify the available tools on the new computer first.

This is a durable project handoff, not a transfer of the old chat transcript, open editor windows, credentials or installed plugins. Update docs/PROJECT_HANDOFF.md and push completed changes before switching computers again.
