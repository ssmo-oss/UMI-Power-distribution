from pathlib import Path
import json,re,html,concurrent.futures,datetime
from jlc_public_fetch import fetch,objects
root=Path('work/d6_stock');root.mkdir(exist_ok=True)
rows=json.loads(Path('work/jlc_combined_parts_d5.json').read_text())['parts']
codes=sorted({p['jlc_code'] for p in rows})
def run(code):
 try:
  s,t=fetch('https://jlcpcb.com/partdetail/'+code)
  obs=objects(t)
  visible=html.unescape(re.sub('<[^>]+>',' ',re.sub('<script.*?</script>','',s,flags=re.S)))
  visible=re.sub(r'\s+',' ',visible)
  (root/(code+'.txt')).write_text(visible,encoding='utf-8')
  (root/(code+'.json')).write_text(json.dumps(obs,indent=2),encoding='utf-8')
  m=re.search(r'In Stock\s*[:：]?\s*([\d,]+)',visible,re.I)
  focus=next((o for o in obs if o.get('componentCode')==code and 'lossNumber' in o),{})
  result={'code':code,'stock':int(m[1].replace(',','')) if m else None,'lossNumber':focus.get('lossNumber'),'leastPatchNumber':focus.get('leastPatchNumber'),'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excerpt':visible[max(0,visible.find('Manufacturer')):][:2500]}
  return result
 except Exception as e:return {'code':code,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(run,codes))
(root/'summary.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{k:v for k,v in r.items() if k!='excerpt'} for r in results]))
