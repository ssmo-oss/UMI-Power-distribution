import urllib.request,re
u='https://www.lcsc.com/product-detail/C207061.html'
try:
 s=urllib.request.urlopen(u,timeout=20).read().decode();open('work/lcsc_holder.html','w',encoding='utf-8').write(s);print(len(s));print('\n'.join(x[:300] for x in re.findall('.{0,40}(?:stockNumber|stockCount|In-Stock|inventory|stock).{0,100}',s)[:20]))
except Exception as e:print(e)
