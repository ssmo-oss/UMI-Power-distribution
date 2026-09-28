from design_d2 import *
b=parse(Path('outputs/UMI_D4/MAIN_POWER/MAIN_POWER.kicad_pcb').read_text());
for f in all_(b,'footprint'):
 r=str(prop(f,'Reference')[2]);a=one(f,'at');print(r,str(f[1]),a[1:])
print('zones',[(str(one(z,'net_name')),one(z,'layer'),len(all_(z,'filled_polygon'))) for z in all_(b,'zone')])
