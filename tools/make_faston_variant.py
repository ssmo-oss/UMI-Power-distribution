import pcbnew
from pathlib import Path
root=Path('design/D8-2L-FASTON/MAIN_POWER')
board_path=root/'MAIN_POWER.kicad_pcb'
board=pcbnew.LoadBoard(str(board_path))
old=next(fp for fp in board.GetFootprints() if fp.GetReference()=='J1')
old_path=old.GetPath()
board.Remove(old)
fp=pcbnew.FootprintLoad(str(root/'UMI_D2.pretty'),'Input_FASTON_250_PAIR')
if fp is None: raise RuntimeError('FASTON footprint failed to load')
fp.SetFPID(pcbnew.LIB_ID('UMI_D2','Input_FASTON_250_PAIR'))
fp.SetReference('J1'); fp.SetValue('12V INPUT - FASTON 250')
fp.SetPosition(pcbnew.VECTOR2I(round(139.6e6),round(108.832e6)))
fp.SetOrientationDegrees(0); fp.SetPath(old_path)
fp.SetField('MPN','63951-4 x2'); fp.GetField('MPN').SetVisible(False)
nets=board.GetNetsByName()
for pad in fp.Pads():
    netname='12V_IN' if pad.GetNumber()=='1' else 'GND'
    net=nets[netname]
    pad.SetNetCode(net.GetNetCode()); pad.SetNet(net)
board.Add(fp)
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
pcbnew.SaveBoard(str(board_path),board)
print('J1 holes:',sum(1 for p in fp.Pads()),'two per tab; 5.08 mm pitch; positive left; both tab axes north/up')
