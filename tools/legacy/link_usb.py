from pathlib import Path
import re,json,uuid,copy,html,zipfile
base=Path.cwd(); out=base/'outputs/UMI_USB_D1';out.mkdir(exist_ok=True)
lib=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')
class Q(str): pass
def parse(text):
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text); stack=[];root=None
 for t in tokens:
  if t=='(':
   a=[]
   if stack:stack[-1].append(a)
   else:root=a
   stack.append(a)
  elif t==')':stack.pop()
  else:stack[-1].append(Q(json.loads(t)) if t.startswith('"') else t)
 assert not stack
 return root
def dump(x):
 if isinstance(x,list):return '('+' '.join(dump(t) for t in x)+')'
 return json.dumps(str(x)) if isinstance(x,Q) else str(x)
def children(x,k):return [a for a in x if isinstance(a,list) and a and a[0]==k]
def child(x,k):return next(iter(children(x,k)),None)
def prop(x,k):return next((a for a in children(x,'property') if a[1]==k),None)
def replace(x,k,a):
 x[:]=[v for v in x if not(isinstance(v,list) and v and v[0]==k)];x.append(a)
def uid():return Q(str(uuid.uuid4()))
def refresh(x):
 for a in x:
  if isinstance(a,list):
   if a[0] in ('uuid','tstamp'):a[:]=['uuid',uid()]
   else:refresh(a)
raise SystemExit('D1 generator retired: inherited Murata footprint has wrong pin pitch and the converter is obsolete. See outputs/ORDER_RELEASE_STATUS.md.')
sch=parse((base/'outputs/UMI_revD_electrical_draft/UMI_USB_D0.kicad_sch').read_text())
root=child(sch,'uuid')[1]; symbols=children(sch,'symbol')
old=parse((base/'outputs/UMI_revD_split_PLACEMENT_DRAFT/UMI_USB_placement_ONLY.kicad_pcb').read_text())
board=[copy.deepcopy(a) for a in old if not(isinstance(a,list) and a[0] in ('footprint','gr_text','net'))]
source_fps={str(prop(f,'Reference')[2]):f for f in children(old,'footprint')}
libsymbols=child(sch,'lib_symbols')
# Match the shield pin number used by the actual provisional USB footprint.
for s in children(libsymbols,'symbol'):
 if s[1] in ('Draft:D_J2','Draft:D_J3'):
  for unit in children(s,'symbol'):
   for p in children(unit,'pin'):
    if child(p,'number')[1]=='5':child(p,'number')[1]=Q('SH')
positions={'J1':(16,16),'U1':(40,15),'J2':(20,27),'J3':(50,27),
 'U2':(26,21),'U3':(56,21),'U4':(42,33),
 'R1':(38,30),'C1':(27,14),'C2':(48,14),'C3':(49,18),
 'R2':(31,21),'R3':(61,21),'C4':(24,18),'C5':(55,18),
 'C6':(19,23),'C7':(49,22.8),'R4':(30,17),'R5':(61,18),'C8':(42,36)}
import csv
rows=list(csv.DictReader((base/'outputs/UMI_revD_electrical_draft/UMI_USB_D0_connections.csv').open()))
netmap={}
for r in rows:
 if r['Reference'] in ('J2','J3') and r['Pin']=='5':r['Pin']='SH'
 if r['Net']!='NC':netmap.setdefault(r['Net'],len(netmap)+1)
