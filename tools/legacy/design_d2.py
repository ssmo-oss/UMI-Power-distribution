"""Text-native KiCad design construction. Does not import pcbnew or launch KiCad."""
from pathlib import Path
import re,json,uuid,copy,csv
BASE=Path.cwd(); OUT=BASE/'outputs/UMI_D2';OUT.mkdir(exist_ok=True)
LIB=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')
class Q(str):pass
def parse(t):
 stack=[];root=None
 for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',t):
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
 return '('+' '.join(map(dump,x))+')' if isinstance(x,list) else json.dumps(str(x)) if isinstance(x,Q) else str(x)
def all_(x,k):return [a for a in x if isinstance(a,list) and a and a[0]==k]
def one(x,k):return next(iter(all_(x,k)),None)
def prop(x,k):return next((a for a in all_(x,'property') if a[1]==k),None)
def set_(x,k,v):x[:]=[a for a in x if not(isinstance(a,list) and a[0]==k)];x.append(v)
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'umi-d2/'+s))
def q(s):return json.dumps(str(s))
def write(path,node):
 s=dump(node);assert dump(parse(s))==s;path.write_text(s,encoding='utf-8')
def rect(x1,y1,x2,y2,layer,width=.1):
 return parse(f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))')
def pad(n,x,y,w,h,drill=None,paste=True):
 kind='thru_hole' if drill else 'smd';shape='rect' if not drill or str(n)=='1' else 'circle'
 return parse(f'(pad {q(n)} {kind} {shape} (at {x} {y}) (size {w} {h}) '+(f'(drill {drill}) (layers "*.Cu" "*.Mask")' if drill else '(layers "F.Cu" "F.Mask"'+(' "F.Paste"' if paste else '')+')')+')')
def custom(name):return ['footprint',Q(name),['version','20241229'],['generator',Q('pcbnew')],['layer',Q('F.Cu')]]
def rdf():
 f=custom('TI_RDF0022A_TPSM63610');f.extend([rect(-3.75,-4,3.75,4,'F.CrtYd',.05),rect(-3.25,-3.75,3.25,3.75,'F.Fab')])
 f.append(['attr','smd'])
 for n in range(1,19):
  left=n<=9;i=n-1 if left else 18-n;x=-2.85 if left else 2.85
  if i in (0,8):
   x=-2.75 if left else 2.75;y=-2.925 if i==0 else 2.925
   # Manufacturer's notched corner land, not a generic QFN corner rectangle.
   p=pad(n,x,y,.4,.4);p[3]='custom'
   pts=[(-.7,-.45),(.7,-.45),(.7,.45),(-.7,.45),(-.7,.2),(-.375,.2),(-.375,-.2),(-.7,-.2)]
   if not left:pts=[(-a,b) for a,b in reversed(pts)]
   p.extend([['options',['clearance','outline'],['anchor','rect']],['primitives',['gr_poly',['pts',*[['xy',str(a),str(b)] for a,b in pts]],['width','0'],['fill','yes']]]]);f.append(p)
  else:f.append(pad(n,x,(i-4)*.65,1.2,.25))
 for n,y in enumerate([-2.25,-.75,.75,2.25],19):
  f.append(pad(n,0,y,3.3,1,paste=False))
  for x in [-1.15,0,1.15]:f.append(parse(f'(pad "" smd rect (at {x} {y}) (size .95 .95) (layers "F.Paste"))'))
 return f
def usb_fp():
 f=custom('USB_A_Wurth_614004190021');f.extend([rect(-4.6,-1.4,11.6,13.5,'F.CrtYd',.05),rect(-3.75,-1.14,10.75,13.01,'F.Fab')])
 f.append(['attr','through_hole'])
 for n,x in enumerate([0,2.5,4.5,7],1):f.append(pad(n,x,0,1.6,1.6,.92))
 for x in [-3.07,10.07]:f.append(pad('SH',x,2.71,3.5,3.5,2.3))
 return f
