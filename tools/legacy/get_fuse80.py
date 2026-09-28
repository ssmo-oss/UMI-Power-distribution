from pathlib import Path
import urllib.request
from pypdf import PdfReader
u='https://www.mouser.com/datasheet/2/240/littelfuse_fks_ato_80v_blade_fuses-523215.pdf'
p=Path('work/datasheets/fuse_80v.pdf')
p.write_bytes(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read())
p.with_suffix('.txt').write_text('\n'.join(x.extract_text() for x in PdfReader(p).pages),encoding='utf-8')
