"""Read-only PCB audit plus D5 BOM/CPL metadata generation. Does not launch KiCad."""
from pathlib import Path
import csv,json,hashlib
from design_d2 import parse,all_,one,prop
root=Path('outputs/UMI_D5');oldroot=Path('outputs/UMI_D4')
oldfix=json.loads(Path('work/cpl_rotation_corrections_d4.json').read_text())
catalog=json.loads(Path('work/jlc_combined_parts_d4.json').read_text())['parts']
def props(n):return {str(p[1]):str(p[2]) for p in all_(n,'property')}
def pads(f):return sorted(json.dumps([str(p[1]),p[2],p[3],one(p,'at'),one(p,'size'),one(p,'drill'),one(p,'layers')]) for p in all_(f,'pad'))
reports={};fixes={}
for name in ['MAIN_POWER','POE_POWER','USB_POWER']:
 d=root/name;design=json.loads((d/'design.json').read_text());pcb=parse((d/(name+'.kicad_pcb')).read_text());sch=parse((d/(name+'.kicad_sch')).read_text())
 fps={props(f).get('Reference'):f for f in all_(pcb,'footprint')};symbols={props(s).get('Reference'):props(s) for s in all_(sch,'symbol')}
 predecessor='USB_POWER' if name=='USB_POWER' else 'MAIN_POWER';oldfps={props(f).get('Reference'):f for f in all_(parse((oldroot/predecessor/(predecessor+'.kicad_pcb')).read_text()),'footprint')}
 proofs={x['reference']:x for x in oldfix[predecessor]};issues=[];rows=[];fixes[name]=[]
 for p in design:
  ref=p['ref'];f=fps[ref];attr=one(f,'attr') or []
  if not p.get('mpn') or p['mpn'].startswith('MECHANICAL') or 'exclude_from_bom' in attr:continue
  for origin,value in [('PCB',props(f).get('MPN')),('schematic',symbols.get(ref,{}).get('MPN'))]:
   if value!=p['mpn']:issues.append([ref,origin,value,p['mpn']])
  hit=next((c for c in catalog if c['mpn']==p['mpn']),{})
  assembly='SMT' if 'smd' in attr else 'MANUAL_THT'
  rows.append({'Reference':ref,'Value':p['value'],'Quantity per board':1,'Manufacturer':p.get('manufacturer',hit.get('manufacturer','')),'Manufacturer part number':p['mpn'],'Footprint':p['fp'],'Assembly':assembly,'LCSC/JLC code':p.get('jlc_code',hit.get('jlc_code','')),'Sourcing note':'D5; dated stock observation, confirm procurement and assembly'})
  if assembly=='SMT' and p.get('rotation',0):
   proof=proofs.get(ref)
   if not proof or ref not in oldfps or pads(f)!=pads(oldfps[ref]) or one(f,'at')[3:]!=one(oldfps[ref],'at')[3:] or p.get('source_fp')!=proof['source_footprint']:issues.append([ref,'Cannot reuse independently proved D4 normalized orientation'])
   else:fixes[name].append(proof)
 groups={}
 for row in rows:
  key=tuple(row[k] for k in ['Manufacturer part number','Footprint','Assembly','Value'])
  if key not in groups:groups[key]=dict(row)
  else:groups[key]['Reference']+=','+row['Reference'];groups[key]['Quantity per board']+=1
 for filename,records in [('BOM_by_reference.csv',rows),('BOM_grouped.csv',list(groups.values()))]:
  with (d/filename).open('w',newline='',encoding='utf-8-sig') as out:w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(records)
 byref={p['ref']:p for p in design}
 with (d/'BOM_JLC_DRAFT.csv').open('w',newline='',encoding='utf-8-sig') as out:
  w=csv.writer(out);w.writerow(['Comment','Designator','Footprint','LCSC Part #','Manufacturer','MPN'])
  for row in groups.values():
   if row['Assembly']=='SMT':w.writerow([row['Value'],row['Reference'],byref[row['Reference'].split(',')[0]]['source_fp'],row['LCSC/JLC code'],row['Manufacturer'],row['Manufacturer part number']])
 reports[name]={'issues':issues,'parts':len(rows),'smt_count':sum(r['Assembly']=='SMT' for r in rows),'pcb_sha256':hashlib.sha256((d/(name+'.kicad_pcb')).read_bytes()).hexdigest(),'orientation_method':'D4 proven canonical pad rotation plus unchanged D5 numbered-pad geometry, baked angle and source identity'}
 (d/'BOM_audit.json').write_text(json.dumps(reports[name],indent=2))
Path('work/d5_metadata_audit.json').write_text(json.dumps(reports,indent=2))
assert not any(r['issues'] for r in reports.values()),reports
Path('work/cpl_rotation_corrections_d5.json').write_text(json.dumps(fixes,indent=2))
print(json.dumps(reports,indent=2))
