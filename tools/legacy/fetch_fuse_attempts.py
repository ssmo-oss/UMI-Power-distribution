import urllib.request,re,html
urls=['https://www.google.com/search?q=%22166.7000.4302%22+pdf&gbv=1','https://www.tme.eu/Document/','https://www.farnell.com/datasheets/2001097.pdf','https://www.mouser.com/datasheet/2/240/Littelfuse_Blade_Fuses_FKS_80V_Datasheet-1316236.pdf','https://www.littelfuse.com/~/media/automotive/datasheets/fuses/blade-fuses/littelfuse_blade_fuses_ato_32v_datasheet.pdf']
for i,u in enumerate(urls):
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=10).read();open('work/datasheets/fuse_attempt'+str(i),'wb').write(b);print(i,len(b),b[:15])
 except Exception as e:print(i,e)
