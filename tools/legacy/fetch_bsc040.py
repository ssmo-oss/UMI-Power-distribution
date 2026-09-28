import urllib.request
from pypdf import PdfReader
u='https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc040n08ns5-datasheet-en.pdf'
b=urllib.request.urlopen(u,timeout=20).read();open('work/datasheets/bsc040.pdf','wb').write(b);s='\n'.join(p.extract_text() or '' for p in PdfReader('work/datasheets/bsc040.pdf').pages);open('work/datasheets/bsc040.txt','w',encoding='utf8').write(s)
print(s[:2000].encode('ascii','replace').decode())
