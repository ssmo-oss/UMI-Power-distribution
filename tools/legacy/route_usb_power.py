"""Explicit USB copper construction with independent geometric screening.

This produces development copper, not fabrication exports. KiCad refill and DRC
are required separately. The generated board is reproducible from the builder.
"""
from design_d2 import *
import sys,math
sys.path.insert(0,str(BASE/'work/geometry_lib'))
from shapely.geometry import box,Polygon,LineString,Point
d=OUT/'USB_POWER';path=d/'USB_POWER.kicad_pcb';b=parse(path.read_text())
b[:]=[a for a in b if not(isinstance(a,list) and a[0] in ('segment','via','zone'))]
netcodes={str(a[2]):str(a[1]) for a in all_(b,'net')}
pads=[];lookup={};routes=[];vias=[];errors=[]
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);ox,oy=map(float,one(f,'at')[1:3]);halfturn=len(one(f,'at'))>3 and float(one(f,'at')[3])%360==180
 for p in all_(f,'pad'):
  if not any(str(v).endswith('.Cu') for v in one(p,'layers')[1:]):continue
  x,y=map(float,one(p,'at')[1:3]);x=(-x if halfturn else x)+ox;y=(-y if halfturn else y)+oy;w,h=map(float,one(p,'size')[1:3]);n=one(p,'net');net=str(n[2]) if n else None
  shape=box(x-w/2,y-h/2,x+w/2,y+h/2)
  if p[3]=='circle':shape=Point(x,y).buffer(w/2)
  if p[3]=='custom':
   for g in one(p,'primitives')[1:]:
    if g[0]=='gr_poly':shape=shape.union(Polygon([(x+float(v[1]),y+float(v[2])) for v in one(g,'pts')[1:]]))
  item=dict(name=ref+'.'+str(p[1]),ref=ref,pin=str(p[1]),net=net,shape=shape,xy=(x,y),th=p[2]!='smd',w=w,h=h)
  pads.append(item);lookup[(ref,str(p[1]))]=item
def at(ref,pin):return lookup[(ref,str(pin))]['xy']
def route(net,width,points,layer='F.Cu'):
 routes.append(dict(net=net,width=width,points=points,layer=layer,shape=LineString(points).buffer(width/2)))
def via(net,xy,size=.6,drill=.3):
 if not any(v['net']==net and v['xy']==xy for v in vias):vias.append(dict(net=net,xy=xy,size=size,drill=drill,shape=Point(xy).buffer(size/2)))
def array(net,xs,ys,size=.6,drill=.3):
 for y in ys:
  for x in xs:via(net,(x,y),size,drill)
def clear(shape,net,layer='F.Cu',all_layers=False):
 for p in pads:
  if p['net']!=net and (all_layers or layer=='F.Cu' or p['th']) and shape.distance(p['shape'])<.1999:return False
 for r in routes:
  if r['net']!=net and (all_layers or r['layer']==layer) and shape.distance(r['shape'])<.1999:return False
 for v in vias:
  if v['net']!=net and shape.distance(v['shape'])<.1999:return False
 return True

# Buck feedback/bootstrap/timing control stays local on the component side.
route('BOOT',.25,[at('U1',2),at('U1',3)])
route('FB',.2,[at('R7',2),(44.05,25.725),(44.05,26.95),at('U1',8)])
route('FB',.2,[at('R1',1),(43.775,27.05),(44.05,26.95)])
route('RT',.2,[at('U1',12),(51.8,26.3),(52,26.5),at('R8',1)])
route('PG',.2,[at('U1',13),(51.75,25.65),(52.35,25.05),(56.1,25.05),(56.1,28.8),at('R9',2)])
for port,x in [(1,28),(2,71)]:
 u='U'+str(port+1);r='R'+str(port+1);fault='R'+str(port+3)
 route('ILIM'+str(port),.2,[at(u,5),(x+2.7,36.975),(x+3.675,36),at(r,1)])
 route('FAULT'+str(port),.2,[at(u,8),(x+1.45,33.5),(x+5.825,33.5),at(fault,2)])
