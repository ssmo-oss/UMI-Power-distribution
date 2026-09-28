from pathlib import Path
import csv,json
from design_d2 import *
root=Path('outputs/UMI_D6');report={}
for name in ['MAIN_POWER','POE_POWER','USB_POWER']:
 d=root/name;path=d/(name+'.kicad_pcb');b=parse(path.read_text());changes=[];schedule=[]
 if name=='MAIN_POWER':
  for t in all_(b,'gr_text'):
   font=one(one(t,'effects'),'font');size=one(font,'size');thick=one(font,'thickness')
   if float(size[1])<1:
    changes.append(str(t[1]));size[1:]=['1','1']
    if thick and float(thick[1])<.15:thick[1]='0.15'
 else:
  origin=one(one(b,'setup'),'aux_axis_origin');ox,oy=map(float,origin[1:])
  for via in all_(b,'via'):
   diameter=float(one(via,'drill')[1]);filled=diameter<=.55
   set_(via,'filling',['filling','yes' if filled else 'no']);set_(via,'capping',['capping','yes' if filled else 'no'])
   x,y=map(float,one(via,'at')[1:3])
   schedule.append({'KiCad X mm':x,'KiCad Y mm':y,'Plot X mm':round(x-ox,6),'Plot Y mm':round(oy-y,6),'Hole mm':diameter,'Treatment':'Epoxy filled and copper capped' if filled else 'Ordinary plated via; do not fill/cap','UUID':one(via,'uuid')[1]})
  with (d/'manufacturing/VIA_TREATMENT.csv').open('w',newline='',encoding='utf-8-sig') as f:
   w=csv.DictWriter(f,fieldnames=list(schedule[0]));w.writeheader();w.writerows(schedule)
 write(path,b)
 report[name]={'enlarged_labels':changes,'filled_capped_vias':sum(r['Hole mm']<=.55 for r in schedule),'ordinary_vias':sum(r['Hole mm']>.55 for r in schedule)}
(root/'FABRICATION_NOTES.md').write_text('''# D6 fabrication instructions

Use separate builds for MAIN (1.2 mm), POE (1.2 mm) and USB (1.6 mm). All are four-layer ENIG, 2 oz outer and 1 oz inner copper; green soldermask and white legend. Maintain exact outlines and mounting holes. Use the source stackup and MANUFACTURING_SPECIFICATION.md; quote any stackup change explicitly.

POE and USB require epoxy resin-filled, copper-capped vias at all positions marked in manufacturing/VIA_TREATMENT.csv. This is a coordinate schedule, not a drill program. Plot coordinates share the Gerber/drill origin; Y is inverted relative to KiCad coordinates. Drill files remain authoritative for hole geometry. Corresponding KiCad via objects explicitly carry filling/capping flags. Filling is not tenting or soldermask plugging.

POE smaller vias (0.254, 0.35 and 0.40 mm) are filled/capped. Its 0.635 mm vias are ordinary plated vias and must not be included in the fill process. USB 0.25/0.30 mm vias are filled/capped. MAIN has no vias requiring this process. All through-hole component and mounting holes remain open.

The POE Coilcraft SER2915H-103KL inductor requires an assembly support fixture. Include it in the SMT quotation. Assemble only the SMT BOM/CPL; connectors, holders and inserts are user-fitted. Preserve the original footprint pad geometry and paste openings. Review every supplier rotation/pin-1 preview before accepting assembly.

The requested construction has published capability support, but the exact selective-fill/copper/thickness combination and fixture still require manufacturer engineering acceptance. No quote is represented as accepted.
''',encoding='utf-8')
Path('work/d6_fabrication_details.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
