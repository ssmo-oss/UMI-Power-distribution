import re,json
from pathlib import Path
for c in ['C206912','C206921']:
 s=Path('work/jlc_live/'+c+'.html').read_text(encoding='utf8');t='\n'.join(str(json.loads(x)[1]) for x in re.findall(r'self\.__next_f\.push\((.*?)\)</script>',s));print('\n'.join(re.findall(r'.{0,50}015400[158].{0,400}',t)[:8]))
