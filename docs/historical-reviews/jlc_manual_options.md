# Manual-part JLC options, 10 main boards

Checked 2026-09-26. Raw live catalogue metadata: `work/jlc_manual_info.json`. Stock counts are not reservations. The `canPresaleNumber` field was correlated with displayed available-order quantity on several parts but is not a universal assembly guarantee; root browser confirmed XT60PW-M requires preorder despite visible stock.

## Approved packaging-only holder substitution

Replace 178.6165.0001 with **178.6165.0002**, JLC **C207061**. Stock617, available-order field514; need60 plus spares. Manufacturer FLR drawing identifies suffix1 as100-pack, suffix2 as500-pack, both complete178.6165.000_ holder. Same80V construction, geometry and PCB thickness limit. No footprint change.

[JLC](https://jlcpcb.com/partdetail/Littelfuse-178_61650002/C207061), [manufacturer drawing mirror](https://datasheet.octopart.com/178.6165.0001-Littelfuse-datasheet-8836287.pdf).

## Input terminal

No verified stocked same-footprint replacement for Phoenix1709681 was found. Original is MKDS10HV/2-ZB-10,16,76A, four zigzag pins (two per potential), not an ordinary two-pin terminal.

**Phoenix1711725 C89120**, MKDS3/2-5,08: live stock2573, order-field2486. Manufacturer24A400V, AWG12 capability. Candidate for nominal20A bus, requiring enclosure40C thermal check and conductor selection. Package change: two pins at0,0 and5.08,0 instead of original four-pin arrangement. Stock KiCad footprint `TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-3-2-5.08_1x02_P5.08mm_Horizontal` has2.6mm copper pads,1.3mm drill,10.2×11.2mm body. Assign polarity consistently with board labels; connector itself is not electrically polarized. This is a localized connector and input-copper change, not a drop-in.

[Manufacturer](https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-3-2-508-1711725), [JLC](https://jlcpcb.com/partdetail/PhoenixContact-1711725/C89120).

XT60PW-M C98732 had8898 displayed stock but root browser confirmed preorder minimum17,14-day lead; not an immediately available alternative.

## Fuse inserts and redesign option

ESKA exact inserts remain unverified in JLC. ATO7.5A Littelfuse0ATO07.5V C1664994 has zero live stock. FKS80V3A166.7000.4302 C3662004 has exactly10 stock/orderable, covering10 boards with no spares; distributor lifecycle warnings were found, but current manufacturer lifecycle was not confirmed. OptiFuseANR80-UL-3A C3662026 has zero. Do not replace53.5V branch fuse with32V fuse.

A feasible alternative retaining replaceability is Littelfuse154 OMNI-BLOK SMT fuse+holder family:

| Rating | MPN | JLC | Live stock/order-field |
|---|---|---|---|
|3A|0154003.DR|C206912|1760/1743|
|10A|0154010.DR|C206921|2331/2276|
|5A|0154005.DR|C206916|Related-product stock3693; detail not yet checked|
|1A|0154001.DR|C206908|Related-product stock1822; detail not yet checked|

Holder125V10A, body9.73×5.03mm, easy fuse replacement. One common new SMT land pattern could replace all six holders, shrinking footprint and manual work. Family offers7A and8A, not7.5A; F1/F2 current choice and time-current coordination need review. Standard154 uses fast453 series; 3A nominal I²t1.65 A²s versus oldFKS8.1, interrupt50A@125VDC versusATO1kA. Available source fault current, capacitor discharge, startup and40C derating must be checked before accepting. Current finding is a redesign candidate, not a completed qualified substitution.

[Manufacturer154](https://www.littelfuse.com/assetdocs/littelfuse-fuse-154-series-data-sheet?assetguid=a8a8a462-7295-481b-a91b-d770dabf005b), [manufacturer451/453](https://www.littelfuse.com/~/media/electronics/datasheets/fuses/littelfuse_fuse_451_453_datasheet.pdf.pdf), [3A JLC](https://jlcpcb.com/partdetail/Littelfuse-0154003DR/C206912).

## Exact shunt land correction

Manufacturer MA Rev30 page8 visually inspected (`work/datasheets/everohms_ma.pdf`, `ma_land.png`), matching latest Rev34 indexed table. For MA2512 2–5mOhm, recommended a=2.60,b=3.68,i=2.55mm, where drawing labels pad-length a, pad-height b, gap i.

Use two rectangular pads **2.60×3.68mm centered(−2.575,0),(+2.575,0)** in unrotated local coordinates, then apply existing footprint rotation. Preserve existing net assignment and Kelvin connections at inner pad edges. Old generic2512 has1.225×3.35mm pads centered±2.9625, so new pads add0.30mm outward and1.075mm inward per side,0.165mm vertically. DRC and sense-route review required. New overall copper width7.75mm, gap2.55mm. No board edits made in this stream.

[Manufacturer Rev34](https://www.everohms.com/data/10000/ftp/S-10-12-05-34.pdf), [visually inspected manufacturer Rev30 mirror](https://uploadcdn.oneyac.com/attachments/files/brand_pdf/%E5%A4%A9%E4%BA%8C/3E/19/MA.pdf).


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
