import urllib.request
u='https://www.yageo.com/upload/media/product/productsearch/datasheet/rchip/PYu-RC_Group_51_RoHS_L_12.pdf'
try:
 b=urllib.request.urlopen(u,timeout=15).read();open('work/datasheets/yageo_rc.pdf','wb').write(b);print(len(b),b[:4])
except Exception as e:print(e)
