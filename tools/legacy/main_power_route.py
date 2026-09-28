"""Main low-voltage distribution routes; incomplete boost/return routing, not fabrication release."""
from design_d2 import *
import sys
sys.path.insert(0,str(BASE/'work/geometry_lib'))
from shapely.geometry import box,Polygon,LineString,Point
D=OUT/'MAIN_POWER';path=D/'MAIN_POWER.kicad_pcb';b=parse(path.read_text())
codes={str(a[2]):str(a[1]) for a in all_(b,'net')};pads=[];lookup={}
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);ox,oy=map(float,one(f,'at')[1:3])
 for p in all_(f,'pad'):
  layers=[str(v) for v in one(p,'layers')[1:]]
  if not any(v.endswith('.Cu') for v in layers):continue
  x,y=map(float,one(p,'at')[1:3]);x+=ox;y+=oy;w,h=map(float,one(p,'size')[1:3]);n=one(p,'net');net=str(n[2]) if n else None
  shape=box(x-w/2,y-h/2,x+w/2,y+h/2)
  if p[3]=='circle':shape=Point(x,y).buffer(w/2)
  if p[3]=='custom':
   for g in one(p,'primitives')[1:]:
    if g[0]=='gr_poly':shape=shape.union(Polygon([(x+float(v[1]),y+float(v[2])) for v in one(g,'pts')[1:]]))
  pads.append((ref+'.'+str(p[1]),net,shape,layers))
  lookup[(ref,str(p[1]))]=(x,y)
def at(ref,pin):return lookup[(ref,str(pin))]
routes=[]
for layer in ['F.Cu','B.Cu']:
 routes.extend([('12V_IN',6,[(45.98,24.96),(15,24.96),(15,65.5)],layer),('12V_IN',6,[(38,24.96),(38,40),(46,40),(46,65.5)],layer),('12V_IN',6,[(46,40),(72,40),(72,47.5)],layer)])
 for x,y in [(17,45),(50,45),(17,63),(50,63),(72,45)]:
  busx=15 if x==17 else 72 if x==72 else 46
  routes.extend([('12V_IN',2,[(busx,y),(x+3.5,y),(x+3.5,y+2.5),(x,y+2.5),(x,y)],layer)])
for net,x,y,jx,jy,w in [('JETSON_12V',26.3,45,21,55,2.5),('SG4A_12V',59.3,45,54,55,2.5),('FAN_12V',26.3,63,21,73,1),('USB_12V',59.3,63,54,73,2.5)]:
 routes.extend([(net,2,[(x,y),(x+3.5,y),(x+3.5,y+2.5),(x,y+2.5),(x,y)],'F.Cu'),(net,w,[(x,y+2.5),(jx,jy-2.2),(jx,jy)],'F.Cu')])
def route(net,width,pts,layer='F.Cu'):routes.append((net,width,pts,layer))
vias=[]
def via(net,x,y,size=.7,drill=.35):vias.append((net,x,y,size,drill));return(x,y)
# Local eFuse controls and low-inductance input/output pad fanout.
route('FUSED_BOOST_12V',2,[(81.3,45),(84.8,45),(84.8,47.5),(81.3,47.5),(81.3,45)])
route('FUSED_BOOST_12V',1.2,[(81.3,47.5),(78,50.5),(74.5,50.5),(74.5,53),at('C21',1)])
route('FUSED_BOOST_12V',.8,[at('C21',1),(75.025,58.65),(76.6,58.65),at('U2',1)])
route('FUSED_BOOST_12V',1,[at('C21',1),(75.025,50.5),(80.175,50.5),at('C22',1)])
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
for ref,x,y in [('R24',76.825,66.2),('R25',81.825,66.2),('C23',86.7,60),('C21',77.75,53),('C22',83,53)]:route('GND',.3,[at(ref,2),via('GND',x,y)])
route('BOOST_IN',.3,[at('U2',17),(81.75,59.25),(81.75,57.3)])
route('BOOST_IN',.3,[at('U2',18),(81.75,58.75)])
for n in range(19,25):route('BOOST_IN',.3,[at('U2',n),(at('U2',n)[0],56.8)])
route('BOOST_IN',1.2,[(77.75,56.8),(81.75,56.8),(81.75,57.3)])
route('BOOST_IN',2,[(81.75,56.8),at('D4',3),(94,56.04)])
for yy in (55,56,57):
 v=via('BOOST_IN',94,yy);route('BOOST_IN',1,[v,(94,56.04)])
