import urllib.request,pypdf
urls=['https://www.lcsc.com/datasheet/lcsc_datasheet_2208261700_VO-SCR2010J7R5_C5140273.pdf','https://datasheet.lcsc.com/lcsc/2208261700_VO-SCR2010J7R5_C5140273.pdf']
for i,u in enumerate(urls):
 try:
  dat=urllib.request.urlopen(u,timeout=15).read();p=f'work/datasheets/VO_alt{i}.pdf';open(p,'wb').write(dat);t='\n'.join(x.extract_text() for x in pypdf.PdfReader(p).pages);open(p+'.txt','w',encoding='utf-8').write(t);print(u,t[:16000])
 except Exception as e:print(type(e).__name__,str(e))
