import sys,json
from pathlib import Path
sys.path.insert(0,str(Path('work/ipc_client').resolve()))
from kipy import KiCad
base=Path.cwd();k=KiCad(socket_path='ipc://'+str((base/'work/usb-release-api/kicad/api.sock').resolve()),timeout_ms=5000)
b=k.get_board();print(b.name,k.get_version())
assert b.name=='USB_POWER.kicad_pcb'
assert len(b.get_footprints())==38
assert len(b.get_tracks())==277
b.refill_zones(block=True,max_poll_seconds=30)
b.save()
p=base/'work/usb-release-verify/USB_POWER.kicad_pcb'
s=p.read_text();print(json.dumps({'saved':str(p),'filled_polygon_sections':s.count('(filled_polygon'),'vias':len(b.get_vias()),'zones':len(b.get_zones())}))
