import csv,json,re,urllib.request,concurrent.futures,datetime
from pathlib import Path
known={
'GRM32ER71K475KE14L':'C711060','GRM188R71E104KA01D':'C77050','GRM1885C1H101JA01D':'C71664','GCM188R71C105KA64D':'C161212','GRM188R71E473KA01D':'C97893','GRM1885C1H152JA01D':'C162204','GRM188R71H153KA01D':'C86021','GRM21BR71H105KA12L':'C77083','GRM188R71H104KA93D':'C77055','GRM1885C1H682JA01D':'C162241','ESR03EZPJ101':'C253328','RT0603BRD071K96L':'C861213','RT0603BRD07100KL':'C122538','RT0603BRD0713K7L':'C861119','RT0603BRD07182RL':'C705731','CRCW060349K9FKEA':'C844789','CRCW06038K45FKEA':'C2076762','CRCW060340K2FKEA':'C844784','CRCW060330K0JNEA':'C2076641'}
cache=Path('work/jlc_main_passive_pages');cache.mkdir(exist_ok=True)
def fetch(pair):
 mpn,code=pair;url='https://jlcpcb.com/partdetail/'+code
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  raw=urllib.request.urlopen(req,timeout=25).read().decode();(cache/(code+'.html')).write_text(raw,encoding='utf8')
  decoded='\n'.join(str(json.loads(c)[1]) for c in re.findall(r'self\.__next_f\.push\((.*?)\)</script>',raw))
  m=re.search(r'"componentInfo":(\{"componentCode":)',decoded)
  info=json.JSONDecoder().raw_decode(decoded[m.start(1):])[0] if m else {}
  return mpn,dict(jlc_code=code,url=url,live_jlc_metadata=info,exact_match=info.get('componentModelEn')==mpn,status='catalog_match_stock_unconfirmed' if info.get('componentModelEn')==mpn else 'catalog_identity_unconfirmed',checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as e:return mpn,dict(jlc_code=code,url=url,status='retrieval_failed',error=str(e))
found=dict(concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,known.items()))
parts={}
for r in csv.DictReader(open('outputs/UMI_D3/MAIN_POWER/BOM_grouped.csv',encoding='utf-8-sig')):
 if not r['Reference'].startswith(('C','R')) or r['Reference']=='R2':continue
 mpn=r['Manufacturer part number']
 if mpn not in parts:parts[mpn]=dict(mpn=mpn,manufacturer=r['Manufacturer'],value=r['Value'],references=[],footprints=[],quantity=0,**found.get(mpn,dict(status='not_found_in_search',jlc_code=None,url=None)))
 parts[mpn]['references']+=r['Reference'].split(',');parts[mpn]['quantity']+=int(r['Quantity per board']);parts[mpn]['footprints'].append(r['Footprint'])
out=dict(scope='MAIN_POWER capacitors and resistors excluding R2; no design changes made',stock_caveat='Live JLC server componentInfo metadata identifies catalog and overseas/preorder stock. It does not establish local available assembly stock. Browser stock confirmation remains required.',parts=list(parts.values()))
Path('work/jlc_main_passives.json').write_text(json.dumps(out,indent=2),encoding='utf8')
for p in out['parts']:
 info=p.get('live_jlc_metadata',{});print(p['mpn'],p['status'],p.get('jlc_code'),info.get('componentLibraryType'),info.get('overseasStockCount'),info.get('canPresaleNumber'))
