import sys,math,json
from pathlib import Path
sys.path.insert(0,'work');from design_d2 import *
def stats(p):
 b=parse(Path(p).read_text());o={n:{'length_mm':0,'segments':0} for n in ['DP1','DM1','DP2','DM2']}
 for s in all_(b,'segment'):
  net=one(s,'net')[1]
  if net in o and one(s,'layer')[1]!='F.Cu':
   o[net]['segments']+=1;o[net]['length_mm']+=math.dist(list(map(float,one(s,'start')[1:3])),list(map(float,one(s,'end')[1:3])))
 return o
r={'before':stats('work/usb_d3_before_signal.kicad_pcb'),'after':stats('outputs/UMI_D3/USB_POWER/USB_POWER.kicad_pcb')};Path('work/usb_d3_signal_improvement.json').write_text(json.dumps(r,indent=2));print(r)
