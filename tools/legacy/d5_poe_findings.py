from design_d2 import *
from collections import Counter
p=Path('outputs/UMI_D5/POE_POWER/POE_POWER.kicad_pcb');b=parse(p.read_text());ids=[]
def walk(n):
 if isinstance(n,list):
  if n and n[0]=='uuid':ids.append(str(n[1]))
  for a in n:walk(a)
walk(b);print('duplicate UUIDs',[(x,c) for x,c in Counter(ids).items() if c>1])
d=json.loads(Path('work/d5_POE_POWER_first.json').read_text());print(json.dumps(d['violations'],indent=2))
