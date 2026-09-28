import urllib.request,concurrent.futures,re
from pathlib import Path
ids=['C77241','C2155766','C19276042','C3278732'];Path('work/jlc_live').mkdir(exist_ok=True)
def f(c):
 try:
  b=urllib.request.urlopen('https://jlcpcb.com/partdetail/'+c,timeout=20).read().decode();Path('work/jlc_live/'+c+'.html').write_text(b,encoding='utf8');return c,len(b),re.findall('.{0,50}(?:stock|Stock|Extended|Basic).{0,70}',b)[:10]
 except Exception as e:return c,str(e)
print(list(concurrent.futures.ThreadPoolExecutor().map(f,ids)))
