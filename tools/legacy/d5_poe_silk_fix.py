from design_d2 import *
from collections import Counter
p=Path('outputs/UMI_D5/POE_POWER/POE_POWER.kicad_pcb');b=parse(p.read_text())
changed=[]
for n in list(all_(b,'gr_text')):
 s=str(n[1]);at=one(n,'at');x,y=map(float,at[1:3]);new=None
 if (s,x,y) in [('+',72.,33.),('GND',77.,33.)]:b.remove(n);changed.append(['remove',s,x,y]);continue
 if s=='Q1':new=(131,37)
 elif s in ('C19','C20'):new=(x,55)
 elif s in ('+53.5V','GND') and y==97:new=(x,95)
 if new:at[1:3]=list(map(str,new));changed.append([s,[x,y],new])
ids=[]
def walk(n):
 if isinstance(n,list):
  if n and n[0]=='uuid':ids.append(str(n[1]))
  for a in n:walk(a)
walk(b);dupes={x:c for x,c in Counter(ids).items() if c>1};assert not dupes,dupes
write(p,b)
report=dict(uuid_count=len(ids),duplicate_uuids=dupes,silkscreen_changes=changed,copper_changed=False)
Path('outputs/UMI_D5/POE_POWER/UUID_AND_SILK_CHECK.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
