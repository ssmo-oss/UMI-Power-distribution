import urllib.request
u='https://uploadcdn.oneyac.com/attachments/files/brand_pdf/%E5%A4%A9%E4%BA%8C/3E/19/MA.pdf'
b=urllib.request.urlopen(u,timeout=20).read();open('work/datasheets/everohms_ma.pdf','wb').write(b);print(len(b))
