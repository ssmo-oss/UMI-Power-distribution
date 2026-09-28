from pathlib import Path
import urllib.request,concurrent.futures
urls={
'fuse_80v_mirror':'https://www.mouser.co.uk/datasheet/2/240/littelfuse_fks_ato_80v_blade_fuses-523215.pdf',
'fuse_holder_mobile':'https://m.littelfuse.com/~/media/commercial-vehicle/datasheets/automotive-fuse-holders/ato/littelfuse-fuse-holder-ato-flr-pcb-datasheet.pdf',
'fuse_80v_mobile':'https://m.littelfuse.com/~/media/automotive/datasheets/fuses/passenger-car-and-commercial-vehicle/blade-fuses/littelfuse_fks_ato_80v_blade_fuses.pdf',
}
def get(k,u):
 try:
  d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
  print(k,len(d),d[:15])
  if d.startswith(b'%PDF'):Path('work/datasheets/'+k+'.pdf').write_bytes(d)
 except Exception as e: print(k,e)
with concurrent.futures.ThreadPoolExecutor() as e:list(e.map(lambda kv:get(*kv),urls.items()))
