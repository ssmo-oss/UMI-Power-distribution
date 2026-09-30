# UMI Power Distribution

Three separate boards distribute a 12 V supply to the UMI system. **D6 is the current prototype revision. It has not been physically qualified or approved for production.**

## Latest mechanical candidate — D8-2L MAIN

The owner supplied [10052907_AA-UMI POWER PCB OUTLINE V2_1.dxf](design/D8-2L/source/10052907_AA-UMI%20POWER%20PCB%20OUTLINE%20V2_1.dxf) for MAIN only on 2026-09-30. [D8-2L](design/D8-2L/README.md) applies its six revised 3.5 mm mounting-hole centers; the 121.8 × 60.5 mm outer contour is unchanged from V2. Fuse holders are on the underside, other components and text are on top, and the power paths are rerouted. J1 is now a pair of flat +12V/GND solder pads for 10 AWG input leads; the lead wires need external strain relief. D7-2L remains unchanged.
A separate FASTON input alternative using two TE 63951-4 tabs is in [D8-2L-FASTON](design/D8-2L-FASTON/README.md); its blades point toward the top edge in the top view. TE recommends 1.57 mm PCB thickness, while the candidate remains 1.2 mm pending confirmation.

**D8 is not ready for manufacturing.** Current KiCad 10.0.6 DRC reports 0 violations and 0 unconnected items; 14 schematic-parity warnings remain. Reconcile the mechanical-hole schematic records and complete thermal and enclosure review before release. See the saved [D8 DRC report](design/D8-2L/MAIN_POWER/verification/D8_DRC_DIRECT_SOLDER.json), [board preview](design/D8-2L/MAIN_POWER/review/MAIN_POWER_D8.svg), and [visual STEP assembly](design/D8-2L/MAIN_POWER/MAIN_POWER_D8.step). The STEP contains the board plus 10 component model proxies; it omits the input wires and is not exact vendor CAD.

| Board | Function | PCB size / thickness | Planned assembly |
|---|---|---|---|
| MAIN_POWER | Fused 12 V distribution | 68 Ãƒâ€” 100.264 mm / 1.2 mm | User fits all 11 through-hole parts |
| POE_POWER | 12 V to nominal 53.5 V, 1.31 A switch supply | 106 Ãƒâ€” 100 mm / 1.2 mm | JLC SMT, user fits 3 through-hole parts |
| USB_POWER | Two charge-only USB-A ports, 3 A electrical design target each | 80 Ãƒâ€” 50 mm / 1.6 mm | JLC SMT, user fits 3 through-hole parts |

All boards use four copper layers, 2 oz outer / 1 oz inner. Planned batch: **10 of each board**. Enclosure ambient limit: **40 Ã‚Â°C**.

## Mechanical update required

On 2026-09-28, the project owner confirmed that the D6 board outlines were out of date. D8-2L now applies the supplied replacement outline to MAIN only. D6 manufacturing files and STEP models remain historical and on hold; POE and USB replacement mechanics are still not supplied. Do not treat D8 as released for manufacture.

## Latest MAIN option: D7-2L

[Two-layer MAIN prototype](design/D7-2L/README.md) preserves the user layout and uses 2 oz copper on each side at 1.2 mm thickness. Native ERC/DRC/parity checks pass. The four-layer D6L1 option remains preserved. Full shared-path voltage-drop/thermal qualification and mechanical confirmation remain pending. PoE and USB are unchanged. [Download D7-2L](packages/UMI_MAIN_POWER_D7_2L_PROTOTYPE.zip).

## Preserved four-layer MAIN layout: D6L1

The user rearranged MAIN components on 2026-09-29. [D6L1](design/D6L1/README.md) restores the branch connections and fills while preserving those placements and graphics. Native DRC/parity: zero violations and zero unconnected items. [Open the current MAIN project](design/D6L1/MAIN_POWER/MAIN_POWER.kicad_pro). Older MAIN Gerbers and STEP files are now stale for this layout. Manufacturing remains on hold.

## MAIN schematic redraw: D6S1

