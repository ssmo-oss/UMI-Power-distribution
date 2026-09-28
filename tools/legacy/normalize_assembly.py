from pathlib import Path
import csv,json,shutil
root=Path('outputs/UMI_TWO_BOARD_DESIGN'); corrections=json.loads(Path('work/cpl_rotation_corrections.json').read_text())
for name,items in corrections.items():
 d=root/name;fix={x['reference']:x for x in items}
 with (d/'assembly'/(name+'_positions.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 with (d/'assembly'/(name+'_CPL_JLC.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation']);w.writerows([r['Ref'],r['PosX'],r['PosY'],'Top',(float(r['Rot'])+fix.get(r['Ref'],{}).get('normalized_CCW_rotation_deg',0))%360] for r in rows)
 with (d/'BOM_JLC_DRAFT.csv').open(encoding='utf-8-sig',newline='') as f:reader=csv.DictReader(f);fields=reader.fieldnames;bom=list(reader)
 for row in bom:
  refs=row['Designator'].split(',');sources={fix[r]['source_footprint'] for r in refs if r in fix}
  if sources:
   assert len(sources)==1;row['Footprint']=sources.pop()
 with (d/'BOM_JLC_DRAFT.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(bom)
 (d/'verification'/'rotation_corrections.json').write_text(json.dumps(items,indent=2))
shutil.copy2('outputs/UMI_D2/ENGINEERING_AND_TEST_NOTES.md',root/'ENGINEERING_AND_TEST_NOTES.md')
p=root/'MANUFACTURING_SPECIFICATION.md';s=p.read_text();s+='\n## Placement rotation normalization\n\nUse *_CPL_JLC.csv with BOM_JLC_DRAFT.csv for the assembly quote. These files normalize rotated local footprint geometry to the unrotated source package, using independently checked pad coordinates. The raw *_positions.csv files retain KiCad local-footprint rotations and must not be substituted blindly. Main U1/Q1/Q2/Q3 normalize to 90 degrees, C19/C20 to 270 degrees. The complete per-reference table is in verification/rotation_corrections.json. Supplier package zero-angle conventions still require placement-preview review.\n';p.write_text(s,encoding='utf-8')
