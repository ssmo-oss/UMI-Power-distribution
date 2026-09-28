from pathlib import Path
import json, shutil, html

root=Path('outputs/UMI_D5')
v=root/'verification';v.mkdir(exist_ok=True)
for name in ['d5_electrical_review.md','d5_electrical_review.json','d5_metadata_audit.json']:
    shutil.copy2(Path('work')/name,v/name)
shutil.copy2('work/jlc_combined_parts_d5.json',root/'PROCUREMENT_RECORD.json')
shutil.copy2('outputs/UMI_D4/PROCUREMENT_CHANGES.json',root/'D4_COMPONENT_CHANGES_RETAINED.json')
for p in root.glob('*.md'):
    t=p.read_text(encoding='utf-8')
    t=t.replace('Native verification is pending in this document; only final D5 reports may establish a pass.', 'Final D5 native checks pass on all three boards: zero DRC violations, unconnected items, schematic parity issues and ERC violations. See each board’s verification folder.')
    t=t.replace('Native checks are pending here; final D5 verification records establish actual pass status.', 'Final D5 DRC and ERC checks pass on all three boards; the per-board verification reports and source hashes record the checked versions.')
    t=t.replace('MANUAL_FUSES_AND_HARNESS_BOM.csv adds inserts and cable-side parts;', 'The single consolidated UMI_COMPONENT_SOURCING.xlsx list includes inserts and cable-side parts;')
    t=t.replace('The manifest records the exact substitutions.', 'D4_COMPONENT_CHANGES_RETAINED.json records the inherited component substitutions; its original MAIN converter references now belong to POE_POWER.')
    p.write_text(t,encoding='utf-8')

