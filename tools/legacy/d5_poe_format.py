from design_d2 import *
b=parse(Path('outputs/UMI_D4/MAIN_POWER/MAIN_POWER.kicad_pcb').read_text())
for k in ['net','segment','zone']:
 a=all_(b,k);print(k,len(a),dump(a[0])[:550] if a else '')
print(dump(prop(all_(b,'footprint')[0],'Reference')));print(dump(one(all_(b,'footprint')[0],'path')))
