import sys
sys.path.insert(0,'work');from design_d2 import *
b=parse(Path('outputs/UMI_TWO_BOARD_DESIGN/USB_POWER/USB_POWER.kicad_pcb').read_text())
for f in all_(b,'footprint'):
 r=prop(f,'Reference');print(r[2],one(f,'at'),one(r,'at'),one(r,'layer'),'hide' in r)
