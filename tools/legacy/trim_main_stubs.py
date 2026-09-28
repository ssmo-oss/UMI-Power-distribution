import json,subprocess,sys
from pathlib import Path
from design_d2 import parse,all_,one,write
base=Path.cwd();p=base/'outputs/UMI_D2/MAIN_POWER/MAIN_POWER.kicad_pcb';report=base/'work/validation_cli_env/main_final_drc.json'
for i in range(8):
 d=json.loads(report.read_text());v=d['violations']
 assert not d['unconnected_items'] and not d['schematic_parity']
 if not v:break
 assert all(x['type'] in ('track_dangling','via_dangling') for x in v)
 ids={x['items'][0]['uuid'] for x in v};b=parse(p.read_text());found=[a for a in all_(b,'segment')+all_(b,'via') if str(one(a,'uuid')[1]) in ids];assert len(found)==len(ids)
 for a in found:b.remove(a)
 write(p,b)
 subprocess.run([sys.executable,str(base/'work/validation_cli_controlled.py'),'--report',str(base/'work/validation_cli_env/main_final_process.json'),'--','pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','--exit-code-violations','--refill-zones','--output',str(report),str(p)],capture_output=True)
 print(i,len(json.loads(report.read_text())['violations']))
else:raise Exception('Review needed')