readme='''# UMI D5 — three-board prototype revision

D5 splits the system into a passive 12 V distribution board, a separate 12 V → 53.5 V PoE-switch supply, and the two-port USB supply. Open **LAYOUT_REVIEW.html** for board images and schematic/assembly drawings. This package replaces D4 for this architecture; older revisions remain separate.

## Boards and connections

| Board | Size | Purpose | SMT / through-hole parts |
|---|---|---|---|
| MAIN_POWER | 68 × 100.264 mm | 12 V input and five fused outputs | 0 / 11 |
| POE_POWER | 106 × 100 mm | Protected 53.5 V boost supply | 53 / 3 |
| USB_POWER | 80 × 50 mm | Two charge-only USB-A sockets | 31 / 3 |

MAIN retains the original mounting-hole centres. POE has its own mounting pattern. USB remains larger than the initial 30 × 60 mm suggestion under the later permission to expand. Mechanical holes are excluded from the component counts.

Connect the external 12 V PSU to MAIN J1. MAIN J2 supplies Jetson, J3 GMSL, J4 fan, J5 USB J1, and J6 POE J1. Each 12 V connector uses pin 1 positive and pin 2 ground. POE J6 is different: pin 1 +53.5 V, pin 2 unused, pin 3 ground. Use the delivered pin schedules and label both harness ends by board name and voltage.

**Use PoE or GMSL, never both in one configuration.** This is a manual configuration rule; the boards do not enforce it electronically. With 90% assumed converter efficiency and the documented load allowances, the larger PoE configuration needs approximately **173.6 W / 14.46 A at 12 V**. Static boost tolerance raises that estimate to approximately 174.5 W / 14.54 A. These are planning estimates, not measured worst-case results. The 20 A input-path design/test target is retained for margin.

## Fuse decision

Keep all six fuses for now: MAIN F1 Jetson 7.5 A, F2 GMSL 7.5 A, F3 fan 1 A, F4 USB 5 A, F5 PoE feed 10 A; POE F6 output 3 A / 80 V. **Unlike the sketch, the PoE feed fuse is on MAIN, at the source of the interboard cable**, so it protects that cable too. There is no duplicate fuse at the POE input; the local electronic protection remains.

Jetson's 7.5 A is a provisional fuse rating, not its load requirement. A 5 A fuse carrying the full 5 A allowance has no demonstrated startup/temperature margin at the stated 40 °C enclosure ambient. Confirm actual current, inrush and the weakest wire segment before reducing it. The mutually exclusive loads reduce the overall budget but do not remove individual branch fault risks. The separate 53.5 V output fuse cannot be declared redundant solely because the converter has an input eFuse. See ENGINEERING_AND_TEST_NOTES.md and verification/d5_electrical_review.md for rationale and sources.

## Checks completed

All three finished boards pass KiCad DRC and ERC: zero violations, zero unconnected items and zero schematic parity issues. Export source hashes match the delivered sources. Independent Gerber/drill checks match all four copper layers, hole locations/sizes and SMT placement centres: MAIN 63 holes / 0 SMT placements, POE 78 / 53, USB 137 / 31. The POE extraction retains the converter's critical copper; the preservation report records the comparison. Assembly references and top/bottom Gerber previews are included.

Use each board's `*_GERBERS.zip` for the fabrication files. POE and USB have assembly paste exports and normalized `*_CPL_JLC.csv`; use the normalized file, not raw KiCad rotations. MAIN is entirely through-hole and has no SMT assembly operation. Review supplier pin-1/orientation previews before assembly approval. Manufacturing settings differ: MAIN/POE 1.2 mm; USB 1.6 mm; all four-layer, 2 oz outer / 1 oz inner. POE and USB require resin-filled, copper-capped pad vias. MAIN does not.

## Procurement and release status

The single UMI_COMPONENT_SOURCING.xlsx list covers all three boards and manual/harness parts, assuming **ten of each board**. It contains dated JLC catalogue observations, not reserved stock. MAIN J1 Phoenix 1709681 and POE R1 ERJ-12ZYJ7R5U remain preorder items; the resistor has a 734-piece purchase minimum. POE F6 has only ten observed inserts and no spare buffer; C1/L1 also have limited headroom. JLC library inventory is for assembly and cannot simply be delivered loose, so the hand-fit/harness supply arrangement still needs resolution.

**These are untested prototype files, not a production-qualified release.** Physical thermal, transient, startup, protection and real-device tests remain, along with procurement and manufacturer quote acceptance. No order, upload, reservation or payment has been made. Review MANUFACTURING_SPECIFICATION.md, MANUAL_ASSEMBLY.md and ENGINEERING_AND_TEST_NOTES.md before procurement or bring-up. SHA256SUMS.txt identifies the packaged files.
'''
(root/'README.md').write_text(readme,encoding='utf-8')
cards=[]
for name,title,size in [('MAIN_POWER','12 V distribution','68 × 100.264 mm'),('POE_POWER','PoE switch supply','106 × 100 mm'),('USB_POWER','Dual USB supply','80 × 50 mm')]:
    cards.append(f'''<section><h2>{title}</h2><p>{name} · {size} · DRC / ERC passed</p><div class="images"><figure><img src="{name}/review/{name}_gerber_top.png" alt="{title} top Gerber view"><figcaption>Top fabrication view</figcaption></figure><figure><img src="{name}/review/{name}_gerber_bottom.png" alt="{title} bottom Gerber view"><figcaption>Bottom fabrication view</figcaption></figure></div><p><a href="{name}/review/{name}_schematic.pdf">Schematic</a> · <a href="{name}/review/{name}_assembly_references.pdf">Assembly references</a> · <a href="{name}/review/{name}_layers.pdf">Layer drawings</a> · <a href="{name}/{name}_GERBERS.zip">Gerber package</a></p></section>''')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UMI D5 · Three boards</title><style>body{margin:0;background:#111a21;color:#e6eff5;font:17px/1.6 system-ui,sans-serif}main{max-width:1140px;margin:auto;padding:42px 28px}h1{font-size:42px;line-height:1.12}h2{margin:0;font-size:27px}p{max-width:950px}.eyebrow{color:#67debd;letter-spacing:.12em;text-transform:uppercase;font-size:13px}section{margin-top:34px;padding:26px;background:#1b2833;border-radius:16px}.images{display:grid;grid-template-columns:1fr 1fr;gap:20px}figure{margin:12px 0}img{display:block;width:100%;height:560px;object-fit:contain;background:#fff;border-radius:8px}figcaption{font-size:14px;color:#bbc8d1}a{color:#79dcc4}.notice{padding:18px 22px;border-left:4px solid #e9b968;background:#332d26;border-radius:8px}.flow{font-family:ui-monospace,monospace;white-space:pre-wrap;padding:20px;background:#0c141b;border-radius:10px}@media(max-width:720px){.images{grid-template-columns:1fr}img{height:auto}h1{font-size:32px}}</style><main><div class="eyebrow">UMI · Revision D5 · 26 September 2026</div><h1>Three boards. Separate PoE supply.</h1><p>The 12 V distribution, PoE boost and USB charging circuits now have separate PCBs. All three pass the configured KiCad electrical and layout checks. This review shows the actual exported fabrication geometry.</p><div class="flow">12 V PSU → MAIN distribution → Jetson + fan + USB board\n                          └→ either GMSL or separate PoE board → switch</div><p><strong>Budget: approximately 174 W / 14.5 A at 12 V.</strong> PoE and GMSL are alternative system configurations, manually selected. The PoE feed fuse stays at MAIN to protect the interboard cable; all six system fuses remain.</p><div class="notice"><strong>Prototype / procurement hold.</strong> Hardware testing, two preorder components, limited stock and the hand-fit parts supply arrangement remain unresolved. A clean software check is not physical qualification.</div><p><a href="README.md">Full revision notes</a> · <a href="UMI_COMPONENT_SOURCING.xlsx">One combined component list</a> · <a href="MANUFACTURING_SPECIFICATION.md">Manufacturing settings</a> · <a href="ENGINEERING_AND_TEST_NOTES.md">Engineering and test plan</a></p>'''+''.join(cards)+'</main></html>'
(root/'LAYOUT_REVIEW.html').write_text(page,encoding='utf-8')
print('D5 review and release notes written')
