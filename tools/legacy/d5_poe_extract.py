"""Extract D4 converter, preserve routed power cell; no KiCad executable imports."""
from design_d2 import *
from validation_schematic_package import package_schematic
import shutil,math
SRC=BASE/'outputs/UMI_D4/MAIN_POWER';D=BASE/'outputs/UMI_D5/POE_POWER';D.mkdir(parents=True,exist_ok=True)
NAME='POE_POWER';local=D/'UMI_D2.pretty';shutil.copytree(SRC/'UMI_D2.pretty',local,dirs_exist_ok=True)
b=parse((SRC/'MAIN_POWER.kicad_pcb').read_text());original=copy.deepcopy(b)
removed={'J1','J2','J3','J4','J5','F1','F2','F3','F4','F5','H1','H2','H3','H4'}
parts=[p for p in json.loads((SRC/'design.json').read_text()) if p['ref'] not in removed]
oldfps={str(prop(f,'Reference')[2]):f for f in all_(b,'footprint')}
b[:]=[n for n in b if not(isinstance(n,list) and ((n[0]=='footprint' and str(prop(n,'Reference')[2]) in removed) or n[0].startswith('gr_') or n[0] in ('dimension','group')))]
# Remove distribution copper, but preserve converter routing and geometry byte-for-byte.
badnets={'12V_IN','JETSON_12V','SG4A_12V','FAN_12V','USB_12V'}
for tag in ['segment','arc','via','zone']:
 for n in list(all_(b,tag)):
  net=one(n,'net');net=str(net[1]) if net else ''
  if net in badnets:b.remove(n);continue
  if tag in ('segment','arc'):
   points=[one(n,k) for k in ('start','mid','end') if one(n,k)]
   if any(float(p[1])<64 for p in points) or (net=='FUSED_BOOST_12V' and any(float(p[2])<48 for p in points)):b.remove(n)
  elif tag=='via' and (float(one(n,'at')[1])<64 or float(one(n,'at')[2])<10 or float(one(n,'at')[2])>110):b.remove(n)
  elif tag=='zone':
   n[:]=[x for x in n if not(isinstance(x,list) and x[0] in ('filled_polygon','fill_segments'))]
   poly=one(n,'polygon');pts=all_(one(poly,'pts'),'xy') if poly else []
   if pts and min(float(p[1]) for p in pts)<64:
    if net!='GND':raise ValueError('Unexpected wide non-ground zone')
    set_(n,'polygon',parse('(polygon (pts (xy 64.5 10.5) (xy 169.5 10.5) (xy 169.5 109.5) (xy 64.5 109.5)))'))
# New keyed input connector from the reviewed D4 footprint.
j=copy.deepcopy(oldfps['J2']);prop(j,'Reference')[2]=Q('J1');prop(j,'Value')[2]=Q('12V FROM MAIN');set_(j,'at',['at','72','37']);set_(j,'uuid',['uuid',Q(uid('D5/POE/J1'))])
for pad_ in all_(j,'pad'):
 if str(pad_[1]) in ('1','2'):set_(pad_,'net',['net',Q('FUSED_BOOST_12V' if str(pad_[1])=='1' else 'GND')])
b.append(j)
parts.insert(0,part('J1','12V FROM MAIN',str(j[1]),{'1':('+12V','12V_IN'),'2':('RETURN','GND')},(72,37),'B2P-VH(LF)(SN)'))
# Four M3 mounting holes, independent from the original enclosure geometry.
holelib=parse((LIB/'MountingHole.pretty/MountingHole_3.2mm_M3.kicad_mod').read_text());holelib[1]=Q('MountingHole_3.2mm_M3');write(local/'MountingHole_3.2mm_M3.kicad_mod',holelib)
for i,(x,y) in enumerate([(69,15),(165,15),(69,105),(165,105)],1):
 f=copy.deepcopy(holelib);f[1]=Q('UMI_D2:MountingHole_3.2mm_M3');set_(f,'at',['at',str(x),str(y)]);set_(f,'uuid',['uuid',Q(uid('D5/POE/H'+str(i)))]);prop(f,'Reference')[2]=Q('H'+str(i));prop(f,'Value')[2]=Q('MountingHole_3.2mm_M3');set_(f,'attr',['attr','exclude_from_pos_files','exclude_from_bom']);b.append(f)
 parts.append(part('H'+str(i),'MountingHole_3.2mm_M3',str(f[1]),{},(x,y),'MECHANICAL'))
