from pathlib import Path
import json,shutil,csv
root=Path('outputs/UMI_D6');old=Path('outputs/UMI_D5');v=root/'verification';v.mkdir(exist_ok=True)
for f in ['d6_electrical_resolution.md','d6_electrical_resolution.json','d6_manual_procurement.json','d6_metadata_audit.json','d6_fabrication_details.json']:
 shutil.copy2(Path('work')/f,v/f)
shutil.copy2('work/d5_electrical_review.md',v/'power_and_fuse_basis.md')
repairs=json.loads(Path('work/d6_manufacturing_repairs.json').read_text())
for c in repairs['POE_POWER']['changes']:
 if 'track' in c:c['after']=.16
for x in repairs.values():x['native_clearance_verification']='Final D6 DRC passed at configured 0.20 mm clearance; see per-board report'
(v/'manufacturing_repairs.json').write_text(json.dumps(repairs,indent=2))
shutil.copy2(old/'D4_COMPONENT_CHANGES_RETAINED.json',root/'D4_COMPONENT_CHANGES_RETAINED.json')
for filename in ['ENGINEERING_AND_TEST_NOTES.md','MANUAL_ASSEMBLY.md','MANUFACTURING_SPECIFICATION.md']:
 t=(old/filename).read_text(encoding='utf-8').replace('D5','D6')
 t=t.replace('MAIN J1 and POE R1 retain their previous exact parts and require procurement/preorder confirmation rather than an unverified geometry or rating substitution.', 'MAIN J1 retains exact Phoenix 1709681, sourced loose from DigiKey. POE R1 changes to stocked Yageo RC2010JK-077R5L, JLC C4169838: same 7.5 ohm, 5%, 0.75 W, 2010 size. Estimated snubber dissipation is 0.301 W nominal and 0.356 W with illustrative capacitor/frequency margins. This resolves the original preorder minimum; it does not establish measured pulse endurance. See verification/d6_electrical_resolution.md.')
 t=t.replace('MAIN J1 and POE R1 remain procurement/preorder items.', 'MAIN J1 has an exact stocked loose-part source; POE R1 now uses the stocked Yageo part.')
 t=t.replace('F6 has exactly ten catalogue pieces for ten systems and no spare allowance.', 'The selected loose F6 source showed 378 pieces; the plan buys 20 for ten fitted plus ten spares. Manufacturer obsolescence is confirmed, so this resolves the current batch rather than future lifetime supply.')
 t=t.replace('The supply/installation arrangement for hand-fitted connectors, fuse holders, fuse inserts and cable-side JST parts remains pending;', 'The selected arrangement is JLC SMT assembly plus user fitting of separately purchased exact loose parts from LCSC/DigiKey;')
 t=t.replace('Agree supply/installation of hand-fitted headers, holders, inserts and cable-side parts, or buy them separately. The manual/harness arrangement remains pending.', 'Buy the exact loose manual parts from the suppliers in the consolidated list and fit them after JLC SMT assembly. Device-end plugs, final cable lengths and tooling remain installation-specific.')
 t=t.replace('MAIN J1 and POE R1 retain exact MPNs needing procurement/preorder confirmation.', 'MAIN J1 uses its original exact MPN via loose procurement; POE R1 uses stocked Yageo RC2010JK-077R5L.')
 t=t.replace('F6 has exactly ten observed inserts and no spares.', 'F6 is sourced loose, with a purchase plan of twenty including ten spares.')
 t=t.replace("F6's observed stock was exactly ten pieces: enough for the ten hand-inserted boards, with **no spare allowance**. Stock was not reserved. Distributor lifecycle warnings were found, but current manufacturer obsolescence was not established; do not represent this as an officially confirmed lifecycle status. Final procurement must confirm ten deliverable exact pieces.", 'F6 is now sourced as an exact loose part from DigiKey, with 378 pieces observed on 26 September 2026. Buy twenty: ten fitted plus ten spares. Littelfuse notice A0377 confirms obsolescence (last order 6 August 2026; last shipment 30 December 2026). Stock is not reserved. This batch can use remaining stock; a future revision needs a lifecycle replacement.')
 t=t.replace('Agree how the assembler will supply/install these items, or source manual parts separately. The manual/harness supply arrangement remains pending.', 'Source manual parts separately from the exact LCSC/DigiKey links in the consolidated list; the user fits these parts. No JLC loose-parts shipment is assumed.')
 t=t.replace('requiring exact-part procurement/preorder confirmation; no alternate terminal footprint was adopted.', 'available as an exact loose part from DigiKey; no alternate terminal footprint was adopted.')
 t=t.replace('The final suffix changes bulk pack size only;', 'The suffix identifies a manufacturer packaging option;')
 t=t.replace('manufacturer-sheet mirror', 'manufacturer-sheet mirror')
 t+='\n\nD6 fabrication detail: the five narrow POE OPT traces are now 0.16 mm; configured clearance remains 0.20 mm. MAIN visible small board legends are enlarged to 1 mm. Individual via filling/capping flags and the per-board VIA_TREATMENT.csv schedules identify selective epoxy fill and copper capping; 0.635 mm POE vias remain ordinary. See FABRICATION_NOTES.md.\n'
 (root/filename).write_text(t,encoding='utf-8')

