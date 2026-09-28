from pathlib import Path
import os,json,ctypes,subprocess
base=Path.cwd();config=base/'work/d4-config/10.0';config.mkdir(parents=True,exist_ok=True)
common=json.loads((base/'work/validation_cli_env/config/10.0/kicad_common.json').read_text())
common['api']['enable_server']=True
(config/'kicad_common.json').write_text(json.dumps(common,indent=2))
temp=base/'work/d4-main-api';temp.mkdir(exist_ok=True)
env=os.environ.copy();env.update(TEMP=str(temp),TMP=str(temp),KICAD_CONFIG_HOME=str(config.parent))
ctypes.windll.kernel32.SetErrorMode(0x8003)
startup=subprocess.STARTUPINFO();startup.dwFlags|=subprocess.STARTF_USESHOWWINDOW;startup.wShowWindow=0
p=subprocess.Popen([r'C:\Program Files\KiCad\10.0\bin\pcbnew.exe',str(base/'outputs/UMI_D4/MAIN_POWER/MAIN_POWER.kicad_pcb')],env=env,startupinfo=startup,creationflags=subprocess.CREATE_NO_WINDOW)
(base/'work/d4_owned_process.json').write_text(json.dumps({'pid':p.pid,'project':str(base/'outputs/UMI_D4/MAIN_POWER'),'temp':str(temp)}))
print(p.pid)
