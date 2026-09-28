import urllib.request,urllib.parse,xml.etree.ElementTree as ET
for q in ['Littelfuse ATO 80V 3A fuse','Littelfuse 178.6165.0001 datasheet']:
 try:
  u='https://www.bing.com/search?format=rss&q='+urllib.parse.quote(q)
  d=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read()
  r=ET.fromstring(d)
  for i in r.findall('.//item')[:6]: print(i.findtext('title'),i.findtext('link'),i.findtext('description'))
 except Exception as e:print(e)
