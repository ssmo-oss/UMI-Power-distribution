"""Run an explicitly supplied official KiCad CLI command with local fault handling.

Only invoke operations authorized by the coordinating agent; never retries.
All configuration changes are isolated to this wrapper process and work directory.
"""
import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--timeout', type=int, default=60)
    ap.add_argument('--report', required=True)
    ap.add_argument('command', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command:
        raise SystemExit('Explicit CLI arguments required')
    base = Path(__file__).resolve().parent / 'validation_cli_env'
    temp, config = base/'temp', base/'config'
    for p in (temp, config):
        p.mkdir(parents=True, exist_ok=True)
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.SetErrorMode.argtypes = [ctypes.c_uint]
    kernel32.SetErrorMode.restype = ctypes.c_uint
    kernel32.GetErrorMode.argtypes = []
    kernel32.GetErrorMode.restype = ctypes.c_uint
    kernel32.SetErrorMode(0x8003)
    mode = kernel32.GetErrorMode()
    assert mode & 0x8003 == 0x8003
    env = os.environ.copy()
    env.update(TEMP=str(temp), TMP=str(temp), KICAD_CONFIG_HOME=str(config))
    cmd = [r'C:\Program Files\KiCad\10.0\bin\kicad-cli.exe', *command]
    report = {'command': cmd, 'process_error_mode_hex': hex(mode),
              'creation_flags': 'CREATE_NO_WINDOW', 'timeout_seconds': args.timeout,
              'environment_overrides': {k: env[k] for k in ('TEMP', 'TMP', 'KICAD_CONFIG_HOME')}}
    started = time.monotonic()
    try:
        proc = subprocess.run(cmd, env=env, cwd=base, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=args.timeout,
                              creationflags=subprocess.CREATE_NO_WINDOW)
        report.update(exit_code=proc.returncode, exit_code_hex=hex(proc.returncode & 0xffffffff),
                      stdout=proc.stdout, stderr=proc.stderr, timed_out=False)
    except subprocess.TimeoutExpired as e:
        report.update(exit_code=None, timed_out=True, stdout=str(e.stdout), stderr=str(e.stderr))
    finally:
        report['elapsed_seconds'] = round(time.monotonic()-started, 3)
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