route('RP_GATE',.25,[at('Q1',4),(29.525,20.5),(33.7,20.5),at('D1',2),at('R6',1)])

# Force fixed-frequency PWM; this uses the datasheet's stated reference limits.
via('VCC',(45.9,25.65),.45,.25);route('VCC',.2,[at('U1',6),(45.9,25.65)])
via('VCC',(51.85,24.35));route('VCC',.2,[at('U1',15),(51.85,24.35)])
route('VCC',.2,[(45.9,25.65),(45.1,25.65),(45.1,23.5),(51.85,23.5),(51.85,24.35)],'B.Cu')

# Raw 12 V reaches the reverse-polarity MOSFET on the back side.
array('12V_IN',[36.4,37.1],[15.7,16.4])
route('12V_IN',1.2,[at('Q1',5),at('Q1',8)])
route('12V_IN',1.2,[at('Q1',7),(37.1,16.365)])
route('12V_IN',1.2,[(36.4,15.7),(37.1,15.7),(37.1,16.4),(36.4,16.4)])
route('12V_IN',2,[at('J1',1),(20,12),(37.1,12),(37.1,16.4)],'B.Cu')
array('12V_PROTECTED',[27.1,27.8],[15.7,16.4])
route('12V_PROTECTED',1.2,[at('Q1',1),at('Q1',3)])
route('12V_PROTECTED',1.2,[(27.1,16.365),at('Q1',2)])
route('12V_PROTECTED',1.2,[(27.1,15.7),(27.8,15.7),(27.8,16.4),(27.1,16.4)])
route('12V_PROTECTED',.8,[at('C1',1),(44,21.75),at('U1',1)])
route('12V_PROTECTED',.8,[at('C2',1),(52,21.75),at('U1',18)])
route('12V_PROTECTED',.25,[at('U1',17),at('U1',18)])
array('12V_PROTECTED',[42.8,43.5],[20,20.7])
array('12V_PROTECTED',[52.4,53.1],[20,20.7])
route('12V_PROTECTED',.9,[(42.8,20),(43.5,20),(43.5,20.7),at('C1',1)])
route('12V_PROTECTED',.9,[(52.4,20),(53.1,20),(53.1,20.7),at('C2',1)])

# Output capacitors sit immediately beside the output lands. Parallel vias feed
# the inner 5 V plane, instead of a narrow shared 6 A trace.
route('5V_BUS',1,[at('U1',9),(45.25,29.3),at('C3',1),at('C9',1)])
route('5V_BUS',1,[at('U1',10),(50.75,29.8),at('C10',1)])
array('5V_BUS',[44.5,45.2],[33.2,33.9])
array('5V_BUS',[51,51.7],[33.2,33.9])
route('5V_BUS',1.2,[at('C3',1),(44.5,33.2),(44.5,33.9),(45.2,33.9),(45.2,33.2)])
route('5V_BUS',1.2,[at('C10',1),(51,33.2),(51,33.9),(51.7,33.9),(51.7,33.2)])
via('5V_BUS',(45.9,25),.45,.25);route('5V_BUS',.2,[at('U1',5),(45.9,25)])
# Additional biased-capacitance margin, with parallel supply/return vias.
for cap in ('C13','C14'):
 x,y=at(cap,1);array('5V_BUS',[x-.325,x+.325],[y-1.8,y-1.1]);route('5V_BUS',1.2,[(x-.325,y-1.8),(x+.325,y-1.8),(x+.325,y-1.1),(x,y)])
 x,y=at(cap,2);array('GND',[x-.325,x+.325],[y+1.6,y+2.3]);route('GND',1.2,[(x,y),(x-.325,y+1.6),(x-.325,y+2.3),(x+.325,y+2.3),(x+.325,y+1.6)])

