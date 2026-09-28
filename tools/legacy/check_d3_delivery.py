from pathlib import Path
import json,shutil
from design_d2 import parse,all_,one,prop
root=Path('outputs/UMI_D3')
for name in ['MAIN_POWER','USB_POWER']:
 d=root/name;b=parse((d/(name+'.kicad_pcb')).read_text());coords={str(prop(f,'Reference')[2]):list(map(float,one(f,'at')[1:3])) for f in all_(b,'footprint')};parts=json.loads((d/'design.json').read_text())
 for p in parts:p['pos']=coords[p['ref']]
 (d/'design.json').write_text(json.dumps(parts,indent=2))
 for report in ['DRC.json','ERC.json']:
  r=json.loads((d/'verification'/report).read_text());assert not r.get('violations',[]);assert not r.get('unconnected_items',[]);assert not r.get('schematic_parity',[])
shutil.copy2('work/d3_assembly_visual_review.md',root/'ASSEMBLY_VISUAL_REVIEW.md')
