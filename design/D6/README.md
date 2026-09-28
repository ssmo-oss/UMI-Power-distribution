# UMI D6 — sourcing and manufacturing corrections

D6 retains the three-board architecture and resolves the known part-sourcing and file-format issues that can be handled before fabrication. **Ready for prototype manufacturing review, not physically qualified for production.**

## Completed

- Replaced the preorder snubber resistor with stocked **Yageo RC2010JK-077R5L / C4169838**. Resistance, tolerance, power rating and footprint are unchanged. Its pulse/thermal behaviour still requires the same prototype measurement as the original part.
- Found exact loose-part sources for all thirteen manual component types. The Phoenix input connector no longer needs JLC preorder. The 80 V fuse has enough observed distributor stock for twenty pieces, including ten spares. It is obsolete; this is a batch solution, not guaranteed long-term availability.
- Defined the supply route: JLC assembles SMT; the user fits separately purchased connectors, holders, inserts and harness components. All remain on **one combined spreadsheet** with purchase links and quantities. Repeated manual MPNs are bought once; later duplicate rows show zero purchase quantity.
- Corrected MAIN/POE inner-layer stackup identities, widened five POE traces from 0.15 to 0.16 mm, enlarged MAIN's small visible labels, and encoded selective via filling/capping in the PCB sources and coordinate schedules.
- Refilled and re-exported all boards. Final KiCad DRC/ERC reports pass with zero reported violations, zero unconnected items and zero schematic-parity issues. Independent Gerber/drill/placement audits and source-hash checks are included.

## Files and order scope

Open **LAYOUT_REVIEW.html** for actual fabrication previews and schematic/assembly drawings. Order ten of each:

| Board | Outline | Thickness | Copper | Assembly |
|---|---|---|---|---|
| MAIN_POWER | 68 × 100.264 mm | 1.2 mm | 4 layers, 2 oz outer / 1 oz inner | Bare board, 11 manual parts |
| POE_POWER | 106 × 100 mm | 1.2 mm | Same | 53 SMT + 3 manual parts |
| USB_POWER | 80 × 50 mm | 1.6 mm | Same | 31 SMT + 3 manual parts |

Use the per-board Gerber ZIP, SMT BOM and normalized CPL. MAIN has no SMT operation. Read FABRICATION_NOTES.md: POE/USB need selective epoxy-filled, copper-capped vias; POE's 0.635 mm vias remain ordinary. Include the POE inductor assembly fixture. The source copper stackup is explicit; do not accept a silent change to 0.5 oz inner copper.

## Electrical configuration

MAIN J1 takes 12 V. J2 supplies Jetson, J3 GMSL, J4 fan, J5 USB J1 and J6 POE J1. All 12 V two-pin headers use pin 1 positive, pin 2 ground. POE J6 is the 53.5 V output: pin 1 positive, pin 2 empty, pin 3 ground.

Use **PoE or GMSL, never both**. There is no electronic interlock. The larger configuration is approximately **174 W / 14.5 A at 12 V**, using the documented allowances and assumed converter efficiency; retain 20 A input-path design/test margin. MAIN retains F1 Jetson 7.5 A, F2 GMSL 7.5 A, F3 fan 1 A, F4 USB 5 A and F5 PoE feed 10 A. POE retains F6 3 A / 80 V. F5 protects the interboard cable at its source. Jetson's 7.5 A is provisional protection, not expected draw; verify startup, temperature and wire protection before changing it.

## Remaining external steps

1. **Manufacturer acceptance and purchasing:** the exact copper/thickness/selective-fill combination and inductor fixture need an accepted quote. QUOTE_REQUEST.md is prepared but unsent. Approve supplier placement/polarity previews and final attrition quantities. C1 requires fourteen pieces including the reported four-piece attrition, against fifteen observed; L1 requires ten against seventeen observed. Inventory is not reserved. Other SMT allowances in the spreadsheet are conservative planning quantities where exact order-page arithmetic was unavailable.
2. **Physical prototype tests:** no assembled hardware was available to test. Thermal rise at 40 °C, stability, snubber pulses, eFuse fault transients, USB load steps and real-device compatibility cannot be established from DRC. TEST_RECORD.csv gives the pending measurements; ENGINEERING_AND_TEST_NOTES.md gives the procedure. All physical results are explicitly unperformed.
3. **Installation details:** final cable lengths, device-end plugs, weakest wire/pigtail ratings, input cable protection and the exact USB-powered device model remain to be confirmed before system integration. The interim interboard harness basis is AWG16, at most 1 m one-way; this is a documented assumption, not a measured installation.

No supplier message, order, reservation, payment or external design upload has been made. D5 is preserved. SHA256SUMS.txt identifies this package.
