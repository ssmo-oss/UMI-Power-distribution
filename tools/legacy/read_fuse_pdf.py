import urllib.request
from pypdf import PdfReader
u='https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_16670004402_apr22_xonlink.pdf'
b=urllib.request.urlopen(u,timeout=15).read();open('work/datasheets/fks80_verified.pdf','wb').write(b)
s='\n'.join(p.extract_text() or '' for p in PdfReader('work/datasheets/fks80_verified.pdf').pages);open('work/datasheets/fks80_verified.txt','w',encoding='utf8').write(s);print(s.encode('ascii','replace').decode()[:9500])
