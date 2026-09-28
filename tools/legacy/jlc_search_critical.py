import urllib.request,re,json,concurrent.futures
from pathlib import Path
parts=['XAL4020-102MEB','ERJ-M1WSF4M0U','MBR1H100SFT3G','SMBJ15A','BSC070N08NS5ATMA1']
def f(m):
 try:
  b=urllib.request.urlopen('https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt='+m,timeout=20).read().decode();Path('work/jlc_live/search_'+m+'.html').write_text(b,encoding='utf8');return m,len(b),list(set(re.findall(r'C\d{4,10}',b)))[:30]
 except Exception as e:return m,str(e)
print(list(concurrent.futures.ThreadPoolExecutor().map(f,parts)))