def part(ref,val,fp,pins,pos,mpn='',types=None):return dict(ref=ref,value=val,fp=fp,pins=pins,pos=pos,mpn=mpn or val,types=types or {})
R='Resistor_SMD:R_0603_1608Metric';C='Capacitor_SMD:C_0603_1608Metric';C1210='Capacitor_SMD:C_1210_3225Metric'
SOT='Package_TO_SOT_SMD:SOT-23-6';VSON='Package_SON:VSON-8-1EP_3x3mm_P0.65mm_EP1.65x2.4mm'
def two(ref,val,fp,a,b,pos,mpn=''):return part(ref,val,fp,{'1':('1',a),'2':('2',b)},pos,mpn)
def usb_parts():
 p=[part('J1','12V INPUT','Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical',{'1':('VIN','12V_IN'),'2':('GND','GND')},(15,15),'B2P-VH(LF)(SN)'),
 part('Q1','AO4407A','Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',{str(i):('S' if i<4 else 'G' if i==4 else 'D','12V_PROTECTED' if i<4 else 'RP_GATE' if i==4 else '12V_IN') for i in range(1,9)},(27,13),'AO4407A',{'4':'input'}),
 two('R6','100k',R,'RP_GATE','GND',(28,35),'RC0603FR-07100KL'),
 part('D1','12V gate clamp','Diode_SMD:D_SOD-123',{'1':('K','12V_PROTECTED'),'2':('A','RP_GATE')},(28,31),'BZT52C12-7-F'),
 part('U1','TPSM63610RDFR','UMI_D2:TI_RDF0022A_TPSM63610',{
 '1':('VIN1','12V_PROTECTED'),'2':('RBOOT','BOOT'),'3':('CBOOT','BOOT'),'4':('SW',None),'5':('VLDOIN','5V_BUS'),'6':('VCC','VCC'),
 '7':('AGND','GND'),'8':('FB','FB'),'9':('VOUT1','5V_BUS'),'10':('VOUT2','5V_BUS'),'11':('AGND','GND'),'12':('RT','RT'),
 '13':('PG','PG'),'14':('SPSP','GND'),'15':('SYNC_MODE','GND'),'16':('NC',None),'17':('EN','12V_PROTECTED'),'18':('VIN2','12V_PROTECTED'),
 '19':('PGND','GND'),'20':('PGND','GND'),'21':('AGND','GND'),'22':('AGND','GND')},(40,18.5),types={'1':'power_in','18':'power_in','5':'power_in','6':'power_out','8':'input','9':'power_out','12':'input','13':'open_collector','14':'input','15':'input','17':'input'}),
 two('C1','10uF 50V X7R',C1210,'12V_PROTECTED','GND',(33.6,15.25),'CNA6P1X7R1H106K'),
 two('C2','10uF 50V X7R',C1210,'12V_PROTECTED','GND',(46.4,15.25),'CNA6P1X7R1H106K'),
 two('C3','47uF 10V X7R',C1210,'5V_BUS','GND',(35.2,25),'GRM32ER71A476ME15L'),
 two('C9','47uF 10V X7R',C1210,'5V_BUS','GND',(40,25),'GRM32ER71A476ME15L'),
 two('C10','47uF 10V X7R',C1210,'5V_BUS','GND',(44.8,25),'GRM32ER71A476ME15L'),
 two('R1','24.9k 0.1%',R,'FB','GND',(35,21),'RT0603BRD0724K9L'),
 two('R7','100k 0.1%',R,'5V_BUS','FB',(35,18.5),'RT0603BRD07100KL'),
 two('R8','15.8k 1%',R,'RT','GND',(46,20),'RC0603FR-0715K8L'),
 two('R9','100k',R,'5V_BUS','PG',(46,22.3),'RC0603FR-07100KL'),
 two('C11','100nF 25V',C,'5V_BUS','GND',(33,23),'GRM188R71E104KA01D'),
 part('C12','47uF 25V bulk','Capacitor_SMD:CP_Elec_6.3x7.7',{'1':('+','12V_PROTECTED'),'2':('-','GND')},(33.5,35.7),'EEE-FK1E470P')]
 for port,x in [(1,24),(2,57)]:
  u='U'+str(port+1);ilim='ILIM'+str(port);v='VBUS'+str(port);fault='FAULT'+str(port);dm='DM'+str(port);dp='DP'+str(port)
  p.extend([part(u,'TPS2557DRB',VSON,{'1':('GND','GND'),'2':('IN','5V_BUS'),'3':('IN','5V_BUS'),'4':('EN','5V_BUS'),'5':('ILIM',ilim),'6':('OUT',v),'7':('OUT',v),'8':('FAULT',fault),'9':('EP','GND')},(x,22),types={'2':'power_in','3':'power_in','4':'input','6':'power_out','8':'open_collector'}),
   two('R'+str(port+1),'32.4k 0.1%',R,ilim,'GND',(x+5,22),'RT0603BRD0732K4L'),
   two('R'+str(port+3),'100k',R,'5V_BUS',fault,(x+5,18),'RC0603FR-07100KL'),
   two('C'+str(port+3),'100nF 25V',C,'5V_BUS','GND',(x,18),'GRM188R71E104KA01D'),
   two('C'+str(port+5),'22uF 10V','Capacitor_SMD:C_1206_3216Metric',v,'GND',(x-6,23.5),'GRM31CR71A226KE15L'),
   part('J'+str(port+1),'USB-A 3A','UMI_D2:USB_A_Wurth_614004190021',{'1':('VBUS',v),'2':('D-',dm),'3':('D+',dp),'4':('GND','GND'),'SH':('SHIELD','GND')},(18 if port==1 else 53,27),'614004190021'),
   part('U'+str(port+4),'USBLC6-2SC6',SOT,{'1':('IO1',dm),'2':('GND','GND'),'3':('IO2',dp),'4':('IO2',dp),'5':('VBUS',v),'6':('IO1',dm)},(33 if port==1 else 47,30),'USBLC6-2SC6')])
 p.extend([part('U4','TPS2513ADBVR',SOT,{'1':('DP1','DP1'),'2':('GND','GND'),'3':('DP2','DP2'),'4':('DM2','DM2'),'5':('IN','5V_BUS'),'6':('DM1','DM1')},(40,31.5),types={'5':'power_in'}),two('C8','100nF 25V',C,'5V_BUS','GND',(40,35),'GRM188R71E104KA01D')])
 # Keep component courtyards clear, including the USB shells behind the edge.
 adjustments={'R6':(40,12),'D1':(34,11.5),'R1':(34.5,21),'R7':(34.5,18.5),
              'C11':(31.2,24),'C12':(59,14),'U6':(46,30),'C5':(57,18.5),'R5':(62,18.5)}
 for component in p:
  if component['ref'] in adjustments:component['pos']=adjustments[component['ref']]
  if component['ref'] in ('U2','U3'):component['mpn']='TPS2557DRBR'
  if component['ref'] in ('C1','C3','R1'):component['rotation']=180
 p.extend([two('C13','47uF 10V X7R',C1210,'5V_BUS','GND',(44,37),'GRM32ER71A476ME15L'),two('C14','47uF 10V X7R',C1210,'5V_BUS','GND',(50,37),'GRM32ER71A476ME15L')])
 # User authorized enlargement. Allocate a larger heat-spreading and routing area.
 positions={'J1':(20,18),'Q1':(32,17),'D1':(32,23),'R6':(37,23),
 'U1':(48,25),'C1':(41.6,21.75),'C2':(54.4,21.75),'C3':(43.2,31.5),
 'C9':(48,31.5),'C10':(52.8,31.5),'R1':(42.5,27.5),'R7':(42.5,25),
 'R8':(54,26.5),'R9':(54,28.8),'C11':(39.2,30.5),'C12':(72,17),
 'U2':(28,36),'R2':(33,36),'R4':(33,32),'C4':(28,32),'C6':(30.5,43.5),'J2':(22,47),'U5':(25.5,43.5),
 'U3':(71,36),'R3':(76,36),'R5':(76,32),'C5':(71,32),'C7':(73.5,43.5),'J3':(65,47),'U6':(68.5,43.5),
 'U4':(47,44),'C8':(47,48),'C13':(44,37),'C14':(50,37)}
 for component in p:component['pos']=positions[component['ref']]
 for component in p:
  if component['ref']=='U1':component['pins']['15']=('SYNC_MODE','VCC')
  if component['ref']=='R7':component.update(value='102k 0.1%',mpn='RT0603BRD07102KL')
  if component['ref']=='C12':component['fp']='Capacitor_SMD:CP_Elec_6.3x5.8'
 for i,pos in enumerate([(14,14),(86,14),(13.5,56),(86,56)],1):
  p.append(part('H'+str(i),'M3 MOUNT','MountingHole:MountingHole_3.2mm_M3',{},pos,'MECHANICAL - NO PURCHASE'))
 return p
