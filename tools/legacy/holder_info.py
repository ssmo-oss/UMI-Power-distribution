import json,re
from pathlib import Path
s=Path('work/jlc_live/C207061.html.decoded').read_text(encoding="utf8"); m=re.search(r'"componentInfo":(\{"componentCode":)',s);d=json.JSONDecoder().raw_decode(s[m.start(1):])[0];print({k:d.get(k) for k in ['componentModelEn','overseasStockCount','canPresaleNumber','dataManualUrl']})

