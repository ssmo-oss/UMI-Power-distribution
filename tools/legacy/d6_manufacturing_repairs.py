"""Authorized narrow D6 repairs: copper stackup identities and OPT trace width."""
import json,hashlib
from pathlib import Path
from design_d2 import parse,all_,one,Q,write
report={}
for name in ['MAIN_POWER','POE_POWER','USB_POWER']:
 d=Path('outputs/UMI_D6')/name;path=d/(name+'.kicad_pcb');before=path.read_bytes();b=parse(before.decode());stack=one(one(b,'setup'),'stackup');changes=[];inner=0
 for layer in all_(stack,'layer'):
  typ=one(layer,'type')
  if typ and str(typ[1])=='copper' and str(layer[1]) not in ('F.Cu','B.Cu'):
   inner+=1;expected=f'In{inner}.Cu'
   if str(layer[1])!=expected:
    changes.append({'stackup_layer_before':str(layer[1]),'after':expected});layer[1]=Q(expected)
    layer[:]=[x for x in layer if not(isinstance(x,list) and x[0] in ('material','epsilon_r','loss_tangent'))]
 # Preserve dielectric thicknesses but normalize their sequence names too.
 index=0
 for layer in all_(stack,'layer'):
  typ=one(layer,'type')
  if typ and str(typ[1]) in ('prepreg','core'):
   index+=1;layer[1]=Q(f'dielectric {index}')
 assert inner==2,(name,inner)
 if name=='POE_POWER':
  for segment in all_(b,'segment'):
   width=one(segment,'width')
   if float(width[1])<.16:
    assert float(width[1])==.15
    changes.append({'track':one(segment,'uuid')[1],'before':.15,'after':.20,'start':one(segment,'start')[1:],'end':one(segment,'end')[1:]});width[1]='0.2'
  project=d/(name+'.kicad_pro');pro=json.loads(project.read_text());pro['board']['design_settings']['rules']['min_track_width']=.16;project.write_text(json.dumps(pro,indent=2))
 if changes:write(path,b)
 report[name]={'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'changes':changes,'native_clearance_verification':'pending root refill/DRC; if 0.20mm fails try0.16mm'}
Path('work/d6_manufacturing_repairs.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