def symbol_schematic(name,parts,directory):
 root=uid(name+'/root'); libs=[];inst=[];rows=[]
 for i,p in enumerate(parts):
  ref=p['ref'];ident=uid(name+'/'+ref);x=70+(i%5)*140;y=65+(i//5)*70;h=max(5,len(p['pins'])*1.27+2.54);sym='P_'+ref
  inbom='no' if ref.startswith('H') and not p['pins'] else 'yes'
  body=f'(symbol "UMI:{sym}" (pin_names (offset 1)) (in_bom yes) (on_board yes) (property "Reference" {q(ref)} (at 0 {h+5} 0) (effects (font (size 1 1)))) (property "Value" {q(p["value"])} (at 0 {h+2.5} 0) (effects (font (size 1 1)))) (symbol "{sym}_0_1" (rectangle (start -15 {h}) (end 15 {-h}) (stroke (width .254) (type default)) (fill (type background)))) (symbol "{sym}_1_1" '
  for j,(num,(func,net)) in enumerate(p['pins'].items()):
   py=(len(p['pins'])-1)*1.27-j*2.54;typ=p['types'].get(num,'passive')
   body+=f'(pin {typ} line (at -20.08 {py} 0) (length 5.08) (name {q(func)} (effects (font (size .9 .9)))) (number {q(num)} (effects (font (size .9 .9)))))'
   gx=x-20.08;gy=y-py
   if net is None:inst.append(f'(no_connect (at {gx} {gy}) (uuid "{uid(ident+num)}"))')
   else:
    inst.append(f'(wire (pts (xy {gx} {gy}) (xy {gx-7.62} {gy})) (stroke (width 0) (type default)) (uuid "{uid(ident+num+"w")}"))')
    inst.append(f'(global_label {q(net)} (shape input) (at {gx-7.62} {gy} 0) (effects (font (size .9 .9)) (justify left bottom)) (uuid "{uid(ident+num+"l")}"))')
   rows.append([ref,p['mpn'],num,func,net or 'NC',typ,p['fp']])
  libs.append(body.replace('(in_bom yes)',f'(in_bom {inbom})')+'))')
  inst.append(f'(symbol (lib_id "UMI:{sym}") (at {x} {y} 0) (unit 1) (in_bom {inbom}) (on_board yes) (dnp no) (uuid "{ident}") (property "Reference" {q(ref)} (at {x} {y-h-5} 0) (effects (font (size 1.2 1.2)))) (property "Value" {q(p["value"])} (at {x} {y-h-2.5} 0) (effects (font (size 1 1)))) (property "Footprint" {q(p["fp"])} (at {x} {y} 0) (effects (font (size 1 1)) hide)) (property "MPN" {q(p["mpn"])} (at {x} {y} 0) (effects (font (size 1 1)) hide)) (instances (project "{name}" (path "/{root}" (reference "{ref}") (unit 1)))))')
 txt=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{root}") (paper "A1") (title_block (title "UMI circuit development") (rev "D2 - ENGINEERING HOLD")) (lib_symbols '+''.join(libs)+')'+''.join(inst)+')'
 write(directory/(name+'.kicad_sch'),parse(txt))
 with (directory/'pin_schedule.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Reference','MPN','Pin','Function','Net','Electrical type','Footprint']);w.writerows(rows)
 return root
