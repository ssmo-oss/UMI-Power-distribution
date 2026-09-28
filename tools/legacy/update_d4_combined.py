import json,csv
from pathlib import Path
p=Path('work');data=json.loads((p/'jlc_combined_parts.json').read_text());mods=json.loads((p/'d4_substitutions.json').read_text());manual=json.loads((p/'d4_manual_substitutions.json').read_text());out=[]
for row in data['parts']:
 r=dict(row);applicable=[m for m in mods if m['board']==r['board'] and m['old_mpn']==r['mpn']]
 applicable += [m for m in manual if m['old_mpn']==r['mpn']]
 if applicable:
  m=applicable[0];r.update(mpn=m['mpn'],manufacturer=m['manufacturer'],jlc_code=m['jlc_code'],current_stock=m['current_stock'],source_url='https://jlcpcb.com/partdetail/'+m['jlc_code'],status='In stock',proposed_alternative='Applied D4: '+m['note'])
  if 'value' in m:r['value']=m['value']
  r['checked_utc']=m.get('checked_utc','2026-09-26')
 r['required_10_pairs']=r['qty_per_pair']*10
 if r['current_stock'] is not None:
  if r['current_stock']<r['required_10_pairs']:r['status']='Insufficient stock for 10 pairs'
  elif r['current_stock']==r['required_10_pairs']:r['status']='Stock exactly equals requirement; no spares'
 if r['mpn']=='1709681':r['status']='JLC preorder; stock 0; lead time unconfirmed';r['proposed_alternative']='Retained exact part. Preorder minimum2, USD4.9074 each. Need10; lead time not shown.'
 if r['mpn']=='ERJ-12ZYJ7R5U':r['status']='JLC preorder; stock 0; lead time unconfirmed';r['jlc_code']='C2086794';r['source_url']='https://jlcpcb.com/partdetail/C2086794';r['proposed_alternative']='Retained exact part. Preorder minimum734, USD0.0118 each, estimated lot USD8.66. Need10; lead time not shown.'
 if r['assembly']!='SMT':r['proposed_alternative']+=' Manual fit retained. JLC purchased components are PCBA inventory and cannot ship loose; arrange JLC assembly or separate external/LCSC loose-part procurement.'
 out.append(r)
data={'revision':'D4','order_pairs':10,'parts':out};(p/'jlc_combined_parts_d4.json').write_text(json.dumps(data,indent=2))
with Path('C:/Users/Sandi/Documents/KiCad/UMI_COMPONENT_SOURCING.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(len(out))
