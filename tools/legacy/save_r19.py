import json
from pathlib import Path
row=dict(ref='R19',mpn='ERA-3AEB8452V',manufacturer='Panasonic',code='C4295220',stock=694,approved=True,assessment='84.5kohm0.1%25ppm100mW75V0603; exactnominalTCRrating replacement.',datasheet='https://api.pim.na.industrial.panasonic.com/file_stream/main/fileversion/1101',url='https://jlcpcb.com/partdetail/C4295220')
p=Path('work/jlc_main_approved_substitutes.json');d=json.loads(p.read_text());d.append(row);p.write_text(json.dumps(d,indent=2))
p=Path('work/jlc_main_passives.json');d=json.loads(p.read_text())
for r in d['parts']:
 if 'R19' in r['references']:r['approved_substitute']=row
p.write_text(json.dumps(d,indent=2))
