import urllib.request
u='https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2304140030_Ever-Ohms-Tech-MA251230FR004MZ_C252682.pdf'
try:
 b=urllib.request.urlopen(u,timeout=20).read();open('work/datasheets/everohms_ma.pdf','wb').write(b);print(len(b),b[:5])
except Exception as e: print(e)
