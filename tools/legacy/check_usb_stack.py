import sys,json
sys.path.insert(0,'work')
from design_d2 import *
p=Path('outputs/UMI_D2/USB_POWER/USB_POWER.kicad_pcb');b=parse(p.read_text())
print(dump(one(b,'general')))
print(dump(one(b,'setup'))[:7000])
print(dump(one(b,'layers')))
