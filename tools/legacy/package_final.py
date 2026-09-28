from pathlib import Path
import json,shutil,zipfile,hashlib
root=Path('outputs/UMI_TWO_BOARD_DESIGN')
(root/'README.md').write_text('''# UMI two-board design — D2 prototype package

Completed 2026-09-26. Open MAIN_POWER/MAIN_POWER.kicad_pro and USB_POWER/USB_POWER.kicad_pro. These are two different boards. Old D1 and UMI_USB_D2 projects are superseded.

## Delivered

- MAIN_POWER: 158 x 100.263962 mm; 4 layers, 1.2 mm; 65 electrical components (53 SMT, 12 hand fitted).
- USB_POWER: 80 x 50 mm; 4 layers, 1.6 mm; 34 electrical components (31 SMT, 3 hand fitted).
- Editable KiCad projects and local libraries, schematics, filled routed boards, Gerbers, plated/non-plated drills, paste, BOMs, corrected placement files, review images/PDFs and verification reports.
- Both final saved boards pass KiCad 10.0.6 DRC and schematic parity with zero reported violations/unconnected items. Both schematics pass ERC with zero reported violations, using the included project settings. Reports list disabled check categories; this is not a claim that every optional KiCad check was enabled.
- Independent exported-file checks match all 133 main-board and 137 USB-board holes and all 53/31 SMT placement centres to their boards.

## Ordering status

Bare-board manufacturing files are prepared for a first prototype. Read MANUFACTURING_SPECIFICATION.md before obtaining a quote: both boards require 2 oz outer/1 oz inner copper and filled/capped vias, and their thicknesses differ.

Assembly BOM and corrected CPL files are prepared for quoting. The assembly order still requires the supplier to resolve blank catalog codes against exact MPNs and approve its placement preview and process. No stock has been reserved, quote approved or order placed. Use *_CPL_JLC.csv; native *_positions.csv retain local footprint rotations and are reference exports only.

This is not a physically qualified production design. No boards have been fabricated or electrically load-tested. Follow ENGINEERING_AND_TEST_NOTES.md for current-limited bring-up, short/load-step and 40 C enclosure testing before connecting valuable equipment. Confirm the switch accepts the actual output range and test the intended headset charging behaviour; USB-A charging identification is not USB PD.

## Files to send

1. Each board's *_GERBERS.zip for bare-board quote, together with MANUFACTURING_SPECIFICATION.md.
2. BOM_JLC_DRAFT.csv and assembly/*_CPL_JLC.csv for SMT quote, plus top paste and orientation notes. Blank part codes are deliberate sourcing items.
3. Keep the board-mounted through-hole BOM and MANUAL_FUSES_AND_HARNESS_BOM.csv for hand assembly.

Review images show exported copper/pads, not proof of assembled clearance. Some optional 3D bodies are absent; use the footprint/mechanical dimensions. The dense F.Fab plot is a reference only. Manual connector/fuse locations are in MANUAL_PLACEMENT_MAP.pdf.
''',encoding='utf-8')
for name,report in [('MAIN_POWER','main_final_export_review.md'),('USB_POWER','usb_final_export_review.md')]:
 shutil.copy2(Path('work')/report,root/name/'verification'/report)
p=root/'ENGINEERING_AND_TEST_NOTES.md';s=p.read_text();s+='\n## Final mechanical and wiring details\n\nMain outline is 158 x 100.263962 mm; USB is 80 x 50 mm. The main retains the original four hole locations. Main J1 is 12 V input; J2 Jetson; J3 SG4A; J4 fan; J5 USB feed; J6 switch. Main J6 pin 1 is +53.5 V, pin 2 unused, pin 3 return. Verify mating orientation from the numbered PCB pads before terminating harnesses. Both boards require filled/capped vias beneath solder pads.\n\nThe simultaneous input budget is approximately 18.4 A; use a 20 A continuous design/test basis for the supply path, not an 18 A rating. Main distribution uses parallel 6 mm outer-layer 2 oz conductors and ground planes. This geometry is not a measured enclosure thermal qualification. Check connector, fuse-holder, copper and converter temperatures under sustained full load at 40 C ambient.\n';p.write_text(s,encoding='utf-8')
Path('outputs/ORDER_RELEASE_STATUS.md').write_text('Current deliverable: UMI_TWO_BOARD_DESIGN/README.md. Both final layouts and exports complete for prototype quoting. SMT sourcing/placement-preview approval and hardware qualification remain as documented. Older D1/D2 development files are superseded.\n')
print('Release documentation written')
