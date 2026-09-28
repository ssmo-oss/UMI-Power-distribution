import urllib.request,re
for u in ['https://www.eska-fuses.de','https://www.eska-fuses.de/en/','https://www.eska-fuses.de/en/products/']:
 try:
  b=urllib.request.urlopen(u,timeout=15).read().decode('utf8','replace');print(u,len(b));print(re.findall(r'href=[\x22\x27]([^\x22\x27]+)',b)[:50]);open('work/datasheets/eska_live.html','w',encoding='utf8').write(b)
 except Exception as e:print(e)
