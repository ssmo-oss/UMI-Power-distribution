from pathlib import Path
p=Path('work/jlc_manual_options.md');s=p.read_text(encoding='utf8');s=s.replace('discontinued lifecycle makes this poor long-term procurement','distributor lifecycle warnings were found, but current manufacturer lifecycle was not confirmed');s += '''

## Final selected insert set — supersedes unresolved insert findings above

All retain existing ATO/FKS holders; no Nano2 change is recommended.

| Ref | Littelfuse MPN | JLC | Live stock / order field | Needed for10boards |
|---|---|---|---:|---:|
|F1,F2|028707.5PXCN|C142688|1944 /1944|20|
|F3|0287001.PXCN|C142679|3722 /3722|10|
|F4|0287005.PXCN|C142682|3448 /3447|10|
|F5|0287010.PXCN|C142683|14671 /14665|10|
|F6|166.7000.4302|C3662004|10 /10|10, no spares|

Manufacturer287 datasheet verifies32VDC/1kA interruption,19.1×5.1×18.8mm ATO envelope,5.2mm blade width,6.5mm exposed length,14.5mm outer blade span. Standard ATO holder fit is supported. PXCN is2000 bulk packaging code, not minimum purchase quantity. Manufacturer ratings table explicitly lists7.5A as028707.5_, not0287007_.

[Manufacturer current287 datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40). [Manufacturer older curve/temperature sheet](https://www.littelfuse.com/~/media/automotive/datasheets/fuses/passenger-car-and-commercial-vehicle/blade-fuses/littelfuse_atof_datasheet.pdf) lists135% opening0.35–600s for1/2A and0.75–600s for3–40A;200%0.1–5s for1/2A and0.15–5s for3–40A. Typical ambient load table at65C:7.5A fuse6A load,5A fuse4A load,10A fuse8A load, supporting intended5A/4A branch,~3AUSBinput and~6.5Aboostinput at40C with startup validation still required. This is not a precise trip-current guarantee.

F6 was previously verified against manufacturerFKS80V drawing/curve inwork/fuse_verification.json andfks80_verified.pdf. Root approved conditional use of ten available pieces for ten hand-inserted boards, subject to actual reservation/supply and no-spares disclosure. Do not claim current manufacturer obsolete status without evidence. JLC loose-insert supply/installation arrangement must be confirmed: catalogue stock alone does not mean loose parts will ship with assembled boards.
''';p.write_text(s,encoding='utf8')
