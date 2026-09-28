import urllib.request,pypdf
u='https://www.yageogroup.com/component-documentation/download/specsheet/RT0603BRD07953RL'
try:
 data=urllib.request.urlopen(u).read();open('work/datasheets/RT0603BRD07953RL.pdf','wb').write(data);print('\n'.join(x.extract_text() for x in pypdf.PdfReader('work/datasheets/RT0603BRD07953RL.pdf').pages))
except Exception as e:print(e)

