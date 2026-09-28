import urllib.request,logging
logging.getLogger('pypdf').setLevel(logging.ERROR)
from pypdf import PdfReader
u='https://xonstorage.blob.core.windows.net/pdf/everohms_ma251230fr006mz_Lcs01_link.pdf';b=urllib.request.urlopen(u,timeout=20).read();open('work/datasheets/everohms_ma.pdf','wb').write(b);r=PdfReader('work/datasheets/everohms_ma.pdf');open('work/datasheets/everohms_ma.txt','w',encoding='utf8').write('\n'.join(p.extract_text() or '' for p in r.pages));print(len(r.pages))

