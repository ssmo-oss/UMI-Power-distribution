import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'ipc_client'))
from kipy import KiCad
base=Path.cwd()
k=KiCad(socket_path='ipc://'+str((base/'work/kicad-api-temp/kicad/api.sock').resolve()),timeout_ms=5000)
b=k.get_board()
assert b.name=='UMI_USB_D2_verify.kicad_pcb',b.name
text=b.get_as_string()
(base/'work/d2-verification/loaded-board.kicad_pcb').write_text(text,encoding='utf-8')
report={'scope':'KiCad GUI IPC load inspection, not ERC or DRC','version':str(k.get_version()),'board':b.name,'footprints':len(b.get_footprints()),'tracks':len(b.get_tracks()),'copper_layers':b.get_copper_layer_count(),'zones':len(b.get_zones()),'vias':len(b.get_vias()),'manufacturing_release':False}
assert report['footprints']==32
assert report['tracks']==26
assert report['copper_layers']==4
(base/'outputs/UMI_D2/UMI_USB_D2/ipc_load_check.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
