from pathlib import Path
import csv,json
base=Path.cwd();root=base/'outputs/UMI_TWO_BOARD_DESIGN'
text='''# Fabrication and assembly specification — prototype

Use the per-board Gerber and drill files as one matched set. Do not combine layers or position files from different revisions. The four copper layers are F.Cu, In1.Cu, In2.Cu and B.Cu in that order.

| Setting | USB_POWER | MAIN_POWER |
|---|---|---|
| Layer count | 4 | 4 |
| Finished thickness | 1.6 mm | 1.2 mm |
| Outer copper | 2 oz / nominal 70 µm | 2 oz / nominal 70 µm |
| Inner copper | 1 oz / nominal 35 µm | 1 oz / nominal 35 µm |
| Finish | ENIG | ENIG |
| Mask / legend | Green / white | Green / white |
| Via-in-pad process | Resin filled and copper capped | Resin filled and copper capped |
| SMT placement | Top side only | Top side only |
| Manual parts | Input and USB sockets | Connectors and fuse holders; fuse inserts fitted separately |

FR-4 construction, nominal Tg at least 150 °C. No controlled-impedance routing is specified. The dielectric splits in the KiCad stackup are nominal; the fabricator may propose its standard construction with the specified total thickness and copper weights. Do not silently change to 0.5 oz inner copper. Final material, tolerances and assembly process must be accepted in the manufacturing quote.

Main board thickness is deliberately below the fuse holder's 1.5 mm PCB limit. A 1.6 mm main board is not an approved substitution. USB and main boards therefore need separate fabrication settings/panels.

**Filled and capped vias are essential beneath exposed solder pads.** Ordinary tenting, solder-mask plugging, or leaving these holes open is not equivalent. The drill files include the vias; the fabricator must apply the specified process. The Gerber preview displays drill positions even where the finished process will cap them. Choose a via-in-pad / POFV process in the quote and ensure the assembler agrees with it.

Gerbers, Excellon drills and component positions share the board's drill/place origin. USB origin is its bottom-left outline corner. Gerber outline strokes are 0.05 mm wide: the USB centreline outline is exactly 80 × 50 mm even though the Gerber-job graphical bounding box is 80.05 × 50.05 mm. Cut along the outline centreline.

The manufacturing folder contains the four copper layers, two solder masks, two legends, outline, plated and non-plated drills, and the Gerber job description. The assembly folder separately contains top paste and the SMT position files. Do not interpret absence of paste in the bare-board Gerber ZIP as absence of stencil data.

## Assembly handoff

- BOM_by_reference.csv is the complete installed electrical-parts list; mounting holes are excluded from purchasing.
- BOM_grouped.csv groups equal ordering parts and local footprints.
- BOM_JLC_DRAFT.csv has known catalog matches and exact manufacturer MPNs. Blank catalog codes require sourcing; they are not approved substitutions. The USB power module has an LCSC catalog match but its JLC assembly sourcing route is not confirmed.
- The native KiCad positions and the JLC-formatted CPL contain only SMT parts. Through-hole connectors and fuse holders are intentionally omitted for hand fitting.
- Verify the assembler's placement preview against the pin-1 marks and the assembly drawing. KiCad rotation zero is not a universal guarantee of every assembler's component-library orientation.
- Confirm stencil treatment of thermal pads and the heavy Coilcraft inductor's support fixture with the assembler. All specified SMT parts are intended for assembly service, including the power modules/inductors.
- No substitute with the same generic name but a different manufacturer is approved for AO4407A or USBLC6-2SC6.

The exported files have been checked against KiCad and independently parsed where the verification report states a pass. This does not replace a manufacturer's DFM review. These are first-prototype files, not evidence of physical qualification or certification. Follow ENGINEERING_AND_TEST_NOTES.md before connecting the actual devices.

Fabricator capability source checked 2026-09-26: [JLCPCB capabilities](https://jlcpcb.com/capabilities/Capab). Relevant published limits include multilayer 2 oz track/space 0.15/0.15 mm, ordinary via-hole range and annular guidance, minimum 1 mm legend text, and filled/plated-over via-in-pad processing. This document is a requested build specification; no manufacturing quote or order has been submitted.
'''
(root/'MANUFACTURING_SPECIFICATION.md').write_text(text,encoding='utf-8')
for name in ['USB_POWER','MAIN_POWER']:
 d=root/name;native=d/'assembly'/(name+'_positions.csv')
 if not native.exists():continue
 with native.open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 with (d/'assembly'/(name+'_CPL_JLC.csv')).open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  w.writerows([r['Ref'],r['PosX'],r['PosY'],'Top' if r['Side']=='top' else 'Bottom',r['Rot']] for r in rows)
print('Manufacturing specification and available CPL files written')