for port,x in [(1,28),(2,71)]:
 u='U'+str(port+1);cap='C'+str(port+3);outcap='C'+str(port+5);j='J'+str(port+1);net='VBUS'+str(port)
 # Two power-input pins plus EN, and both power-output pins, are connected.
 for pin in [2,3,4]:route('5V_BUS',.35,[at(u,pin),(x-2.35,at(u,pin)[1])])
 route('5V_BUS',.65,[(x-2.35,35.675),(x-2.35,36.975)])
 route('5V_BUS',1,[(x-2.35,36.325),(x-3,35.675),(x-3,31),at(cap,1)])
 array('5V_BUS',[x-3.4,x-2.7],[30.2,30.9])
 route('5V_BUS',1,[(x-3.4,30.2),(x-2.7,30.2),(x-2.7,30.9),(x-3.4,30.9)])
 for pin in [6,7]:route(net,.35,[at(u,pin),(x+2.3,at(u,pin)[1])])
 route(net,.65,[(x+2.3,35.675),(x+2.3,36.325)])
 array(net,[x+2.5,x+3.15],[34.8,35.45])
 route(net,.8,[(x+2.5,34.8),(x+3.15,34.8),(x+3.15,35.45),(x+2.5,35.45)])
 route(net,.5,[(x+2.3,35.675),(x+2.5,35.45)])
 jx,jy=at(j,1)
 route(net,2,[(x+2.5,35.45),(jx,35.45),(jx,jy)],'B.Cu')
 # Bulk/ESD port VBUS connections will join this back-side branch.

# Thermal vias require resin fill and copper cap (VIPPO) underneath U1.
array('GND',[46.9,48,49.1],[22.75,24.25,25.75,27.25],.45,.25)
for net,xy,pin in [('GND',(45.9,26.3),7),('GND',(50.1,26.95),11),('GND',(50.1,25),14)]:
 via(net,xy,.45,.25);route(net,.2,[at('U1',pin),xy])

# Port charging-identification lines are charge-only (not a USB data link).
signal_nodes={n:[] for n in ('DM1','DP1','DM2','DP2')}
for port,ref,dx in [(1,'U5',0),(2,'U6',43)]:
 # Connector-to-array front copper makes the protection point part of the path.
 j='J'+str(port+1)
 route('DM'+str(port),.2,[at(j,2),(23.4+dx,45.9),(23.4+dx,42.55),at(ref,1)])
 route('DP'+str(port),.2,[at(j,3),(26.6375+dx,46.8625),at(ref,4)])
 for prefix,p1,p2,y in [('DM',1,6,42.55),('DP',3,4,44.45)]:
  net=prefix+str(port);route(net,.2,[at(ref,p1),at(ref,p2)])
  xy=(27.35+dx,y)
  route(net,.2,[at(ref,p2),xy]);via(net,xy);signal_nodes[net].append(xy)
 for net,pin,xy in [('DP1',1,(44.7,43.05)),('DM1',6,(49.3,43.05)),('DP2',3,(44.7,44.95)),('DM2',4,(49.3,44.95))]:
  if net.endswith(str(port)):
   route(net,.2,[at('U4',pin),xy]);via(net,xy);signal_nodes[net].append(xy)
 net='VBUS'+str(port);cap='C'+str(port+5);cx,cy=at(cap,1)
 # Short broad clamp return to the nearby port capacitor, with parallel feed vias.
 route(net,.5,[at(ref,5),at(cap,1)])
 array(net,[cx-.35,cx+.35],[cy-2.6])
 route(net,.8,[(cx-.35,cy-2.6),(cx+.35,cy-2.6),(cx,cy-2.6),at(cap,1)])
 route(net,1,[(cx,cy-2.6),(at(j,1)[0],cy-2.6)],'B.Cu')
 # Direct ground route and nearby plane via, independent of controller return.
 gxy=(25.15+dx,43.5);via('GND',gxy);route('GND',.4,[at(ref,2),gxy])

