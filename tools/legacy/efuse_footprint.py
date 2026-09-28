"""TI TPS25982 RGE0024M footprint, transcribed from manufacturer drawing.
Source: https://www.ti.com/lit/ds/symlink/tps25982.pdf
Drawing 4223975/B, 03/2018, PDF pages 55-57 (one-based), Rev D datasheet.
Pure text; does not import or launch KiCad.
"""
from pathlib import Path
import json

NAME='TI_RGE0024M_TPS25982'
PIN_FUNCTIONS={**{str(i):'IN' for i in (1,2,3,16,25)},
 **{str(i):'OUT' for i in range(17,25)},
 **{str(i):'GND' for i in (4,5,14,26)},
 '6':'EN_UVLO','7':'ITIMER','8':'ILIM','9':'IMON','10':'RETRY_DLY',
 '11':'NRETRY','12':'LDSTRT','13':'PG','15':'DVDT'}
# Optional thermal vias, not embedded in the library footprint. Vias under paste
# must be filled/plugged/tented per TI drawing; route nets according to parent pad.
THERMAL_VIA_CENTERS={25:[(x,y) for x in (-1.1,0,1.1) for y in (-1.1,-.15)],
                     26:[(x,.925) for x in (-1.1,0,1.1)]}

def geometry():
 p=[]
 for n in range(1,25):
  if n<=6: x,y,w,h=-1.9125,-1.25+(n-1)*.5,.575,.24
  elif n<=12: x,y,w,h=-1.25+(n-7)*.5,1.9125,.24,.575
  elif n<=18: x,y,w,h=1.9125,1.25-(n-13)*.5,.575,.24
  else:x,y,w,h=1.25-(n-19)*.5,-1.9125,.24,.575
  p.append(dict(number=str(n),x=x,y=y,w=w,h=h,layer='copper'))
 p.extend([dict(number='25',x=0,y=-.625,w=2.7,h=1.45,layer='copper'),
           dict(number='26',x=0,y=.925,w=2.7,h=.85,layer='copper')])
 for x in (-.694,.694):
  p.append(dict(number='',x=x,y=-.625,w=1.188,h=1.3,layer='paste'))
  p.append(dict(number='',x=x,y=.925,w=1.188,h=.76,layer='paste'))
 return p

def footprint_text():
 s=[f'(footprint "{NAME}" (version 20241229) (generator "pcbnew") (layer "F.Cu")',
 '(descr "TI RGE0024M 4x4mm VQFN-24, split thermal pads 25=IN and 26=GND; TI drawing4223975/B")',
 '(tags "TPS259824ONRGER RGE0024M split thermal power pad") (attr smd)',
 '(property "Reference" "REF**" (at 0 -3.1) (layer "F.SilkS") (effects (font (size 1 1) (thickness .15))))',
 f'(property "Value" "{NAME}" (at 0 3.1) (layer "F.Fab") (effects (font (size 1 1) (thickness .15))))',
 '(fp_rect (start -2 -2) (end 2 2) (stroke (width .1) (type solid)) (fill none) (layer "F.Fab"))',
 '(fp_line (start -2 -1.5) (end -1.5 -2) (stroke (width .1) (type solid)) (layer "F.Fab"))',
 '(fp_line (start -2.4 -1.5) (end -2.4 -2.4) (stroke (width .12) (type solid)) (layer "F.SilkS"))',
 '(fp_line (start -2.4 -2.4) (end -1.5 -2.4) (stroke (width .12) (type solid)) (layer "F.SilkS"))',
 '(fp_rect (start -2.5 -2.5) (end 2.5 2.5) (stroke (width .05) (type solid)) (fill none) (layer "F.CrtYd"))']
 for p in geometry():
  n,x,y,w,h=p['number'],p['x'],p['y'],p['w'],p['h']
  layers='"F.Paste"' if p['layer']=='paste' else '"F.Cu" "F.Mask"'+(' "F.Paste"' if int(n)<=24 else '')
  ratio=.05/min(w,h)
  mask='' if p['layer']=='paste' else ' (solder_mask_margin .05)'
  s.append(f'(pad "{n}" smd roundrect (at {x} {y}) (size {w} {h}) (layers {layers}) (roundrect_rratio {ratio:.9f}){mask})')
 return '\n'.join(s)+'\n)\n'

def footprint():
 """Return the mutable s-expression used by the existing main-board builder."""
 from design_d2 import parse
 return parse(footprint_text())

def verify_geometry():
 p=geometry();c=[a for a in p if a['layer']=='copper'];assert len(c)==26
 assert {a['number'] for a in c}==set(map(str,range(1,27)))
 assert set(PIN_FUNCTIONS)==set(map(str,range(1,27)))
 assert PIN_FUNCTIONS['25']=='IN' and PIN_FUNCTIONS['26']=='GND'
 a,b=c[24:];gap=(b['y']-b['h']/2)-(a['y']+a['h']/2)
 assert abs(gap-.4)<1e-9
 # All separately numbered copper lands must be physically disjoint.
 clearances=[]
 for i,a in enumerate(c):
  for b in c[i+1:]:
   dx=max(0,abs(a['x']-b['x'])-(a['w']+b['w'])/2)
   dy=max(0,abs(a['y']-b['y'])-(a['h']+b['h'])/2)
   assert dx>0 or dy>0,(a['number'],b['number'])
   clearances.append((dx*dx+dy*dy)**.5)
 return dict(copper_pads=26,paste_apertures=28,thermal_pad_gap_mm=gap,
             minimum_bounding_box_copper_gap_mm=min(clearances),
             upper_paste_area_ratio=2*1.188*1.3/(2.7*1.45),
             lower_paste_area_ratio=2*1.188*.76/(2.7*.85),
             thermal_via_drill_mm=.2,
             not_checked='KiCad DRC, solder process and actual assembly')

if __name__=='__main__':
 out=Path(__file__).parent
 (out/(NAME+'.kicad_mod')).write_text(footprint_text(),encoding='utf8')
 (out/'efuse_footprint_geometry.json').write_text(json.dumps({'verification':verify_geometry(),'pin_functions':PIN_FUNCTIONS,'lands':geometry(),'optional_thermal_vias':THERMAL_VIA_CENTERS},indent=2),encoding='utf8')
 print(json.dumps(verify_geometry(),indent=2))
