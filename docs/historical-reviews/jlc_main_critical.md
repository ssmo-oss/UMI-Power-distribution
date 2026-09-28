# Main critical JLC sourcing review

Verified 2026-09-26 from live JLC server-rendered componentInfo. All selected catalogue rows are Extended. Inventory is a snapshot, not reserved stock or an approved assembly quote. Preorder minimum is distinct from displayed in-stock minimum. No upload or order was made.

| Ref | MPN | JLC | Stock | Orderable | Assessment |
|---|---|---|---:|---:|---|
| L1 | SER2915H-103KL | [C19276042](https://jlcpcb.com/partdetail/C19276042) | 17 | 16 | exact; low stock and high assembly difficulty |
| U2 | TPS259824ONRGER | [C2155766](https://jlcpcb.com/partdetail/C2155766) | 1926 | 1920 | exact |
| R2 | MA251230FR004MZ | [C252682](https://jlcpcb.com/partdetail/C252682) | 2724 | 2699 | same electrical value substitute; generic land overlap verified |
| Q1,Q2,Q3 | BSC072N08NS5ATMA1 | [C3278732](https://jlcpcb.com/partdetail/C3278732) | 1 | 0 | unavailable quantity |
| L2 | XAL4020-102MEC | [C4555951](https://jlcpcb.com/partdetail/C4555951) | 9145 | 9104 | packaging suffix substitution |
| Q1,Q2,Q3 | BSC040N08NS5 | [C534333](https://jlcpcb.com/partdetail/C534333) | 6718 | 6628 | recommended prototype substitute; dynamic qualification required |
| D2 | NRVB1H100SFT3G | [C604266](https://jlcpcb.com/partdetail/C604266) | 211 | 208 | automotive qualified same-family substitution |
| U1 | LM5122MHX/NOPB | [C77241](https://jlcpcb.com/partdetail/C77241) | 13966 | 13939 | exact |
| D3 | SMBJ15A | [C83846](https://jlcpcb.com/partdetail/C83846) | 12782 | 12262 | exact |
| D4 | SS10P4-M3/86A | [C968538](https://jlcpcb.com/partdetail/C968538) | 7260 | 7224 | exact |

## Substitution assessment

BSC040N08NS5 (C534333): same Infineon PG-TDSON-8 source pins 1–3, gate 4, drain 5–8 and 80 V rating. RDS(on) 4 mOhm maximum at 10 V, 5.7 mOhm at 6 V improves conduction versus original. Gate charge rises to 43 typical / 54 maximum nC at 10 V; Coss also rises. At 223.9 kHz (RT=40.2 kOhm), three devices times 54 nC plus controller 5 mA yields 41.27 mA; with 10% frequency increase 44.9 mA, below the 50 mA minimum VCC current limit. This supports prototype substitution but does not replace ringing/thermal validation. [Infineon datasheet](https://www.infineon.com/assets/row/public/documents/24/49/infineon-bsc040n08ns5-datasheet-en.pdf), [TI datasheet](https://www.ti.com/lit/ds/symlink/lm5122.pdf).

XAL4020-102MEC replaces -102MEB by Coilcraft packaging code change B to C. Same 1 uH ±20%, 14.6 mOhm maximum DCR, 8.7 A saturation (30% drop), 6.7 A / 9.6 A RMS at 20 / 40 C rise. [Coilcraft family](https://www.coilcraft.com/en-us/products/power/shielded-inductors/molded-inductor/xal/xal40xx/), [datasheet](https://www.coilcraft.com/getmedia/6adcb47d-8b55-416c-976e-1e22e0d2848c/xal4000.pdf).

NRVB1H100SFT3G replaces MBR1H100SFT3G: same onsemi family datasheet, SOD-123FL, 100 V 1 A; NRVB is automotive-qualified prefix. Pinout unchanged. JLC linked manufacturer sheet is captured in raw metadata.

MA251230FR004MZ replaces obsolete Panasonic ERJ-M1WSF4M0U: same 4 mOhm ±1%, improved ±50 ppm/C and 3 W rating. Existing 2512 pad spans x=2.35…3.575 mm, part ends ±3.175 mm, nominal terminal length 1.15 mm: nominal solder overlap 0.825 mm, body-short tolerance minimum about 0.698 mm. Existing lands differ from manufacturer preferred pattern; accept for prototype with assembler land review, do not infer 3 W capability on generic lands. Present dissipation approximately 0.17–0.3 W. [Manufacturer MA specification](https://www.everohms.com/data/10000/ftp/S-10-12-05-34.pdf). Direct PDF download returned 403; manufacturer-indexed dimensional/specification text was accessible. Full drawing review remains an assembly check.

## Remaining assembly limits

L1 has only 16 orderable pieces and high assembly difficulty. D4 TO-277A may require fixture review. Stock of a part does not mean the assembled project is accepted; quote, orientation review, part attrition, fixture availability and prototype tests remain. The original FET has zero available order quantity, so its BOM cannot be submitted unchanged.

## Fuses

Retain branch fuses for this revision. The TPS259824 protects the boost input path, not the other 12 V branches. USB per-port current limiting does not protect the upstream 12 V cable. Fuses give replaceable branch cable/connector fault protection and are pragmatic at these power levels, although six automotive holders consume substantial area and require manual fit. Removing them would require coordinated electronic protection for every branch, verified fault behavior and revised layout; it is not an availability-only substitution. The 53.5 V output fuse must remain voltage-rated above the actual output; a 32 V automotive fuse is unsuitable there. Verified ESKA 80 V 3 A part and other fuse codes are in work/fuse_verification.json.