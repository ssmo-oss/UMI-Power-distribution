from pathlib import Path
import shutil
src=Path('outputs/UMI_D3');dst=Path('outputs/UMI_D4');dst.mkdir(exist_ok=True)
s=(src/'ENGINEERING_AND_TEST_NOTES.md').read_text(encoding='utf8')
s=s.replace('# UMI two-board system — engineering and prototype test notes','# UMI D4 — engineering and prototype test notes')
s=s.replace('The latest authorized enclosure assumption', 'D4 is a procurement revision for ten MAIN_POWER and ten USB_POWER prototypes. It is not a tested hardware release or an order-ready approval.\n\nThe latest authorized enclosure assumption')
s=s.replace('## Wiring and assembly','''## D4 component changes

The manifest records the exact substitutions. Main Q1–Q3 are Infineon BSC040N08NS5: same 80 V package/pinout, lower on-resistance but increased gate/output charge. The driver-current budget was reviewed; switching-node ringing, gate waveform and 40 °C thermal tests remain required. L2 changes to Coilcraft XAL4020-102MEC (packaging suffix), D2 to onsemi NRVB1H100SFT3G (same family/pinout), and the 4 mΩ shunt R2 to Ever Ohms MA251230FR004MZ. R2 uses the manufacturer-recommended 2.60 × 3.68 mm pads with a 2.55 mm inner gap; Kelvin sense continuity must be preserved.

R20 changes from 931 Ω to 953 Ω, with R19 84.5 kΩ and R18 1.96 kΩ, all 0.1%. The nominal boost target is **53.518163 V**. The calculated static tolerance interval is **52.879495–54.159133 V**, excluding ripple, bias effects and transients. A switch adapter label of 53.5 V is not evidence of its maximum acceptable input; verify the actual switch input range and startup behavior before connection.

Selected capacitors/resistors use the equivalents listed in the substitution manifest. No branch current ratings or fuse ratings were increased. USB input capacitors use the complete TDK order code CNA6P1X7R1H106KT000A. Main J1 and R1 retain their previous exact parts and require procurement/preorder confirmation rather than an unverified geometry or rating substitution.

## Wiring and assembly''')
s=s.replace('Read the final release-status file before ordering. Exact MPNs are provided where selected; blank catalog codes in BOM_JLC_DRAFT.csv are unresolved assembler sourcing, not permission for substitution. Confirm all sourcing, copper thickness, board thickness, via-in-pad processing, assembly orientation and the heavy-inductor fixture in the quote. No order, payment or external upload has been made.','''Read the D4 README and procurement records before ordering. The requested batch is ten of each board. Live catalogue inventory is not reserved inventory and does not establish assembly acceptance. Main J1 and R1 remain procurement/preorder items. Main C1 and L1 have limited stock headroom; assembler attrition must be included. F6 has exactly ten catalogue pieces for ten systems and no spare allowance.

JLC parts-library components are for PCBA orders and cannot simply be shipped loose. The supply/installation arrangement for hand-fitted connectors, fuse holders, fuse inserts and cable-side JST parts remains pending; catalogue matches do not complete the harness procurement. Confirm copper/thickness, filled/capped vias, placement orientation and the heavy-inductor fixture in the quote. No physical test, order, payment or external upload is established by these documents.''')
s=s.replace('WÃ¼rth','Würth')
(dst/'ENGINEERING_AND_TEST_NOTES.md').write_text(s,encoding='utf8')
s=(src/'MANUFACTURING_SPECIFICATION.md').read_text(encoding='utf8')
s=s.replace('# Fabrication and assembly specification — prototype','# D4 fabrication and assembly specification — ten prototypes of each board')
s=s.replace('The USB power module has an LCSC catalog match but its JLC assembly sourcing route is not confirmed.','A populated catalogue code is a sourcing reference, not stock reservation or assembler acceptance. Main J1 and R1 remain exact-part procurement/preorder items; consult the D4 procurement status.')
s=s.replace('The exported files have been checked against KiCad and independently parsed where the verification report states a pass.','Only the D4 verification records establish which exported files and checks passed. Do not inherit a D3 pass result after a source change.')
s += '''

## D4 handoff conditions

Build quantity is ten MAIN_POWER plus ten USB_POWER boards. Board outline, mounting holes, thickness and copper specification are unchanged by the procurement revision. Main shunt R2 has new manufacturer-recommended pads (2.60 × 3.68 mm, 2.55 mm gap); this requires fresh D4 copper/connectivity and stencil review. Do not reuse the D3 paste file.

Fuse holders are now Littelfuse 178.6165.0002, a packaging-only change from .0001. Insert values remain 7.5 A, 7.5 A, 1 A, 5 A, 10 A and 3 A; the last insert is rated 80 V DC. The exact inserts appear in MANUAL_ASSEMBLY.md. No Nano2 or electronic-fuse redesign was adopted.

Use the D4 normalized CPL and its matching BOM only. Verify every substituted part against the assembler's library/pin-1 preview. Reserve sufficient components for ten boards plus the assembler's required attrition; visible stock is not a reservation. C1/L1 and the ten-piece F6 supply need particular attention. F6 is hand-inserted and has no spare allowance in the observed stock.

JLC library parts are PCBA-only and are not shipped separately. Hand-fitting authorization does not arrange delivery of loose catalogue parts. Obtain an explicit assembler supply/installation arrangement or source manual/harness items separately. This remains unresolved and prevents describing the whole package as ready to order without conditions. No hardware testing or manufacturing quote is claimed.
'''
(dst/'MANUFACTURING_SPECIFICATION.md').write_text(s,encoding='utf8')
manual='''# D4 manual assembly and harness parts

The batch is **ten MAIN_POWER and ten USB_POWER boards**, forming ten systems. Use each board's BOM_by_reference.csv for board-mounted through-hole parts. MANUAL_FUSES_AND_HARNESS_BOM.csv adds inserts and cable-side parts; do not count holders as inserts.

| Position | Insert | Rating | JLC reference | Installed quantity for ten systems |
|---|---|---|---|---:|
| Main F1/F2 | Littelfuse 028707.5PXCN | 7.5 A, 32 V DC | C142688 | 20 |
| Main F3 | Littelfuse 0287001.PXCN | 1 A, 32 V DC | C142679 | 10 |
| Main F4 | Littelfuse 0287005.PXCN | 5 A, 32 V DC | C142682 | 10 |
| Main F5 | Littelfuse 0287010.PXCN | 10 A, 32 V DC | C142683 | 10 |
| Main F6 | Littelfuse 166.7000.4302 | 3 A, 80 V DC | C3662004 | 10 |

All six holders are Littelfuse **178.6165.0002**, JLC C207061: sixty installed holders. The final suffix changes bulk pack size only; holder geometry and 80 V rating are unchanged. The 287-series 32 V inserts retain standard ATO fit and 1 kA breaking rating. The FKS 80 V insert retains the compatible ATO/FKS format and 1 kA breaking rating. Never substitute a 32 V insert on the 53.5 V switch output.

F6's observed stock was exactly ten pieces: enough for the ten hand-inserted boards, with **no spare allowance**. Stock was not reserved. Distributor lifecycle warnings were found, but current manufacturer obsolescence was not established; do not represent this as an officially confirmed lifecycle status. Final procurement must confirm ten deliverable exact pieces.

JLC parts-library stock is for PCBA use and cannot simply be shipped loose. The listed codes do not mean loose fuse inserts, holders or harness parts will arrive with the boards. Agree how the assembler will supply/install these items, or source manual parts separately. The manual/harness supply arrangement remains pending.

Main board thickness remains 1.2 mm, below the holder's 1.5 mm limit. USB remains 1.6 mm. The JST header drawing uses 1.6 mm PCB; verify seating, retention and excess lead protrusion on the thinner main board. Input terminal J1 retains Phoenix 1709681, requiring exact-part procurement/preorder confirmation; no alternate terminal footprint was adopted.

Cable housings for main J2–J5 and USB J1 change to **JST VHR-2N-BK**, a black colour variant of VHR-2N with unchanged mating geometry: fifty housings for ten systems. Main switch connector uses VHR-3N, with contacts only in positions1 and3; position2 remains empty. Confirm pin1 positive and return using final numbered pads and the pin schedule before terminating any harness.

JST SVH-41T-P1.1 accepts AWG20–16 with the specified insulation diameter. For thinner fan wires use the compatible SVH-21T-P1.1 (AWG22–18) and adjust counts. Use appropriate crimp tooling and retention/pull checks; do not tin conductors before crimping. Housing/terminal catalogue availability is not a completed cable assembly.

Installed quantities exclude spares, purchasing pack multiples, device-end plugs, supply-input cable, mounting hardware and enclosure-specific lengths. Interboard cable length remains provisional; verify it in the enclosure. Provide upstream cable protection appropriate to the actual supply-input wire and installation. Branch fuses do not protect a short before the PCB.

The manufacturer time-current curves and typical temperature derating support the selected ratings, but nuisance-opening, contact-temperature and startup checks remain required at40 °C. Fuse clearing alone does not establish semiconductor short-circuit survival. No physical bring-up or thermal tests have been performed by the software agent.

Sources: [Littelfuse287 ATOF](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40), [LittelfuseFKS80 manufacturer-sheet mirror](https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_16670004402_apr22_xonlink.pdf), [FLR holder manufacturer-sheet mirror](https://datasheet.octopart.com/178.6165.0001-Littelfuse-datasheet-8836287.pdf), [JST VH](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf).
'''
(dst/'MANUAL_ASSEMBLY.md').write_text(manual,encoding='utf8')
refs=dst/'verification/reference_documents';refs.mkdir(parents=True,exist_ok=True)
for name in ['everohms_ma.pdf','fks80_verified.pdf','jst_vh.pdf','bsc040.pdf','efuse.pdf']:
 p=Path('work/datasheets')/name
 if p.exists():shutil.copy2(p,refs/name)
print('Three D4 documents written; reference PDFs copied.')