route('BOOST_IN',2,[(94,56),(97.5,56),(97.5,48)],'B.Cu')
route('BOOST_IN',1.5,[(97.5,48),(88.5,46),(81.5,23)],'B.Cu')
for ref,vx,vy in [('C19',81.5,23),('C2',87.5,36),('C4',87.5,41),('C3',88.5,46),('R2',97.5,48)]:
 route('BOOST_IN',1.2,[at(ref,1),via('BOOST_IN',vx,vy)])
for yy in (47,49):
 route('BOOST_IN',1,[via('BOOST_IN',97.5,yy,.8,.4),(97.5,48)])
 route('BOOST_IN',1,[(97.5,yy),(97.5,48)],'B.Cu')
route('BOOST_IN',1.5,[(87.5,36),(87.5,41),(88.5,46)],'B.Cu')
route('SENSE_LOW',2.5,[at('R2',2),at('L1',1)])
for ref,x,y in [('D4',88.96,50.9),('D4',91.04,50.9)]:
 pin=1 if x==88.96 else 2;route('GND',.8,[at(ref,pin),via('GND',x,y)])
for ref,x,y in [('C19',94.5,23),('C2',95,36),('C4',95,41),('C3',95,46)]:route('GND',.8,[at(ref,2),via('GND',x,y)])
route('UVLO',.2,[at('U2',13),(82.5,61.25),via('UVLO',82.5,62.3)])
route('UVLO',.2,[(82.5,62.3),(100,79),(108.825,82)],'B.Cu')
route('UVLO',.2,[at('R10',2),via('UVLO',108.825,82)])
errors=[];shapes=[]
for i,(net,width,pts,layer) in enumerate(routes):
 shape=LineString(pts).buffer(width/2)
 if not box(10.5,10.5,167.5,109.763962).covers(shape):errors.append('Route '+str(i)+' crosses edge margin')
 for name,pnet,pshape,players in pads:
  if layer not in players and '*.Cu' not in players:continue
  if net!=pnet and shape.distance(pshape)<.2-1e-5:errors.append(f'{net} route {i} too close to {name}: {shape.distance(pshape):.3f} mm')
 for onet,oshape,olayer in shapes:
  if layer==olayer and net!=onet and shape.distance(oshape)<.2-1e-5:errors.append(f'{net} route {i} too close to {onet}')
 shapes.append((net,shape,layer))
for net,x,y,size,drill in vias:
 shape=Point(x,y).buffer(size/2)
 for name,pnet,pshape,players in pads:
  if pnet!=net and shape.distance(pshape)<.2-1e-5:errors.append(f'{net} via{x,y} too close to {name}')
 for onet,oshape,olayer in shapes:
  if onet!=net and shape.distance(oshape)<.2-1e-5:errors.append(f'{net} via{x,y} too close to {onet} route')
if errors:raise SystemExit('\n'.join(errors))
b[:]=[a for a in b if not(isinstance(a,list) and a[0] in ('segment','zone','via'))]
for i,(net,width,pts,layer) in enumerate(routes):
 for j,(s,e) in enumerate(zip(pts,pts[1:])):
  b.append(parse(f'(segment (start {s[0]} {s[1]}) (end {e[0]} {e[1]}) (width {width}) (layer "{layer}") (net {codes[net]}) (uuid "{uid("main/distribution/"+str(i)+"/"+str(j))}"))'))
for i,(net,x,y,size,drill) in enumerate(vias):b.append(parse(f'(via (at {x} {y}) (size {size}) (drill {drill}) (layers "F.Cu" "B.Cu") (net {codes[net]}) (uuid "{uid("main/input-via/"+str(i))}"))'))
for layer in ['In1.Cu','In2.Cu']:
 b.append(parse(f'(zone (net {codes["GND"]}) (net_name "GND") (layer "{layer}") (uuid "{uid("main/ground-plane/"+layer)}") (hatch edge .5) (connect_pads (clearance .3)) (min_thickness .25) (fill yes (thermal_gap .4) (thermal_bridge_width .7)) (polygon (pts (xy 10.5 10.5) (xy 167.5 10.5) (xy 167.5 109.763962) (xy 10.5 109.763962))))'))
write(path,b)
(D/'distribution_route_screen.json').write_text(json.dumps(dict(scope='Conservative pad bounding shapes versus proposed distribution tracks; not KiCad DRC. No current/thermal approval implied.',segments=len(all_(b,'segment')),ground_zones=2,zones_require_KiCad_refill=True,clearance_screen_mm=.2,errors=errors,boost_routing_complete=False,ground_routing_complete=False),indent=2))
print('Distribution tracks:',len(all_(b,'segment')),'; conservative geometric clearance screen passed; boost and return routing incomplete.')


