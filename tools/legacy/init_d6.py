from pathlib import Path
import shutil
old=Path('outputs/UMI_D5');new=Path('outputs/UMI_D6');assert not new.exists()
new.mkdir()
for name in ['MAIN_POWER','POE_POWER','USB_POWER']:
 src=old/name;dst=new/name;dst.mkdir()
 for p in src.iterdir():
  if p.is_dir() and p.name=='UMI_D2.pretty':shutil.copytree(p,dst/p.name)
  elif p.is_file() and (p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_sym'] or p.name in ['fp-lib-table','sym-lib-table','design.json','pin_schedule.csv']):
   shutil.copy2(p,dst/p.name)
 for sub in ['manufacturing','assembly','review','verification']:(dst/sub).mkdir()
 for suffix in ['.kicad_pcb','.kicad_sch']:
  p=dst/(name+suffix);p.write_text(p.read_text(encoding='utf-8').replace('D5','D6'),encoding='utf-8')
for name in ['export_d5.py','d5_api.py','prepare_d5_metadata.py','deliver_d5.py']:
 t=(Path('work')/name).read_text().replace('D5','D6').replace('d5','d6')
 (Path('work')/name.replace('d5','d6')).write_text(t)
print(new)