readme='''# UMI D6 — sourcing and manufacturing corrections

D6 retains the three-board architecture and resolves the known part-sourcing and file-format issues that can be handled before fabrication. **Ready for prototype manufacturing review, not physically qualified for production.**

## Completed

- Replaced the preorder snubber resistor with stocked **Yageo RC2010JK-077R5L / C4169838**. Resistance, tolerance, power rating and footprint are unchanged. Its pulse/thermal behaviour still requires the same prototype measurement as the original part.
- Found exact loose-part sources for all thirteen manual component types. The Phoenix input connector no longer needs JLC preorder. The 80 V fuse has enough observed distributor stock for twenty pieces, including ten spares. It is obsolete; this is a batch solution, not guaranteed long-term availability.
- Defined the supply route: JLC assembles SMT; the user fits separately purchased connectors, holders, inserts and harness components. All remain on **one combined spreadsheet** with purchase links and quantities. Repeated manual MPNs are bought once; later duplicate rows show zero purchase quantity.
- Corrected MAIN/POE inner-layer stackup identities, widened five POE traces from 0.15 to 0.16 mm, enlarged MAIN's small visible labels, and encoded selective via filling/capping in the PCB sources and coordinate schedules.
- Refilled and re-exported all boards. Final KiCad DRC/ERC reports pass with zero reported violations, zero unconnected items and zero schematic-parity issues. Independent Gerber/drill/placement audits and source-hash checks are included.

## Files and order scope

Open **LAYOUT_REVIEW.html** for actual fabrication previews and schematic/assembly drawings. Order ten of each:

| Board | Outline | Thickness | Copper | Assembly |
|---|---|---|---|---|
| MAIN_POWER | 68 × 100.264 mm | 1.2 mm | 4 layers, 2 oz outer / 1 oz inner | Bare board, 11 manual parts |
| POE_POWER | 106 × 100 mm | 1.2 mm | Same | 53 SMT + 3 manual parts |
| USB_POWER | 80 × 50 mm | 1.6 mm | Same | 31 SMT + 3 manual parts |

Use the per-board Gerber ZIP, SMT BOM and normalized CPL. MAIN has no SMT operation. Read FABRICATION_NOTES.md: POE/USB need selective epoxy-filled, copper-capped vias; POE's 0.635 mm vias remain ordinary. Include the POE inductor assembly fixture. The source copper stackup is explicit; do not accept a silent change to 0.5 oz inner copper.

## Electrical configuration

MAIN J1 takes 12 V. J2 supplies Jetson, J3 GMSL, J4 fan, J5 USB J1 and J6 POE J1. All 12 V two-pin headers use pin 1 positive, pin 2 ground. POE J6 is the 53.5 V output: pin 1 positive, pin 2 empty, pin 3 ground.

Use **PoE or GMSL, never both**. There is no electronic interlock. The larger configuration is approximately **174 W / 14.5 A at 12 V**, using the documented allowances and assumed converter efficiency; retain 20 A input-path design/test margin. MAIN retains F1 Jetson 7.5 A, F2 GMSL 7.5 A, F3 fan 1 A, F4 USB 5 A and F5 PoE feed 10 A. POE retains F6 3 A / 80 V. F5 protects the interboard cable at its source. Jetson's 7.5 A is provisional protection, not expected draw; verify startup, temperature and wire protection before changing it.

## Remaining external steps

1. **Manufacturer acceptance and purchasing:** the exact copper/thickness/selective-fill combination and inductor fixture need an accepted quote. QUOTE_REQUEST.md is prepared but unsent. Approve supplier placement/polarity previews and final attrition quantities. C1 requires fourteen pieces including the reported four-piece attrition, against fifteen observed; L1 requires ten against seventeen observed. Inventory is not reserved. Other SMT allowances in the spreadsheet are conservative planning quantities where exact order-page arithmetic was unavailable.
2. **Physical prototype tests:** no assembled hardware was available to test. Thermal rise at 40 °C, stability, snubber pulses, eFuse fault transients, USB load steps and real-device compatibility cannot be established from DRC. TEST_RECORD.csv gives the pending measurements; ENGINEERING_AND_TEST_NOTES.md gives the procedure. All physical results are explicitly unperformed.
3. **Installation details:** final cable lengths, device-end plugs, weakest wire/pigtail ratings, input cable protection and the exact USB-powered device model remain to be confirmed before system integration. The interim interboard harness basis is AWG16, at most 1 m one-way; this is a documented assumption, not a measured installation.

No supplier message, order, reservation, payment or external design upload has been made. D5 is preserved. SHA256SUMS.txt identifies this package.
'''
(root/'README.md').write_text(readme,encoding='utf-8')
page=(old/'LAYOUT_REVIEW.html').read_text(encoding='utf-8').replace('D5','D6')
page=page.replace('Hardware testing, two preorder components, limited stock and the hand-fit parts supply arrangement remain unresolved. A clean software check is not physical qualification.', 'Known sourcing and fabrication-file issues are resolved. Manufacturer acceptance, live order matching and physical prototype tests remain. All manual parts have exact loose-part sources; the 80 V fuse is obsolete but stocked for this batch.')
page=page.replace('<strong>Prototype / procurement hold.</strong>','<strong>Prototype review package.</strong>')
page=page.replace('Engineering and test plan</a>','Engineering and test plan</a> · <a href="QUOTE_REQUEST.md">Prepared quote request</a> · <a href="FABRICATION_NOTES.md">Selective via treatment</a>')
(root/'LAYOUT_REVIEW.html').write_text(page,encoding='utf-8')
(root/'QUOTE_REQUEST.md').write_text('''# Prepared engineering quotation request — not sent

Please quote fabrication of ten each of UMI D6 MAIN_POWER, POE_POWER and USB_POWER, with top-side SMT assembly on POE and USB only. MAIN is bare-board supply; all connectors, fuse holders/inserts and cable-side parts are excluded from SMT assembly and will be user-fitted.

MAIN: 68 × 100.263962 mm, four layers, 1.2 mm finished thickness. POE: 106 × 100 mm, four layers, 1.2 mm. USB: 80 × 50 mm, four layers, 1.6 mm. All require 2 oz outer / 1 oz inner copper, ENIG, green soldermask, white silkscreen and FR-4 Tg150 or better. Please confirm the exact stackups and tolerances without changing outline, mounting holes or copper weights.

POE and USB require selective epoxy resin fill with copper capping of the vias identified in their manufacturing/VIA_TREATMENT.csv files. POE 0.254/0.35/0.40 mm vias and USB 0.25/0.30 mm vias are included; POE 0.635 mm ordinary vias and all component/mounting holes must remain open. Please confirm capability and pricing for this selective process at the specified copper/thickness combinations.

POE has 53 top SMT placements, USB 31. Use the normalized *_CPL_JLC.csv and matching BOM_JLC_DRAFT.csv. Please verify rotation/pin 1 in the placement preview, paste treatment over filled/capped pads, and support fixture requirements for Coilcraft SER2915H-103KL / C19276042. Include the required fixture in the quote. Add removable handling rails if needed rather than changing the board outlines.

Please confirm available quantities and assembly attrition for all SMT parts. Particular constraints: POE C1 C23481145, ten installed plus four catalogue attrition; POE L1 C19276042, ten installed; POE R1 C4169838, ten installed with supplier-confirmed minimum/attrition. The consolidated sourcing list contains dated observations, not reservations. State lead time, freight, any engineering exceptions and whether all parts can be supplied before committing to production.

Please return the complete engineering acceptance and quotation for review before any fabrication, assembly or purchase is authorised.
''',encoding='utf-8')
tests=[
('T01','All','Unpowered identity, polarity and shorts','Exact BOM and assembly drawing match; all output polarities match pin schedule; investigate any unexpected low resistance'),
('T02','USB','No-load output voltage at 12 V input','5.012–5.181 V static regulator calculation before transient effects; record each connector voltage'),
('T03','USB','Independent and simultaneous 0–3 A port loads','Both ports sustain intended load without oscillation or unintended shutdown; record cable-end drop and temperatures'),
('T04','USB','Startup, hot-plug, load release and load steps','Record min/max port voltage and settling; compare against actual device limits before connection; initial source ceiling target5.25 V'),
('T05','POE','No-load and 0–1.31 A output sweep','Nominal53.518 V; static calculation52.879–54.159 V; record ripple/regulation/efficiency; verify switch input range separately'),
('T06','POE','R1 snubber waveform and temperature','Measure switching waveform and calculate actual pulse energy/RMS power; confirm resistor manufacturer repetitive-pulse suitability and thermal margin'),
('T07','POE','Startup into switch-equivalent capacitance','No sustained oscillation, unintended current-limit latch or overshoot beyond actual switch permitted input'),
('T08','POE','Controlled overload and fault shutdown','Record eFuse IN/OUT and gate/switch-node excursions; remain within device absolute maxima; confirm latch/reset; use protected fixture'),
('T09','MAIN','Loaded voltage drop and contact heating','Record each branch and input path at intended configuration loads, then evaluate20 A design margin with suitable loads; protect weakest cable'),
('T10','System','40 °C enclosure soak','Record steady temperatures and estimate junctions within recommended operating limits; USB regulator recommended maximum125 °C junction'),
('T11','System','Actual Jetson, GMSL/PoE and USB device boot/load','Test two mutually exclusive configurations separately; measure inrush and confirm fuse/harness suitability and USB charging behaviour'),
('T12','System','Installation and EMC/ESD checks','Verify actual cable lengths/gauges/device plugs/input protection and final enclosure; no compliance claim without applicable tests')]
with (root/'TEST_RECORD.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.writer(f);w.writerow(['Test ID','Board','Measurement','Acceptance basis','Status','Measured result','Instrument/setup','Operator/date']);w.writerows([*t,'NOT PERFORMED','','',''] for t in tests)
print('D6 release notes, engineering docs, quote request and physical test record written')
