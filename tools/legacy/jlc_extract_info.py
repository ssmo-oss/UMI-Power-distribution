import json,re
from pathlib import Path
out=[]
for p in Path('work/jlc_live').glob('*.decoded'):
 s=p.read_text(encoding='utf8');m=re.search(r'"componentInfo":(\{"componentCode":)',s)
 if m:
  d=json.JSONDecoder().raw_decode(s[m.start(1):])[0];out.append(d);print(p.name,json.dumps(d,ensure_ascii=True)[:6000])
Path('work/jlc_live/critical_info.json').write_text(json.dumps(out,indent=2))
