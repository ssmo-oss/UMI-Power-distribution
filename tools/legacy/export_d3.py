"""Validate and export a filled D3 board without changing copper."""
from pathlib import Path
import subprocess,sys,json
base=Path.cwd();name=sys.argv[1];d=base/'outputs/UMI_D3'/name
board=d/(name+'.kicad_pcb');sch=d/(name+'.kicad_sch')
for sub in ['manufacturing','assembly','review','verification']:(d/sub).mkdir(exist_ok=True)
commands=[('DRC',['pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','--exit-code-violations','--output',str(d/'verification/DRC.json'),str(board)]),('ERC',['sch','erc','--format','json','--severity-all','--exit-code-violations','--output',str(d/'verification/ERC.json'),str(sch)]),('gerbers',['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','--use-drill-file-origin','--check-zones','--output',str(d/'manufacturing'),str(board)]),('drill',['pcb','export','drill','--format','excellon','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--output',str(d/'manufacturing'),str(board)]),('paste',['pcb','export','gerbers','--layers','F.Paste','--use-drill-file-origin','--output',str(d/'assembly'),str(board)]),('positions',['pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--smd-only','--exclude-fp-th','--exclude-dnp','--output',str(d/'assembly'/(name+'_positions.csv')),str(board)]),('schematic',['sch','export','pdf','--output',str(d/'review'/(name+'_schematic.pdf')),str(sch)]),('layers',['pcb','export','pdf','--mode-multipage','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,F.Fab,Edge.Cuts','--common-layers','Edge.Cuts','--output',str(d/'review'/(name+'_layers.pdf')),str(board)]),('render',['pcb','render','--side','top','--width','1600','--height','1000','--output',str(d/'review'/(name+'_top.png')),str(board)])]
for key,args in commands:
 report=d/'verification'/('export_'+key+'.json')
 subprocess.run([sys.executable,str(base/'work/validation_cli_controlled.py'),'--report',str(report),'--',*args],capture_output=True)
 r=json.loads(report.read_text());print(key,r['exit_code'],flush=True)
 if r['exit_code']!=0:raise SystemExit(r)
# Independent parser is the same audited procedure, pointed at this revision.
s=(base/'work/verify_gerber_package.py').read_text().replace("'outputs/UMI_TWO_BOARD_DESIGN'","'outputs/UMI_D3'")
namespace={'__name__':'d3_audit'};exec(compile(s,'d3_audit','exec'),namespace);namespace['verify'](name)
sys.path.insert(0,str(base/'work/gerber_lib'));import resvg_py
for side in ['top','bottom']:
 p=d/'review'/(name+'_gerber_'+side+'.svg');p.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),width=1800,dpi=96))