# Every remaining power/ground SMD pad gets an explicit plane connection.
# Candidates are screened against actual custom-pad polygons and routed copper.
def connect_plane(p):
 net=p['net'];x,y=p['xy']
 if p['th']:return True
 # A pad already linked to a same-net via through a local track can be skipped
 # only when a geometric union confirms a continuous connection.
 from shapely.ops import unary_union
 copper=unary_union([p['shape']]+[r['shape'] for r in routes if r['net']==net and r['layer']=='F.Cu']+[v['shape'] for v in vias if v['net']==net])
 connected=[g for g in getattr(copper,'geoms',[copper]) if g.intersects(p['shape'])]
 if any(g.intersects(v['shape']) for g in connected for v in vias if v['net']==net):return True
 candidates=[]
 for radius in [.7,1,1.4,1.8,2.3,2.8]:
  for angle in range(0,360,45):
   candidates.append((round(x+radius*math.cos(math.radians(angle)),3),round(y+radius*math.sin(math.radians(angle)),3)))
 for pos in candidates:
  if not(10.8<pos[0]<89.2 and 10.8<pos[1]<59.2):continue
  if net=='12V_PROTECTED' and not(pos[1]<22.95):continue
  if net=='5V_BUS' and not(pos[1]>24.2):continue
  vs=Point(pos).buffer(.3);ts=LineString([(x,y),pos]).buffer(.15)
  if clear(vs,net,all_layers=True) and clear(ts,net):
   via(net,pos);route(net,.3,[(x,y),pos]);return True
 return False
unconnected_plane=[]
for p in pads:
 if p['net'] in ('GND','5V_BUS','12V_PROTECTED') and not connect_plane(p):unconnected_plane.append(p['name'])

# Grid routing is confined to low-current back-side charge/ESD connections.
# Main power paths above remain explicitly sized and placed.
import heapq,itertools
from shapely.ops import unary_union
from shapely.prepared import prep
def back_route(net,a,z,width=.2,layer='B.Cu'):
 obstacles=[p['shape'] for p in pads if (p['th'] or layer=='F.Cu') and p['net']!=net]
 obstacles += [v['shape'] for v in vias if v['net']!=net]
 obstacles += [r['shape'] for r in routes if r['layer']==layer and r['net']!=net]
 forbidden=prep(unary_union(obstacles).buffer(.2+width/2+.04))
 step=.05;start=tuple(round(v/step) for v in a);goal=tuple(round(v/step) for v in z)
 def point(n):return (round(n[0]*step,5),round(n[1]*step,5))
 cache={}
 def available(n):
  if n not in cache:
   x,y=point(n);cache[n]=11<x<89 and 11<y<59 and not forbidden.intersects(Point(x,y))
  return cache[n]
 if not available(start) or not available(goal):raise RuntimeError(f'{net}: blocked route endpoint {a} {z}')
 def h(n):
  dx=abs(n[0]-goal[0]);dy=abs(n[1]-goal[1]);return max(dx,dy)+.41421356237*min(dx,dy)
 heap=[(h(start),0,start)];cost={start:0};parent={};finished=False
 while heap:
  _,g,n=heapq.heappop(heap)
  if g>cost.get(n,1e30):continue
  if n==goal:finished=True;break
  if len(cost)>250000:break
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
   nxt=(n[0]+dx,n[1]+dy);ng=g+(1.41421356237 if dx and dy else 1)
   if ng<cost.get(nxt,1e30) and available(nxt):cost[nxt]=ng;parent[nxt]=n;heapq.heappush(heap,(ng+h(nxt),ng,nxt))
 if not finished:
  if layer=='B.Cu':return back_route(net,a,z,width,'F.Cu')
  raise RuntimeError(f'No route for {net}: {a} to {z}')
 nodes=[goal]
 while nodes[-1]!=start:nodes.append(parent[nodes[-1]])
 nodes.reverse();simplified=[nodes[0]];lastdir=None
 for i in range(1,len(nodes)):
  direction=(nodes[i][0]-nodes[i-1][0],nodes[i][1]-nodes[i-1][1])
  if lastdir is not None and direction!=lastdir:simplified.append(nodes[i-1])
  lastdir=direction
 simplified.append(nodes[-1]);points=[point(n) for n in simplified]
 if points[0]!=a:points.insert(0,a)
 if points[-1]!=z:points.append(z)
 route(net,width,points,layer)
 print('Routed',net,'on',layer,':',len(points)-1,'segments')
