from pathlib import Path
import sys
sys.path.insert(0,'work/gerber_lib')
from gerbonara import LayerStack
s=LayerStack.open(Path('outputs/UMI_TWO_BOARD_DESIGN/USB_POWER/manufacturing'))
for l in s.drill_layers:
 print(l,len(l.objects))
 for o in l.objects[:4]:print(o,o.x,o.y,o.tool.diameter,o.tool.plated,o.plated)
