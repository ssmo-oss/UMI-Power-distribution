# Manual-fitting parts review

Status: connector mating parts verified from primary datasheet; fuse order-code/curve verification still open. No design edits made by this review.

## JST VH harness ends — verified

Source: [JST VH manufacturer datasheet](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf), saved as `work/datasheets/jst_vh.pdf`; rendered pages 1 and 2 were inspected because embedded text encoding is defective.

| Use | Exact part | Quantity for PCB-side harness interfaces | Evidence |
|---|---|---:|---|
| Mate standard B2P-VH headers | JST VHR-2N | 5 | Housing table, page 2; two circuits, 3.96 mm pitch |
| Mate standard B3P-VH switch header | JST VHR-3N | 1 | Housing table, page 2; three circuits, 3.96 mm pitch |
| AWG16 receptacle contact | JST SVH-41T-P1.1 | 12 if every populated wire uses this compatible wire range | Page 2: AWG20–16, 0.5–1.25 mm², insulation OD 1.7–3.0 mm, tin-plated copper alloy |
| Optional smaller-wire receptacle contact | JST SVH-21T-P1.1 | Replace relevant contact quantities, do not add blindly | Page 2: AWG22–18, 0.33–0.83 mm², insulation OD 1.7–3.0 mm |

The five 2-position housings cover main-board Jetson, SG4A, fan and USB outputs, plus USB-board input. Thus both ends of the interboard cable are included. Device-side proprietary/barrel connector ends are **not** included or verified here. The 3-position switch housing should contain contacts only in positions 1 (+53.5 V) and 3 (return); position 2 remains empty according to the present design. Housing position numbering must be followed from the drawing, not inferred from a front/back photograph.

The AWG16 selection is supported explicitly by the manufacturer table. A smaller fan pigtail must use a contact matched to its actual conductor and insulation size, or a suitable transition to the chosen harness wire; do not crimp undersized conductors in the AWG20–16 contact. The `S` contact designation is strip/reel form. Hand-fitting still requires proper contact crimping; buying the right contact does not establish a hand-tool setting or completed crimp quality. Manufacturer-listed applicators are APLMK SVH41-11 / SVH21-11 for their machine system, not evidence of a generic hand crimper.

Page 1 rates standard-header VH at 10 A with AWG16, 250 V AC/DC, and −40 to +105°C including current-caused temperature rise. These ratings support the intended per-branch currents but do not establish harness temperature rise in the actual enclosure. Page 1 states 1.6 mm applicable PCB thickness: the USB board uses 1.6 mm, while the main board's thinner stackup chosen for its fuseholder requires a mechanical fit/solder projection review. This is not an electrical-current derating curve.

## Fuses — desired values, not yet released purchase codes

| Ref | Intended nominal value | Circuit |
|---|---:|---|
| F1 | 7.5 A | Jetson 12 V |
| F2 | 7.5 A | SG4A 12 V |
| F3 | 1 A | Fan 12 V |
| F4 | 5 A | USB-board 12 V |
| F5 | 10 A | Boost input |
| F6 | 3 A, **80 V DC minimum** | 53.5 V switch output |

All six holders are currently identified as Littelfuse `178.6165.0001`. The root-provided candidate for F6 is Littelfuse `166.7000.4302` (FKS 80 V). This review has **not yet verified** its order-code suffix, time-current curve, temperature correction or physical fit against the holder. Do not promote it to a released order line solely because its family name and nominal ratings sound appropriate.

The supplied public manufacturer/Mouser PDF paths returned access errors in this stream. `work/datasheets/fuse_80v.pdf` is actually an HTML response, not a usable datasheet. The web-search tool also failed authentication, and this stream has no available browser surface. JST's primary PDF was accessible directly. These access limitations are recorded to distinguish missing evidence from a component failure.

Needed before releasing fuse lines: exact manufacturer ordering table, blade/body mechanical dimensions matched to the 178 holder, DC interrupting rating at the application voltage, nominal melting/clearing characteristics, 40°C temperature correction, and startup/inrush coordination. No generic automotive-fuse derating number has been substituted for manufacturer data. Fuses protect wiring and fault energy; nominal fuse current is not an exact trip threshold or a substitute for the eFuse's semiconductor fault protection.
