from jlc_public_fetch import fetch,objects
import json
from pathlib import Path
for code in ['C17565246','C5140273']:
 try:
  s,t=fetch('https://jlcpcb.com/partdetail/'+code); a=[o for o in objects(t) if 'overseasStockCount' in o];Path('work/jlc_evidence/'+code+'_candidate.json').write_text(json.dumps(a,indent=2));print(code,json.dumps(a[:1]))
 except Exception as e:print(code,str(e))