for n,i in netmap.items():board.append(['net',str(i),Q(n)])
local=out/'UMI_USB.pretty';local.mkdir(exist_ok=True)
report=[]
for s in symbols:
 ref=str(prop(s,'Reference')[2]); value=str(prop(s,'Value')[2]); existing=str(prop(s,'Footprint')[2])
 if ref in source_fps:
  f=copy.deepcopy(source_fps[ref]); name=str(f[1]).split(':')[-1]
 else:
  family,name=existing.split(':'); f=parse((lib/(family+'.pretty')/(name+'.kicad_mod')).read_text())
 fpname='UMI_USB:'+name
 prop(s,'Footprint')[2]=Q(fpname)
 project=child(child(s,'instances'),'project');project[1]=Q('UMI_USB_D1')
 f[1]=Q(fpname)
 for key in ('version','generator','generator_version','path','sheetname','sheetfile','at','uuid'):
  f[:]=[a for a in f if not(isinstance(a,list) and a[0]==key)]
 refresh(f);f.extend([['uuid',uid()],['at',*map(str,positions[ref])],['path',Q('/'+root+'/'+child(s,'uuid')[1])],['sheetname',Q('')],['sheetfile',Q('UMI_USB_D1.kicad_sch')]])
 for k,v in [('Reference',ref),('Value',value)]:
  p=prop(f,k)
  if p:p[2]=Q(v)
  else:f.append(['property',Q(k),Q(v),['at','0','-3','0'],['layer',Q('F.Fab')],['effects',['font',['size','1','1']]]])
 # Restore solder-mask openings on inherited module through-hole pads.
 pins={r['Pin']:r['Net'] for r in rows if r['Reference']==ref}
 actual={str(p[1]) for p in children(f,'pad') if p[1]}
 assert set(pins)<=actual,(ref,pins,actual)
 for pad in children(f,'pad'):
  pad[:]=[a for a in pad if not(isinstance(a,list) and a[0] in ('net','pinfunction','pintype'))]
  if pad[2]=='thru_hole' and Q('*.Mask') not in child(pad,'layers'):child(pad,'layers').append(Q('*.Mask'))
  n=pins.get(str(pad[1]),'NC')
  if n!='NC':pad.append(['net',str(netmap[n]),Q(n)])
 board.append(f)
 # Package local footprint definitions so opening the project needs no custom library setup.
 lf=copy.deepcopy(f);lf[1]=Q(name)
 for k in ('at','path','sheetname','sheetfile','uuid'):lf[:]=[a for a in lf if not(isinstance(a,list) and a[0]==k)]
 for p in children(lf,'pad'):p[:]=[a for a in p if not(isinstance(a,list) and a[0]=='net')]
 lf.insert(2,['version','20241229']);lf.insert(3,['generator',Q('pcbnew')])
 (local/(name+'.kicad_mod')).write_text(dump(lf),encoding='utf-8')
 report.append({'reference':ref,'pads':sorted(actual),'schematic_link':str(child(f,'path')[1])})
for t in children(sch,'text'):
 if 'REVIEW DRAFT' in t[1]:t[1]=Q('D1: linked placement draft; unrouted; DO NOT FABRICATE.')
 if 'Passive review' in t[1]:t[1]=Q('Review symbols: ERC not sign-off. USB connectors and module footprint provisional; protection and thermal design open.')
child(child(sch,'title_block'),'rev')[1]=Q('D1 LINKED PLACEMENT - HOLD')
board.append(['gr_text',Q('UMI USB D1 - UNROUTED / ENGINEERING HOLD'),['at','40','44'],['layer',Q('Dwgs.User')],['uuid',uid()],['effects',['font',['size','1','1'],['thickness','.15']]]])
for ext,obj in [('kicad_sch',sch),('kicad_pcb',board)]:
 text=dump(obj);assert dump(parse(text))==text
 (out/('UMI_USB_D1.'+ext)).write_text(text,encoding='utf-8')
(out/'UMI_USB_D1.kicad_pro').write_text(json.dumps({'meta':{'filename':'UMI_USB_D1.kicad_pro','version':1}},indent=2))
(out/'fp-lib-table').write_text('(fp_lib_table (lib (name "UMI_USB") (type "KiCad") (uri "${KIPRJMOD}/UMI_USB.pretty") (options "") (descr "Packaged draft footprints")))')
# Validate correspondence from saved files, independent of the construction loop.
saved=parse((out/'UMI_USB_D1.kicad_pcb').read_text()); fps=children(saved,'footprint')
boxes=[]
for f in fps:
 pts=[]
 for g in children(f,'fp_line')+children(f,'fp_rect'):
  if child(g,'layer')[1]=='F.CrtYd':pts.extend([child(g,'start')[1:3],child(g,'end')[1:3]])
 if pts:
  x,y=map(float,child(f,'at')[1:3]);xs=[float(p[0])+x for p in pts];ys=[float(p[1])+y for p in pts]
  boxes.append((str(prop(f,'Reference')[2]),min(xs),min(ys),max(xs),max(ys)))
