"""Merge distribution/eFuse routes with preserved reference converter copper."""
from design_d2 import *
D=OUT/'MAIN_POWER';path=D/'MAIN_POWER.kicad_pcb';b=parse(path.read_text());codes={str(a[2]):str(a[1]) for a in all_(b,'net')};lookup={}
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);ox,oy=map(float,one(f,'at')[1:3])
 for p in all_(f,'pad'):
  x,y=map(float,one(p,'at')[1:3]);lookup[(ref,str(p[1]))]=(x+ox,y+oy)
def at(ref,pin):return lookup[(ref,str(pin))]
routes=[];vias=[]
def route(net,w,points,layer='F.Cu'):routes.append((net,w,points,layer))
def via(net,x,y,size=.7,drill=.35):vias.append((net,x,y,size,drill));return(x,y)
for layer in ('F.Cu','B.Cu'):
 route('12V_IN',6,[(45.98,24.96),(15,24.96),(15,65.5)],layer)
 route('12V_IN',6,[(38,24.96),(38,40),(46,40),(46,65.5)],layer)
 route('12V_IN',6,[(46,24.96),(66,24.96),(66,30)],layer)
 for x,y in [(17,45),(50,45),(17,63),(50,63),(66,30)]:
  busx=15 if x==17 else 66 if x==66 else 46
  route('12V_IN',2,[(busx,y),(x+3.5,y),(x+3.5,y+2.5),(x,y+2.5),(x,y)],layer)
for net,x,y,jx,jy,w in [('JETSON_12V',26.3,45,21,55,2.5),('SG4A_12V',59.3,45,54,55,2.5),('FAN_12V',26.3,63,21,73,1),('USB_12V',59.3,63,54,73,2.5)]:
 route(net,2,[(x,y),(x+3.5,y),(x+3.5,y+2.5),(x,y+2.5),(x,y)])
 route(net,w,[(x,y+2.5),(jx,jy-2.2),(jx,jy)])
route('FUSED_BOOST_12V',2,[(75.3,30),(78.8,30),(78.8,32.5),(75.3,32.5),(75.3,30)])
route('FUSED_BOOST_12V',2,[(75.3,32.5),(72,40),(70,48),(70,52),at('C21',1)])
route('FUSED_BOOST_12V',.8,[at('C21',1),at('C22',1)])
route('FUSED_BOOST_12V',.8,[at('C21',1),(72.05,54),(75.025,54),(75.025,58.65),(76.6,58.65),at('U2',1)])
route('FUSED_BOOST_12V',.3,[at('U2',1),at('U2',2),at('U2',3)])
for n in (1,2,3):route('FUSED_BOOST_12V',.3,[at('U2',n),(78.2,at('U2',n)[1])])
route('FUSED_BOOST_12V',.3,[(80,59.75),at('U2',16)])
route('FUSED_BOOST_12V',.25,[(75.025,54.5),(71,54.5),(71,57),at('R22',1)])
route('FUSED_BOOST_12V',.8,[at('D3',1),via('FUSED_BOOST_12V',67.5,70,.8,.4)])
route('FUSED_BOOST_12V',1.5,[(67.5,70),via('FUSED_BOOST_12V',73.5,54.5,.8,.4)],'B.Cu')
route('FUSED_BOOST_12V',1.2,[(73.5,54.5),via('FUSED_BOOST_12V',76.4,58.75,.7,.35)],'B.Cu')
route('GND',.8,[at('D3',2),via('GND',76.5,70,.8,.4)])
route('EFUSE_EN',.2,[at('R22',2),at('R23',1)])
route('EFUSE_EN',.2,[at('R23',1),(73.825,61.25),at('U2',6)])
route('EFUSE_ILIM',.2,[at('U2',8),(78.25,62.8),at('R24',1)])
route('EFUSE_IMON',.2,[at('U2',9),(78.75,62.3),(79.3,62.85),(79.3,64.125),at('R25',1)])
route('EFUSE_DVDT',.2,[at('U2',15),(82.25,60.25),(83,60),at('C23',1)])
route('GND',.25,[at('U2',4),(76.5,60.25),(76.5,60.75),at('U2',5),(78.2,60.75)])
route('GND',.25,[at('R23',2),(75.475,60.75),(76.5,60.75)])
for n in (10,12):route('GND',.25,[at('U2',n),(at('U2',n)[0],60.925)])
route('GND',.25,[at('U2',14),(80,60.75)])
route('GND',.25,[(76.5,60.25),via('GND',76.25,60.2)])
for ref,x,y in [('R24',76.825,66.2),('R25',81.825,66.2),('C23',88,60),('C21',75,52),('C22',75,49)]:route('GND',.3,[at(ref,2),via('GND',x,y)])
route('BOOST_IN',.3,[at('U2',17),(81.75,59.25),(81.75,57.3)])
route('BOOST_IN',.3,[at('U2',18),(81.75,58.75)])
for n in range(19,25):route('BOOST_IN',.3,[at('U2',n),(at('U2',n)[0],56.8)])
route('BOOST_IN',1.2,[(77.75,56.8),(81.75,56.8),(81.75,57.3)])
route('BOOST_IN',2,[at('D4',3),(79,56.8),(81.75,56.8),(86,55),(86,40.94),at('C19',1)])
via('BOOST_IN',86.778,40.94,.8,.4)
route('GND',1,[at('C2',2),via('GND',100.24,53,.8,.4)])
route('GND',1,[at('C19',2),via('GND',94.5,49.64,.8,.4)])
for n,x in [(1,77.96),(2,80.04)]:
 route('GND',1,[at('D4',n),via('GND',x,49.5,.8,.4)])
