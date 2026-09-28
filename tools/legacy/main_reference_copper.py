"""Transplant TI reference tracks and zone outlines; always requires native refill/DRC."""
from design_d2 import *
from main_reference_layout import canonical_net,REFERENCE_OFFSET_X,REFERENCE_Y_TOP
import math
D=OUT/'MAIN_POWER';path=D/'MAIN_POWER.kicad_pcb';b=parse(path.read_text())
data=json.loads((BASE/'work/datasheets/pmp_reference_copper.json').read_text())
codes={str(a[2]):str(a[1]) for a in all_(b,'net')}
layers={1:'F.Cu',2:'In1.Cu',3:'In2.Cu',32:'B.Cu','TOP':'F.Cu','MID1':'In1.Cu','MID2':'In2.Cu','BOTTOM':'B.Cu'}
def xy(p):return (round(p[0]+REFERENCE_OFFSET_X,7),round(REFERENCE_Y_TOP-p[1],7))
def trackxy(p,net):
 x,y=xy(p)
 if net=='OPT' and abs(y-68.9895005)<.00001:y=69.034
 if net=='SLOPE' and abs(y-61.5075012)<.00001:y=61.4
 return x,y
def pts(points):return ' '.join(f'(xy {x} {y})' for x,y in map(xy,points))
def zone(net,layer,points,key,priority=1):
 return parse(f'(zone (net {codes[net]}) (net_name "{net}") (layer "{layer}") (uuid "{uid(key)}") (hatch edge .5) (priority {priority}) (connect_pads yes (clearance .2)) (min_thickness .15) (fill yes (thermal_gap .25) (thermal_bridge_width .3)) (polygon (pts {pts(points)})))')
b[:]=[a for a in b if not(isinstance(a,list) and a[0] in ('segment','via','zone'))]
skipped=[]
for typ in ('tracks','vias','fills','polygons'):
 for i,item in enumerate(data[typ]):
  # Native DRC identified these terminal branches to omitted reference options.
  if typ=='tracks' and i in (39,40,41,43,44,64,101,112,113,123,149):continue
  if typ=='vias' and i==23:continue
  net=canonical_net(item['net']);key='main/reference/'+typ+'/'+str(i)
  if net not in codes:skipped.append((typ,i,item['net']));continue
  layer=layers.get(item['layer'])
  if typ=='tracks':
   s=trackxy(item['start_mm'],net);e=trackxy(item['end_mm'],net)
   if i==151:e=(86.778,40.94)
   w=.15 if net=='OPT' else item['width_mm'];b.append(parse(f'(segment (start {s[0]} {s[1]}) (end {e[0]} {e[1]}) (width {w}) (layer "{layer}") (net {codes[net]}) (uuid "{uid(key)}"))'))
  elif typ=='vias':
   x,y=xy(item['xy_mm']);b.append(parse(f'(via (at {x} {y}) (size {item["diameter_mm"]}) (drill {item["drill_mm"]}) (layers "F.Cu" "B.Cu") (net {codes[net]}) (uuid "{uid(key)}"))'))
  elif typ=='polygons':
   assert not any(a['round'] for a in item['vertex_arcs'])
   b.append(zone(net,layer,item['vertices_mm'],key,100-int(item['properties'].get('POURINDEX','50'))))
  else:
   x1,y1=item['start_mm'];x2,y2=item['end_mm'];cx=(x1+x2)/2;cy=(y1+y2)/2;a=math.radians(item['rotation'])
   p=[(cx+(x-cx)*math.cos(a)-(y-cy)*math.sin(a),cy+(x-cx)*math.sin(a)+(y-cy)*math.cos(a)) for x,y in [(x1,y1),(x2,y1),(x2,y2),(x1,y2)]]
   b.append(zone(net,layer,p,key,150+i))
for i,item in enumerate(data['regions']):
 if item['kind']!=1:continue
 layer=layers[item['layer']]
 b.append(parse(f'(zone (net 0) (net_name "") (layer "{layer}") (uuid "{uid("main/reference/cutout/"+str(i))}") (hatch edge .5) (keepout (tracks allowed) (vias allowed) (pads allowed) (copperpour not_allowed) (footprints allowed)) (polygon (pts {pts(item["vertices_mm"])})))'))
write(path,b)
(D/'reference_copper_import.json').write_text(json.dumps(dict(source=data['source'],segments=len(all_(b,'segment')),vias=len(all_(b,'via')),zones=len(all_(b,'zone')),skipped_optional_nets=skipped,requires_native_refill_and_validation=True),indent=2))
print('Reference copper:',len(all_(b,'segment')),'tracks,',len(all_(b,'via')),'vias,',len(all_(b,'zone')),'zones')
