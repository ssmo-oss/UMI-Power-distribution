from pathlib import Path
import json
from design_d2 import parse,all_,one,prop,Q,write
d=Path('outputs/UMI_D6/POE_POWER')
old='ERJ-12ZYJ7R5U';new='RC2010JK-077R5L'
parts=json.loads((d/'design.json').read_text())
p=next(p for p in parts if p['ref']=='R1');assert p['mpn']==old
p.update(mpn=new,manufacturer='Yageo',jlc_code='C4169838')
(d/'design.json').write_text(json.dumps(parts,indent=2))
for suffix,key in [('.kicad_pcb','footprint'),('.kicad_sch','symbol')]:
 path=d/('POE_POWER'+suffix);tree=parse(path.read_text())
 node=next(x for x in all_(tree,key) if prop(x,'Reference') and prop(x,'Reference')[2]=='R1')
 assert prop(node,'MPN')[2]==old;prop(node,'MPN')[2]=Q(new)
 for field,value in [('Manufacturer','Yageo'),('JLC','C4169838'),('LCSC','C4169838'),('JLCPCB Part #','C4169838')]:
  if prop(node,field):prop(node,field)[2]=Q(value)
 write(path,tree)
print('D6 POE R1 updated; electrical value, footprint and copper unchanged')
