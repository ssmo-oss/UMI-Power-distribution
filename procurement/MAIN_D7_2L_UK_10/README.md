# MAIN D7-2L purchasing and fabrication package

Prepared 29 September 2026 for **10 MAIN boards only**, retaining the latest layout and 3 mm FAN branch tracks. The PCB and schematic were not modified for this task.

## What to use

- `MAIN_D7_2L_UK_PARTS_10.xlsx`: one combined purchasing list with exact part numbers, quantities, spares, observed GBP prices, stock and source links.
- `DIGIKEY_BASKET_IMPORT.csv`: nine order lines for DigiKey UK. Map the three columns to Part Number, Quantity and Customer Reference in the basket file importer.
- `DIGIKEY_BULK_ADD.txt`: same nine lines without headers for the basket's Bulk Add text box.
- `JLCPCB_MAIN_D7_2L_GERBERS.zip`: fabrication upload containing seven Gerbers, two drill files and the Gerber job file. Use the separate order settings text file.
- `MAIN_BOARD_BOM_MANUAL_ASSEMBLY.csv` and `MAIN_WIRING_PIN_SCHEDULE.csv`: reference assembly and wiring information. These are not a JLCPCB SMT assembly submission.

## Purchase quantities and cost

The list supplies all 11 soldered components per board, five removable fuse inserts and five MAIN-end two-pin mating housings with ten contacts per board. Quantities include a 20% spares allowance, rounded to supplier order multiples. Contacts are **200 individual contacts (two strips of 100)**, not 200 packs. Required without spares: 10 input blocks, 50 holders, 50 PCB headers, 20 x 7.5 A fuses, 10 each of 1 A / 5 A / 10 A fuses, 50 housings and 100 contacts.

Observed parts estimate: **GBP 259.48 excluding VAT, delivery and PCB fabrication**. Prices come from displayed DigiKey UK tiers; web search pages may be cached. Holder and 100-contact-strip availability were also checked in the browser. Stock is not reserved and all prices need refresh at checkout. Changing spreadsheet quantities recalculates quantities and totals using the recorded unit prices; it does not retrieve new tier prices. CSV/TXT are the fixed ten-board snapshot and do not auto-update with spreadsheet edits.

The online basket could not be completed: DigiKey's Bulk Add returned an `Error / POST` dialog, and an individual product Add to Basket retry did not show a successful addition. The import files are provided instead. No checkout, payment, account creation or order submission occurred.

## Assembly and harness details

- J1 Phoenix 1709681 is a fixed screw-clamp PCB terminal block. The PSU wires enter it directly; it does not take a mating plug.
- J2–J6 use JST B2P-VH(LF)(SN), cataloged by DigiKey as B2P-VH. Their matching cable housings are natural-colour VHR-2N with SVH-41T-P1.1 female contacts. Natural housing colour replaces the earlier black VHR-2N-BK selection; the mating family and circuit are unchanged.
- Contacts accept 16–20 AWG wire; use the specified contact/wire tooling and validate finished crimps. Do not crimp a thinner fan pigtail into an oversized contact. Adapt the harness with appropriate terminals/splices once actual wire gauges are known.
- Pin 1 on each output is its fused +12 V; pin 2 is ground. Verify physical pin numbering before terminating each cable.
- Fuse mapping: F1 Jetson 7.5 A; F2 GMSL 7.5 A; F3 fan 1 A; F4 USB-board feed 5 A; F5 PoE-board 12 V feed 10 A. These are the existing design values, not newly proven load ratings. All inserts in this MAIN list are 32 VDC-rated ATO fuses. Do not use them on the 53.5 V PoE output.
- PoE and GMSL are alternative system configurations, never simultaneous loads. Both physical branches are populated in this purchasing list.
- Wire lengths, device-end plugs, PSU-end terminations, enclosure mounting hardware and crimp tooling are not included because their installation details are unspecified. The mating connector list covers the MAIN end only.

JST family reference: https://www.jst-mfg.com/product/pdf/eng/eVH.pdf

## Fabrication status

Order settings: 10 bare FR-4 boards, two copper layers, 2 oz each side, 1.2 mm finished thickness, ENIG, green solder mask, white legend. No stencil or assembly service is needed for this all-through-hole MAIN design. Exact nominal outline is 68 x 100.263962 mm.

The saved native DRC report has zero violations, zero unconnected items and zero schematic-parity findings under the project's configured checks; saved ERC has zero violations. The package audit verifies the PCB/schematic hashes against the saved two-layer audit and verifies each ZIP member against the export directory. No claim of live JLCPCB DFM approval is made.

**Existing release limits remain:** final mechanical outline/holes are unconfirmed and full-board thermal/voltage-drop testing at 40 C enclosure ambient is outstanding. This package is suitable for a fabrication quote and prototype review; it is not a production-qualified release. Do not treat clean DRC as an ampacity or mechanical-fit certificate.
