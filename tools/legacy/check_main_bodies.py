import sys,math,json
sys.path.insert(0,'work');from design_d2 import parse
b=parse(open('outputs/UMI_D2/MAIN_POWER/MAIN_POWER.kicad_pcb').read())
def node(n,k):return next((x for x in n if isinstance(x,list) and x and x[0]==k),None)
for f in b:
 if not isinstance(f,list) or not f or f[0]!='footprint':continue
 ref=next((x[2] for x in f if isinstance(x,list) and x[:2]==['property','Reference']),None)
 if ref not in ['R1','C1','C5','L2','C20']:continue
 print(ref,node(f,'at'))
 for e in f:
  if isinstance(e,list) and e and (e[0]=='pad' or (e[0].startswith('fp_') and node(e,'layer')==['layer','F.Fab'])):print(e)
