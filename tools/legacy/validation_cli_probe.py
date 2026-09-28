"""Version-only isolated official KiCad CLI probe; does not open any design.

Microsoft documents SetErrorMode inheritance by child processes:
https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-seterrormode
Do not add CREATE_DEFAULT_ERROR_MODE, which would undo inheritance.
"""
from pathlib import Path
import ctypes
import json
import os
import subprocess
import time

base = Path(__file__).resolve().parent / 'validation_cli_env'
temp = base / 'temp'
config = base / 'config'
for p in (temp, config):
    p.mkdir(parents=True, exist_ok=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
kernel32.SetErrorMode.argtypes = [ctypes.c_uint]
kernel32.SetErrorMode.restype = ctypes.c_uint
kernel32.GetErrorMode.argtypes = []
kernel32.GetErrorMode.restype = ctypes.c_uint
previous = kernel32.SetErrorMode(0x8003)
mode = kernel32.GetErrorMode()
assert mode & 0x8003 == 0x8003, hex(mode)
env = os.environ.copy()
env.update(TEMP=str(temp), TMP=str(temp), KICAD_CONFIG_HOME=str(config))
cmd = [r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe', '--version']
report = {'command': cmd, 'process_error_mode_hex': hex(mode),
          'previous_process_error_mode_hex': hex(previous),
          'creation_flags': 'CREATE_NO_WINDOW', 'timeout_seconds': 20,
          'environment_overrides': {k: env[k] for k in ('TEMP','TMP','KICAD_CONFIG_HOME')}}
started = time.monotonic()
try:
    p = subprocess.run(cmd, env=env, cwd=base, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=20,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    report.update(exit_code=p.returncode, exit_code_hex=hex(p.returncode & 0xffffffff),
                  stdout=p.stdout, stderr=p.stderr, timed_out=False)
except subprocess.TimeoutExpired as e:
    report.update(exit_code=None, timed_out=True, stdout=str(e.stdout), stderr=str(e.stderr))
finally:
    report['elapsed_seconds'] = round(time.monotonic()-started, 3)
    (base/'version_probe.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))
