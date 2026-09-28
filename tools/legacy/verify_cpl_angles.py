import sys,json,math,csv
from pathlib import Path
sys.path.insert(0,'work');from design_d2 import parse,LIB
from main_power_d2 import mosfet_land,panasonic_g_land

def get(n,k):return next((e for e in n if isinstance(e,list) and e and e[0]==k),None)
def pads(f):return {str(e[1]):list(map(float,get(e,'at')[1:3])) for e in f if isinstance(e,list) and e and e[0]=='pad' and str(e[1])}
out={}
for board in ['MAIN_POWER','USB_POWER']:
 p=Path('outputs/UMI_TWO_BOARD_DESIGN')/board;design=json.loads((p/'design.json').read_text());b=parse((p/(board+'.kicad_pcb')).read_text());fps={next(e[2] for e in f if isinstance(e,list) and e[:2]==['property','Reference']):f for f in b if isinstance(f,list) and f and f[0]=='footprint'};rows=[]
 for d in design:
  angle=d.get('rotation',0)
  if not angle:continue
  source=d['source_fp'];fam,fn=source.split(':')
  if fn=='BSC072N08NS5_TDSON_8':original=mosfet_land()
  elif fn=='Panasonic_FK_G_10x10.2':original=panasonic_g_land()
  else:original=parse((LIB/(fam+'.pretty')/(fn+'.kicad_mod')).read_text())
  a=pads(original);z=pads(fps[d['ref']]);c=round(math.cos(math.radians(angle)));s=round(math.sin(math.radians(angle)));error=max(math.dist([c*x-s*y,s*x+c*y],z[n]) for n,(x,y) in a.items());assert error<.00001,(d['ref'],error)
  rows.append({'reference':d['ref'],'source_footprint':source,'baked_angle_clockwise_board_view_deg':angle,'normalized_CCW_rotation_deg':(-angle)%360,'max_pad_position_error_mm':error})
 out[board]=rows
Path('work/cpl_rotation_corrections.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
