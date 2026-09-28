"""Main power circuit capture; engineering hold until layout and validation finish."""
from design_d2 import *
from efuse_footprint import footprint as efuse_land, PIN_FUNCTIONS
from main_reference_layout import reference_parts,rotate_footprint,dense_passive_courtyard

def panasonic_g_land():
 # Panasonic FK catalog ABA0000C1181, 2026-02-10, p2: G land a=4.6,b=4.1,c=2.0 mm.
 f=custom('Panasonic_FK_G_10x10.2');f.extend([rect(-6.65,-5.65,6.65,5.65,'F.CrtYd',.05),rect(-5.15,-5.15,5.15,5.15,'F.Fab')])
 f.extend([pad('1',-4.35,0,4.1,2),pad('2',4.35,0,4.1,2)])
 f.append(parse('(fp_text user "+" (at -3.4 -3.7) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))'))
 return f

def phoenix_land():
 # Manufacturer drilling plan, 1709681 datasheet 2025-03-21 p7.
 # Origin is rear left body corner; pin-1 pair is rear row, pin-2 pair is forward row.
 f=custom('Phoenix_1709681');f.extend([rect(-.5,-.5,20.82,19.2,'F.CrtYd',.05),rect(0,0,20.32,18.7,'F.Fab')])
 for n,x,y in [('1',2.98,1.96),('1',6.98,1.96),('2',13.14,12.12),('2',17.14,12.12)]:f.append(pad(n,x,y,3.2,3.2,1.5))
 return f

def mosfet_land():
 f=parse((LIB/'Package_TO_SOT_SMD.pretty/TDSON-8-1.kicad_mod').read_text())
 f[1]=Q('BSC072N08NS5_TDSON_8')
 # KiCad's base land merges drains 5-8 into copper pad 5. Preserve the explicit
 # manufacturer lead numbers in the netlist with overlapping same-net copper.
 for n,y in [('6',.635),('7',-.635),('8',-1.905)]:
  p=pad(n,2.905,y,.75,.5,paste=False);set_(p,'layers',['layers',Q('F.Cu')]);f.append(p)
 return f

def inductor_land():
 f=custom('Coilcraft_SER2915H');f.append(rect(-13.95,-9.9,13.95,9.9,'F.Fab'))
 outline=[(-14.45,-10.4),(14.45,-10.4),(14.45,10.4),(8.24,10.4),(8.24,17.65),(1.91,17.65),(1.91,10.4),(-1.91,10.4),(-1.91,17.65),(-8.24,17.65),(-8.24,10.4),(-14.45,10.4)]
 for a,z in zip(outline,outline[1:]+outline[:1]):f.append(parse(f'(fp_line (start {a[0]} {a[1]}) (end {z[0]} {z[1]}) (stroke (width .05) (type default)) (layer "F.CrtYd"))'))
 f.extend([pad('1',-5.075,14.355,5.33,5.59),pad('2',5.075,14.355,5.33,5.59),pad('3',0,-7.46,6.35,5.28)])
 return f

