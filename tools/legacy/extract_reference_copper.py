from pathlib import Path
import sys,struct,json,collections
sys.path.insert(0,'work/main_lib');import olefile
F=olefile.OleFileIO('work/datasheets/PMP21274_REVA.PcbDoc');S=.00000254
u16=lambda b,o:struct.unpack_from('<H',b,o)[0]
u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
i32=lambda b,o:struct.unpack_from('<i',b,o)[0]
double=lambda b,o:struct.unpack_from('<d',b,o)[0]
xy=lambda b,o:[v*S for v in struct.unpack_from('<ii',b,o)]
def prop(b,o=0):
 n=u32(b,o);end=o+4+n;assert end<=len(b)
 return dict(v.split('=',1) for v in b[o+4:end].decode('latin1').rstrip('\0').split('|') if '=' in v),end
def props(stream):
 b=F.openstream(stream+'/Data').read();o=0;r=[]
 while o<len(b):p,o=prop(b,o);r.append(p)
 return r
nets=props('Nets6');comps=props('Components6')
def base(b):
 n=u16(b,3);c=u16(b,7)
 return dict(layer=b[0],net=nets[n]['NAME'] if n!=65535 else None,net_index=n,component=comps[c]['SOURCEDESIGNATOR'] if c!=65535 else None,polygon_index=u16(b,5),is_keepout=b[2]==2,is_polygon_outline=bool(b[1]&2))
def records(stream):
 b=F.openstream(stream+'/Data').read();o=0
 while o<len(b):
  typ=b[o];n=u32(b,o+1);end=o+5+n;assert end<=len(b),(stream,o,n)
  yield typ,b[o+5:end]
  o=end
 assert o==len(b)
def unit(s):
 s=str(s).lower();return float(s[:-3])*.0254 if s.endswith('mil') else float(s[:-2]) if s.endswith('mm') else float(s)
def region(b,extended):
 r=base(b);p,o=prop(b,18);r['properties']=p;r['kind']=int(p.get('KIND',0));r['layer_v7']=p.get('V7_LAYER');nv=u32(b,o)+(1 if extended else 0);o+=4;vv=[];arcs=[]
 for _ in range(nv):
  if extended:
   vv.append(xy(b,o+1));arcs.append(dict(round=bool(b[o]),center_mm=xy(b,o+9),radius_mm=i32(b,o+17)*S,start_angle=double(b,o+21),end_angle=double(b,o+29)));o+=37
  else:vv.append([double(b,o)*S,double(b,o+8)*S]);o+=16
 holes=[]
 for _ in range(u16(b,14)):
  count=u32(b,o);o+=4;h=[]
  for _ in range(count):h.append([double(b,o)*S,double(b,o+8)*S]);o+=16
  holes.append(h)
 assert o<=len(b),(o,len(b));r.update(vertices_mm=vv,holes_mm=holes,unparsed_tail_bytes=len(b)-o)
 if extended:r['vertex_arcs']=arcs
 return r
out=dict(source='TI PMP21274 REVA, TIDRTY5',coordinates='millimetres, original Altium positive Y up; no offset',parser_reference='work/datasheets/altium_parser_pcb.cpp',tracks=[],vias=[],regions=[],shape_based_regions=[],polygons=[],fills=[],arcs=[]);stats={}
for stream,key in [('Tracks6','tracks'),('Vias6','vias'),('Regions6','regions'),('ShapeBasedRegions6','shape_based_regions'),('Fills6','fills'),('Arcs6','arcs')]:
 raw=list(records(stream));stats[stream]=dict(total=len(raw),types=dict(collections.Counter(t for t,b in raw)))
 for index,(typ,b) in enumerate(raw):
  if key=='tracks':
   assert typ==4;r=base(b);r.update(start_mm=xy(b,13),end_mm=xy(b,21),width_mm=i32(b,29)*S,subpolygon_index=u16(b,33),layer_v7=u32(b,41) if len(b)>=45 else None)
  elif key=='vias':
   assert typ==3;r=base(b);r.update(xy_mm=xy(b,13),diameter_mm=i32(b,21)*S,drill_mm=i32(b,25)*S,fromlayer=b[29],tolayer=b[30]);r['component']=None;r.pop('polygon_index')
  elif key in ('regions','shape_based_regions'):
   assert typ==11;r=region(b,key=='shape_based_regions')
  elif key=='fills':
   assert typ==6;r=base(b);r.update(start_mm=xy(b,13),end_mm=xy(b,21),rotation=double(b,29))
  else:
   assert typ==1;r=base(b);r.update(center_mm=xy(b,13),radius_mm=i32(b,21)*S,start_angle=double(b,25),end_angle=double(b,33),width_mm=i32(b,41)*S)
  r['source_index']=index
  if (r['net'] is not None or key in ('regions','shape_based_regions')) and (key=='vias' or 1<=r['layer']<=32):out[key].append(r)
for index,p in enumerate(props('Polygons6')):
 n=int(p.get('NET',65535));verts=[];arcs=[];i=0
 while 'VX'+str(i) in p:
  s=str(i);verts.append([unit(p['VX'+s]),unit(p['VY'+s])]);arcs.append(dict(round=int(p.get('KIND'+s,0))!=0,radius_mm=unit(p.get('R'+s,'0mil')),center_mm=[unit(p.get('CX'+s,'0mil')),unit(p.get('CY'+s,'0mil'))],start_angle=float(p.get('SA'+s,0)),end_angle=float(p.get('EA'+s,0))));i+=1
 out['polygons'].append(dict(source_index=index,net=nets[n]['NAME'] if n!=65535 else None,layer=p.get('LAYER'),layer_v7=p.get('LAYER_V7'),vertices_mm=verts,vertex_arcs=arcs,properties=p))
for key in ('regions','shape_based_regions'):
 for r in out[key]:
  if r['net'] is None and r['polygon_index']!=65535:
   r['net']=out['polygons'][r['polygon_index']]['net'];r['net_inherited_from_polygon']=True
out['stream_statistics']=stats
Path('work/datasheets/pmp_reference_copper.json').write_text(json.dumps(out,indent=2))
print(json.dumps(stats));print({k:len(out[k]) for k in ['tracks','vias','regions','shape_based_regions','polygons','fills','arcs']})
for k in ['tracks','vias','regions','shape_based_regions','polygons','fills','arcs']:print(k,collections.Counter(str(r.get('layer')) for r in out[k]))

