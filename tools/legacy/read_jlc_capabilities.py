import urllib.request,re,html
from pathlib import Path
u='https://jlcpcb.com/capabilities/Capab'
d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read().decode()
s=html.unescape(re.sub('<[^>]+>',' ',re.sub(r'<(script|style).*?</\1>','',d,flags=re.S)))
s=re.sub(r'\s+',' ',s);Path('work/jlc_capabilities.txt').write_text(s,encoding='utf-8')
for m in re.finditer(r'2\s*oz|0\.2mm|0\.20',s,re.I):print(s[max(0,m.start()-200):m.start()+450])