def main_parts():
 p=[]
 def add2(ref,value,fp,a,z,pos,mpn=''):p.append(two(ref,value,fp,a,z,pos,mpn))
 conn='Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical'
 fuse='Fuse:FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165'
 p.append(part('J1','12V PSU INPUT','UMI_Custom:Phoenix_1709681',{'1':('+12V','12V_IN'),'2':('RETURN','GND')},(39,23),'1709681'))
 for i,(label,net,fval,fpos,jpos) in enumerate([
  ('JETSON 12V 5A','JETSON_12V','7.5A',(17,45),(21,55)),
  ('SG4A 12V 4A','SG4A_12V','7.5A',(50,45),(54,55)),
  ('FAN 12V 0.14A','FAN_12V','1A',(17,63),(21,73)),
  ('USB BOARD 12V','USB_12V','5A',(50,63),(54,73))],1):
  add2('F'+str(i),fval+' FUSE HOLDER',fuse,'12V_IN',net,fpos,'178.6165.0001')
  p.append(part('J'+str(i+1),label,conn,{'1':('+12V',net),'2':('RETURN','GND')},jpos,'B2P-VH(LF)(SN)'))
 add2('F5','10A BOOST INPUT FUSE HOLDER',fuse,'12V_IN','FUSED_BOOST_12V',(66,30),'178.6165.0001')
 add2('F6','3A 80V BOOST OUTPUT FUSE HOLDER',fuse,'53V5_RAW','SWITCH_53V5',(146,89),'178.6165.0001')
 p.append(part('J6','SWITCH 53.5V 1.31A','Connector_JST:JST_VH_B3P-VH_1x03_P3.96mm_Vertical',{'1':('+53V5','SWITCH_53V5'),'2':('NC',None),'3':('RETURN','GND')},(144,101),'B3P-VH(LF)(SN)'))
 pins={
 '1':('SYNCOUT',None),'2':('OPT','OPT'),'3':('CSN','CSN'),'4':('CSP','CSP'),'5':('VIN','IC_VIN'),
 '6':('UVLO','UVLO'),'7':('SS','SS'),'8':('RT','RT'),'9':('AGND','GND'),'10':('FB','FB'),
 '11':('COMP','COMP'),'12':('SLOPE','SLOPE'),'13':('MODE','MODE'),'14':('RES','RES'),'15':('PGND','GND'),
 '16':('LO','LO'),'17':('VCC','VCC'),'18':('SW','SW'),'19':('HO','HO'),'20':('BST','BST'),'21':('EP','GND')}
 p.append(part('U1','LM5122MHX/NOPB','Package_SO:HTSSOP-20-1EP_4.4x6.5mm_P0.65mm_EP3.4x6.5mm_Mask2.4x3.7mm',pins,(125,78),types={'5':'power_in','17':'power_out','3':'input','4':'input','6':'input','10':'input','16':'output','19':'output'}))
 p.append(part('L1','10uH','UMI_D2:Coilcraft_SER2915H',{'1':('IN','SENSE_LOW'),'2':('OUT','SW'),'3':('MOUNT',None)},(110,25),'SER2915H-103KL'))
 add2('L2','1uH','Inductor_SMD:L_Coilcraft_XAL4020-XXX','BOOST_OUT','53V5_RAW',(145,62),'XAL4020-102MEB')
 for ref,source,drain,gate,pos in [('Q1','SW','BOOST_OUT','HO',(145,50)),('Q2','GND','SW','GATE2',(125,50)),('Q3','GND','SW','GATE3',(135,50))]:
  p.append(part(ref,'BSC072N08NS5ATMA1','UMI_D2:BSC072N08NS5_TDSON_8',{str(n):('S' if n<4 else 'G' if n==4 else 'D',source if n<4 else gate if n==4 else drain) for n in range(1,9)},pos))
 caps=[
 ('C1','470pF 100V','SW','SNUB',(137,44),'GRM2165C2A471JA01D','0805'),
 ('C2','4.7uF 80V','BOOST_IN','GND',(91,36),'GRM32ER71K475KE14L','1210'),
 ('C3','4.7uF 80V','BOOST_IN','GND',(92,46),'GRM32ER71K475KE14L','1210'),
 ('C4','4.7uF 80V','BOOST_IN','GND',(91,41),'GRM32ER71K475KE14L','1210'),
 ('C5','4.7uF 80V','BOOST_OUT','GND',(125,58),'GRM32ER71K475KE14L','1210'),
 ('C6','4.7uF 80V','BOOST_OUT','GND',(130,58),'GRM32ER71K475KE14L','1210'),
 ('C7','4.7uF 80V','BOOST_OUT','GND',(135,58),'GRM32ER71K475KE14L','1210'),
 ('C8','4.7uF 80V','BOOST_OUT','GND',(140,58),'GRM32ER71K475KE14L','1210'),
 ('C9','100nF 25V','BST','SW',(135,73),'GRM188R71E104KA01D','0603'),
 ('C10','100pF 50V','CSP','CSN',(114,73),'GRM1885C1H101JA01D','0603'),
 ('C11','1uF 16V','VCC','GND',(136,78),'GCM188R71C105KA64D','0603'),
 ('C13','100pF 50V','UVLO','GND',(114,84),'GRM1885C1H101JA01D','0603'),
 ('C14','47nF 25V','RES','GND',(132,84),'GRM188R71E473KA01D','0603'),
 ('C15','470nF 100V','IC_VIN','GND',(119,71),'GRM21BR72A474KA73L','0805'),
 ('C16','100nF 25V','SS','GND',(118,84),'GRM188R71E104KA01D','0603'),
 ('C17','1500pF 50V','COMP','FB',(126,89),'GRM1885C1H152JA01D','0603'),
 ('C18','15nF 50V','COMP','COMP_RC',(130,92),'GRM188R71H153KA01D','0603')]
 fps={'0603':C,'0805':'Capacitor_SMD:C_0805_2012Metric','1210':C1210}
 for ref,val,a,z,pos,mpn,size in caps:add2(ref,val,fps[size],a,z,pos,mpn)
 for ref,net,pos in [('C19','BOOST_IN',(88,23)),('C20','53V5_RAW',(155,64))]:
  p.append(part(ref,'47uF 80V','UMI_D2:Panasonic_FK_G_10x10.2',{'1':('+',net),'2':('-','GND')},pos,'EEE-FK1K470P'))
 resistors=[
 ('R1','7.5','SNUB','BOOST_OUT',(143,44),'ERJ-12ZYJ7R5U','Resistor_SMD:R_2010_5025Metric'),
 ('R2','4mOhm','BOOST_IN','SENSE_LOW',(103,48),'ERJ-M1WSF4M0U','Resistor_SMD:R_2512_6332Metric'),
 ('R3','100','BOOST_IN','CSP',(108,73),'ESR03EZPJ101',R),('R4','100','SENSE_LOW','CSN',(108,76),'ESR03EZPJ101',R),
 ('R5','0','LO','GATE2',(125,64),'ERJ-3GEY0R00V',R),('R21','0','LO','GATE3',(135,64),'ERJ-3GEY0R00V',R),
 ('R8','0','OPT','GND',(118,76),'ERJ-3GEY0R00V',R),
 ('R10','49.9k','BOOST_IN','UVLO',(108,81),'CRCW060349K9FKEA',R),
 ('R11','3.3','BOOST_IN','IC_VIN',(114,70),'CRCW06033R30JNEA',R),
 ('R12','0','VCC','MODE',(136,81),'ERJ-3GEY0R00V',R),
 ('R13','8.45k','UVLO','GND',(108,84),'CRCW06038K45FKEA',R),
 ('R14','30k','SLOPE','GND',(132,87),'CRCW060330K0JNEA',R),
 ('R16','40.2k','RT','GND',(118,88),'CRCW060340K2FKEA',R),
 ('R17','20.5k','FB','COMP_RC',(130,95),'CRCW060320K5FKEA',R),
 ('R18','1.96k 0.1%','FB','GND',(121,92),'RT0603BRD071K96L',R),
 ('R19','84.5k 0.1%','FB_HIGH','FB',(121,95),'RT0603BRD0784K5L',R),
 ('R20','931 0.1%','53V5_RAW','FB_HIGH',(116,95),'RT0603BRD07931RL',R)]
 for ref,val,a,z,pos,mpn,fp in resistors:add2(ref,val,fp,a,z,pos,mpn)
 p.append(part('D2','MBR1H100SFT3G','Diode_SMD:D_SOD-123F',{'1':('K','BST'),'2':('A','VCC')},(140,73)))
 enets={'IN':'FUSED_BOOST_12V','OUT':'BOOST_IN','GND':'GND','EN_UVLO':'EFUSE_EN','ITIMER':None,'ILIM':'EFUSE_ILIM','IMON':'EFUSE_IMON','RETRY_DLY':'GND','NRETRY':None,'LDSTRT':'GND','PG':'UVLO','DVDT':'EFUSE_DVDT'}
 p.append(part('U2','TPS259824ONRGER','UMI_D2:TI_RGE0024M_TPS25982',{n:(fn,enets[fn]) for n,fn in PIN_FUNCTIONS.items()},(79,60),types={'1':'power_in','25':'power_in','17':'power_out','6':'input','13':'open_collector'}))
 for ref,value,a,z,pos,mpn in [
  ('R22','100k 0.1%','FUSED_BOOST_12V','EFUSE_EN',(73,57),'RT0603BRD07100KL'),
  ('R23','13.7k 0.1%','EFUSE_EN','GND',(74.65,60),'RT0603BRD0713K7L'),
  ('R24','182 0.1%','EFUSE_ILIM','GND',(76,65),'RT0603BRD07182RL'),
  ('R25','511 0.1%','EFUSE_IMON','GND',(81,65),'RT0603BRD07511RL')]:add2(ref,value,R,a,z,pos,mpn)
 add2('C21','1uF 50V X7R','Capacitor_SMD:C_0805_2012Metric','FUSED_BOOST_12V','GND',(73,52),'GRM21BR71H105KA12L')
 add2('C22','100nF 50V',C,'FUSED_BOOST_12V','GND',(73,49),'GRM188R71H104KA93D')
 add2('C23','6.8nF 50V C0G',C,'EFUSE_DVDT','GND',(85,60),'GRM1885C1H682JA01D')
 p.append(part('D3','SMBJ15A','Diode_SMD:D_SMB',{'1':('K','FUSED_BOOST_12V'),'2':('A','GND')},(72,70),'SMBJ15A'))
 p.append(part('D4','SS10P4-M3/86A','Package_TO_SOT_SMD:TO-277A',{'1':('A1','GND'),'2':('A2','GND'),'3':('K','BOOST_IN')},(79,53)))
 return p

