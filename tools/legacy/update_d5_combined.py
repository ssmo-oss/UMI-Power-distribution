import csv,json
from pathlib import Path
p=Path('work');old=json.loads((p/'jlc_combined_parts_d4.json').read_text())['parts'];parts=[]
for board in ['MAIN_POWER','POE_POWER','USB_POWER']:
 groups={}
 for b in csv.DictReader((Path('outputs/UMI_D5')/board/'BOM_by_reference.csv').open(encoding='utf-8-sig')):
  mpn=b['Manufacturer part number'];key=(mpn,b['Assembly'])
  if key not in groups:
   prior=next(x for x in old if x['mpn']==mpn);r=dict(prior);r.update(board=board,refs=[],qty_per_pair=0,value=b['Value'],assembly=b['Assembly']);groups[key]=r
  groups[key]['refs'].append(b['Reference']);groups[key]['qty_per_pair']+=1
 for r in groups.values():r['refs']=','.join(r['refs']);parts.append(r)
for row in old:
 if row['assembly'] not in ('MANUAL_INSERT','MANUAL_HARNESS'):continue
 r=dict(row)
 if r['mpn']=='VHR-2N-BK':r.update(qty_per_pair=7,refs='MAIN J2,J3,J4,J5,J6; POE J1; USB J1')
 elif r['mpn']=='SVH-41T-P1.1':r.update(qty_per_pair=16,refs='Contacts for eight housings')
 elif r['mpn']=='VHR-3N':r.update(refs='POE J6 output housing')
 if 'F6 insert' in r['refs']:r.update(board='POE_POWER',refs='POE F6 insert')
 if r['assembly']=='MANUAL_INSERT':r['proposed_alternative']+=' Fuse value remains provisional pending protection coordination review.'
 parts.append(r)
for r in parts:r['required_10_pairs']=10*r['qty_per_pair']
assert sum(r['qty_per_pair'] for r in parts)==131
(p/'jlc_combined_parts_d5.json').write_text(json.dumps({'revision':'D5','order_sets':10,'parts':parts},indent=2))
for target in [Path('C:/Users/Sandi/Documents/KiCad/UMI_COMPONENT_SOURCING.csv'),Path('outputs/UMI_D5/UMI_COMPONENT_SOURCING.csv')]:
 with target.open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(parts[0]));w.writeheader();w.writerows(parts)
print(len(parts),sum(r['qty_per_pair'] for r in parts))
