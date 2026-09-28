from pathlib import Path
import sys,subprocess,json
base=Path.cwd();root=base/'outputs/UMI_TWO_BOARD_DESIGN'
for name in ['MAIN_POWER','USB_POWER']:
 d=root/name
 for mode in ['drc','erc']:
  args=['pcb','drc','--all-track-errors','--schematic-parity'] if mode=='drc' else ['sch','erc']
  args+=['--format','json','--severity-all','--exit-code-violations','--output',str(d/'verification'/(mode.upper()+'.json')),str(d/(name+('.kicad_pcb' if mode=='drc' else '.kicad_sch')))]
  report=d/'verification'/(mode+'_process.json')
  subprocess.run([sys.executable,str(base/'work/validation_cli_controlled.py'),'--report',str(report),'--',*args],capture_output=True)
  r=json.loads(report.read_text());print(name,mode,r['exit_code'],r['stdout']);assert r['exit_code']==0
 subprocess.run([sys.executable,str(base/'work/verify_gerber_package.py'),name],check=True,stdout=subprocess.DEVNULL)
 sys.path.insert(0,str(base/'work/gerber_lib'));import resvg_py
 (d/'review'/(name+'_gerber_top.png')).write_bytes(resvg_py.svg_to_bytes(svg_path=str(d/'review'/(name+'_gerber_top.svg')),width=1800,dpi=96))
