from pathlib import Path
import urllib.request,concurrent.futures
urls={
'gate_zener':'https://www.diodes.com/assets/Datasheets/ds18004.pdf',
'fuse_holder':'https://www.littelfuse.com/~/media/commercial-vehicle/datasheets/automotive-fuse-holders/ato/littelfuse-fuse-holder-ato-flr-pcb-datasheet.pdf',
'fuse_80v':'https://www.littelfuse.com/~/media/automotive/datasheets/fuses/passenger-car-and-commercial-vehicle/blade-fuses/littelfuse_ato_80v_datasheet.pdf',
}
def get(k,u):
 try:
  data=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read()
  Path('work/datasheets/'+k+'.pdf').write_bytes(data)
  print(k,len(data),data[:15])
 except Exception as e: print(k,str(e))
with concurrent.futures.ThreadPoolExecutor() as e:list(e.map(lambda kv:get(*kv),urls.items()))
