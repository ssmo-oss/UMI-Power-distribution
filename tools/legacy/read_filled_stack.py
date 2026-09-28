from pathlib import Path
import sys
sys.path.insert(0,'work');from design_d2 import *
b=parse(Path('work/validation_cli_env/usb_snapshot_07/USB_POWER.kicad_pcb').read_text());print(dump(one(one(b,'setup'),'stackup')))
