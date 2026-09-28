from pathlib import Path
import json,math
from design_d2 import parse,all_,one,prop
root=Path('outputs/UMI_D3')
def signatures(path):
 b=parse(path.read_text());fp={str(prop(f,'Reference')[2]):f for f in all_(b,'footprint')};sig={}
 for r,f in fp.items():
  if r.startswith('H'):continue
  sig[r]={'at':one(f,'at'),'pads':[[p[1],one(p,'at'),one(p,'size'),one(p,'net'),one(p,'layers')] for p in all_(f,'pad')]}
 return b,fp,sig
for name in ['MAIN_POWER','USB_POWER']:
 old,of,os=signatures(Path('outputs/UMI_TWO_BOARD_DESIGN')/name/(name+'.kicad_pcb'));new,nf,ns=signatures(root/name/(name+'.kicad_pcb'))
 assert os==ns,(name,'Unexpected component geometry/net/placement change')
 report={'board':name,'electrical_component_placements_pads_and_nets_unchanged':True,'old_segment_count':len(all_(old,'segment')),'new_segment_count':len(all_(new,'segment')),'old_via_count':len(all_(old,'via')),'new_via_count':len(all_(new,'via')),'mounting_holes':{r:{'D2':one(of[r],'at')[1:3],'D3':one(nf[r],'at')[1:3]} for r in nf if r.startswith('H')}}
 d=root/name/'verification';d.mkdir(exist_ok=True);(d/'D2_to_D3_comparison.json').write_text(json.dumps(report,indent=2));print(name,report['old_segment_count'],report['new_segment_count'])
