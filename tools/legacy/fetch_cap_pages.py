import urllib.request,concurrent.futures
urls={'murata':'https://www.murata.com/en-global/products/productdetail?partno=GRM32ER71A476ME15%23','tdk':'https://product.tdk.com/en/search/capacitor/ceramic/mlcc/info?part_no=CNA6P1X7R1H106K'}
def f(k,u):
 try:
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=15).read().decode('utf8','replace');open('work/datasheets/'+k+'_cap_live.html','w',encoding='utf8').write(r);return k,len(r)
 except Exception as e:return k,str(e)
print(list(concurrent.futures.ThreadPoolExecutor().map(lambda kv:f(*kv),urls.items())))
