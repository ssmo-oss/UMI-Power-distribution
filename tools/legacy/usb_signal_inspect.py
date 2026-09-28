import sys
sys.path.insert(0,'work');from design_d2 import *
b=parse(Path('outputs/UMI_D3/USB_POWER/USB_POWER.kicad_pcb').read_text())
for x in all_(b,'segment')+all_(b,'via'):
 n=one(x,'net')
 if n and any(z in str(n) for z in ['DP1','DM1','DP2','DM2']):print(dump(x))
