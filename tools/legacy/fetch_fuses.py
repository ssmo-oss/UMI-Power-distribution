import urllib.request,concurrent.futures
urls=['https://www.littelfuse.com/assetdocs/littelfuse-blade-fuses-fks-80v-datasheet?assetguid=8c3779da-b959-4d41-a976-61652acdf364','https://www.google.com/search?q=%22166.7000.4302%22+pdf','https://www.google.com/search?q=Littelfuse+ATO+32V+0287001+datasheet+pdf']
def f(u):
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read();fn='work/datasheets/fuse_search'+str(urls.index(u))+'.html';open(fn,'wb').write(b);return u,len(b)
 except Exception as e:return u,str(e)
print(list(concurrent.futures.ThreadPoolExecutor().map(f,urls)))