def build_usb():
 name='USB_POWER';d=OUT/name;d.mkdir(exist_ok=True);local=d/'UMI_D2.pretty';local.mkdir(exist_ok=True)
 customs={'TI_RDF0022A_TPSM63610':rdf(),'USB_A_Wurth_614004190021':usb_fp()}
 parts=usb_parts()
 for p in parts:
  p['source_fp']=p['fp'];p['fp']='UMI_D2:'+p['fp'].split(':')[1]+('_R180' if p.get('rotation')==180 else '')
 root=symbol_schematic(name,parts,d)
 from validation_schematic_package import package_schematic
 package_schematic(d/(name+'.kicad_sch'),externally_driven_nets=['12V_PROTECTED','GND'])
 board=parse((BASE/'outputs/UMI_USB_D1/UMI_USB_D1.kicad_pcb').read_text())
 board[:]=[a for a in board if not(isinstance(a,list) and a[0] in ('footprint','net','gr_text','segment','via','zone'))]
 board[:]=[a for a in board if not(isinstance(a,list) and a[0].startswith('gr_') and one(a,'layer') and one(a,'layer')[1]=='Edge.Cuts')]
 board.append(parse(f'(gr_rect (start 10 10) (end 90 60) (stroke (width .05) (type solid)) (fill none) (layer "Edge.Cuts") (uuid "{uid("usb/expanded-outline")}"))'))
 layers=one(board,'layers');layers.insert(2,['4',Q('In1.Cu'),'signal']);layers.insert(3,['6',Q('In2.Cu'),'signal'])
 nets=sorted({n for p in parts for _,n in p['pins'].values() if n}|{f'unconnected-({p["ref"]}-{func}-Pad{num})' for p in parts for num,(func,n) in p['pins'].items() if n is None});codes={n:i+1 for i,n in enumerate(nets)}
 board.extend([['net',str(i),Q(n)] for n,i in codes.items()])
 for p in parts:
  fam,fn=p['source_fp'].split(':');f=copy.deepcopy(customs[fn]) if fam=='UMI_D2' else parse((LIB/(fam+'.pretty')/(fn+'.kicad_mod')).read_text())
  if p.get('rotation')==180:
   # Explicit library variant preserves this intentional passive land rotation.
   # The placed object and its library definition have identical local geometry.
   fn+='_R180';f[1]=Q(fn)
   for a in f:
    if not isinstance(a,list) or a[0] not in ('pad','fp_line','fp_rect','fp_arc','fp_poly','fp_text','property'):continue
    for tag in ('at','start','end','mid'):
     pt=one(a,tag)
     if pt:pt[1:3]=[str(-float(v)) for v in pt[1:3]]
    if a[0] in ('pad','fp_text','property'):
     pt=one(a,'at')
     if len(pt)==3:pt.append('180')
     else:pt[3]=str((float(pt[3])+180)%360)
    pts=one(a,'pts')
    if pts:
     for pt in pts[1:]:pt[1:3]=[str(-float(v)) for v in pt[1:3]]
   for model in all_(f,'model'):
    rz=one(one(model,'rotate'),'xyz');rz[3]=str((float(rz[3])+180)%360)
  # Library variant and placed variant share the identical pads.
  write(local/(fn+'.kicad_mod'),f)
  f[1]=Q('UMI_D2:'+fn)
  f[:]=[a for a in f if not(isinstance(a,list) and a[0] in ('version','generator','at','uuid','path','sheetfile','sheetname'))]
  f.extend([['at',*map(str,p['pos'])],['uuid',Q(uid(name+'/'+p['ref']+'/fp'))],['path',Q('/'+root+'/'+uid(name+'/'+p['ref']))],['sheetname',Q('')],['sheetfile',Q(name+'.kicad_sch')]])
  for k,v in [('Reference',p['ref']),('Value',p['value'])]:
   a=prop(f,k)
   if a:a[2]=Q(v)
   else:f.append(parse(f'(property {q(k)} {q(v)} (at 0 -4 0) (layer "F.Fab") (effects (font (size 1 1))))'))
  if p['ref'] in ('H1','H2','H3','H4','C1','C10','R7','R9'):
   one(prop(f,'Reference'),'layer')[1]=Q('F.Fab')
  if p['ref']=='C13':one(prop(f,'Reference'),'at')[1:]=['-3.5','0','90']
  f.append(parse(f'(property "MPN" {q(p["mpn"])} (at 0 0 0) (layer "F.Fab") (effects (font (size 1 1)) hide))'))
  for k,a in enumerate(all_(f,'pad')):
   num=str(a[1]);n=p['pins'].get(num,(None,None))[1]
   if num in p['pins'] and n is None:n=f'unconnected-({p["ref"]}-{p["pins"][num][0]}-Pad{num})'
   if n:a.append(['net',str(codes[n]),Q(n)])
   set_(a,'uuid',['uuid',Q(uid(name+'/'+p['ref']+'/pad/'+str(k)))])
  board.append(f)
 board.append(parse('(gr_text "USB POWER - ENGINEERING HOLD - NOT FOR ORDER" (at 50 65) (layer "Dwgs.User") (effects (font (size 1 1) (thickness .15))))'))
 for label,x,y,size in [('UMI USB POWER',50,13,1.2),('12V INPUT',21,26,1),('1:+12V 2:GND',21,28,1),('CHARGE ONLY',48,57,1)]:
  board.append(parse(f'(gr_text {q(label)} (at {x} {y}) (layer "F.SilkS") (uuid "{uid("usb-label/"+label)}") (effects (font (size {size} {size}) (thickness .15))))'))
 setup=one(board,'setup')
 set_(setup,'aux_axis_origin',['aux_axis_origin','10','60'])
 set_(setup,'capping',['capping','yes'])
 set_(setup,'filling',['filling','yes'])
 set_(setup,'stackup',parse('''(stackup
  (layer "F.SilkS" (type "Top Silk Screen"))
  (layer "F.Paste" (type "Top Solder Paste"))
  (layer "F.Mask" (type "Top Solder Mask") (thickness 0.01))
  (layer "F.Cu" (type "copper") (thickness 0.07))
  (layer "dielectric 1" (type "prepreg") (thickness 0.2) (material "FR4"))
  (layer "In1.Cu" (type "copper") (thickness 0.035))
  (layer "dielectric 2" (type "core") (thickness 0.97) (material "FR4"))
  (layer "In2.Cu" (type "copper") (thickness 0.035))
  (layer "dielectric 3" (type "prepreg") (thickness 0.2) (material "FR4"))
  (layer "B.Cu" (type "copper") (thickness 0.07))
  (layer "B.Mask" (type "Bottom Solder Mask") (thickness 0.01))
  (layer "B.Paste" (type "Bottom Solder Paste"))
  (layer "B.SilkS" (type "Bottom Silk Screen"))
  (copper_finish "ENIG") (dielectric_constraints no)
  (edge_connector no) (castellated_pads no) (edge_plating no))'''))
 write(d/(name+'.kicad_pcb'),board)
 (d/(name+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':name+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_clearance':.2,'min_track_width':.2,'min_via_diameter':.45,'min_through_hole_diameter':.25,'min_via_annular_width':.1,'min_copper_edge_clearance':.25}}}},indent=2))
 (d/'fp-lib-table').write_text('(fp_lib_table (lib (name "UMI_D2") (type "KiCad") (uri "${KIPRJMOD}/UMI_D2.pretty") (options "") (descr "UMI D2 footprints")))')
 (d/'design.json').write_text(json.dumps(parts,indent=2))
 return d,len(parts)
if __name__=='__main__':print(build_usb())
