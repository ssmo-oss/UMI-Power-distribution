from pathlib import Path
import json,csv,html,shutil,zipfile,hashlib
root=Path('outputs/UMI_TWO_BOARD_DESIGN')
for name,w,h in [('MAIN_POWER',158,100.263962),('USB_POWER',80,50)]:
 d=root/name;parts=json.loads((d/'design.json').read_text());manual=[x for x in parts if x['ref'].startswith(('J','F'))];scale=5
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{int(h*scale+220)}" viewBox="0 0 1000 {int(h*scale+220)}"><rect width="100%" height="100%" fill="white"/><text x="30" y="30" font-family="sans-serif" font-size="22">{name} — manual placement map, top view</text>',f'<rect x="30" y="55" width="{w*scale}" height="{h*scale}" fill="#e8f2e8" stroke="#333"/>']
 for p in manual:
  x=30+(p['pos'][0]-10)*scale;y=55+(p['pos'][1]-10)*scale
  svg.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#222"/><text x="{x+7}" y="{y-6}" font-family="sans-serif" font-size="14">{p["ref"]}</text>')
 for i,p in enumerate(manual):
  x=30+(i%2)*480;y=80+h*scale+(i//2)*20
  svg.append(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="12">{html.escape(p["ref"]+": "+p["value"])}</text>')
 svg.append('</svg>');(d/'review'/'MANUAL_PLACEMENT_MAP.svg').write_text(''.join(svg),encoding='utf-8')
p=root/'README.md';p.write_text(p.read_text().replace('MANUAL_PLACEMENT_MAP.pdf','each board’s review/MANUAL_PLACEMENT_MAP.svg'),encoding='utf-8')
shutil.copy2('work/main_final_validation_review.md',root/'MAIN_POWER/verification/main_final_validation_review.md')
for name in ['MAIN_POWER','USB_POWER']:
 d=root/name
 with zipfile.ZipFile(d/(name+'_GERBERS.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted((d/'manufacturing').iterdir()):
   if p.suffix.lower()!='.pdf':z.write(p,p.name)
files=[p for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt']
(root/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in sorted(files))+'\n')
dest=Path(r'C:\Users\Sandi\Documents\KiCad\UMI_TWO_BOARD_DESIGN');shutil.copytree(root,dest,dirs_exist_ok=True)
for p in root.rglob('*'):
 if p.is_file():assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((dest/p.relative_to(root)).read_bytes()).digest()
archive=dest.parent/'UMI_TWO_BOARD_DESIGN_D2_PROTOTYPE.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.rglob('*')):
  if p.is_file():z.write(p,Path(root.name)/p.relative_to(root))
print(json.dumps({'destination':str(dest),'files_verified':len(files)+1,'archive':str(archive)}))
