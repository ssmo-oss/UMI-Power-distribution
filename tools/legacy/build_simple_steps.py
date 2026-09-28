from pathlib import Path
import sys,json,math,hashlib,shutil,zipfile
sys.path.insert(0,str(Path('work/step_lib').resolve()))
from design_d2 import parse,all_,one,prop
from OCP.STEPControl import STEPControl_Reader,STEPControl_Writer,STEPControl_AsIs
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepBndLib import BRepBndLib
from OCP.Bnd import Bnd_Box
from OCP.BRepBuilderAPI import BRepBuilderAPI_GTransform,BRepBuilderAPI_Transform
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.gp import gp_Pnt,gp_GTrsf,gp_Trsf,gp_Ax1,gp_Dir,gp_Vec

out=Path('outputs/UMI_D6_STEP');native=Path('work/step_native');native.mkdir(exist_ok=True)
source=Path('C:/Users/Sandi/Documents/KiCad/UMI_THREE_BOARD_DESIGN_D6');audit={};rows=[]
def read(p):
 r=STEPControl_Reader();assert r.ReadFile(str(p))==IFSelect_RetDone;r.TransferRoots();s=r.OneShape();assert BRepCheck_Analyzer(s).IsValid();return s
def bounds(s):
 b=Bnd_Box();BRepBndLib.Add_s(s,b);lo=b.CornerMin();hi=b.CornerMax();return [lo.X(),lo.Y(),lo.Z(),hi.X(),hi.Y(),hi.Z()]
def count(s):
 ex=TopExp_Explorer(s,TopAbs_SOLID);n=0
 while ex.More():n+=1;ex.Next()
 return n
def write(p,s,n):
 assert BRepCheck_Analyzer(s).IsValid();w=STEPControl_Writer();w.Transfer(s,STEPControl_AsIs);assert w.Write(str(p))==IFSelect_RetDone
 s2=read(p);assert count(s2)==n,(p,count(s2),n)
 return {'solids':n,'valid_after_reimport':True,'bounds_mm':bounds(s2),'bytes':p.stat().st_size}
def height(ref,fp):
 if ref.startswith('F'):return 5.0
 if 'Phoenix_1709681' in fp:return 20.0
 if 'JST_VH' in fp:return 10.0
 if 'USB_A' in fp:return 8.0
 if 'SER2915' in fp:return 15.5
 if 'XAL4020' in fp:return 2.1
 if 'Panasonic_FK' in fp:return 10.2
 if 'CP_Elec_6.3x5.8' in fp:return 5.8
 if 'TPSM63610' in fp:return 4.0
 if 'SOT-23' in fp:return 1.2
 if 'HTSSOP' in fp or 'TSSOP' in fp:return 1.2
 if 'VSON' in fp or 'TPS25982' in fp:return 1.0
 if ref.startswith('Q'):return 1.2
 if ref.startswith('R'):return .6
 if ref.startswith('C'):return 2.5 if '1210' in fp else 1.0
 if ref.startswith('D'):return 2.5 if 'SMB' in fp or 'TO-277' in fp else 1.3
 return 1.5
def fab_bounds(f):
 points=[]
 for g in f:
  if not isinstance(g,list) or not one(g,'layer') or one(g,'layer')[1]!='F.Fab':continue
  if g[0] in ('fp_line','fp_rect','fp_arc'):
   for k in ('start','end','mid'):
    p=one(g,k)
    if p:points.append(tuple(map(float,p[1:3])))
  if g[0]=='fp_poly':points.extend(tuple(map(float,p[1:3])) for p in one(g,'pts')[1:])
  if g[0]=='fp_circle':
   c=tuple(map(float,one(g,'center')[1:3]));e=tuple(map(float,one(g,'end')[1:3]));r=math.dist(c,e);points.extend([(c[0]-r,c[1]-r),(c[0]+r,c[1]+r)])
 assert points,prop(f,'Reference')
 return min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)

