"""Read-only connectivity test using official IPC client, never pcbnew or CLI."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'ipc_client'))
from kipy import KiCad
try:
    k=KiCad(timeout_ms=3000)
    print('KiCad version:',k.get_version())
    b=k.get_board()
    print('Board:',b.name)
    print('Footprints:',len(b.get_footprints()))
except Exception as e:
    print(type(e).__name__+': '+str(e))
    sys.exit(1)
