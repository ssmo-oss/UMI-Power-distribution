"""D3 presentation and distribution cleanup on the checked delivered board."""
from design_d2 import *
import shutil,math
src=BASE/'outputs/UMI_TWO_BOARD_DESIGN/MAIN_POWER';dst=BASE/'outputs/UMI_D3/MAIN_POWER';dst.mkdir(parents=True,exist_ok=True)
for name in ('MAIN_POWER.kicad_pcb','MAIN_POWER.kicad_sch','MAIN_POWER.kicad_pro','UMI.kicad_sym','sym-lib-table','fp-lib-table','design.json','pin_schedule.csv','BOM_by_reference.csv','BOM_grouped.csv'):
 shutil.copy2(src/name,dst/name)
shutil.copytree(src/'UMI_D2.pretty',dst/'UMI_D2.pretty',dirs_exist_ok=True)
b=parse((dst/'MAIN_POWER.kicad_pcb').read_text())
def text(s,x,y,size=1.2,thick=.18,justify='left',layer='F.SilkS'):
 just='' if justify=='center' else f'(justify {justify})'
 b.append(parse(f'(gr_text {q(s)} (at {x} {y}) (layer "{layer}") (uuid "{uid("main-d3/text/"+s+str(x)+str(y))}") (effects (font (size {size} {size}) (thickness {thick})) {just}))'))
def line(a,z,layer='F.SilkS',w=.2):
 b.append(parse(f'(gr_line (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (stroke (width {w}) (type solid)) (layer "{layer}") (uuid "{uid("main-d3/line/"+str(a)+str(z)+layer)}"))'))
# Clear obsolete free-standing labels; the original reviewed copper and symbols remain.
b[:]=[n for n in b if not(isinstance(n,list) and n[0]=='gr_text')]
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);r=prop(f,'Reference');v=prop(f,'Value')
 if v:set_(v,'hide',['hide','yes'])
 if r:
  set_(r,'layer',['layer',Q('F.Fab')]);set_(r,'hide',['hide','yes'])
 # Restore engineering references in a clean assembly layer, without values.
 ox,oy=map(float,one(f,'at')[1:3])
 text(ref,ox,oy,.8,.12,'left','F.Fab')
# Rounded outline; retain all original hole centres and maximum dimensions.
b[:]=[n for n in b if not(isinstance(n,list) and n[0].startswith('gr_') and one(n,'layer') and one(n,'layer')[1]=='Edge.Cuts')]
x0,y0,x1,y1,r=10,10,168,110.263962,3
for a,z in [((x0+r,y0),(x1-r,y0)),((x1,y0+r),(x1,y1-r)),((x1-r,y1),(x0+r,y1)),((x0,y1-r),(x0,y0+r))]:line(a,z,'Edge.Cuts',.05)
for cx,cy,ang in [(x1-r,y0+r,-90),(x1-r,y1-r,0),(x0+r,y1-r,90),(x0+r,y0+r,180)]:
 p=[(cx+r*math.cos(math.radians(t)),cy+r*math.sin(math.radians(t))) for t in (ang,ang+45,ang+90)]
 b.append(parse(f'(gr_arc (start {p[0][0]} {p[0][1]}) (mid {p[1][0]} {p[1][1]}) (end {p[2][0]} {p[2][1]}) (stroke (width .05) (type solid)) (layer "Edge.Cuts") (uuid "{uid("main-d3/corner/"+str(ang))}"))'))
# Chamfer the broad, noncritical 12-V distribution trunks consistently.
netnames={str(n[1]):str(n[2]) for n in all_(b,'net')}
for seg in list(all_(b,'segment')):
 if netnames.get(str(one(seg,'net')[1]),str(one(seg,'net')[1]))!='12V_IN' or float(one(seg,'width')[1])!=6:continue
 s=tuple(map(float,one(seg,'start')[1:3]));e=tuple(map(float,one(seg,'end')[1:3]));points=None
 if s==(45.98,24.96) and e==(15.,24.96):points=[s,(18,24.96),(15,27.96)]
 elif s==(15.,24.96) and e==(15.,65.5):points=[(15,27.96),e]
 elif s==(38.,24.96) and e==(38.,40.):points=[s,(38,37),(41,40)]
 elif s==(38.,40.) and e==(46.,40.):points=[(41,40),(43,40),(46,43)]
 elif s==(46.,40.) and e==(46.,65.5):points=[(46,43),e]
 if points:
  b.remove(seg)
  for j,(a,z) in enumerate(zip(points,points[1:])):
   c=copy.deepcopy(seg);set_(c,'start',['start',*map(str,a)]);set_(c,'end',['end',*map(str,z)]);set_(c,'uuid',['uuid',Q(uid('main-d3/chamfer/'+str(one(seg,'uuid')[1])+'/'+str(j)))]);b.append(c)
