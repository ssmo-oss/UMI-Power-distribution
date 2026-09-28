from pathlib import Path
import json,csv,math
parts=json.loads(Path('work/jlc_combined_parts_d5.json').read_text())['parts']
manual={p['mpn']:p for p in json.loads(Path('work/d6_manual_procurement.json').read_text())['parts']}
attr={p['code']:p for p in json.loads(Path('work/d6_stock/summary.json').read_text())}
seen=set()
for r in parts:
 if r['mpn']=='ERJ-12ZYJ7R5U':
  r.update(mpn='RC2010JK-077R5L',manufacturer='Yageo',jlc_code='C4169838',current_stock=220,status='In stock; prototype snubber substitute',checked_utc='2026-09-26',source_url='https://jlcpcb.com/partdetail/C4169838',proposed_alternative='D6: same 7.5 ohm, 5%, 0.75 W, 2010 geometry. About 0.30 W estimated snubber dissipation; measured pulse/thermal qualification still required. Replaces preorder Panasonic part.')
 if r['assembly'].startswith('MANUAL'):
  p=manual[r['mpn']];first=r['mpn'] not in seen;seen.add(r['mpn'])
  r.update(purchase_quantity=p['recommended_loose_quantity'] if first else 0,purchase_supplier=p['supplier'],purchase_stock=p['observed_stock'],purchase_url=p['source_url'],purchase_basis=p['quantity_basis']+'; combined across all board rows for this MPN; quantity shown only on first occurrence.' if first else 'Included in first occurrence of this MPN; do not purchase twice.')
  r['status']='Exact loose part in stock; user-fit'
  r['proposed_alternative']='D6 exact MPN retained. Purchase separately as loose parts from the listed supplier; omit from JLC SMT assembly.'
  if r['mpn']=='166.7000.4302':
   r['status']='Obsolete; exact loose stock covers batch'
   r['proposed_alternative']='Manufacturer obsolescence confirmed; purchase 20: ten fitted plus ten replacement inserts. Suitable supply route for this batch, not guaranteed future availability. Never substitute 32 V fuse.'
 else:
  a=attr.get(r['jlc_code'],{});loss=a.get('lossNumber');minimum=a.get('leastPatchNumber');n=r['required_10_pairs']
  qty=max(n,minimum)+loss if loss is not None and minimum is not None else max(n+10,30)
  basis=f'Conservative planning: max({n} installed, {minimum} minimum)+{loss} attrition. Exact order-page quantity controls.' if loss is not None and minimum is not None else 'Conservative placeholder allowance; part-specific attrition/minimum must be resolved by JLC BOM matching.'
  if r['jlc_code']=='C4169838':qty=30;basis='Ten fitted plus twenty planning allowance; confirm exact JLC minimum and attrition at matching.'
  r.update(purchase_quantity=qty,purchase_supplier='JLCPCB SMT assembly',purchase_stock=r['current_stock'],purchase_url=r['source_url'],purchase_basis=basis)
  if r['jlc_code']=='C23481145':r['proposed_alternative']='Retained 100 V C0G 470 pF 5% snubber capacitor. Ten installed plus four reported attrition requires14; observed15 leavesone. Reserve/match at order, stock not guaranteed.'
  if r['jlc_code']=='C19276042':r['proposed_alternative']='Retained exact magnetics. Ten installed; current catalogue minimum/attrition fields0/0. Observed17. Include required assembly fixture in quote.'
  r['proposed_alternative']+=' JLC stock is the dated observation, not reserved inventory.'
 if r['mpn']=='178.6165.0002':r['value']='ATO/FKS fuse holder; insert separate'
 if r['mpn']=='B2P-VH(LF)(SN)':r['value']='2-pin 12 V header'
for p in manual.values():assert p['observed_stock']>=p['recommended_loose_quantity']
assert sum(p['qty_per_pair'] for p in parts)==131
out={'revision':'D6','order_sets':10,'parts':parts}
Path('work/jlc_combined_parts_d6.json').write_text(json.dumps(out,indent=2))
root=Path('outputs/UMI_D6')
(root/'PROCUREMENT_RECORD.json').write_text(json.dumps(out,indent=2))
with (root/'UMI_COMPONENT_SOURCING.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(parts[0]));w.writeheader();w.writerows(parts)
print('Combined procurement list:',len(parts),'rows;',len(manual),'manual MPNs with adequate loose stock')
