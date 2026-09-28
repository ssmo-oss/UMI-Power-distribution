import csv,json,concurrent.futures
from datetime import datetime,timezone
from pathlib import Path
from jlc_public_fetch import fetch,objects
codes={'GRM188R71E104KA01D':'C77050','GRM31CR71A226KE15L':'C91604','BZT52C12-7-F':'C124196','AO4407A':'C16072','RT0603BRD0724K9L':'C136967','RT0603BRD0732K4L':'C861323','RC0603FR-07100KL':'C14675','RC0603FR-0715K8L':'C155689','TPSM63610RDFR':'C7125816','TPS2557DRBR':'C130056','TPS2513ADBVR':'C473910','USBLC6-2SC6':'C7519'}
def audit(item):
 mpn,code=item;url='https://jlcpcb.com/partdetail/'+code
 try:
  html,rsc=fetch(url);d=Path('work/jlc_evidence');d.mkdir(exist_ok=True);(d/(code+'.html')).write_text(html,encoding='utf-8');obs=objects(rsc);(d/(code+'.json')).write_text(json.dumps(obs,indent=2),encoding='utf-8');rows=[r for r in obs if r.get('componentCode')==code and r.get('componentModelEn')==mpn];merged={}
  for r in rows:merged.update(r)
  return {'mpn':mpn,'jlc_code':code,'url':url,'checked_utc':datetime.now(timezone.utc).isoformat(),'exact_match':bool(rows),**{k:merged.get(k) for k in ('componentBrandEn','componentSpecificationEn','componentLibraryType','overseasStockCount','canPresaleNumber','isBuyComponent','allowPostFlag','noBuyReason','initialPrice','preMinPurchaseNum')}}
 except Exception as e:return {'mpn':mpn,'jlc_code':code,'url':url,'error':str(e)}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:result=list(ex.map(audit,codes.items()))
 Path('work/jlc_usb_known.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