# Ordered 45-degree approaches outside the converter cell, retaining widths.
paths={
 ('53V5_RAW',(160.684,40.939999),(164.5,40.94)):[(160.684,40.939999),(162.5,40.94),(164.5,42.94)],
 ('53V5_RAW',(164.5,40.94),(164.5,83.)):[(164.5,42.94),(164.5,80),(161.5,83)],
 ('53V5_RAW',(164.5,83.),(146.,83.)):[(161.5,83),(149,83),(146,86)],
 ('53V5_RAW',(146.,83.),(149.5,91.5)):[(146,86),(146,89)],
 ('SWITCH_53V5',(155.3,91.5),(155.3,97.)):[(155.3,91.5),(155.3,95),(153.3,97)],
 ('SWITCH_53V5',(155.3,97.),(144.,97.)):[(153.3,97),(146,97),(144,99)],
 ('SWITCH_53V5',(144.,97.),(144.,101.)):[(144,99),(144,101)],
 ('FUSED_BOOST_12V',(75.3,32.5),(72.,40.)):[(75.3,32.5),(72,35.8),(72,40)],
 ('FUSED_BOOST_12V',(72.,40.),(70.,48.)):[(72,40),(72,46),(70,48)],
 ('FUSED_BOOST_12V',(67.5,70.),(73.5,54.5)):[(67.5,70),(67.5,60.5),(73.5,54.5)],
 ('FUSED_BOOST_12V',(73.5,54.5),(76.4,58.75)):[(73.5,54.5),(73.5,55.85),(76.4,58.75)],
 ('UVLO',(82.5,62.3),(85.,81.)):[(82.5,62.3),(82.5,78.5),(85,81)],
 ('UVLO',(85.,81.),(141.,81.)):[(85,81),(138.5,81),(141,78.5)],
 ('UVLO',(141.,81.),(141.,70.4)):[(141,78.5),(141,72.9),(138.5,70.4)],
 ('UVLO',(141.,70.4),(131.609,70.4)):[(138.5,70.4),(131.609,70.4)]}
for seg in list(all_(b,'segment')):
 s=tuple(map(float,one(seg,'start')[1:3]));e=tuple(map(float,one(seg,'end')[1:3]));net=str(one(seg,'net')[1]);points=paths.get((net,s,e))
 if points:
  b.remove(seg)
  for j,(a,z) in enumerate(zip(points,points[1:])):
   c=copy.deepcopy(seg);set_(c,'start',['start',*map(str,a)]);set_(c,'end',['end',*map(str,z)]);set_(c,'uuid',['uuid',Q(uid('main-d3/approach/'+str(one(seg,'uuid')[1])+'/'+str(j)))]);b.append(c)
# Service-facing silkscreen: every replaceable fuse and plug has a clear function.
text('UMI',15,85,3,.45);text('MAIN POWER',27,85,2.2,.33)
line((15,88),(77,88),w=.3)
text('12V DISTRIBUTION  /  53.5V BOOST',15,91,1.2,.18)
text('REV D3  |  ENGINEERING PROTOTYPE',15,94,1,.15)
text('DC INPUT ONLY',15,97,1,.15)
text('J1  INPUT 12V DC',39,16,1.2,.18)
text('+12V',41,21.1,1,.15);text('GND',61.5,36.2,1,.15)
for a,z in [((39,23),(59.32,23)),((59.32,23),(59.32,41.7)),((59.32,41.7),(39,41.7)),((39,41.7),(39,23))]:line(a,z,w=.15)
text('F5  BOOST INPUT / 10A',66,26,1,.15)
for x,y,f,j,name,rating in [(17,45,'F1','J2','JETSON','7.5A'),(50,45,'F2','J3','SG4A','7.5A'),(17,63,'F3','J4','FAN','1A'),(50,63,'F4','J5','USB BOARD','5A')]:
 text(f+'  '+rating,x+17.5,y,1.1,.16)
 text(j+'  '+name,x+12,y+10,1.1,.16)
 text('+',x+4,y+6.8,1.2,.18,'center');text('-',x+7.96,y+6.8,1.2,.18,'center')
text('53.5V BOOST CONVERTER',108,15,1.3,.2)
text('F6  SWITCH OUTPUT / 3A',141,86,1.1,.16)
text('J6  ETHERNET SWITCH',143,107,1.1,.16)
for s,x in [('+',144),('NC',147.96),('-',151.92)]:text(s,x,98.2,1,.15,'center')
text('53.5V / 1.31A',138,94.4,1.1,.16)
text('U2  INPUT PROTECTION',66,79,1,.15)
# A readable circuit key occupies spare space without separating critical copper.
text('POWER STAGE',91,87,1.3,.2)
text('L1  10uH BOOST INDUCTOR',91,90,1,.15)
text('Q1  SYNCHRONOUS RECTIFIER',91,93,1,.15)
text('Q2 / Q3  LOW-SIDE SWITCHES',91,96,1,.15)
text('U1  LM5122 CONTROLLER',91,99,1,.15)
text('C19  INPUT   /   C20  OUTPUT',91,102,1,.15)
for ref,x,y in [('L1',99,37),('Q1',130,41),('Q2',139,51),('Q3',119,52),('U1',121,65),('U2',82.8,64),('C19',89,37.5),('C20',157.5,37.5)]:text(ref,x,y,1,.15)
write(dst/'MAIN_POWER.kicad_pcb',b)
(dst/'D3_CHANGES.md').write_text('''# D3 main-board refinement

Based on the saved, checked D2 board. The TI converter component placement, current loops, protection circuit and original mounting holes are retained. This revision adds service labels, fuse values, plug polarity, a component key, consistent distribution-bus chamfers and 3 mm corner radii. Dense SMT values are hidden in the assembly view.

Native electrical/geometry checks and manufacturing exports must be regenerated for this revision. This is an engineering prototype, not a tested production design.
''')
print(dst)



