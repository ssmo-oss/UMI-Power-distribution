"""Place the boost components using TI PMP21274 source pad geometry, not visual guesses."""
import json,math,copy
from design_d2 import *
REFERENCE_OFFSET_X=67.4232
REFERENCE_Y_TOP=118.5436
NET_MAP={'V+':'BOOST_IN','CSPP_N':'SENSE_LOW','CSP_P':'CSP','CSP_N':'CSN','VIN':'IC_VIN','SW_P':'SW','SW_N':'HO','NetQ2_4':'GATE2','NetQ3_4':'GATE3','NetC1_1':'SNUB','NetC5_1':'BOOST_OUT','VOUT':'53V5_RAW','NetR19_2':'FB_HIGH','NetC18_2':'COMP_RC','SYN/RT':'RT'}
def canonical_net(net):return NET_MAP.get(net,net)

def reference_parts(parts,customs,inherited):
 data=json.loads((BASE/'work/datasheets/pmp_reference_geometry.json').read_text());report=[]
 groups={}
 for pad in data['pads']:
  if pad['ref']:groups.setdefault(pad['ref'],{}).setdefault(pad['pin'],pad)
 refs={'U1','Q1','Q2','Q3','L1','L2','D2'}|{'C'+str(i) for i in range(1,21)}|{'R'+str(i) for i in range(1,22)}
 for part in parts:
  ref=part['ref']
  if ref not in refs or ref not in groups:continue
  if ref[0] in 'RC' and ref not in ('C19','C20'):
   mapped={k:canonical_net(v['net']) for k,v in groups[ref].items() if k in part['pins']}
   assert sorted(mapped.values())==sorted(v[1] for v in part['pins'].values()),(ref,mapped,part['pins'])
   for pin,net in mapped.items():part['pins'][pin]=(part['pins'][pin][0],net)
  ident=part['fp'];fam,fn=ident.split(':')
  f=copy.deepcopy(customs[ident]) if ident in customs else copy.deepcopy(inherited[ident]) if ident in inherited else parse((LIB/(fam+'.pretty')/(fn+'.kicad_mod')).read_text())
  local={}
  for pad in all_(f,'pad'):
   pin=str(pad[1])
   if pin and pin in groups[ref]:local.setdefault(pin,tuple(map(float,one(pad,'at')[1:3])))
  if ref.startswith('Q'):local={k:v for k,v in local.items() if k in ['1','2','3','4']}
  if ref=='L1':local={k:v for k,v in local.items() if k in ['1','2']}
  if ref=='U1':local={k:v for k,v in local.items() if k!='21'}
  target={k:(groups[ref][k]['xy_mm'][0]+REFERENCE_OFFSET_X,REFERENCE_Y_TOP-groups[ref][k]['xy_mm'][1]) for k in local}
  choices=[]
  for angle in (0,90,180,270):
   ca=round(math.cos(math.radians(angle)));sa=round(math.sin(math.radians(angle)))
   rot={k:(ca*x-sa*y,sa*x+ca*y) for k,(x,y) in local.items()}
   dx=sum(target[k][0]-rot[k][0] for k in local)/len(local);dy=sum(target[k][1]-rot[k][1] for k in local)/len(local)
   err=(sum((rot[k][0]+dx-target[k][0])**2+(rot[k][1]+dy-target[k][1])**2 for k in local)/len(local))**.5
   choices.append((err,angle,dx,dy))
  err,angle,x,y=min(choices);part['pos']=(round(x,6),round(y,6));part['rotation']=angle
  if ref=='C20':part['pos']=(round(x+.5,6),round(y,6))
  if ref=='C1':part['pos']=(round(x,6),round(y+.05,6))
  if ref=='R20':part['pos']=(round(x+.2,6),round(y,6))
  report.append(dict(reference=ref,rotation=angle,position_mm=part['pos'],land_center_rms_difference_mm=err))
 return report

def dense_passive_courtyard(f):
 """0.1-mm assembly margin around actual chip body and land extents; no copper change."""
 points=[]
 for n in f:
  if not isinstance(n,list):continue
  layer=one(n,'layer')
  if n[0]=='pad':
   x,y=map(float,one(n,'at')[1:3]);w,h=map(float,one(n,'size')[1:3]);points.extend([(x-w/2,y-h/2),(x+w/2,y+h/2)])
  elif layer and layer[1]=='F.Fab' and n[0] in ('fp_line','fp_rect'):
   for k in ('start','end'):
    a=one(n,k)
    if a:points.append(tuple(map(float,a[1:3])))
 if points:
  f[:]=[n for n in f if not(isinstance(n,list) and one(n,'layer') and one(n,'layer')[1]=='F.CrtYd')]
  f.append(rect(min(x for x,y in points)-.1,min(y for x,y in points)-.1,max(x for x,y in points)+.1,max(y for x,y in points)+.1,'F.CrtYd',.05))
 return f

def rotate_footprint(f,angle):
 """Bake an orthogonal rotation into a local-library variant (including pad shapes)."""
 angle%=360
 if not angle:return f
 def r(x,y,a=angle):
  c=round(math.cos(math.radians(a)));s=round(math.sin(math.radians(a)));return(round(c*x-s*y,7),round(s*x+c*y,7))
 for node in f:
  if not isinstance(node,list):continue
  if node[0] not in ('pad','fp_line','fp_rect','fp_arc','fp_circle','fp_poly','fp_text','property'):continue
  oldang=0
  a=one(node,'at')
  if a and len(a)>3:oldang=float(a[3])
  for k in ('at','start','end','mid','center'):
   pt=one(node,k)
   if pt:pt[1:3]=map(str,r(*map(float,pt[1:3])))
  pts=one(node,'pts')
  if pts:
   for pt in pts[1:]:pt[1:3]=map(str,r(*map(float,pt[1:3])))
  if node[0]=='pad':
   total=(oldang+angle)%360
   if a:a[3:]=[]
   if total%180==90:
    sz=one(node,'size');sz[1],sz[2]=sz[2],sz[1]
   primitives=one(node,'primitives')
   if primitives:
    for prim in primitives[1:]:
     pts=one(prim,'pts')
     if pts:
      for pt in pts[1:]:pt[1:3]=map(str,r(*map(float,pt[1:3]),a=total))
  elif a and len(a)>3:a[3]=str((oldang+angle)%360)
 # Models require an independent axis/orientation review after the placement transplant.
 # Keep the manufacturing geometry authoritative and omit unverified 3-D rotations.
 f[:]=[n for n in f if not(isinstance(n,list) and n[0]=='model')]
 return f
