from pathlib import Path
import json,copy,csv
from design_d2 import *
d=Path('outputs/UMI_D4/MAIN_POWER');path=d/'MAIN_POWER.kicad_pcb'
b=parse(path.read_text(encoding='utf-8'));f=next(f for f in all_(b,'footprint') if prop(f,'Reference')[2]=='R2')
assert str(f[1])=='UMI_D2:R_2512_6332Metric_R270'
name='EverOhms_MA2512_2to5mOhm_R270';f[1]=Q('UMI_D2:'+name)
one(f,'descr')[1]=Q('Ever Ohms MA2512 2-5mOhm recommended land, a2.60 b3.68 gap2.55; MA Rev30/34 p8; rotated270 geometry')
for p in all_(f,'pad'):
    p[3]='rect';one(p,'at')[1:]=['0','2.575' if p[1]=='1' else '-2.575'];one(p,'size')[1:]=['3.68','2.60']
    p[:]=[x for x in p if not(isinstance(x,list) and x[0]=='roundrect_rratio')]
for rect in all_(f,'fp_rect'):
    if one(rect,'layer')[1]=='F.CrtYd':one(rect,'start')[1:]=['-2.10','-4.15'];one(rect,'end')[1:]=['2.10','4.15']
lib=copy.deepcopy(f);lib[1]=Q(name)
lib[:]=[x for x in lib if not(isinstance(x,list) and x[0] in ['uuid','at','path','sheetfile','sheetname'])]
for p in all_(lib,'pad'):p[:]=[x for x in p if not(isinstance(x,list) and x[0] in ['net','uuid'])]
write(d/'UMI_D2.pretty'/(name+'.kicad_mod'),lib);write(path,b)
s=parse((d/'MAIN_POWER.kicad_sch').read_text(encoding='utf-8'))
sf=next(x for x in all_(s,'symbol') if prop(x,'Reference') and prop(x,'Reference')[2]=='R2');prop(sf,'Footprint')[2]=Q('UMI_D2:'+name)
write(d/'MAIN_POWER.kicad_sch',s)
parts=json.loads((d/'design.json').read_text());p=next(x for x in parts if x['ref']=='R2');p['fp']='UMI_D2:'+name;p['source_fp']='UMI_D2:EverOhms_MA2512_2to5mOhm'
(d/'design.json').write_text(json.dumps(parts,indent=2),encoding='utf-8')
with (d/'pin_schedule.csv').open(encoding='utf-8-sig',newline='') as fh:rows=list(csv.DictReader(fh))
for row in rows:
    if row['Reference']=='R2':row['Footprint']=p['fp']
with (d/'pin_schedule.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    w=csv.DictWriter(fh,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(d/'GEOMETRY_EDITED').write_text('R2 manufacturer recommended pads. Refill zones and revalidate.\n')
print('R2 manufacturer land applied; pin1 remains +Y, pin2 -Y; supplier rotation90CCW retained')
