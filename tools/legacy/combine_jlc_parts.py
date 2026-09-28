import json,csv
from pathlib import Path
p=Path('work'); base=Path('outputs/UMI_D3')
usb={x['mpn']:x for x in json.loads((p/'jlc_usb.json').read_text())['parts']}
pas={x['mpn']:x for x in json.loads((p/'jlc_main_passives.json').read_text())['parts']}
crit=json.loads((p/'jlc_main_critical.json').read_text())
manual={'178.6165.0001':('C207060',1),'1709681':('C5872886',0),'614004190021':('C6402847',426),'B2P-VH(LF)(SN)':('C160315',318370),'B3P-VH(LF)(SN)':('C160316',160039),'VHR-3N':('C157899',47874),'SVH-41T-P1.1':('C160350',111659)}
parts=[]
def alttext(a):
 m=a.get('live_jlc_metadata',a);stock=a.get('reported_jlc_stock',m.get('overseasStockCount'))
 return f"{a.get('mpn',m.get('componentModelEn',''))} {a.get('jlc_code',m.get('componentCode',''))}; stock {stock if stock is not None else 'unverified'}; {a.get('assessment',a.get('status',''))}; {a.get('url','')}"
for board in ['MAIN_POWER','USB_POWER']:
 grouped={}
 for b in csv.DictReader((base/board/'BOM_grouped.csv').open(encoding='utf-8-sig')):
  mpn=b['Manufacturer part number'];key=(mpn,b['Assembly'])
  if key not in grouped:grouped[key]=dict(board=board,refs=[],qty_per_pair=0,mpn=mpn,manufacturer=b['Manufacturer'],value=b['Value'],assembly=b['Assembly'],jlc_code='',current_stock=None,status='Exact JLC availability unverified',checked_utc='2026-09-26',source_url='',proposed_alternative='')
  r=grouped[key];r['refs'].append(b['Reference']);r['qty_per_pair']+=int(b['Quantity per board'])
 for r in grouped.values():
  r['refs']=','.join(r['refs']);m=r['mpn'];x=usb.get(m) if board=='USB_POWER' else pas.get(m)
  if x:
   stock=x.get('displayed_stock',x.get('reported_jlc_stock'));r.update(jlc_code=x.get('jlc_code',''),current_stock=stock,source_url=x.get('url',''),checked_utc=x.get('checked_utc','2026-09-26'))
   r['status']='In stock (Extended)' if stock and stock>0 else 'Out of stock' if stock==0 else 'Exact JLC availability unverified'
   r['proposed_alternative']=' | '.join(alttext(a) for a in x.get('proposed_alternates',[]))
   if x.get('match_note'):r['proposed_alternative']=x['match_note']+' '+x.get('manufacturer_source','')
  if board=='MAIN_POWER':
   exact=[c for c in crit if c['componentModelEn']==m]
   if exact:
    c=exact[0];r.update(jlc_code=c['componentCode'],current_stock=c['overseasStockCount'],source_url=c['url'],status='In stock (Extended)')
   alts=[c for c in crit if c['reference']==r['refs'] and c['componentModelEn']!=m]
   if alts:r['proposed_alternative']=' | '.join(alttext(c) for c in alts)
  if m in manual:r.update(jlc_code=manual[m][0],current_stock=manual[m][1],source_url='https://jlcpcb.com/partdetail/'+manual[m][0],status='In stock; user-fit through-hole' if manual[m][1] else 'Out of stock; user-fit through-hole')
  if m=='GRM1885C1H101JA01D':r.update(jlc_code='C71664',current_stock=171060,status='In stock (Extended)',source_url='https://jlcpcb.com/partdetail/C71664')
  if r['current_stock'] is not None and 0<r['current_stock']<r['qty_per_pair']:r['status']='Insufficient stock for one pair'
  elif r['current_stock'] is not None and 0<r['current_stock']<100:r['status']+='; low stock'
  if m=='ERJ-M1WSF4M0U':r['status']='Discontinued (EOL); exact JLC availability unverified';r['proposed_alternative']='Original part is discontinued (EOL). '+r['proposed_alternative']
  parts.append(r)
for b in csv.DictReader((base/'MANUAL_FUSES_AND_HARNESS_BOM.csv').open(encoding='utf-8-sig')):
 m=b['MPN'];code,stock=manual.get(m,('',None));r=dict(board='MAIN_POWER' if 'insert' in b['Use'] else 'HARNESS',refs=b['Use'],qty_per_pair=int(b['Quantity per system']),mpn=m,manufacturer=b['Manufacturer'],value=b['Description'],assembly='MANUAL_INSERT' if 'insert' in b['Use'] else 'MANUAL_HARNESS',jlc_code=code,current_stock=stock,status='In stock; manual fit' if stock else 'Exact JLC availability unverified',checked_utc='2026-09-26',source_url='https://jlcpcb.com/partdetail/'+code if code else b['Manufacturer source'],proposed_alternative='')
 if m=='VHR-2N':r['proposed_alternative']='VHR-2N-BK, C595405; stock 30543; black housing candidate, not applied. https://jlcpcb.com/partdetail/C595405'
 if r['assembly']=='MANUAL_INSERT':r['status']='Not found in live JLC catalogue search';r['source_url']='https://jlcpcb.com/parts/componentSearch?isSearch=true&searchTxt='+m
 parts.append(r)
(p/'jlc_combined_parts.json').write_text(json.dumps({'parts':parts},indent=2),encoding='utf-8')
out=Path('C:/Users/Sandi/Documents/KiCad/UMI_COMPONENT_SOURCING.csv');out.parent.mkdir(exist_ok=True)
with out.open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(parts[0]));w.writeheader();w.writerows(parts)
print(len(parts),sum(x['qty_per_pair'] for x in parts))
