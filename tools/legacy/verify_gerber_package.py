"""Independent exported-Gerber/Excellon and placement-file checks."""
from pathlib import Path
import sys,json,csv,math,warnings
BASE=Path.cwd();sys.path.insert(0,str(BASE/'work/gerber_lib'))
from gerbonara import LayerStack
from gerbonara.utils import MM
from design_d2 import parse,all_,one,prop
def verify(name):
 d=BASE/'outputs/UMI_TWO_BOARD_DESIGN'/name
 with warnings.catch_warnings(record=True) as captured:
  stack=LayerStack.open(d/'manufacturing')
  bounds=stack.board_bounds(MM)
  (d/'review'/(name+'_gerber_top.svg')).write_text(str(stack.to_pretty_svg(side='top',margin=1)),encoding='utf-8')
  (d/'review'/(name+'_gerber_bottom.svg')).write_text(str(stack.to_pretty_svg(side='bottom',margin=1)),encoding='utf-8')
  warnings_list=[str(w.message) for w in captured]
 copper={str(k):len(v.objects) for k,v in stack.graphic_layers.items() if k[1]=='copper'}
 assert len(copper)==4,copper
 assert all(n>0 for n in copper.values())
 drills=[]
 for layer in stack.drill_layers:
  # Gerbonara 1.6.3 does not interpret KiCad's X2 Excellon plating comments.
  # Read that explicit exported attribute rather than assuming from filename.
  header=Path(layer.original_path).read_text()
  if 'TF.FileFunction,NonPlated,' in header:plated=False
  elif 'TF.FileFunction,Plated,' in header:plated=True
  else:raise ValueError('Missing Excellon plating declaration')
  for obj in layer.objects:
   drills.append(dict(x=obj.x,y=obj.y,diameter=obj.tool.diameter,plated=plated))
 pcb=parse((d/(name+'.kicad_pcb')).read_text())
 ox,oy=map(float,one(one(pcb,'setup'),'aux_axis_origin')[1:3])
 expected=[]
 for f in all_(pcb,'footprint'):
  fx,fy=map(float,one(f,'at')[1:3]);rotation=float(one(f,'at')[3]) if len(one(f,'at'))>3 else 0
  a=math.radians(rotation)
  for p in all_(f,'pad'):
   dr=one(p,'drill')
   if dr is None:continue
   if dr[1]=='oval':raise NotImplementedError('Add slot-geometry verification before accepting slots')
   px,py=map(float,one(p,'at')[1:3]);x=fx+px*math.cos(a)+py*math.sin(a);y=fy-px*math.sin(a)+py*math.cos(a)
   expected.append(dict(x=x-ox,y=oy-y,diameter=float(dr[1]),plated=p[2]=='thru_hole'))
 for v in all_(pcb,'via'):
  x,y=map(float,one(v,'at')[1:3]);expected.append(dict(x=x-ox,y=oy-y,diameter=float(one(v,'drill')[1]),plated=True))
 remaining=list(drills)
 for e in expected:
  match=next((v for v in remaining if v['plated']==e['plated'] and all(abs(v[k]-e[k])<.002 for k in ['x','y','diameter'])),None)
  assert match is not None,('Missing drill',e)
  remaining.remove(match)
 assert not remaining,('Extra exported drills',remaining)
 parts={p['ref']:p for p in json.loads((d/'design.json').read_text())}
 fps={str(prop(f,'Reference')[2]):f for f in all_(pcb,'footprint')}
 expected_refs={ref for ref,f in fps.items() if 'smd' in (one(f,'attr') or [])}
 with (d/'assembly'/(name+'_positions.csv')).open(newline='',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
 assert {r['Ref'] for r in rows}==expected_refs
 for r in rows:
  p=parts[r['Ref']]
  assert abs(float(r['PosX'])-(p['pos'][0]-ox))<.002
  assert abs(float(r['PosY'])-(oy-p['pos'][1]))<.002
  assert r['Side']=='top'
 report={'board':name,'independent_parser':'gerbonara1.6.3','copper_layers':copper,'outline_stroke_bounds_mm':bounds,'exported_drill_count':len(drills),'expected_drill_count':len(expected),'smt_position_count':len(rows),'drill_positions_and_sizes_match_board':True,'cpl_references_and_centres_match_board':True,'parser_warnings':warnings_list,'scope':'Export consistency and independent parsing; not electrical or hardware qualification'}
 (d/'verification'/'manufacturing_export_audit.json').write_text(json.dumps(report,indent=2))
 print(json.dumps(report,indent=2))
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else 'USB_POWER')
