from pathlib import Path
import sys,os,json,ctypes,subprocess
base=Path.cwd();name=sys.argv[1];assert name in ['MAIN_POWER','POE_POWER','USB_POWER'];mode=sys.argv[2]
temp=base/('work/d6-'+name.lower()+'-api');temp.mkdir(exist_ok=True)
if mode=='launch':
 env=os.environ.copy();env.pop('KICAD_CONFIG_HOME',None);env.update(TEMP=str(temp),TMP=str(temp))
 ctypes.windll.kernel32.SetErrorMode(0x8003)
 s=subprocess.STARTUPINFO();s.dwFlags|=subprocess.STARTF_USESHOWWINDOW;s.wShowWindow=0
 p=subprocess.Popen([r'C:\Program Files\KiCad\10.0\bin\pcbnew.exe',str(base/'outputs/UMI_D6'/name/(name+'.kicad_pcb'))],env=env,startupinfo=s,creationflags=subprocess.CREATE_NO_WINDOW)
 (temp/'owned_process.json').write_text(json.dumps({'pid':p.pid,'board':name}));print(name,p.pid)
elif mode in ['fill','save']:
 sys.path.insert(0,str(base/'work/ipc_client'));from kipy import KiCad
 k=KiCad(socket_path='ipc://'+str(temp/'kicad/api.sock'),timeout_ms=5000);b=k.get_board()
 assert b.name==name+'.kicad_pcb' and Path(b.document.project.path).resolve()==(base/'outputs/UMI_D6'/name).resolve()
 if mode=='fill':b.revert();b.refill_zones(block=True,max_poll_seconds=30)
 b.save();print(name,'saved',len(b.get_zones()),'zones')
