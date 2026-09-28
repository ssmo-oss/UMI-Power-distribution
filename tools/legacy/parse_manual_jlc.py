import re,json
from pathlib import Path
out=[]
for c in ['C207061','C1664994','C3662004','C3662026','C98732','C89120','C206912','C206921','C142679','C142682','C142683','C142688','C877612','C4169838']:
 p=Path('work/jlc_live/'+c+'.html');s=p.read_text(encoding='utf8');t='\n'.join(str(json.loads(x)[1]) for x in re.findall(r'self\.__next_f\.push\((.*?)\)</script>',s));m=re.search(r'"componentInfo":(\{"componentCode":)',t);d=json.JSONDecoder().raw_decode(t[m.start(1):])[0];out.append(d);print({k:d.get(k) for k in ['componentCode','componentModelEn','overseasStockCount','canPresaleNumber','dataManualUrl']})
Path('work/jlc_manual_info.json').write_text(json.dumps(out,indent=2))




