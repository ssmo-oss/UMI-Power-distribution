"""Copy immutable validation inputs, recording hashes and checking source stability."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('source');ap.add_argument('destination')
a=ap.parse_args();src=Path(a.source).resolve();dst=Path(a.destination).resolve()
if dst.exists():raise SystemExit('Choose a new destination for each validation snapshot')
files=[p for p in src.rglob('*') if p.is_file() and (p.suffix in ('.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_mod','.kicad_sym','.kicad_dru') or p.name in ('fp-lib-table','sym-lib-table'))]
hashes={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
manifest={'utc':datetime.now(timezone.utc).isoformat(),'source':str(src),'destination':str(dst),'files':[]}
for p in files:
    target=dst/p.relative_to(src);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
    h=hashlib.sha256(target.read_bytes()).hexdigest()
    if h!=hashes[p] or hashlib.sha256(p.read_bytes()).hexdigest()!=h:raise SystemExit(f'Source changed during snapshot: {p}')
    manifest['files'].append({'relative_path':str(p.relative_to(src)),'sha256':h,'source_mtime_ns':p.stat().st_mtime_ns})
(dst/'snapshot_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'utc':manifest['utc'],'destination':str(dst),'files':len(files)},indent=2))
