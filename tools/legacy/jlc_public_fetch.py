import urllib.request,json,re,sys
from pathlib import Path
def fetch(url):
 s=urllib.request.urlopen(url,timeout=25).read().decode();parts=re.findall(r'self\.__next_f\.push\((\[.*?\])\)</script>',s)
 t=''.join(a[1] for x in parts if len(a:=json.loads(x))>1 and isinstance(a[1],str))
 return s,t
def objects(t):
 out=[];dec=json.JSONDecoder()
 for m in re.finditer(r'\{',t):
  try:
   obj,_=dec.raw_decode(t[m.start():])
   if isinstance(obj,dict) and ('componentCode' in obj or 'componentLibraryType' in obj):out.append(obj)
  except (ValueError,RecursionError):pass
 return out
if __name__=='__main__':
 sys.stdout.reconfigure(encoding='utf-8');url=sys.argv[1];s,t=fetch(url);key=re.sub('[^a-zA-Z0-9]','_',url)[-90:];d=Path('work/jlc_evidence');d.mkdir(exist_ok=True);(d/(key+'.html')).write_text(s,encoding='utf-8');obs=objects(t);(d/(key+'.json')).write_text(json.dumps(obs,indent=2),encoding='utf-8');print(json.dumps(obs,ensure_ascii=False))
