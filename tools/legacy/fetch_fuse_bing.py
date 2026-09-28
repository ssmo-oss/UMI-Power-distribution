import urllib.request,re,html
for i,q in enumerate(['%22166.7000.4302%22+pdf','littelfuse+ATO+287+pdf']):
 try:
  b=urllib.request.urlopen('https://www.bing.com/search?q='+q,timeout=15).read().decode();open('work/datasheets/bingfuse'+str(i)+'.html','w',encoding='utf8').write(b);print('\n'.join(html.unescape(u) for u in re.findall(r'https?[^\s<>\x22]+',b) if 'pdf' in u.lower()))
 except Exception as e: print(e)