for i,a in enumerate(boxes):
 for b in boxes[i+1:]:
  assert not(min(a[3],b[3])>max(a[1],b[1]) and min(a[4],b[4])>max(a[2],b[2])),('courtyard overlap',a[0],b[0])
for row in rows:
 f=next(f for f in fps if prop(f,'Reference')[2]==row['Reference'])
 pads=[p for p in children(f,'pad') if p[1]==row['Pin']]
 assert pads
 for p in pads:
  n=child(p,'net');assert (str(n[2]) if n else 'NC')==row['Net']
(out/'connectivity_check.json').write_text(json.dumps({'components':len(fps),'nets':len(netmap),'pin_rows_checked':len(rows),'pad_net_matches':True,'symbol_paths_present':True,'axis_aligned_courtyard_overlaps':0,'tracks':0,'KiCad_open_ERC_DRC':'NOT RUN','components_detail':report},indent=2))
# Geometry preview from saved board; no KiCad runtime required.
svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="5 5 70 43"><rect x="10" y="10" width="60" height="30" fill="#164c36" stroke="#ddd" stroke-width=".2"/>']
for f in fps:
 x,y=map(float,child(f,'at')[1:3]);ref=str(prop(f,'Reference')[2])
 svg.append(f'<g transform="translate({x},{y})">')
 for line in children(f,'fp_line'):
  if child(line,'layer')[1] not in ('F.CrtYd','F.Fab'):continue
  a=child(line,'start')[1:3];b=child(line,'end')[1:3]
  svg.append(f'<path d="M {a[0]} {a[1]} L {b[0]} {b[1]}" stroke="#a4cabb" stroke-width=".12"/>')
 for p in children(f,'pad'):
  a=child(p,'at');size=child(p,'size');px,py=map(float,a[1:3]);w,h=map(float,size[1:3])
  svg.append(f'<rect x="{px-w/2}" y="{py-h/2}" width="{w}" height="{h}" fill="#d1b265"/>')
  d=child(p,'drill')
  if d and d[1]!='oval':svg.append(f'<circle cx="{px}" cy="{py}" r="{float(d[1])/2}" fill="#102d22"/>')
 svg.append(f'<text x="0" y="-2.5" font-size="1.1" fill="white">{html.escape(ref)}</text></g>')
svg.append('<text x="10" y="45" font-size="1.4">60 × 30 mm — placement draft, unrouted</text></svg>')
(out/'placement.svg').write_text(''.join(svg),encoding='utf-8')
(out/'README.md').write_text('''# UMI USB D1 — linked placement draft

Open UMI_USB_D1.kicad_pro in KiCad, then its schematic or PCB. Local footprint library is included.

This is an editable 60 × 30 mm placement draft, not a manufacturing release. There are 20 linked components, named pad nets and no routed copper. Two provisional USB-A ports face the same long edge. Input and converter occupy the opposite side of the board.

Changes: added all draft support components to PCB; linked each footprint to its schematic symbol; corrected USB shield numbering to SH; restored missing solder-mask openings on inherited converter pads; bundled footprints.

Checks performed: text structure round-trip; every scheduled pin has a matching footprint pad and net; symbol paths assigned. KiCad loading, ERC, DRC and 3D inspection have NOT been performed. Custom review symbols still use passive pin types and do not provide meaningful electrical-rule checking.

Open engineering items before routing/release: verify 3 A USB-A connector selection and exact mechanical drawing; validate inherited Murata footprint and trim against manufacturer drawing; settle input fault protection and port ESD; check capacitor effective capacitance, switch thermal design and full-load voltage drop; confirm enclosure/mounting/height; choose copper stackup and routing; run KiCad ERC/DRC and prototype load/short-circuit/thermal tests. No mounting holes are assumed.

The TPS2557 pinout was checked against https://www.ti.com/lit/ds/symlink/tps2557.pdf . Charging-controller reference: https://www.ti.com/lit/ds/symlink/tps2513a.pdf . Neither source establishes that the connected headset will draw 3 A from USB-A.

No KiCad executable or KiCad-bundled Python was launched to create this package.
''',encoding='utf-8')
with zipfile.ZipFile(out.with_suffix('.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for p in out.rglob('*'):
  if p.is_file():z.write(p,p.relative_to(out.parent))
print(json.dumps({'output':str(out),'components':len(fps),'nets':len(netmap),'pins_checked':len(rows)}))
