from pathlib import Path
import json,collections,hashlib,csv
from design_d2 import *
root=Path('outputs/UMI_D6');report={}
for name in ['MAIN_POWER','POE_POWER','USB_POWER']:
 d=root/name;b=parse((d/(name+'.kicad_pcb')).read_text());old=parse((Path('outputs/UMI_D5')/name/(name+'.kicad_pcb')).read_text());issues=[]
 setup=one(b,'setup');stack=one(setup,'stackup');cu=[x[1] for x in all_(stack,'layer') if one(x,'type')[1]=='copper'];assert cu==['F.Cu','In1.Cu','In2.Cu','B.Cu'],cu
 oldtracks={one(s,'uuid')[1]:s for s in all_(old,'segment')};changes=[]
 for s in all_(b,'segment'):
  uid=one(s,'uuid')[1];prior=oldtracks[uid]
  if s!=prior:changes.append({'uuid':uid,'old_width':one(prior,'width')[1],'new_width':one(s,'width')[1]});clone=[x for x in s if not(isinstance(x,list) and x[0]=='width')];previous=[x for x in prior if not(isinstance(x,list) and x[0]=='width')];assert clone==previous
 assert len(changes)==(5 if name=='POE_POWER' else 0)
 for via in all_(b,'via'):
  expected='yes' if float(one(via,'drill')[1])<=.55 else 'no'
  assert one(via,'filling')[1]==expected and one(via,'capping')[1]==expected
 uuids=[]
 def walk(n):
  if isinstance(n,list):
   if n and n[0]=='uuid':uuids.append(n[1])
   for x in n:walk(x)
 walk(b);assert len(uuids)==len(set(uuids))
 for check in ['DRC','ERC']:assert json.loads((d/'verification'/('export_'+check+'.json')).read_text())['exit_code']==0
 hashes=json.loads((d/'verification/export_source_hashes.json').read_text())
 for filename,h in hashes.items():assert hashlib.sha256(Path(filename).read_bytes()).hexdigest()==h
 report[name]={'stackup_copper_layers':cu,'native_checks':'pass','copper_segment_changes':changes,'via_treatment_readback':'pass','duplicate_UUIDs':0,'source_hashes_current':True}
parts=json.loads(Path('work/jlc_combined_parts_d6.json').read_text())['parts'];assert all(p['purchase_quantity']<=p['purchase_stock'] for p in parts)
for p in parts:
 if p['mpn']=='RC2010JK-077R5L':assert p['jlc_code']=='C4169838'
assert len(parts)==70 and sum(p['qty_per_pair'] for p in parts)==131
report['procurement']={'rows':70,'installed_per_set':131,'planned_buy_quantities_within_observed_stock':True,'stock_reserved':False}
(root/'verification/FINAL_AUDIT.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
