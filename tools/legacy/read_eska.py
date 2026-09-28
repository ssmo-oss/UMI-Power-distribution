import urllib.request
from pypdf import PdfReader
u='https://www.eska-fuses.de/fileadmin/produkte/datenblaetter/ESKA_KFZ_Sicherungen.pdf'
b=urllib.request.urlopen(u,timeout=20).read();open('work/datasheets/eska_auto.pdf','wb').write(b)
r=PdfReader('work/datasheets/eska_auto.pdf')
for i,p in enumerate(r.pages):
 s=p.extract_text() or ''
 if '80 V' in s or '80V' in s or '340.' in s:print('PAGE',i+1,s.encode('ascii','replace').decode()[:9500])
open('work/datasheets/eska_auto.txt','w',encoding='utf8').write('\n'.join(p.extract_text() or '' for p in r.pages))
