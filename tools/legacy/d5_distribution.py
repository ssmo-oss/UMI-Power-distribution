"""Build the passive 12V distribution PCB; preserve original four mounting centres."""
from pathlib import Path
import json,copy,shutil
from design_d2 import *
from validation_schematic_package import package_schematic
src=Path('outputs/UMI_D4/MAIN_POWER');d=Path('outputs/UMI_D5/MAIN_POWER');d.mkdir(parents=True,exist_ok=True)
for fn in ['MAIN_POWER.kicad_pro','fp-lib-table','sym-lib-table']:shutil.copy2(src/fn,d/fn)
shutil.copytree(src/'UMI_D2.pretty',d/'UMI_D2.pretty',dirs_exist_ok=True)
old=parse((src/'MAIN_POWER.kicad_pcb').read_text());oldfps={str(prop(f,'Reference')[2]):f for f in all_(old,'footprint')}
orig=json.loads((src/'design.json').read_text());parts=[copy.deepcopy(p) for p in orig if p['ref'] in ['J1','J2','J3','J4','J5','F1','F2','F3','F4','F5']]
new=copy.deepcopy(next(p for p in parts if p['ref']=='J2'));new.update(ref='J6',value='POE BOARD 12V INPUT',pos=[42.02,98]);new['pins']['1']=('+12V','FUSED_BOOST_12V');parts.append(new)
positions={'J1':(33.84,21),'F1':(17,46),'J2':(21,56),'F2':(50,46),'J3':(54,56),'F3':(17,67),'J4':(21,77),'F4':(50,67),'J5':(54,77),'F5':(37.6,88),'J6':(42.02,98)}
for p in parts:
    p['pos']=list(positions[p['ref']])
    if p['ref']=='J3':p['value']='GMSL 12V / EXCLUSIVE WITH POE'
    if p['ref']=='F5':p['value']='10A POE CABLE FUSE HOLDER'
for ref in ['H1','H2','H3','H4']:
    f=oldfps[ref];parts.append(dict(ref=ref,value='M3 MOUNT',fp=str(f[1]),source_fp='MountingHole:MountingHole_3.2mm_M3',pins={},pos=list(map(float,one(f,'at')[1:3])),mpn='MECHANICAL - NO PURCHASE',types={}))
root=symbol_schematic('MAIN_POWER',parts,d);package_schematic(d/'MAIN_POWER.kicad_sch',externally_driven_nets=['12V_IN','GND'])
sch=parse((d/'MAIN_POWER.kicad_sch').read_text());one(one(sch,'title_block'),'title')[1]=Q('UMI 12V distribution');one(one(sch,'title_block'),'rev')[1]=Q('D5 - THREE BOARD PROTOTYPE');write(d/'MAIN_POWER.kicad_sch',sch)
b=copy.deepcopy(old);b[:]=[x for x in b if not(isinstance(x,list) and (x[0] in ['footprint','net','segment','via','zone'] or x[0].startswith('gr_')))]
set_(one(b,'setup'),'aux_axis_origin',['aux_axis_origin','10','110.263962'])
netnames=sorted({n for p in parts for _,n in p['pins'].values() if n});codes={n:i+1 for i,n in enumerate(netnames)}
# Current KiCad accepts named nets; canonical numeric table is emitted for construction.
b.extend([['net',str(c),Q(n)] for n,c in codes.items()])
def resetids(node,key):
    for i,x in enumerate(node):
        if isinstance(x,list):
            if x[0]=='uuid':x[1]=Q(uid('d5-main/'+key+'/'+str(i)))
            else:resetids(x,key+'/'+str(i))
for p in parts:
    ref=p['ref'];f=copy.deepcopy(oldfps['J2' if ref=='J6' else ref]);resetids(f,ref)
    set_(f,'at',['at',*[str(v) for v in p['pos']]])
    prop(f,'Reference')[2]=Q(ref);prop(f,'Value')[2]=Q(p['value'])
    if prop(f,'MPN'):prop(f,'MPN')[2]=Q(p['mpn'])
    set_(f,'path',['path',Q('/'+root+'/'+uid('MAIN_POWER/'+ref))])
    set_(f,'sheetfile',['sheetfile',Q('MAIN_POWER.kicad_sch')])
    if ref.startswith('H'):set_(f,'attr',['attr','exclude_from_pos_files','exclude_from_bom'])
    for a in all_(f,'pad'):
        num=str(a[1]);a[:]=[x for x in a if not(isinstance(x,list) and x[0]=='net')]
        if num in p['pins']:
            n=p['pins'][num][1];a.append(['net',str(codes[n]),Q(n)])
    b.append(f)
