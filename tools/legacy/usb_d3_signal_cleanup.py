from pathlib import Path
import sys,shutil,uuid
sys.path.insert(0,'work');from design_d2 import *
p=Path('outputs/UMI_D3/USB_POWER/USB_POWER.kicad_pcb');backup=Path('work/usb_d3_before_signal.kicad_pcb')
if not backup.exists():shutil.copy2(p,backup)
b=parse(backup.read_text());nets=['DP1','DM1','DP2','DM2']
b[:]=[x for x in b if not(isinstance(x,list) and x and x[0]=='segment' and one(x,'layer')[1]=='B.Cu' and one(x,'net')[1] in nets)]
paths={'DM1':('B.Cu',[(27.35,42.55),(43.3,42.55),(44.1,41.75),(45.6,41.75),(46.9,43.05),(49.3,43.05)]),'DP1':('B.Cu',[(27.35,44.45),(43.3,44.45),(44.7,43.05)]),'DM2':('In2.Cu',[(49.3,44.95),(52.25,42),(69.8,42),(70.35,42.55)]),'DP2':('In2.Cu',[(44.7,44.95),(45.45,45.7),(69.1,45.7),(70.35,44.45)])}
for net,(layer,pts) in paths.items():
 for a,z in zip(pts,pts[1:]):b.append(['segment',['start',*map(str,a)],['end',*map(str,z)],['width','.2'],['layer',Q(layer)],['net',Q(net)],['uuid',Q(str(uuid.uuid4()))]])
write(p,b)

