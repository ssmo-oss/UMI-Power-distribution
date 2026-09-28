from pathlib import Path
import csv,json
base=Path.cwd();d=base/'outputs/UMI_TWO_BOARD_DESIGN';d.mkdir(exist_ok=True)
review=json.loads((base/'work/fuse_verification.json').read_text())['preferred_eska']
rows=[]
for p in review['parts']:
 rows.append([','.join('MAIN_POWER '+r+' insert' for r in p['references']),p['quantity'],'ESKA',p['mpn'],f"{p['current_A']} A / {p['voltage_VDC']} VDC blade fuse",'Fit into existing holder; holder purchased separately',review['source']])
rows.extend([
 ['Main J2,J3,J4,J5 and USB J1 cable housings',5,'JST','VHR-2N','2-position VH housing','One system set; device-end connectors are application-specific','https://www.jst-mfg.com/product/pdf/eng/eVH.pdf'],
 ['Main J6 switch cable housing',1,'JST','VHR-3N','3-position VH housing','Populate only the two power positions in the final pin schedule','https://www.jst-mfg.com/product/pdf/eng/eVH.pdf'],
 ['Contacts for the six housings',12,'JST','SVH-41T-P1.1','Crimp socket contact, AWG20–16','Assumes all conductors fit 0.5–1.25 mm² and insulation OD1.7–3.0 mm; buy spare contacts','https://www.jst-mfg.com/product/pdf/eng/eVH.pdf'],
])
with (d/'MANUAL_FUSES_AND_HARNESS_BOM.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Use','Quantity per system','Manufacturer','MPN','Description','Assembly note','Manufacturer source']);w.writerows(rows)
(d/'MANUAL_ASSEMBLY.md').write_text('''# Manual assembly and harness parts

Use each board's **BOM_by_reference.csv** for its through-hole connectors and fuse holders. **MANUAL_FUSES_AND_HARNESS_BOM.csv** adds the six fuse inserts and the cable-side JST parts; it does not duplicate the board-mounted parts.

The switch output requires ESKA **340.022-80V, 3 A, 80 VDC**. Do not substitute a common 32 V automotive fuse on the 53.5 V rail. The older Littelfuse FKS code considered during development is not the preferred BOM because distributor results indicated end of life.

ESKA's manufacturer catalog verifies the selected current/voltage ratings, time-current windows and standard blade dimensions. It specifies 1000 A breaking capacity. Its 32 V temperature graph gives an approximate 0.97 factor at 40 °C; the 80 V page does not provide a 40 °C correction. Check temperatures and nuisance opening under actual enclosure load. Fuse operation is not proof that a semiconductor survives an output short.

Main board thickness is 1.2 mm to stay below the fuse holder's 1.5 mm PCB limit. The JST reference drawing uses a 1.6 mm PCB; the shorter board leaves more lead protrusion. Check seating and clip retention on the first assembly. The USB board is 1.6 mm thick.

JST SVH-41T-P1.1 contacts accept AWG20–16 conductors with the specified insulation diameter. If using thinner fan wiring, select SVH-21T-P1.1 (AWG22–18) instead for those positions and reduce the larger-contact count accordingly. Correct crimp tooling and pull-checks are required.

The table gives **one system's installed quantity**, not purchasing pack size or spare allowance. Live distributor stock and pricing have not been reserved. Device-end plugs, input cable gauge, mounting hardware and final harness length depend on the enclosure and devices and are not invented in this BOM.

Primary sources: [ESKA automotive catalog, pages 16 and 19](https://www.eska-fuses.de/fileadmin/produkte/datenblaetter/ESKA_KFZ_Sicherungen.pdf), [JST VH series](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf).
''',encoding='utf-8')
print('Manual fuse and harness BOM generated')
