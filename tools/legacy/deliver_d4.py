from pathlib import Path
import csv,json,shutil,hashlib,zipfile
import sys
assert '--authorize-delivery' in sys.argv,'Explicit --authorize-delivery required after D4 review'
root=Path('outputs/UMI_D4');fixes=json.loads(Path('work/cpl_rotation_corrections_d4.json').read_text())
for name in ['MAIN_POWER','USB_POWER']:
 d=root/name
 for check in ['DRC','ERC']:
  r=json.loads((d/'verification'/('export_'+check+'.json')).read_text());assert r['exit_code']==0,(name,check)
 for fn,digest in json.loads((d/'verification/export_source_hashes.json').read_text()).items():assert hashlib.sha256(Path(fn).read_bytes()).hexdigest()==digest,'Stale export '+fn
for name,items in fixes.items():
 d=root/name;fix={x['reference']:x for x in items}
 with (d/'assembly'/(name+'_positions.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
 with (d/'assembly'/(name+'_CPL_JLC.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation']);w.writerows([r['Ref'],r['PosX'],r['PosY'],'Top',(float(r['Rot'])+fix.get(r['Ref'],{}).get('normalized_CCW_rotation_deg',0))%360] for r in rows)
 (d/'verification'/'rotation_corrections.json').write_text(json.dumps(items,indent=2))
 with zipfile.ZipFile(d/(name+'_GERBERS.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((d/'manufacturing').iterdir()):
   if p.suffix.lower()!='.pdf':z.write(p,p.name)
# No obsolete development exports or locks belong in the package.
files=[p for p in root.rglob('*') if p.is_file() and p.name not in ('SHA256SUMS.txt','GEOMETRY_EDITED') and not p.name.endswith(('.lck','.kicad_prl'))]
(root/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in sorted(files))+'\n')
dest=Path(r'C:\Users\Sandi\Documents\KiCad\UMI_TWO_BOARD_DESIGN_D4');dest.mkdir(exist_ok=True)
for p in files+[root/'SHA256SUMS.txt']:
 target=dest/p.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256(target.read_bytes()).digest()
archive=dest.parent/'UMI_TWO_BOARD_DESIGN_D4_PROTOTYPE.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[root/'SHA256SUMS.txt']:z.write(p,Path(dest.name)/p.relative_to(root))
(dest.parent/'UMI_LATEST.txt').write_text('Latest revision: UMI_TWO_BOARD_DESIGN_D4. Open its README.md and LAYOUT_REVIEW.html. Earlier UMI_TWO_BOARD_DESIGN is preserved D2.\n')
print(json.dumps({'destination':str(dest),'verified_files':len(files)+1,'archive':str(archive)}))

