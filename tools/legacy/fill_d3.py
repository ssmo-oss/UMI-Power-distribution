from pathlib import Path
import sys,json
sys.path.insert(0,str(Path('work/ipc_client').resolve()))
from kipy import KiCad
name=sys.argv[1];short='usb' if name=='USB_POWER' else 'main';base=Path.cwd();k=KiCad(socket_path='ipc://'+str(base/('work/d3-'+short+'-api/kicad/api.sock')),timeout_ms=5000)
b=k.get_board();assert b.name==name+'.kicad_pcb'
assert Path(b.document.project.path).resolve()==(base/'outputs/UMI_D3'/name).resolve()
b.revert();b.refill_zones(block=True,max_poll_seconds=30);b.save();print(name,'saved filled zones',len(b.get_zones()))