def line(a,z,layer,width=.05):b.append(parse(f'(gr_line (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (stroke (width {width}) (type solid)) (layer "{layer}") (uuid "{uid("d5main/edge/"+str(a)+str(z))}"))'))
# Rounded 68 x100.263962 outline, original hole coordinates unchanged.
x0,y0,x1,y1,r=10,10,78,110.263962,3
for a,z in [((x0+r,y0),(x1-r,y0)),((x1,y0+r),(x1,y1-r)),((x1-r,y1),(x0+r,y1)),((x0,y1-r),(x0,y0+r))]:line(a,z,'Edge.Cuts')
for a,m,z in [((75,10),(77.12132,10.87868),(78,13)),((78,y1-3),(77.12132,y1-.87868),(75,y1)),((13,y1),(10.87868,y1-.87868),(10,y1-3)),((10,13),(10.87868,10.87868),(13,10))]:b.append(parse(f'(gr_arc (start {a[0]} {a[1]}) (mid {m[0]} {m[1]}) (end {z[0]} {z[1]}) (stroke (width .05) (type solid)) (layer "Edge.Cuts") (uuid "{uid("d5main/arc/"+str(a))}"))'))
def text(label,x,y,size=1,layer='F.SilkS'):
    justify=' (justify mirror)' if layer=='B.SilkS' else ''
    b.append(parse(f'(gr_text {json.dumps(label)} (at {x} {y}) (layer "{layer}") (uuid "{uid("d5main/text/"+label+layer+str(x)+str(y))}") (effects (font (size {size} {size}) (thickness .15)){justify}))'))
text('UMI 12V DISTRIBUTION',44,14,1.55);text('D5  |  3-BOARD SYSTEM',44,18,1.0)
text('J1  INPUT 12V DC',44,41.0,1.1)
text('+12V',29,23,1);text('GND',56.5,32.5,1)
for i,(name,amp,x,y) in enumerate([('JETSON','7.5A',23.4,46),('GMSL','7.5A',56.4,46),('FAN','1A',23.4,67),('USB BOARD','5A',56.4,67),('POE BOARD','10A',44,88)],1):
    text(f'F{i}  {amp}',x,y-3,1)
    text(f'J{i+1}  {name}',x,y+15.9,1)
    j=next(p for p in parts if p['ref']=='J'+str(i+1));jx,jy=j['pos'];text('+',jx-4.4,jy-1,.9);text('-',jx+8,jy-1,.9)
text('12V ONLY  |  FUSES ARE NOT LOAD RATINGS',44,108, .85)
text('GMSL OR POE - NEVER BOTH',44,42,1,'B.SilkS')
text('D5  /  40C AMBIENT DESIGN BASIS',44,15,1.1,'B.SilkS')
text('JETSON 5A  /  FAN 0.14A  /  USB FEED 3A',44,26.8,.95,'B.SilkS')
text('WORST CONFIG ~174W AT 12V',44,30.0,1.1,'B.SilkS')
text('CONNECT POE BOARD TO J6 ONLY',44,38.5,1,'B.SilkS')
text('UPSTREAM PSU CABLE PROTECTION REQUIRED',44,104,.9,'B.SilkS')
def route(net,width,pts,layer):
    for j,(a,z) in enumerate(zip(pts,pts[1:])):
        if a==z:continue
        b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width {width}) (layer "{layer}") (net {codes[net]}) (uuid "{uid("d5main/track/"+net+layer+str(j)+str(a)+str(z))}"))'))
for i in range(1,6):
    f=next(p for p in parts if p['ref']=='F'+str(i));j=next(p for p in parts if p['ref']=='J'+str(i+1));x,y=f['pos'];jx,jy=j['pos'];net=f['pins']['2'][1]
    for layer in ['F.Cu','B.Cu']:
        # Tie every blade-terminal pin, keep the central plastic locating hole clear.
        route('12V_IN',2,[(x,y),(x+3.5,y),(x+3.5,y+2.5),(x,y+2.5),(x,y)],layer)
        route(net,2,[(x+9.3,y),(x+12.8,y),(x+12.8,y+2.5),(x+9.3,y+2.5),(x+9.3,y)],layer)
        width=1.0 if i==3 else 3.0
        # A short45-degree shoulder keeps the output trace out of the return pad.
        route(net,width,[(x+9.3,y+2.5),(x+9.3,y+3.1),(jx,y+3.1+abs(x+9.3-jx)),(jx,jy)],layer)
for layer,net in [('F.Cu','12V_IN'),('In1.Cu','12V_IN'),('In2.Cu','GND'),('B.Cu','GND')]:
    b.append(parse(f'(zone (net {codes[net]}) (net_name "{net}") (layer "{layer}") (uuid "{uid("d5main/plane/"+layer)}") (hatch edge .5) (connect_pads yes (clearance .4)) (min_thickness .25) (fill yes (thermal_gap .4) (thermal_bridge_width .7)) (polygon (pts (xy 10.5 10.5) (xy 77.5 10.5) (xy 77.5 109.763962) (xy 10.5 109.763962))))'))
write(d/'MAIN_POWER.kicad_pcb',b)
(d/'design.json').write_text(json.dumps(parts,indent=2),encoding='utf-8')
print('MAIN_POWER: 68x100.263962mm, 5 source-side fuse branches, original4 mounting centres; fill required')
