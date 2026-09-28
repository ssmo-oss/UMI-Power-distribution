import urllib.request,pypdf
u='https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-078K45L'
try:
 data=urllib.request.urlopen(u).read();open('work/datasheets/RC0603FR-078K45L.pdf','wb').write(data);print('\n'.join(x.extract_text() for x in pypdf.PdfReader('work/datasheets/RC0603FR-078K45L.pdf').pages))
except Exception as e:print(e)