# Net rename is intentional: this input is already fused on MAIN.
def rename(node):
 if not isinstance(node,list):return
 if node and node[0]=='net' and len(node)>1 and str(node[1])=='FUSED_BOOST_12V':node[1]=Q('12V_IN')
 for a in node:
  if isinstance(a,list):rename(a)
rename(b)
for p in parts:
 for pn,pair in p['pins'].items():
  if pair[1]=='FUSED_BOOST_12V':p['pins'][pn]=[pair[0],'12V_IN']
 f=next(f for f in all_(b,'footprint') if str(prop(f,'Reference')[2])==p['ref']);p['pos']=list(map(float,one(f,'at')[1:3]));p['fp']=str(f[1])
 # D4 actual MPN and value are authoritative for recent sourcing edits.
 if not p['ref'].startswith('H'):
  p['value']=str(prop(f,'Value')[2]);mpn=prop(f,'MPN');p['mpn']=str(mpn[2]) if mpn else p['mpn']
# New low-frequency input route joins the existing validated input filter at (70,48).
for layer in ['F.Cu','B.Cu']:
 for idx,(a,z) in enumerate(zip([(72,37),(72,46),(70,48)],[(72,46),(70,48),(70,52)])):
  b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width 2) (layer "{layer}") (net "12V_IN") (uuid "{uid("D5/POE/input/"+layer+str(idx))}"))'))
# On the back layer connect the added input conductor to its existing via corridor.
b.append(parse(f'(segment (start 70 52) (end 70 58) (width 1.5) (layer "B.Cu") (net "12V_IN") (uuid "{uid("D5/POE/input/backjoin")}"))'))
b.append(parse(f'(segment (start 70 58) (end 67.5 60.5) (width 1.5) (layer "B.Cu") (net "12V_IN") (uuid "{uid("D5/POE/input/backjoin2")}"))'))
def line(a,z,layer='F.SilkS',w=.2):b.append(parse(f'(gr_line (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (stroke (width {w}) (type solid)) (layer "{layer}") (uuid "{uid("D5/POE/line/"+str(a)+str(z)+layer)}"))'))
def text(s,x,y,size=1.2,layer='F.SilkS',left=False):
 just='(justify left)' if left else ''
 b.append(parse(f'(gr_text {q(s)} (at {x} {y}) (layer "{layer}") (uuid "{uid("D5/POE/text/"+s+str(x)+str(y))}") (effects (font (size {size} {size}) (thickness .18)) {just}))'))
x0,y0,x1,y1,r=64,10,170,110,3
for a,z in [((x0+r,y0),(x1-r,y0)),((x1,y0+r),(x1,y1-r)),((x1-r,y1),(x0+r,y1)),((x0,y1-r),(x0,y0+r))]:line(a,z,'Edge.Cuts',.05)
for cx,cy,ang in [(x1-r,y0+r,-90),(x1-r,y1-r,0),(x0+r,y1-r,90),(x0+r,y0+r,180)]:
 pts=[(cx+r*math.cos(math.radians(t)),cy+r*math.sin(math.radians(t))) for t in (ang,ang+45,ang+90)]
 b.append(parse(f'(gr_arc (start {pts[0][0]} {pts[0][1]}) (mid {pts[1][0]} {pts[1][1]}) (end {pts[2][0]} {pts[2][1]}) (stroke (width .05) (type solid)) (layer "Edge.Cuts") (uuid "{uid("D5/POE/corner/"+str(ang))}"))'))
