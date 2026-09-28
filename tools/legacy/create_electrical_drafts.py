"""Write review schematics using only Python's standard library; no pcbnew runtime."""
from pathlib import Path
from uuid import uuid4
import json,csv
out=Path('outputs/UMI_revD_electrical_draft');out.mkdir(parents=True,exist_ok=True)
def uid():return str(uuid4())
def q(s):return json.dumps(str(s))
def schematic(name,title,parts,notes):
 root=uid();lib=[];items=[];rows=[]
 for index,(ref,value,pins,footprint) in enumerate(parts):
  x=55+(index%3)*90;y=40+(index//3)*45
  sym='D_'+ref;n=len(pins);h=max(5,(n-1)*1.27+2.54)
  body=f'(symbol "Draft:{sym}" (pin_names (offset 1)) (in_bom yes) (on_board yes) (property "Reference" "{ref}" (at 0 {h+5} 0) (effects (font (size 1 1)))) (property "Value" {q(value)} (at 0 {h+2.5} 0) (effects (font (size 1 1)))) (symbol "{sym}_0_1" (rectangle (start -12 {h}) (end 12 {-h}) (stroke (width .254) (type default)) (fill (type background)))) (symbol "{sym}_1_1" '
  for j,(num,pname,net) in enumerate(pins):
   py=(n-1)*1.27-j*2.54
   body+=f'(pin passive line (at -17.08 {py} 0) (length 5.08) (name {q(pname)} (effects (font (size .9 .9)))) (number {q(num)} (effects (font (size .9 .9)))))'
  lib.append(body+'))')
  id=uid()
  items.append(f'(symbol (lib_id "Draft:{sym}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid "{id}") (property "Reference" "{ref}" (at {x} {y-h-5} 0) (effects (font (size 1.1 1.1)))) (property "Value" {q(value)} (at {x} {y-h-2.5} 0) (effects (font (size .9 .9)))) (property "Footprint" {q(footprint)} (at {x} {y} 0) (effects (font (size 1 1)) hide)) (instances (project "{name}" (path "/{root}" (reference "{ref}") (unit 1)))))')
  for j,(num,pname,net) in enumerate(pins):
   py=y-((n-1)*1.27-j*2.54);px=x-17.08
   if net is None:
    items.append(f'(no_connect (at {px} {py}) (uuid "{uid()}"))')
   else:
    items.append(f'(wire (pts (xy {px} {py}) (xy {px-5.08} {py})) (stroke (width 0) (type default)) (uuid "{uid()}"))')
    items.append(f'(label {q(net)} (at {px-5.08} {py} 0) (effects (font (size .9 .9)) (justify left bottom)) (uuid "{uid()}"))')
   rows.append([ref,value,num,pname,net or 'NC',footprint])
 for i,note in enumerate(notes):
  items.append(f'(text {q(note)} (at 15 {15+i*5} 0) (effects (font (size 1.2 1.2)) (justify left bottom)) (uuid "{uid()}"))')
 txt=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{root}") (paper "A2") (title_block (title {q(title)}) (rev "D0 - DESIGN REVIEW ONLY")) (lib_symbols '+''.join(lib)+')'+''.join(items)+')'
 (out/(name+'.kicad_sch')).write_text(txt)
 with (out/(name+'_connections.csv')).open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Reference','Value','Pin','Function','Net','Candidate footprint']);w.writerows(rows)
def two(ref,val,a,b,fp=''):
 return(ref,val,[('1','1',a),('2','2',b)],fp)
usb=[
 two('J1','12V from main board','12V_USB_IN','GND','Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical'),
 ('U1','OKR-T/10-W12-C candidate',[('1','ON_OFF',None),('2','VIN','12V_USB_IN'),('3','GND','GND'),('4','VOUT','5V_BUS'),('5','TRIM','TRIM')],''),
 two('R1','267R 0.1% - verify module trim','TRIM','GND','Resistor_SMD:R_0603_1608Metric'),
 two('C1','22uF 25V effective C TBD','12V_USB_IN','GND','Capacitor_SMD:C_1210_3225Metric'),
 two('C2','1uF 10V','5V_BUS','GND','Capacitor_SMD:C_0805_2012Metric'),
 two('C3','10uF 10V','5V_BUS','GND','Capacitor_SMD:C_1206_3216Metric'),
]
for port in [1,2]:
 usb.append(('U'+str(port+1),'TPS2557DRB',[('1','GND','GND'),('2','IN','5V_BUS'),('3','IN','5V_BUS'),('4','EN','5V_BUS'),('5','ILIM','ILIM'+str(port)),('6','OUT','VBUS'+str(port)),('7','OUT','VBUS'+str(port)),('8','FAULT','FAULT'+str(port)),('9','EP','GND')],'Package_SON:VSON-8-1EP_3x3mm_P0.65mm_EP1.65x2.4mm'))
 usb.append(two('R'+str(port+1),'32.4k 0.1%','ILIM'+str(port),'GND','Resistor_SMD:R_0603_1608Metric'))
 usb.append(two('C'+str(port+3),'100nF local','5V_BUS','GND','Capacitor_SMD:C_0603_1608Metric'))
 usb.append(two('C'+str(port+5),'22uF 10V - transient review','VBUS'+str(port),'GND','Capacitor_SMD:C_1206_3216Metric'))
 usb.append(('J'+str(port+1),'USB-A connector TBD',[('1','VBUS','VBUS'+str(port)),('2','D-','DM'+str(port)),('3','D+','DP'+str(port)),('4','GND','GND'),('5','SHIELD','GND')],''))
 usb.append(two('R'+str(port+3),'100k fault pull-up','5V_BUS','FAULT'+str(port),'Resistor_SMD:R_0603_1608Metric'))
usb += [('U4','TPS2513ADBVR',[('1','DP1','DP1'),('2','GND','GND'),('3','DP2','DP2'),('4','DM2','DM2'),('5','IN','5V_BUS'),('6','DM1','DM1')],'Package_TO_SOT_SMD:SOT-23-6'),two('C8','100nF local','5V_BUS','GND','Capacitor_SMD:C_0603_1608Metric')]
# A2 sheet needed for complete pin schedule without overlaps.
schematic('UMI_USB_D0','USB power circuit candidate - 60 x 30 mm',usb,['REVIEW DRAFT: not linked to placement PCB; no manufacturing release.','Passive review symbols: ERC is not an electrical sign-off. USB-A charging compatibility, ESD and input protection remain open.'])
main=[two('J1','Phoenix 1709681 candidate','12V_IN','GND'),two('F0','INPUT FUSE TBD','12V_IN','12V_BUS')]
for n,(load,val) in enumerate([('JETSON','12V 5A'),('SG4A','12V 4A design allowance'),('USB','12V 4A design allowance'),('FAN','12V 0.14A')],1):
 main.extend([two('F'+str(n),'FUSE TBD - '+load,'12V_BUS',load),two('J'+str(n+1),val,load,'GND')])
main += [two('F5','BOOST INPUT FUSE TBD','12V_BUS','BOOST_IN'),('U1','53.5V BOOST - FUNCTIONAL BLOCK ONLY',[('1','INPUT','BOOST_IN'),('2','RETURN','GND'),('3','OUTPUT','53V5_RAW')],''),two('F6','DC-rated output fuse TBD','53V5_RAW','53V5_SWITCH'),two('J6','SWITCH 53.5V 1.31A','53V5_SWITCH','GND')]
schematic('UMI_MAIN_D0','Main PDB topology - boost circuit not implemented',main,['TOPOLOGY DRAFT: converter and protection component design incomplete.','Existing DXF outline retained in separate placement study; no schematic-to-PCB link yet.'])
print(out.resolve())

