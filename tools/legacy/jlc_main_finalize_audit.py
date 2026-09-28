import json,collections
from pathlib import Path
p=Path('work/jlc_main_passives.json');data=json.loads(p.read_text());alts=json.loads(Path('work/jlc_main_alternates.json').read_text())
zero=next(a for a in alts if a['mpn']=='ERJ3GEY0R00V')
for row in data['parts']:
 if row['mpn']=='ERJ-3GEY0R00V':
  for k in ('jlc_code','url','live_jlc_metadata','checked_utc'):row[k]=zero[k]
  row['exact_match']=True;row['identity_note']='Panasonic manufacturer hyphen omitted in JLC model: ERJ3GEY0R00V.'
 info=row.get('live_jlc_metadata',{});stock=info.get('overseasStockCount')
 if stock is not None:
  row['reported_jlc_stock']=stock;row['stock_field']='overseasStockCount';row['status']='live_jlc_in_stock' if stock>0 else 'live_jlc_zero_stock';row['library_type']='Extended' if info.get('componentLibraryType')=='expand' else info.get('componentLibraryType')
 row['proposed_alternates']=[a for a in alts if set(a['references'].split(','))&set(row['references']) and a['mpn']!='ERJ3GEY0R00V']
data['stock_caveat']='Counts are live public JLC page purchasing metadata (overseasStockCount); coordinating browser checks established this field matches displayed In Stock. Not reserved, final order quantity/attrition and assembly eligibility must be confirmed at ordering. Zero differs from search not found and HTTP429 unknown.'
data['unfetched_candidates']=[dict(references='C14',mpn='CC0603KRX7R9BB473',jlc_code='C107093',url='https://jlcpcb.com/partdetail/YAGEO-CC0603KRX7R9BB473/C107093',spec='47nF 50V X7R +/-10% 0603',stock='unknown; browser check requested',assessment='Same value/dielectric/package; voltage upgraded25to50V. Soft-start timing capacitance DC-bias verification still required.')]
p.write_text(json.dumps(data,indent=2),encoding='utf8')
lines=['# MAIN_POWER JLC passive availability audit','',data['stock_caveat'],'','No PCB, schematic or BOM substitutions have been applied. R2 shunt is handled by the parallel critical-parts review.','', '| References | Original MPN | JLC code | Library | Live stock | Status |','|---|---|---|---|---:|---|']
for r in data['parts']:
 code=f"[{r['jlc_code']}]({r['url']})" if r.get('jlc_code') else '—'
 lines.append('| '+ ' | '.join([', '.join(r['references']),r['mpn'],code,str(r.get('library_type','Unknown')),str(r.get('reported_jlc_stock','Unknown')),r['status']])+' |')
lines+=['','## Substitution candidates, not approved','', '| Ref | Candidate | JLC | Live stock | Assessment |','|---|---|---|---:|---|']
for a in alts:
 i=a.get('live_jlc_metadata',{});lines.append('| '+' | '.join([a['references'],a['mpn'],f"[{a['jlc_code']}]({a['url']})",str(i.get('overseasStockCount','Unknown')),a['assessment']])+ ' |')
lines+=['','## Engineering constraints','',
'- C2–C8 should retain the exact Murata 80 V, 4.7 µF, 1210 part where possible. Nominal capacitance alone does not establish effective capacitance at 53.5 V. A different 80/100 V ceramic requires DC-bias data and control-loop review.',
'- C1 is the snubber capacitor: preserve 470 pF, C0G/NP0, at least100 V and +/-5% or better. Do not substitute X7R or a50 V part.',
'- R1 needs repetitive snubber pulse capability, not merely matching 7.5 ohm/2010/wattage. The stocked UniRoyal candidate is not approved until its pulse curve is checked.',
'- C19/C20 hybrid candidate has much lower ESR than the original Panasonic FK electrolytic. The changed output-filter damping and converter stability need review; matching body size and voltage is insufficient. EEE-FN1K470UL is rejected as a direct replacement:8 mm body,1.3 ohm ESR and130 mA ripple differ from the10 mm original.',
'- R18/R19/R20 feedback divider and R22/R23/R24/R25 protection components retain0.1% requirements. Do not silently substitute generic1% parts. Same-value15ppm Yageo alternatives improve TCR but currently have unknown/zero stock.',
'- C18 compensation capacitor: YageoC107076 has matching15 nF50 VX7R10%0603 nominal specs and substantial live stock; compare effective capacitance in its low-voltage compensation application before final substitution.',
'- C14 alternate C107093 (CC0603KRX7R9BB473) has matching47 nF/X7R/10%/0603 and higher50 V rating; live inventory still needs browser confirmation.',
'- The exact8.45 kohm R13 has only5 reported parts; this is not enough for a comfortable small assembly order including attrition.','',
'HTTP429 occurred on C71664, C861034, C17565246, C596323 and C597304. Their stock remains unknown; no claim of out-of-stock follows from rate limiting. Raw live page evidence is retained in work/jlc_main_passive_pages/.']
Path('work/jlc_main_passives.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print(collections.Counter(r['status']for r in data['parts']))