The MAIN schematic was redrawn on 2026-09-29 with explicit branch wiring. [Open the D6S1 project](design/D6S1/MAIN_POWER/MAIN_POWER.kicad_pro), [view the schematic PDF](design/D6S1/MAIN_POWER/review/MAIN_POWER_schematic.pdf), or read the [revision notes](design/D6S1/README.md). The physical MAIN PCB is unchanged from D6; PoE and USB remain D6. The outline hold still applies. For another computer or agent, read [START_HERE.md](START_HERE.md).

## Start here

- [D6 design and manufacturing overview](design/D6/README.md)
- KiCad 10 projects: [MAIN](design/D6/MAIN_POWER/MAIN_POWER.kicad_pro), [POE](design/D6/POE_POWER/POE_POWER.kicad_pro), [USB](design/D6/USB_POWER/USB_POWER.kicad_pro). Each project includes its PCB, schematic and local libraries.
- [Complete D6 prototype package](packages/UMI_THREE_BOARD_DESIGN_D6_PROTOTYPE.zip)
- [Combined component sourcing spreadsheet](design/D6/UMI_COMPONENT_SOURCING.xlsx) and [CSV](design/D6/UMI_COMPONENT_SOURCING.csv): one list for SMT, manual parts and harness parts.
- [Layout review](design/D6/LAYOUT_REVIEW.html): download/clone and open locally to view linked fabrication and assembly drawings.
- [Simplified STEP models](mechanical/D6/README.md) and [STEP ZIP](packages/UMI_D6_STEP.zip).
- [Engineering calculations and bring-up procedure](design/D6/ENGINEERING_AND_TEST_NOTES.md), [fabrication requirements](design/D6/FABRICATION_NOTES.md), [manual assembly](design/D6/MANUAL_ASSEMBLY.md).
- [Open items and project decisions](docs/PROJECT_HANDOFF.md).

## Configuration

The PoE switch and SENSING GMSL board are **alternative configurations; never connect both loads** under this power budget. No hardware interlock enforces this. The larger configuration is approximately 174 W / 14.5 A at 12 V under the documented assumptions; retain the 20 A input-path design/test margin.

MAIN J1 is the 12 V input. MAIN J2/J3/J4/J5/J6 feed Jetson/GMSL/fan/USB/POE respectively. All two-pin 12 V headers use pin 1 positive, pin 2 ground. POE J6 supplies 53.5 V: pin 1 positive, pin 2 unused, pin 3 ground. Consult the project pin schedules before making cables.

## Verification and limitations

The supplied D6 records report zero KiCad DRC/ERC violations, zero unconnected items and zero schematic-parity issues. Gerber/drill/placement checks and source hashes are included in each board's verification folder. These are file checks, not hardware measurements. [TEST_RECORD.csv](design/D6/TEST_RECORD.csv) records physical tests as unperformed.

Supplier acceptance of copper thickness, selective filled/capped vias and the PoE inductor fixture is pending. Stock observations are historical snapshots, not reservations. The output fuse is obsolete and its observed stock only supports a batch sourcing plan. No order or payment has been placed.

STEP files preserve board outlines and holes and add simplified component proxies. Component heights are estimates: do not use them for final enclosure-clearance signoff. Missing KiCad 3D bodies do not remove a component from the assembly BOM; check the SMT BOM/CPL and separately fitted parts.

## Repository contents

`design/D6/` is the editable current design and manufacturing package. `mechanical/D6/` contains six STEP models and their verification/assumptions. `packages/` contains the original current delivery ZIPs. `archive/` contains superseded snapshots, including the original revC input. `docs/historical-reviews/` preserves prior engineering reviews; they can contain findings later resolved by D6. `tools/legacy/` contains development scripts, with execution caveats in its README.

Transferred on 2026-09-28. See [transfer record](docs/TRANSFER_RECORD.md) and [SHA256 manifest](TRANSFER_SHA256SUMS.txt). No license has been selected; this import does not assign new licensing terms to project files or third-party library assets.