route('UVLO',.2,[at('U2',13),(82.5,61.25),via('UVLO',82.5,62.3)])
route('UVLO',.2,[(82.5,62.3),(85,81),(141,81),(141,70.4),via('UVLO',131.609,70.4)],'B.Cu')
route('UVLO',.2,[(131.609,70.4),at('R10',1)])
route('53V5_RAW',2,[at('C20',1),(164.5,40.94),(164.5,83),(146,83),at('F6',1)])
route('53V5_RAW',2,[(146,89),(149.5,89),(149.5,91.5),(146,91.5),(146,89)])
route('SWITCH_53V5',2,[(155.3,89),(158.8,89),(158.8,91.5),(155.3,91.5),(155.3,89)])
route('SWITCH_53V5',2,[(155.3,91.5),(155.3,97),(144,97),at('J6',1)])
for i,(net,w,points,layer) in enumerate(routes):
 for j,(a,z) in enumerate(zip(points,points[1:])):
  if a==z:continue
  b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width {w}) (layer "{layer}") (net {codes[net]}) (uuid "{uid("main/merge/"+str(i)+"/"+str(j))}"))'))
for i,(net,x,y,size,drill) in enumerate(vias):b.append(parse(f'(via (at {x} {y}) (size {size}) (drill {drill}) (layers "F.Cu" "B.Cu") (net {codes[net]}) (uuid "{uid("main/merge-via/"+str(i))}"))'))
for layer in ('In1.Cu','In2.Cu','B.Cu'):
 b.append(parse(f'(zone (net {codes["GND"]}) (net_name "GND") (layer "{layer}") (uuid "{uid("main/full-ground/"+layer)}") (hatch edge .5) (priority 1) (connect_pads yes (clearance .3)) (min_thickness .25) (fill yes (thermal_gap .4) (thermal_bridge_width .7)) (polygon (pts (xy 10.5 10.5) (xy 167.5 10.5) (xy 167.5 109.763962) (xy 10.5 109.763962))))'))
write(path,b)
print('Merged',len(all_(b,'segment')),'tracks',len(all_(b,'via')),'vias')
