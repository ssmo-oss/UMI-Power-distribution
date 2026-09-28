# UMI Power Distribution

Three separate boards distribute a 12 V supply to the UMI system. **D6 is the current prototype revision. It has not been physically qualified or approved for production.**

| Board | Function | PCB size / thickness | Planned assembly |
|---|---|---|---|
| MAIN_POWER | Fused 12 V distribution | 68 × 100.264 mm / 1.2 mm | User fits all 11 through-hole parts |
| POE_POWER | 12 V to nominal 53.5 V, 1.31 A switch supply | 106 × 100 mm / 1.2 mm | JLC SMT, user fits 3 through-hole parts |
| USB_POWER | Two charge-only USB-A ports, 3 A electrical design target each | 80 × 50 mm / 1.6 mm | JLC SMT, user fits 3 through-hole parts |

All boards use four copper layers, 2 oz outer / 1 oz inner. Planned batch: **10 of each board**. Enclosure ambient limit: **40 °C**.

## Mechanical update required

On 2026-09-28, the project owner confirmed that the current board outlines are out of date. **D6 manufacturing files and STEP models are on hold pending corrected outlines and mounting geometry.** The size table above describes the existing D6 files, not the approved final mechanics. The replacement mechanical source has not yet been identified. Apply the correct boundaries, mounting holes and connector constraints, then update placement/routing as necessary, rerun checks and regenerate manufacturing/STEP outputs before supplier submission.

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
