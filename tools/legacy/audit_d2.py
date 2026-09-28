from design_d2 import *
from itertools import combinations
from collections import Counter
import html
d=OUT/'USB_POWER'
b=parse((d/'USB_POWER.kicad_pcb').read_text())
boxes=[];pads=[];ids=[]
def walk(x):
 if isinstance(x,list):
  if x and x[0]=='uuid':ids.append(str(x[1]))
  for y in x:walk(y)
walk(b)
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="7 7 86 57"><rect x="10" y="10" width="80" height="45" fill="#123e35" stroke="black" stroke-width=".15"/>']
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);ox,oy=map(float,one(f,'at')[1:3]);points=[];sgn=-1 if len(one(f,'at'))>3 and float(one(f,'at')[3])%360==180 else 1
 for g in f:
  if not isinstance(g,list) or not one(g,'layer') or one(g,'layer')[1]!='F.CrtYd':continue
  for k in ('start','end'):
   a=one(g,k)
   if a:points.append((ox+sgn*float(a[1]),oy+sgn*float(a[2])))
 if points:
  x0=min(x for x,y in points);x1=max(x for x,y in points);y0=min(y for x,y in points);y1=max(y for x,y in points)
  boxes.append((ref,x0,y0,x1,y1))
  svg.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#87bda6" stroke-width=".07"/>')
 for p in all_(f,'pad'):
  if not any(str(v).endswith('.Cu') for v in one(p,'layers')[1:]):continue
  x,y=map(float,one(p,'at')[1:3]);w,h=map(float,one(p,'size')[1:3]);x=sgn*x+ox;y=sgn*y+oy
  n=one(p,'net');net=str(n[2]) if n else None
  pads.append(dict(ref=ref,pin=str(p[1]),x=x,y=y,w=w,h=h,net=net))
  svg.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="#d5b957"/><text x="{x}" y="{y+.16}" text-anchor="middle" font-size=".48">{html.escape(str(p[1]))}</text>')
 svg.append(f'<text x="{ox}" y="{oy-1.5}" text-anchor="middle" fill="white" font-family="sans-serif" font-size=".8">{ref}</text>')
overlaps=[]
for a,c in combinations(boxes,2):
 dx=min(a[3],c[3])-max(a[1],c[1]);dy=min(a[4],c[4])-max(a[2],c[2])
 if dx>0.001 and dy>0.001:overlaps.append(dict(a=a[0],b=c[0],intersection_mm=[round(dx,3),round(dy,3)]))
report=dict(scope='Geometric screening only; not KiCad DRC or ERC',footprints=len(boxes),copper_pads=len(pads),duplicate_uuids=[i for i,n in Counter(ids).items() if n>1],courtyard_bounding_box_overlaps=overlaps,routed_segments=len(all_(b,'segment')))
(d/'geometry_screen.json').write_text(json.dumps(report,indent=2))
for seg in all_(b,'segment'):
 a=one(seg,'start');z=one(seg,'end');w=one(seg,'width')[1]
 svg.append(f'<path d="M {a[1]} {a[2]} L {z[1]} {z[2]}" stroke="#ff8877" stroke-width="{w}" fill="none"/>')
(d/'placement.svg').write_text(''.join(svg)+ '<text x="50" y="60" text-anchor="middle" font-size="1.2">USB POWER — ENGINEERING HOLD — NOT FOR ORDER</text></svg>')
(BASE/'work/usb_pads.json').write_text(json.dumps(pads,indent=2))
print(json.dumps(report,indent=2))
