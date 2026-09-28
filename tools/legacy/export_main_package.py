from pathlib import Path
import shutil,subprocess,sys,json
base=Path.cwd();name='MAIN_POWER';source=base/'work/main-release-verify'
dest=base/'outputs/UMI_TWO_BOARD_DESIGN'/name
dest.mkdir(parents=True,exist_ok=True)
for filename in [name+'.kicad_pcb',name+'.kicad_sch',name+'.kicad_pro','fp-lib-table','sym-lib-table','UMI.kicad_sym','design.json','pin_schedule.csv','BOM_by_reference.csv','BOM_grouped.csv','BOM_JLC_DRAFT.csv','BOM_audit.json']:
 shutil.copy2(source/filename,dest/filename)
shutil.copytree(source/'UMI_D2.pretty',dest/'UMI_D2.pretty',dirs_exist_ok=True)
board=dest/(name+'.kicad_pcb');schematic=dest/(name+'.kicad_sch')
for sub in ['manufacturing','assembly','review','verification']:(dest/sub).mkdir(exist_ok=True)
commands=[
 ('gerbers',['pcb','export','gerbers','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','--use-drill-file-origin','--check-zones','--output',str(dest/'manufacturing'),str(board)]),
 ('drill',['pcb','export','drill','--format','excellon','--drill-origin','plot','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',str(dest/'review'/'MAIN_POWER_drill_report.txt'),'--output',str(dest/'manufacturing'),str(board)]),
 ('paste',['pcb','export','gerbers','--layers','F.Paste','--use-drill-file-origin','--output',str(dest/'assembly'),str(board)]),
 ('positions',['pcb','export','pos','--format','csv','--units','mm','--use-drill-file-origin','--smd-only','--exclude-fp-th','--exclude-dnp','--output',str(dest/'assembly'/'MAIN_POWER_positions.csv'),str(board)]),
 ('schematic',['sch','export','pdf','--output',str(dest/'review'/'MAIN_POWER_schematic.pdf'),str(schematic)]),
 ('layers',['pcb','export','pdf','--mode-multipage','--layers','F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,F.Fab,Edge.Cuts','--common-layers','Edge.Cuts','--output',str(dest/'review'/'MAIN_POWER_layers.pdf'),str(board)]),
 ('render',['pcb','render','--side','top','--width','1600','--height','1000','--output',str(dest/'review'/'MAIN_POWER_top.png'),str(board)]),
]
for key,args in commands:
 report=dest/'verification'/('export_'+key+'.json')
 r=subprocess.run([sys.executable,str(base/'work/validation_cli_controlled.py'),'--timeout','60','--report',str(report),'--',*args],capture_output=True,text=True)
 data=json.loads(report.read_text());print(key,data.get('exit_code'),data.get('stderr','')[:200])
 if data.get('exit_code')!=0:raise SystemExit(key+' failed')
shutil.copy2(base/'work/validation_cli_env/main_final_drc.json',dest/'verification'/'DRC.json')
shutil.copy2(base/'work/validation_cli_env/main_erc_07.json',dest/'verification'/'ERC.json')
print(dest)
