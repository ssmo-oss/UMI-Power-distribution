from pathlib import Path
import sys,shutil,math,copy,uuid,json
sys.path.insert(0,'work');from design_d2 import *
src=Path('outputs/UMI_TWO_BOARD_DESIGN/USB_POWER');dst=Path('outputs/UMI_D3/USB_POWER');dst.mkdir(parents=True,exist_ok=True)
for name in ['USB_POWER.kicad_pcb','USB_POWER.kicad_sch','USB_POWER.kicad_pro','fp-lib-table','sym-lib-table','UMI.kicad_sym','design.json']:
 shutil.copy2(src/name,dst/name)
shutil.copytree(src/'UMI_D2.pretty',dst/'UMI_D2.pretty',dirs_exist_ok=True)
b=parse((dst/'USB_POWER.kicad_pcb').read_text());placements={'U1':(48,18.5),'C1':(41.6,19.45),'R7':(39.2,25),'R9':(57,28.8),'C3':(43.2,33.8),'C9':(48,33.8),'C10':(52.8,33.8),'C13':(44,39.4),'C14':(50,39.4)}
for f in all_(b,'footprint'):
 ref=str(prop(f,'Reference')[2]);atf=one(f,'at');ox,oy=map(float,atf[1:3])
 if ref in ['H1','H3']:atf[1]='13.5'
 if ref in ['H2','H4']:atf[1]='86.5'
 if ref in placements:
  r=prop(f,'Reference');x,y=placements[ref];one(r,'at')[1:]=[str(x-ox),str(y-oy),'0'];one(r,'layer')[1]=Q('F.SilkS');font=one(one(r,'effects'),'font');one(font,'size')[1:]=['1','1'];font.append(['thickness','0.15']) if one(font,'thickness') is None else None
# Consistent port labels occupy clear area above connector edge.
for txt,x,y in [('PORT 1  5V / 3A',25.5,54),('PORT 2  5V / 3A',68.5,54)]:
 b.append(['gr_text',Q(txt),['at',str(x),str(y),'0'],['layer',Q('F.SilkS')],['effects',['font',['size','1','1'],['thickness','.15']]],['uuid',Q(str(uuid.uuid4()))]])
# Chamfer only degree-two back-layer 90degree nodes away from vias/pads.
segments=all_(b,'segment');nodes={}
for s in segments:
 if one(s,'layer')[1]!='B.Cu':continue
 for tag in ['start','end']:
  xy=tuple(map(float,one(s,tag)[1:3]));nodes.setdefault(xy,[]).append((s,tag))
viaxy={tuple(map(float,one(v,'at')[1:3])) for v in all_(b,'via')};changes=[]
for xy,ss in nodes.items():
 if len(ss)!=2 or xy in viaxy:continue
 (a,ta),(c,tc)=ss
 if one(a,'net')!=one(c,'net') or one(a,'width')!=one(c,'width'):continue
 pa=tuple(map(float,one(a,'end' if ta=='start' else 'start')[1:3]));pc=tuple(map(float,one(c,'end' if tc=='start' else 'start')[1:3]));va=[pa[i]-xy[i] for i in range(2)];vc=[pc[i]-xy[i] for i in range(2)];la=math.hypot(*va);lc=math.hypot(*vc)
 if min(la,lc)<2 or abs(sum(va[i]*vc[i] for i in range(2)))>1e-7:continue
 d=min(.8,la*.2,lc*.2);aa=[xy[i]+va[i]*d/la for i in range(2)];cc=[xy[i]+vc[i]*d/lc for i in range(2)];one(a,ta)[1:]=list(map(str,aa));one(c,tc)[1:]=list(map(str,cc));new=copy.deepcopy(a);one(new,'start')[1:]=list(map(str,aa));one(new,'end')[1:]=list(map(str,cc));one(new,'uuid')[1]=Q(str(uuid.uuid4()));b.append(new);changes.append(xy)
write(dst/'USB_POWER.kicad_pcb',b);print('chamfered',len(changes),changes)
(dst/'D3_changes.json').write_text(json.dumps({'backside_chamfered_nodes':changes,'silk_reference_positions':placements,'mounting_holes_x':[13.5,86.5]},indent=2))


