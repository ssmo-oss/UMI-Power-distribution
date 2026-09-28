from design_d2 import *
a=parse(Path('outputs/UMI_D4/MAIN_POWER/MAIN_POWER.kicad_pcb').read_text());b=parse(Path('outputs/UMI_D5/POE_POWER/POE_POWER.kicad_pcb').read_text())
exclude={'12V_IN','FUSED_BOOST_12V','JETSON_12V','SG4A_12V','USB_12V','FAN_12V','GND'}
r={}
for typ in ['segment','via','zone']:
 aa={str(one(n,'uuid')[1]):n for n in all_(a,typ) if one(n,'net') and str(one(n,'net')[1]) not in exclude};bb={str(one(n,'uuid')[1]):n for n in all_(b,typ)}
 bad=[]
 for ident,n in aa.items():
  orig=copy.deepcopy(n);current=copy.deepcopy(bb.get(ident))
  if typ=='zone':
   for x in [orig,current]:
    if x:x[:]=[z for z in x if not(isinstance(z,list) and z[0]=='filled_polygon')]
  if dump(orig)!=dump(current):bad.append(ident)
 r[typ]={'critical_items':len(aa),'changed':bad}
Path('outputs/UMI_D5/POE_POWER/CRITICAL_COPPER_PRESERVATION.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
