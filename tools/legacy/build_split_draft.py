from pathlib import Path
import pcbnew as p
import json

root=Path.cwd()
src=root/'work/source_revC/UMI_PDB_revC_6OUT_ENGINEERING_HOLD'
out=root/'outputs/UMI_revD_split_PLACEMENT_DRAFT'
out.mkdir(parents=True,exist_ok=True)
old=p.LoadBoard(str(src/'UMI_PDB_revC_6OUT.kicad_pcb'))
mm=p.FromMM
def pos(x,y): return p.VECTOR2I(mm(x),mm(y))
def text(b,s,x,y,size=1):
    t=p.PCB_TEXT(b); t.SetText(s); t.SetPosition(pos(x,y)); t.SetTextSize(pos(size,size)); t.SetTextThickness(mm(.15)); t.SetLayer(p.Dwgs_User); b.Add(t)
def clone(b,ref,newref,x,y,value):
    f=p.Cast_to_FOOTPRINT(next(f for f in old.GetFootprints() if f.GetReference()==ref).Duplicate(False))
    f.SetReference(newref); f.SetValue(value); f.SetPosition(pos(x,y))
    for pad in f.Pads(): pad.SetNetCode(0)
    b.Add(f)
    text(b,newref+' '+value,x,y-4,.8)
    return f
main=p.LoadBoard(str(src/'UMI_PDB_revB_DXF_mechanics.kicad_pcb'))
for d in list(main.GetDrawings()):
    if isinstance(d,p.PCB_TEXT): main.Remove(d)
clone(main,'J1','J1',39,23,'12V INPUT')
for i,(name,x,y) in enumerate([('JETSON 12V 5A',17,45),('SG4A 12V 3A ASSUMED',50,45),('USB BOARD 12V',17,63),('FAN 12V 0.14A',50,63),('SWITCH 53.5V 1.31A',17,81)],1):
    clone(main,'F1','F'+str(i),x,y,'FUSE TBD')
    clone(main,'J2','J'+str(i+1),x+4,y+10,name)
text(main,'BOOST CIRCUIT\nSPACE REQUIRED\nNOT IMPLEMENTED',60,86,1)
text(main,'REV D MAIN: PLACEMENT STUDY ONLY\nNO CIRCUIT / NO ROUTING / DO NOT FABRICATE',44,119,1.2)
p.SaveBoard(str(out/'UMI_MAIN_placement_ONLY.kicad_pcb'),main)
usb=p.BOARD()
for a,b in [((10,10),(70,10)),((70,10),(70,40)),((70,40),(10,40)),((10,40),(10,10))]:
    s=p.PCB_SHAPE(); s.SetShape(p.SHAPE_T_SEGMENT); s.SetStart(pos(*a));s.SetEnd(pos(*b));s.SetLayer(p.Edge_Cuts);s.SetWidth(mm(.05));usb.Add(s)
clone(usb,'J2','J1',20,35,'12V INPUT')
clone(usb,'U1','U1',40,25,'5V BUCK CANDIDATE')
lib=Path('C:/Program Files/KiCad/10.0/share/kicad/footprints')
for i,x in enumerate([23,53],2):
    f=p.FootprintLoad(str(lib/'Connector_USB.pretty'),'USB_A_Molex_67643_Horizontal')
    f.SetReference('J'+str(i));f.SetPosition(pos(x,17));usb.Add(f)
text(usb,'USB-A FOOTPRINTS FOR SPACE STUDY ONLY',40,7,.8)
text(usb,'60 x 30 mm\nPORT PROTECTION + CHARGING CIRCUIT TBD\nNO ROUTING / DO NOT FABRICATE',40,49,1)
p.SaveBoard(str(out/'UMI_USB_placement_ONLY.kicad_pcb'),usb)
report={}
for path in out.glob('*.kicad_pcb'):
    b=p.LoadBoard(str(path))
    report[path.name]={'loads_in_KiCad':True,'footprints':len(list(b.GetFootprints())),'tracks':len(list(b.GetTracks())),'status':'Unconnected placement study; no electrical validation'}
(out/'draft_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
