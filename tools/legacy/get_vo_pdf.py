import urllib.request,pypdf
u='https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2208261700_VO-SCR2010J7R5_C5140273.pdf'
p='work/datasheets/VO_SCR2010.pdf';urllib.request.urlretrieve(u,p);t='\n'.join(x.extract_text() for x in pypdf.PdfReader(p).pages);open('work/datasheets/VO_SCR2010.txt','w',encoding='utf-8').write(t);print(t[:18000])