for name,expected,size in [('MAIN_POWER',11,(68,100.263962,1.2)),('POE_POWER',56,(106,100,1.2)),('USB_POWER',34,(80,50,1.6))]:
 p=source/name/(name+'.kicad_pcb');digest=hashlib.sha256(p.read_bytes()).hexdigest();b=parse(p.read_text());ox,oy=map(float,one(one(b,'setup'),'aux_axis_origin')[1:3])
 bare=out/(name+'_D6_BARE.step');backup=native/bare.name
 if not backup.exists():shutil.copy2(bare,backup)
 shape=read(backup);bb=bounds(shape);t=size[2];zspan=bb[5]-bb[2]-2e-7
 stretch=gp_GTrsf();stretch.SetValue(3,3,t/zspan);shape=BRepBuilderAPI_GTransform(shape,stretch,True).Shape()
 ba=write(bare,shape,1);box=ba['bounds_mm'];assert abs(box[3]-box[0]-size[0])<1e-4 and abs(box[4]-box[1]-size[1])<1e-4 and abs(box[5]-box[2]-t)<1e-4
 compound=TopoDS_Compound();builder=BRep_Builder();builder.MakeCompound(compound);builder.Add(compound,shape);n=1;placed=0
 for f in all_(b,'footprint'):
  ref=str(prop(f,'Reference')[2]);mpn=prop(f,'MPN');attr=one(f,'attr') or []
  if ref.startswith('H') or 'exclude_from_bom' in attr:continue
  x0,y0,x1,y1=fab_bounds(f);at=one(f,'at');x,y=map(float,at[1:3]);angle=float(at[3]) if len(at)>3 else 0;h=height(ref,str(f[1]))
  body=BRepPrimAPI_MakeBox(gp_Pnt(x0,-y1,t),x1-x0,y1-y0,h).Shape()
  tr=gp_Trsf();tr.SetRotation(gp_Ax1(gp_Pnt(0,0,0),gp_Dir(0,0,1)),math.radians(angle));body=BRepBuilderAPI_Transform(body,tr,True).Shape()
  tr=gp_Trsf();tr.SetTranslation(gp_Vec(x-ox,oy-y,0));body=BRepBuilderAPI_Transform(body,tr,True).Shape();builder.Add(compound,body);n+=1;placed+=1
  rows.append({'board':name,'reference':ref,'MPN':str(mpn[2]) if mpn else '', 'body_xy_basis':'Bounding rectangle of footprint F.Fab graphics','estimated_height_mm':h,'x_kicad_mm':x,'y_kicad_mm':y,'rotation_deg':angle,'bounds_in_step_mm':bounds(body),'status':'Simplified visual proxy; height not certified'})
  if ref.startswith('F'):
   insert=BRepPrimAPI_MakeBox(gp_Pnt(x-ox+(x0+x1)/2-9.5,oy-y-(y0+y1)/2-2.5,t+h),19,5,13).Shape();builder.Add(compound,insert);n+=1
   rows.append({'board':name,'reference':ref+'_INSERT','MPN':'See fuse insert BOM','estimated_height_mm':13,'status':'Estimated fuse body above holder; not a certified envelope','bounds_in_step_mm':bounds(insert)})
 assert placed==expected,(name,placed)
 simplified=out/(name+'_D6_SIMPLIFIED.step');sa=write(simplified,compound,n)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
 audit[name]={'source_sha256':digest,'bare':ba,'simplified':sa,'electrical_components_represented':placed,'source_unchanged':True}
(out/'COMPONENT_PROXY_DIMENSIONS.json').write_text(json.dumps(rows,indent=2))
(out/'STEP_VERIFICATION.json').write_text(json.dumps(audit,indent=2))
(out/'README.md').write_text('''# UMI D6 simplified STEP models

Six files: BARE and SIMPLIFIED for MAIN_POWER, POE_POWER and USB_POWER. Units are millimetres.

BARE files retain the native KiCad board outline, rounded corners, mounting and component holes. Small via holes are intentionally omitted. The native board-only export omits outer conductor/mask thickness; its Z dimension was scaled to the specified finished 1.2 mm MAIN/POE and 1.6 mm USB thickness. X/Y geometry is unchanged. No tracks, pads, copper zones or text are modelled.

SIMPLIFIED files add a rectangular body proxy for every board-mounted electrical component, including the through-hole parts intended for manual assembly. They also show simple fuse-insert proxies. Component X/Y outlines derive from the saved footprint fabrication graphics and placements. Heights are approximate visual allowances, not verified manufacturer maximum dimensions. Leads, solder joints, connector internals, mating plugs, cables and standoffs are omitted. These models are useful for arrangement and visualisation, but NOT final enclosure-clearance signoff. Consult COMPONENT_PROXY_DIMENSIONS.json for each assumption.

Origin: each board's Gerber/drill origin. X points right, Y points upward when viewed from the component side, Z points upward. Bare PCB bottom is Z=0; component bodies start at the finished PCB top. All boards are exported separately; their relative installation positions are not defined.

Every file was reimported with Open CASCADE and checked for valid solid geometry and expected solid count. Bare PCB dimensions were checked against the design. MAIN: 68 × 100.263962 × 1.2 mm; POE: 106 × 100 × 1.2 mm; USB: 80 × 50 × 1.6 mm. The original KiCad/manufacturing files were not modified.
''',encoding='utf-8')
dest=Path('C:/Users/Sandi/Documents/KiCad/UMI_D6_STEP');dest.mkdir(exist_ok=True)
for p in out.iterdir():
 if p.is_file():shutil.copy2(p,dest/p.name)
archive=dest.parent/'UMI_D6_STEP.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(out.iterdir()):
  if p.is_file():z.write(p,'UMI_D6_STEP/'+p.name)
print(json.dumps(audit,indent=2))
