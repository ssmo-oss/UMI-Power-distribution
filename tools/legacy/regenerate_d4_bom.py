"""Regenerate D4 BOMs from D4 design identities, D3 assembly classification and approved substitution manifest."""
import csv,json
from pathlib import Path
base=Path('outputs');manifest=json.loads(Path('work/d4_substitutions.json').read_text());catalog=json.loads(Path('work/jlc_combined_parts.json').read_text())['parts']
for board in ['MAIN_POWER','USB_POWER']:
 d=base/'UMI_D4'/board;parts=json.loads((d/'design.json').read_text());byref={p['ref']:p for p in parts}
 changes={ref:m for m in manifest if m['board']==board for ref in m['refs']}
 old=list(csv.DictReader((base/'UMI_D3'/board/'BOM_grouped.csv').open(encoding='utf-8-sig')));groups={}
 for b in old:
  for ref in b['Reference'].split(','):
   p=byref[ref];m=changes.get(ref);assert not m or p['mpn']==m['mpn'],(ref,'manifest/design mismatch')
   known=next((x for x in catalog if x['board']==board and x['mpn']==p['mpn']),{})
   code=m['jlc_code'] if m else known.get('jlc_code','');manufacturer=m['manufacturer'] if m else b['Manufacturer']
   value=p['value'];key=(p['mpn'],p['fp'],b['Assembly'],manufacturer,value,code)
   if key not in groups:groups[key]={'Reference':[],'Value':value,'Quantity per board':0,'Manufacturer':manufacturer,'Manufacturer part number':p['mpn'],'Footprint':p['fp'],'Assembly':b['Assembly'],'LCSC/JLC code':code,'Sourcing note':m.get('note','Approved substitution') if m else 'Exact catalog identity; check stock and order acceptance'}
   row=groups[key];row['Reference'].append(ref);row['Quantity per board']+=1
 rows=list(groups.values())
 for row in rows:row['Reference']=','.join(row['Reference'])
 with (d/'BOM_grouped.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 expanded=[]
 for row in rows:
  for ref in row['Reference'].split(','):expanded.append({**row,'Reference':ref,'Quantity per board':1})
 with (d/'BOM_by_reference.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(expanded)
 with (d/'BOM_JLC_DRAFT.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #','Manufacturer','MPN'])
  for row in rows:
   if row['Assembly']=='SMT':w.writerow([row['Value'],row['Reference'],byref[row['Reference'].split(',')[0]]['source_fp'],row['LCSC/JLC code'],row['Manufacturer'],row['Manufacturer part number']])
 (d/'BOM_audit.json').write_text(json.dumps({'revision':'D4','board':board,'reference_count':len(expanded),'smt_count':sum(x['Assembly']=='SMT' for x in expanded),'manual_count':sum(x['Assembly']!='SMT' for x in expanded),'missing_smt_jlc_codes':[x['Reference'] for x in expanded if x['Assembly']=='SMT' and not x['LCSC/JLC code']],'source':'D4 design identities + approved substitutions + original assembly classification','source_footprints_used_for_supplier_orientation':True},indent=2))
 print(board,len(rows),sum(x['Quantity per board'] for x in rows))
