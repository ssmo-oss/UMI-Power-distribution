import sys,csv,json,math
from pathlib import Path
sys.path.insert(0,'work');from design_d2 import parse
p=Path('outputs/UMI_TWO_BOARD_DESIGN/MAIN_POWER');b=parse((p/'MAIN_POWER.kicad_pcb').read_text())
def get(n,k):return next((e for e in n if isinstance(e,list) and e and e[0]==k),None)
fps={}
for f in b:
 if not isinstance(f,list) or not f or f[0]!='footprint':continue
 ref=next((e[2] for e in f if isinstance(e,list) and e[:2]==['property','Reference']),None);fps[ref]=f
bom=list(csv.DictReader((p/'BOM_by_reference.csv').open(encoding='utf-8-sig')));cpl=list(csv.DictReader((p/'assembly/MAIN_POWER_positions.csv').open(encoding='utf-8-sig')));draft=list(csv.DictReader((p/'BOM_JLC_DRAFT.csv').open(encoding='utf-8-sig')));origin=list(map(float,get(get(b,'setup'),'aux_axis_origin')[1:3]))
smts={r['Reference'] for r in bom if r['Assembly']=='SMT'};manual={r['Reference'] for r in bom if r['Assembly']!='SMT'};cplrefs={r['Ref'] for r in cpl};draftrefs={x.strip() for r in draft for x in r['Designator'].split(',')};errors=[]
for r in cpl:
 at=get(fps[r['Ref']],'at');x,y=map(float,at[1:3]);rot=float(at[3]) if len(at)>3 else 0
 if abs(float(r['PosX'])-(x-origin[0]))>1e-5 or abs(float(r['PosY'])-(origin[1]-y))>1e-5 or abs(float(r['Rot'])-rot)>1e-5:errors.append(r['Ref'])
print('coverage',len(bom),len(cpl),smts-cplrefs,cplrefs-smts,smts-draftrefs,draftrefs-smts,'manual',manual,'coordinate errors',errors,'origin',origin)
for ref in ['U1','U2','Q1','Q2','D3','D4','C19','C20']:
 f=fps[ref];print(ref,'at',get(f,'at'))
 for e in f:
  if isinstance(e,list) and e and e[0]=='pad':print(e[1],get(e,'at'),get(e,'net'))


