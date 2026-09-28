from pathlib import Path
p=Path('work/fill_usb_final_ipc.py')
s=p.read_text().replace('usb-final-api','usb-release-api').replace('==36','==38').replace('==263','==277').replace('work/validation_cli_env/usb_snapshot_07','work/usb-release-verify')
Path('work/fill_usb_release_ipc.py').write_text(s)