for net,nodes in signal_nodes.items():
 connected=[nodes[0]];remaining=nodes[1:]
 while remaining:
  _,a,z=min((math.dist(a,z),a,z) for a in connected for z in remaining)
  back_route(net,a,z);connected.append(z);remaining.remove(z)

# Screen all explicit copper (filled zones are checked after KiCad fills them).
for i,r in enumerate(routes):
 for p in pads:
  if p['net']!=r['net'] and (r['layer']=='F.Cu' or p['th']) and r['shape'].distance(p['shape'])<.1999:
   errors.append(f"route{i} {r['net']} vs {p['name']} clearance {r['shape'].distance(p['shape']):.3f}")
 for j,s in enumerate(routes[:i]):
  if s['net']!=r['net'] and s['layer']==r['layer'] and s['shape'].distance(r['shape'])<.1999:errors.append(f"route{i} {r['net']} vs route{j} {s['net']}")
for i,v in enumerate(vias):
 for p in pads:
  if p['net']!=v['net'] and v['shape'].distance(p['shape'])<.1999:errors.append(f"via{i} {v['net']} vs {p['name']}")
 for j,r in enumerate(routes):
  if r['net']!=v['net'] and v['shape'].distance(r['shape'])<.1999:errors.append(f"via{i} {v['net']} vs route{j} {r['net']}")
 for j,w in enumerate(vias[:i]):
  if w['net']!=v['net'] and v['shape'].distance(w['shape'])<.1999:errors.append(f"via{i} {v['net']} vs via{j} {w['net']}")
report=dict(scope='Explicit copper geometric screening only, not KiCad DRC',errors=errors,unconnected_plane_pads=unconnected_plane,planned_routes=len(routes),planned_vias=len(vias),all_routing_complete=False)
(BASE/'work/usb_power_route_screen.json').write_text(json.dumps(report,indent=2))
if errors:raise SystemExit('\n'.join(errors))
for i,r in enumerate(routes):
 for j,(a,z) in enumerate(zip(r['points'],r['points'][1:])):
  if a==z:continue
  b.append(parse(f'(segment (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (width {r["width"]}) (layer {q(r["layer"])}) (net {netcodes[r["net"]]}) (uuid "{uid("usb-route/"+str(i)+"/"+str(j))}"))'))
for i,v in enumerate(vias):
 x,y=v['xy'];b.append(parse(f'(via (at {x} {y}) (size {v["size"]}) (drill {v["drill"]}) (layers "F.Cu" "B.Cu") (net {netcodes[v["net"]]}) (uuid "{uid("usb-via/"+str(i))}"))'))
for i,(net,layer,bounds) in enumerate([('GND','F.Cu',(10.5,10.5,89.5,59.5)),('GND','In1.Cu',(10.5,10.5,89.5,59.5)),('12V_PROTECTED','In2.Cu',(10.5,10.5,89.5,23.3)),('5V_BUS','In2.Cu',(10.5,23.8,89.5,59.5)),('GND','B.Cu',(10.5,10.5,89.5,59.5))]):
 x0,y0,x1,y1=bounds
 b.append(parse(f'(zone (net {netcodes[net]}) (net_name {q(net)}) (layer {q(layer)}) (uuid "{uid("usb-zone/"+str(i))}") (hatch edge .5) (connect_pads yes (clearance .25)) (min_thickness .2) (filled_areas_thickness no) (fill yes (thermal_gap .3) (thermal_bridge_width .5)) (polygon (pts (xy {x0} {y0}) (xy {x1} {y0}) (xy {x1} {y1}) (xy {x0} {y1}))))'))
write(path,b)
(d/'power_route_screen.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