text('UMI / POE POWER',94,88,2);text('D5  |  PROTOTYPE',94,91.5,1.2);line((72,94),(123,94))
text('12V IN  >  53.5V / 1.31A OUT',94,97,1.1);text('INPUT FUSE ON MAIN BOARD',94,100,1.1);text('PIN 1 +12V   /   PIN 2 GND',81,30,1.0)
text('J1 / 12V FROM MAIN',81,27,1.2);text('+',72,33,1.2);text('GND',77,33,1)
text('J6 / ETHERNET SWITCH',150,107,1.1);text('F6 / 3A 80V DC',149,77,1.2)
text('+53.5V',141,97,1);text('GND',154,97,1)
for ref,x,y in [('U1',123,64),('U2',79,69),('L1',113,15),('Q1',121,37),('Q2',139,49),('Q3',121,49),('C19',92.6,52),('C20',160.7,52)]:text(ref,x,y,1)
# Schematic references remain unchanged for traceability; new root/path isolates this board.
root=symbol_schematic(NAME,parts,D);package_schematic(D/(NAME+'.kicad_sch'),['12V_IN','IC_VIN'])
sch=parse((D/(NAME+'.kicad_sch')).read_text());set_(sch,'paper',['paper',Q('A0'),'portrait']);set_(sch,'title_block',parse('(title_block (title "UMI PoE supply - 12V to 53.5V") (rev "D5 PROTOTYPE"))'));write(D/(NAME+'.kicad_sch'),sch)
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);set_(f,'path',['path',Q('/'+root+'/'+uid(NAME+'/'+ref))]);f[:]=[n for n in f if not(isinstance(n,list) and n[0]=='sheetname')];set_(f,'sheetfile',['sheetfile',Q(NAME+'.kicad_sch')])
 p=next(p for p in parts if p['ref']==ref)
 if not prop(f,'MPN'):f.append(parse(f'(property "MPN" {q(p["mpn"])} (at 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness .15))))'))
 else:prop(f,'MPN')[2]=Q(p['mpn'])
 for pr in all_(f,'property'):
  if pr[1] in ('Reference','Value'):set_(pr,'hide',['hide','yes'])
set_(one(b,'setup'),'aux_axis_origin',['aux_axis_origin','64','110']);set_(b,'title_block',parse('(title_block (title "UMI PoE power converter") (rev "D5 PROTOTYPE"))'))
# Remove exact duplicated conductor segments introduced at the input junction.
seen=set()
for seg in list(all_(b,'segment')):
 key=(str(one(seg,'net')[1]),str(one(seg,'layer')[1]),float(one(seg,'width')[1]),tuple(sorted([tuple(map(float,one(seg,k)[1:3])) for k in ('start','end')])))
 if key in seen:b.remove(seg)
 else:seen.add(key)
write(D/(NAME+'.kicad_pcb'),b)
project=json.loads((SRC/'MAIN_POWER.kicad_pro').read_text());project.get('meta',{})['filename']=NAME+'.kicad_pro';(D/(NAME+'.kicad_pro')).write_text(json.dumps(project,indent=2))
(D/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "UMI_D2") (type "KiCad") (uri "${KIPRJMOD}/UMI_D2.pretty") (options "") (descr "Self contained verified footprints")))')
(D/'design.json').write_text(json.dumps(parts,indent=2))
report={'source':'UMI_D4/MAIN_POWER','outline_mm':[106,100],'stackup':'4 layers;1.2mm;2oz outer/1oz inner','removed_refs':sorted(removed),'retained_refs':[p['ref'] for p in parts],'input':'J1 pin1+12V pin2GND; upstream MAIN F5 protects cable','output':'F6 3A80V DC;J6 pad1+53.5V pad3GND, pad2unused','validation':'SOURCE ONLY, awaiting zone refill and native ERC/DRC/parity','critical_geometry':'Existing converter/eFuse placement and copper retained; distribution removed,inputrouting added,newgroundboundaries'}
(D/'EXTRACTION_REPORT.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
