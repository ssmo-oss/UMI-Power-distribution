import re,html
from pathlib import Path
for p in Path('work/jlc_live').glob('*.html'):
 s=html.unescape(re.sub('<[^>]+>',' ',re.sub('<script.*?</script>','',p.read_text(encoding='utf8'),flags=re.S)));s=re.sub(r'\s+',' ',s);Path(str(p)+'.txt').write_text(s,encoding='utf8');i=s.find('Manufacturer');print(p.name,s[i:i+2200].encode('ascii','replace').decode())