def reflow_schematic(name,parts,d):
 """Align electrical endpoints to the KiCad 1.27 mm grid and provide real library."""
 path=d/(name+'.kicad_sch');sch=parse(path.read_text());owners={}
 for i,p in enumerate(parts):
  ident=uid(name+'/'+p['ref']);dx=69.85+(i%8)*139.7-(70+(i%5)*140);dy=64.77+(i//8)*69.85-(65+(i//5)*70)
  owners[ident]=(dx,dy,False)
  for n in p['pins']:
   for suffix in ('','w','l'):owners[uid(ident+n+suffix)]=(dx-.24,dy,True)
 def shift(node,dx,dy):
  if not isinstance(node,list):return
  if node and node[0] in ('at','xy'):
   node[1:3]=[str(round(float(node[1])+dx,6)),str(round(float(node[2])+dy,6))]
  for child in node:
   if isinstance(child,list):shift(child,dx,dy)
 for node in sch:
  if not isinstance(node,list):continue
  ident=one(node,'uuid')
  if ident and str(ident[1]) in owners:
   dx,dy,_=owners[str(ident[1])];shift(node,dx,dy)
 libs=one(sch,'lib_symbols')
 for symbol in libs[1:]:
  for sub in all_(symbol,'symbol'):
   for pn in all_(sub,'pin'):one(pn,'at')[1]='-20.32'
 set_(sch,'paper',['paper',Q('A0')])
 # Explicit source declaration after the VIN filter resistor. It is a boardless
 # power flag, not an extra component to assemble.
 flag=parse('(symbol "UMI:PWR_IC_VIN" (power) (pin_names (offset 0)) (in_bom no) (on_board no) (property "Reference" "#FLG" (at 0 0 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at 0 2.54 0) (effects (font (size 1 1)))) (symbol "PWR_IC_VIN_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.27 1.905) (xy 0 2.54) (xy 1.27 1.905) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))) (symbol "PWR_IC_VIN_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))))')
 libs.append(flag);fx,fy=1066.8,762
 sch.append(parse(f'(symbol (lib_id "UMI:PWR_IC_VIN") (at {fx} {fy} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{uid(name+"/powerflag")}") (property "Reference" "#FLG01" (at {fx} {fy} 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at {fx} {fy-3.81} 0) (effects (font (size 1 1)))) (instances (project "{name}" (path "/{uid(name+"/root")}" (reference "#FLG01") (unit 1)))))'))
 sch.append(parse(f'(global_label "IC_VIN" (shape input) (at {fx} {fy} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid(name+"/powerflaglabel")}"))'))
 sch.append(parse(f'(symbol (lib_id "UMI:PWR_IC_VIN") (at {fx} {fy-25.4} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{uid(name+"/efusepowerflag")}") (property "Reference" "#FLG02" (at {fx} {fy-25.4} 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at {fx} {fy-29.21} 0) (effects (font (size 1 1)))) (instances (project "{name}" (path "/{uid(name+"/root")}" (reference "#FLG02") (unit 1)))))'))
 sch.append(parse(f'(global_label "FUSED_BOOST_12V" (shape input) (at {fx} {fy-25.4} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{uid(name+"/efusepowerflaglabel")}"))'))
 write(path,sch)
 library=['kicad_symbol_lib',['version','20241209'],['generator',Q('kicad_symbol_editor')]]
 for symbol in libs[1:]:
  lib=copy.deepcopy(symbol);lib[1]=Q(str(lib[1]).split(':',1)[-1]);library.append(lib)
 write(d/'UMI.kicad_sym',library)
 (d/'sym-lib-table').write_text('(sym_lib_table (lib (name "UMI") (type "KiCad") (uri "${KIPRJMOD}/UMI.kicad_sym") (options "") (descr "UMI main circuit symbols")))')

def build():
 name='MAIN_POWER';d=OUT/name;d.mkdir(exist_ok=True);local=d/'UMI_D2.pretty';local.mkdir(exist_ok=True)
 source=parse((BASE/'outputs/UMI_revD_split_PLACEMENT_DRAFT/UMI_MAIN_placement_ONLY.kicad_pcb').read_text())
 inherited={str(f[1]):f for f in all_(source,'footprint')}
 customs={'UMI_D2:Coilcraft_SER2915H':inductor_land(),'UMI_D2:Panasonic_FK_G_10x10.2':panasonic_g_land(),'UMI_Custom:Phoenix_1709681':phoenix_land(),'UMI_D2:BSC072N08NS5_TDSON_8':mosfet_land(),'UMI_D2:TI_RGE0024M_TPS25982':efuse_land()}
 parts=main_parts()
 reference_report=reference_parts(parts,customs,inherited)
 for p in parts:
  p['source_fp']=p['fp'];p['fp']='UMI_D2:'+p['fp'].split(':')[1]+('_R'+str(p['rotation']) if p.get('rotation') else '')
 holes=[]
 for f in all_(source,'footprint'):
  ref=str(prop(f,'Reference')[2])
  if ref.startswith('H'):holes.append(part(ref,str(prop(f,'Value')[2]),'UMI_D2:'+str(f[1]).split(':')[-1],{},tuple(map(float,one(f,'at')[1:3])),'MECHANICAL'))
 root=symbol_schematic(name,parts+holes,d)
 reflow_schematic(name,parts+holes,d)
 # Original mounting holes are retained. The user authorized a larger outline.
 board=copy.deepcopy(source)
 set_(board,'layers',parse('(layers (0 "F.Cu" signal) (4 "In1.Cu" signal) (6 "In2.Cu" signal) (2 "B.Cu" signal) (13 "F.Paste" user) (15 "B.Paste" user) (5 "F.SilkS" user) (7 "B.SilkS" user) (1 "F.Mask" user) (3 "B.Mask" user) (17 "Dwgs.User" user) (19 "Cmts.User" user) (25 "Edge.Cuts" user) (27 "Margin" user) (31 "F.CrtYd" user) (29 "B.CrtYd" user) (35 "F.Fab" user) (33 "B.Fab" user))'))
 board[:]=[a for a in board if not(isinstance(a,list) and (a[0] in ('net','segment','via','zone','gr_text') or (a[0]=='footprint' and not str(prop(a,'Reference')[2]).startswith('H')) or (a[0].startswith('gr_') and one(a,'layer') and one(a,'layer')[1]=='Edge.Cuts')))]
 for hole in all_(board,'footprint'):
  fn=str(hole[1]).split(':')[-1];hole[1]=Q('UMI_D2:'+fn)
  ref=str(prop(hole,'Reference')[2]);set_(hole,'path',['path',Q('/'+root+'/'+uid(name+'/'+ref))])
  set_(hole,'attr',['attr','exclude_from_pos_files','exclude_from_bom'])
  hole.append(parse('(property "MPN" "MECHANICAL" (at 0 0 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1))))'))
  hf=copy.deepcopy(hole);hf[1]=Q(fn)
  hf[:]=[a for a in hf if not(isinstance(a,list) and a[0] in ('at','uuid','path','sheetfile','sheetname'))]
  write(local/(fn+'.kicad_mod'),hf)
 board.append(parse('(gr_rect (start 10 10) (end 168 110.263962) (stroke (width .05) (type solid)) (fill none) (layer "Edge.Cuts") (uuid "'+uid('main/outline')+'"))'))
 def pcb_net(p,pin):
  fn,n=p['pins'][pin]
  return n if n else 'unconnected-('+p['ref']+'-'+fn+'-Pad'+pin+')'
 nets=sorted({pcb_net(p,pin) for p in parts for pin in p['pins']});codes={n:i+1 for i,n in enumerate(nets)}
 board.extend([['net',str(i),Q(n)] for n,i in codes.items()])
 for p in parts:
  ident=p['source_fp'];fam,fn=ident.split(':')
  if ident in customs:f=copy.deepcopy(customs[ident])
  elif ident in inherited:f=copy.deepcopy(inherited[ident])
  else:f=parse((LIB/(fam+'.pretty')/(fn+'.kicad_mod')).read_text())
  f=rotate_footprint(f,p.get('rotation',0));fn=p['fp'].split(':')[1];f[1]=Q(fn)
  if p['ref'][0] in 'RC' and p['ref'] not in ('C19','C20'):f=dense_passive_courtyard(f)
  if not p['ref'].startswith(('F','J')):
   # Dense converter markings belong in the assembly drawing; generic reference
   # texts otherwise cross adjacent pads in the manufacturer reference placement.
   for n in f:
    if isinstance(n,list) and one(n,'layer') and one(n,'layer')[1]=='F.SilkS':one(n,'layer')[1]=Q('F.Fab')
  set_(f,'attr',['attr','through_hole' if p['ref'].startswith(('F','J')) else 'smd'])
  f[:]=[a for a in f if not(isinstance(a,list) and a[0] in ('at','uuid','path','sheetfile','sheetname'))]
  for pa in all_(f,'pad'):pa[:]=[a for a in pa if not(isinstance(a,list) and a[0] in ('net','uuid','pinfunction','pintype'))]
  def refresh_ids(node,path=''):
   if not isinstance(node,list):return
   if node and node[0]=='uuid':node[1]=Q(uid(name+'/'+p['ref']+'/nested/'+path))
   for j,child in enumerate(node):
    if isinstance(child,list):refresh_ids(child,path+'/'+str(j))
  refresh_ids(f)
  write(local/(fn+'.kicad_mod'),f)
  f[1]=Q('UMI_D2:'+fn);f[:]=[a for a in f if not(isinstance(a,list) and a[0] in ('version','generator'))]
  f.extend([['at',*map(str,p['pos'])],['uuid',Q(uid(name+'/'+p['ref']+'/fp'))],['path',Q('/'+root+'/'+uid(name+'/'+p['ref']))],['sheetname',Q('')],['sheetfile',Q(name+'.kicad_sch')]])
  for key,value in [('Reference',p['ref']),('Value',p['value']),('MPN',p['mpn'])]:
   a=prop(f,key)
   if a:a[2]=Q(value)
   else:f.append(parse(f'(property {q(key)} {q(value)} (at 0 -4 0) (layer "F.Fab") '+('(hide yes) ' if key=='MPN' else '')+'(effects (font (size 1 1))))'))
  for k,pa in enumerate(all_(f,'pad')):
   net=pcb_net(p,str(pa[1])) if str(pa[1]) in p['pins'] else None
   if net:pa.append(['net',str(codes[net]),Q(net)])
   pa.append(['uuid',Q(uid(name+'/'+p['ref']+'/pad/'+str(k)))])
  board.append(f)
 board.append(parse('(gr_text "MAIN POWER - ENGINEERING HOLD / ROUTING INCOMPLETE" (at 88 115) (layer "Dwgs.User") (effects (font (size 1.5 1.5) (thickness .2))))'))
 set_(one(board,'general'),'thickness',['thickness','1.2'])
 setup=one(board,'setup');set_(setup,'aux_axis_origin',['aux_axis_origin','10','110.263962'])
 set_(setup,'stackup',parse('''(stackup
 (layer "F.SilkS" (type "Top Silk Screen")) (layer "F.Paste" (type "Top Solder Paste"))
 (layer "F.Mask" (type "Top Solder Mask") (thickness .01))
 (layer "F.Cu" (type "copper") (thickness .07))
 (layer "dielectric 1" (type "prepreg") (thickness .2) (material "FR4"))
 (layer "In1.Cu" (type "copper") (thickness .035))
 (layer "dielectric 2" (type "core") (thickness .57) (material "FR4"))
 (layer "In2.Cu" (type "copper") (thickness .035))
 (layer "dielectric 3" (type "prepreg") (thickness .2) (material "FR4"))
 (layer "B.Cu" (type "copper") (thickness .07))
 (layer "B.Mask" (type "Bottom Solder Mask") (thickness .01))
 (layer "B.Paste" (type "Bottom Solder Paste")) (layer "B.SilkS" (type "Bottom Silk Screen"))
 (copper_finish "ENIG") (dielectric_constraints no) (edge_connector no) (castellated_pads no) (edge_plating no))'''))
 write(d/(name+'.kicad_pcb'),board)
 (d/(name+'.kicad_pro')).write_text(json.dumps({'meta':{'filename':name+'.kicad_pro','version':1},'board':{'design_settings':{'rules':{'min_through_hole_diameter':.25,'min_track_width':.15,'min_via_diameter':.5,'min_via_annular_width':.1,'min_copper_edge_clearance':.5,'min_hole_to_hole':.2}}}},indent=2))
 (d/'fp-lib-table').write_text('(fp_lib_table (lib (name "UMI_D2") (type "KiCad") (uri "${KIPRJMOD}/UMI_D2.pretty") (options "") (descr "UMI D2 footprints")))')
 (d/'design.json').write_text(json.dumps(parts,indent=2))
 (d/'reference_placement.json').write_text(json.dumps(dict(source='TI PMP21274_REVA.PcbDoc from https://www.ti.com/lit/zip/TIDRTY5',scope='Reference placement transplanted using matching electrical-pad centers; land patterns remain reviewed local KiCad footprints.',parts=reference_report),indent=2))
 (d/'README.md').write_text('''# MAIN_POWER — engineering hold

This is the main distribution and boost board, not another USB-board revision.
The enlarged provisional outline is 158 x 100.263962 mm. The four inherited mounting holes remain in place; enclosure integration is deferred with user authorization.

The boost circuit is captured from TI PMP21274, with the feedback divider changed to a nominal 53.5 V. This is an unvalidated adaptation, not a manufacturing release. The reference inductor and parallel low-side MOSFETs are retained. Optional unpopulated reference parts are omitted.

Outstanding: circuit review, input fault interruption, fuse coordination and exact fuse ordering codes, inherited terminal-footprint verification, package/land-pattern verification, component placement, routing and thermal design, power startup/stability checks, KiCad ERC/DRC, assembly sourcing and fabrication exports. No fabrication files are supplied.

Reference: https://www.ti.com/tool/PMP21274
Controller: https://www.ti.com/lit/ds/symlink/lm5122.pdf
Inductor land pattern: https://www.coilcraft.com/getmedia/a2805f49-c9b8-42c0-9939-b2d75eed7288/ser2900.pdf
''')
 print(name,len(parts),'electrical components; original holes retained; unrouted engineering hold')
if __name__=='__main__':build()

