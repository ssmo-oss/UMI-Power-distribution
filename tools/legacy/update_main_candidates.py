import json
from pathlib import Path
p=Path('work/jlc_main_passives.json');d=json.loads(p.read_text())
for r in d['parts']:
 if 'C14' in r['references']:
  r['proposed_alternates'].append(dict(mpn='CC0603KRX7R9BB473',jlc_code='C107093',url='https://jlcpcb.com/partdetail/C107093',reported_jlc_stock=1574400,library_type='Extended',primary_datasheet='https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB473',assessment='Manufacturer-verified 47nF50VX7R10%, 0603 1.6x0.8x0.8mm +/-0.1; same nominal capacitance, dielectric, tolerance and footprint. Higher voltage rating. Suitable proposed timing-capacitor replacement; validate timing in prototype.'))
 if 'C18' in r['references']:
  for a in r['proposed_alternates']:
   if a.get('mpn')=='CC0603KRX7R9BB153':a.update(primary_datasheet='https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB153',assessment='Manufacturer-verified15nF50VX7R10%,0603 1.6x0.8x0.8mm+/-0.1. Nominal and mechanical drop-in; compensation performance still requires loop testing; no high-bias bulk-capacitor substitution involved.')
 if 'C1' in r['references']:
  for a in r['proposed_alternates']:
   if a.get('jlc_code')=='C17565246':a.update(status='out_of_stock',reported_jlc_stock=0)
 if 'R1' in r['references']:
  r['proposed_alternates'].append(dict(mpn='SCR2010J7R5',jlc_code='C5140273',reported_jlc_stock=235,url='https://jlcpcb.com/partdetail/C5140273',assessment='Unapproved candidate: nominal7.5ohm5%750mW2010; primary PDF blocked403 so repetitive pulse rating not verified. Snubber application requires pulse review, not just average wattage.'))
p.write_text(json.dumps(d,indent=2),encoding='utf-8')
with Path('work/jlc_main_passives.md').open('a',encoding='utf-8') as f:
 f.write('\n## Manufacturer-reviewed capacitor alternatives\n\nC14: Yageo CC0603KRX7R9BB473, C107093, live JLC stock1,574,400. C18: Yageo CC0603KRX7R9BB153, C107076, live403,038. Both 50V X7R10%,0603; manufacturer dimensions1.6x0.8x0.8mm +/-0.1. C14 preserves47nF with higher voltage rating; C18 preserves15nF. Prototype timing/loop checks remain required.\n\nPrimary sources: https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB473 and https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB153\n\nC1 alternative C17565246 now verified zero stock. R1 VO SCR2010J7R5 C5140273 live235 stock, but not approved: manufacturer PDF inaccessible and repetitive snubber-pulse rating unverified.\n')
