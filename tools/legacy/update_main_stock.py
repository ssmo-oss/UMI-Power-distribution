import json,datetime
from pathlib import Path
p=Path('work/jlc_main_passives.json');d=json.loads(p.read_text())
updates={'C1':('C97904',0,317),'C15':('C97926',12424,1),'R1':('C2086794',0,734),'R11':('C4212014',0,388),'R17':('C844143',155,1),'R19':('C705797',10,1),'R20':('C861600',7,1),'R25':('C861455',678,1)}
for r in d['parts']:
 for ref,(code,stock,minimum) in updates.items():
  if ref in r['references']:
   r.update(jlc_code=code,url='https://jlcpcb.com/partdetail/'+code,reported_jlc_stock=stock,library_type='Extended',status='in_stock' if stock else 'out_of_stock_preorder',exact_match=True,stock_field='Root live JLC browser displayed stock',minimum_order=minimum,checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
   if ref=='R1':r['rating_correction']='Original Panasonic is 750 mW, not 500 mW.'
   if ref in ('R19','R20'):r['quantity_caution']='Low stock: quantity and assembler attrition must fit available stock.'
p.write_text(json.dumps(d,indent=2),encoding='utf-8')
with Path('work/jlc_main_passives.md').open('a',encoding='utf-8') as f:
 f.write('\n## Additional exact parts confirmed in live JLC browser\n\n|Ref|Code|Stock|Minimum|\n|---|---|---:|---:|\n')
 for ref,(code,stock,minimum) in updates.items():f.write(f'|{ref}|[{code}](https://jlcpcb.com/partdetail/{code})|{stock}|{minimum}|\n')
 f.write('\nAll Extended. R1 original rating is 750 mW. R19/R20 stocks are low; do not equate listed stock with sufficient assembly quantity.\n')
