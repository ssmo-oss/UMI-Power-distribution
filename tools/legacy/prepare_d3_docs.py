from pathlib import Path
import shutil
src=Path('outputs/UMI_TWO_BOARD_DESIGN');dst=Path('outputs/UMI_D3')
for name in ['README.md','MANUFACTURING_SPECIFICATION.md','MANUAL_ASSEMBLY.md','MANUAL_FUSES_AND_HARNESS_BOM.csv','ENGINEERING_AND_TEST_NOTES.md']:
 shutil.copy2(src/name,dst/name)
p=dst/'README.md';s=p.read_text().replace('D2 prototype package','D3 refined prototype package').replace('Old D1 and UMI_USB_D2 projects are superseded.','D1, D2 and UMI_USB_D2 projects are superseded for this revision.').replace('The dense F.Fab plot is a reference only. Manual connector/fuse locations are in each board’s review/MANUAL_PLACEMENT_MAP.svg.','Use the reference-only assembly drawings in each review folder and the BOM for part values.')
s+='''
## D3 layout refinement

Open LAYOUT_REVIEW.html for a before/after comparison rendered from the actual fabrication layers.

The main power bus and long output runs have cleaner 45-degree approaches. Connector functions, fuse values and polarity are marked, and the main board has 3 mm corner radii. Its mounting-hole centres are retained. The USB board has consistent reference placement, matched port legends, five chamfered backside bends and symmetric mounting columns. USB hole centres are x=13.5/86.5 mm, y=14/56 mm in KiCad board coordinates; use the current outline/drills when making the enclosure.

The electrically sensitive converter placement and short switching/ESD paths were retained. Aesthetic refinement is not a claim of perfection or physical qualification. Fresh revision-specific DRC/ERC and export audits are included.
''';p.write_text(s,encoding='utf-8')
print('D3 documentation prepared')
