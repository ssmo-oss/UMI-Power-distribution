import json
from pathlib import Path
rows=[dict(ref='C1',mpn='C0805C471J1GACTU',manufacturer='KEMET',code='C23481145',stock=15,approved=True,assessment='470pF100VC0G5%0805;2x1.25x0.78mm. Exact nominal/footprint replacement; stock only10boards+5spares.',datasheet='https://www.tme.eu/Document/5fe0fdceeb8fc4b9dab34992e074b417/C0805C471J1GACTU.pdf'),dict(ref='R11',mpn='RC0603FR-073R3L',manufacturer='Yageo',code='C137725',stock=159032,approved=True,assessment='3.3ohm1%100mW75V0603±200ppm; improves original5%tolerance, sameVINdecouplingrole.',datasheet='https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-073R3L'),dict(ref='R13',mpn='RC0603FR-078K45L',manufacturer='Yageo',code='C163417',stock=529,approved=True,assessment='8.45k1%100mW75V0603±100ppm, exactnominalandcase replacement.',datasheet='https://www.yageogroup.com/component-documentation/download/specsheet/RC0603FR-078K45L')]
Path('work/jlc_main_approved_substitutes.json').write_text(json.dumps(rows,indent=2))
p=Path('work/jlc_main_passives.json');d=json.loads(p.read_text())
for row in rows:
 row['url']='https://jlcpcb.com/partdetail/'+row['code']
 for part in d['parts']:
  if row['ref'] in part['references']:part['approved_substitute']=row
p.write_text(json.dumps(d,indent=2))
