"""Read-only D4 identity and orientation consistency gate. No KiCad launch."""
import csv,json,hashlib,math
from pathlib import Path
from design_d2 import parse,all_,one,prop
base=Path.cwd();corrections=json.loads((base/'work/cpl_rotation_corrections.json').read_text());report={}
def properties(n):return {str(x[1]):str(x[2]) for x in all_(n,'property')}
def geometry(f):
 return sorted(json.dumps([str(p[1]),p[2],p[3],one(p,'at'),one(p,'size'),one(p,'drill'),one(p,'layers')]) for p in all_(f,'pad'))
for name in ['MAIN_POWER','USB_POWER']:
 d=base/'outputs/UMI_D4'/name;old=base/'outputs/UMI_D3'/name
 pcb=parse((d/(name+'.kicad_pcb')).read_text());sch=parse((d/(name+'.kicad_sch')).read_text())
 fps={properties(f).get('Reference'):f for f in all_(pcb,'footprint')}
 oldfps={properties(f).get('Reference'):f for f in all_(parse((old/(name+'.kicad_pcb')).read_text()),'footprint')}
 symbols={properties(s).get('Reference'):properties(s) for s in all_(sch,'symbol')}
 design={r['ref']:r for r in json.loads((d/'design.json').read_text())}
 bom={}
 for row in csv.DictReader((d/'BOM_grouped.csv').open(encoding='utf-8-sig')):
  for ref in row['Reference'].split(','):
   assert ref not in bom,'Duplicate BOM reference '+ref
   bom[ref]=row['Manufacturer part number']
 issues=[]
 for ref,mpn in bom.items():
  candidates={'BOM':mpn,'design':design.get(ref,{}).get('mpn'),'PCB':properties(fps[ref]).get('MPN'),'schematic':symbols.get(ref,{}).get('MPN')}
  if len(set(candidates.values()))!=1:issues.append({'reference':ref,'identity_mismatch':candidates})
 # Previous pad-normalization proof is reusable only if complete numbered pad
 # geometry, footprint angle and source-footprint identity remain unchanged.
 for item in corrections[name]:
  ref=item['reference'];a=fps[ref];b=oldfps[ref]
  if name=='MAIN_POWER' and ref=='R2':
   canonical=parse((d/'UMI_D2.pretty/EverOhms_MA2512_2to5mOhm.kicad_mod').read_text())
   pads={str(p[1]):p for p in all_(a,'pad')};errors=[]
   for p in all_(canonical,'pad'):
    q=pads[str(p[1])];x,y=map(float,one(p,'at')[1:3]);actual=list(map(float,one(q,'at')[1:3]));size=list(map(float,one(p,'size')[1:3]));actual_size=list(map(float,one(q,'size')[1:3]))
    errors.extend([math.dist([y,-x],actual),math.dist(size[::-1],actual_size)])
   if max(errors)>1e-6 or design[ref].get('source_fp')!='UMI_D2:EverOhms_MA2512_2to5mOhm':issues.append({'reference':ref,'new_shunt_geometry_error':errors})
   item.update(source_footprint='UMI_D2:EverOhms_MA2512_2to5mOhm',baked_angle_clockwise_board_view_deg=270,normalized_CCW_rotation_deg=90,max_pad_position_error_mm=max(errors),proof='D4 manufacturer canonical numbered pad centers and sizes transformed R270')
   continue
  if geometry(a)!=geometry(b) or one(a,'at')[3:]!=one(b,'at')[3:] or design[ref].get('source_fp')!=item['source_footprint']:
   issues.append({'reference':ref,'rotation_proof_requires_rederivation':True})
 report[name]={'issues':issues,'bom_references':len(bom),'source_sha256':hashlib.sha256((d/(name+'.kicad_pcb')).read_bytes()).hexdigest(),'orientation_method':'D3 every-pad normalized orientation proof plus unchanged D4 pad geometry/footprint angle/source identity'}
(base/'work/d4_metadata_audit.json').write_text(json.dumps(report,indent=2))
assert not any(r['issues'] for r in report.values()),report
(base/'work/cpl_rotation_corrections_d4.json').write_text(json.dumps(corrections,indent=2))
print(json.dumps(report,indent=2))
