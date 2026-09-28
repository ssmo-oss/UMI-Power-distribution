from jlc_public_fetch import fetch,objects
import json
s,t=fetch('https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt=1709681')
obs=objects(t);print(json.dumps(obs)[:4000]);print('len',len(s),len(t))
from pathlib import Path
Path('work/jlc_evidence/manual_search.html').write_text(s,encoding='utf-8')
