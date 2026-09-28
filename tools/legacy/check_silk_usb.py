from pathlib import Path
import sys
sys.path.insert(0,'work');from design_d2 import *
b=parse(Path('outputs/UMI_D2/USB_POWER/USB_POWER.kicad_pcb').read_text())
for a in all_(b,'gr_text'):
 if one(a,'layer')[1]=='F.SilkS':print(a[1],dump(one(a,'effects')))
for f in all_(b,'footprint'):
 for a in all_(f,'property')+all_(f,'fp_text'):
  if one(a,'layer') and one(a,'layer')[1]=='F.SilkS':
   sz=one(one(one(a,'effects'),'font'),'size')
   if sz and min(map(float,sz[1:]))<1:print(prop(f,'Reference')[2],a[1:3],sz)
