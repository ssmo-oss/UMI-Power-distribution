# D6 manual assembly and harness parts

The batch is **ten MAIN_POWER, ten POE_POWER and ten USB_POWER boards**, forming ten systems. Use each board's BOM_by_reference.csv for board-mounted through-hole parts. The single consolidated UMI_COMPONENT_SOURCING.xlsx list includes inserts and cable-side parts; do not count holders as inserts.

| Position | Insert | Rating | JLC reference | Installed quantity for ten systems |
|---|---|---|---|---:|
| Main F1/F2 | Littelfuse 028707.5PXCN | 7.5 A, 32 V DC | C142688 | 20 |
| Main F3 | Littelfuse 0287001.PXCN | 1 A, 32 V DC | C142679 | 10 |
| Main F4 | Littelfuse 0287005.PXCN | 5 A, 32 V DC | C142682 | 10 |
| Main F5 | Littelfuse 0287010.PXCN | 10 A, 32 V DC | C142683 | 10 |
| POE F6 | Littelfuse 166.7000.4302 | 3 A, 80 V DC | C3662004 | 10 |

All six system holders are Littelfuse **178.6165.0002**, JLC C207061: sixty installed holders. The suffix identifies a manufacturer packaging option; holder geometry and 80 V rating are unchanged. The 287-series 32 V inserts retain standard ATO fit and 1 kA breaking rating. The FKS 80 V insert retains the compatible ATO/FKS format and 1 kA breaking rating. Never substitute a 32 V insert on the 53.5 V switch output.

F6 is now sourced as an exact loose part from DigiKey, with 378 pieces observed on 26 September 2026. Buy twenty: ten fitted plus ten spares. Littelfuse notice A0377 confirms obsolescence (last order 6 August 2026; last shipment 30 December 2026). Stock is not reserved. This batch can use remaining stock; a future revision needs a lifecycle replacement.

JLC parts-library stock is for PCBA use and cannot simply be shipped loose. The listed codes do not mean loose fuse inserts, holders or harness parts will arrive with the boards. Source manual parts separately from the exact LCSC/DigiKey links in the consolidated list; the user fits these parts. No JLC loose-parts shipment is assumed.

MAIN and POE thickness remains 1.2 mm, below the holder's 1.5 mm limit. USB remains 1.6 mm. The JST header drawing uses 1.6 mm PCB; verify seating, retention and excess lead protrusion on the thinner MAIN and POE boards. Input terminal J1 retains Phoenix 1709681, available as an exact loose part from DigiKey; no alternate terminal footprint was adopted.

Cable housings for MAIN J2–J6, POE J1 and USB J1 change to **JST VHR-2N-BK**, a black colour variant of VHR-2N with unchanged mating geometry: seventy housings for ten systems. POE switch connector uses VHR-3N, with contacts only in positions 1 and 3; position 2 remains empty. Confirm pin 1 positive and return using final numbered pads and the pin schedule before terminating any harness.

JST SVH-41T-P1.1 accepts AWG20–16 with the specified insulation diameter. For thinner fan wires use the compatible SVH-21T-P1.1 (AWG22–18) and adjust counts. Use appropriate crimp tooling and retention/pull checks; do not tin conductors before crimping. Housing/terminal catalogue availability is not a completed cable assembly.

Installed quantities exclude spares, purchasing pack multiples, device-end plugs, supply-input cable, mounting hardware and enclosure-specific lengths. Interboard cable length remains provisional; verify it in the enclosure. Provide upstream cable protection appropriate to the actual supply-input wire and installation. Branch fuses do not protect a short before the PCB.

The manufacturer time-current curves and typical temperature derating support the selected ratings, but nuisance-opening, contact-temperature and startup checks remain required at 40 °C. Fuse clearing alone does not establish semiconductor short-circuit survival. No physical bring-up or thermal tests have been performed by the software agent.

Sources: [Littelfuse287 ATOF](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40), [LittelfuseFKS80 manufacturer-sheet mirror](https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_16670004402_apr22_xonlink.pdf), [FLR holder manufacturer-sheet mirror](https://datasheet.octopart.com/178.6165.0001-Littelfuse-datasheet-8836287.pdf), [JST VH](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf).


## Three-board wiring and configuration

MAIN J1 is the source12V input. MAIN J2Jetson,J3GMSL,J4fan,J5USB andJ6POE each use pin 1positive,pin 2GND. MAIN F5 protects the cable feeding POE J1. No duplicate POE input fuse is fitted. POE J6 is the53.5V output: pin 1positive,pin 2empty,pin 3GND. MAIN J6 and POE J6 have different voltages: label by board name and voltage.

PoE switch and GMSL must never be used in the same configuration. This is a manual configuration constraint, not interlocked hardware. Test the two permitted configurations separately. All six fuses remain; no removal is approved based on the lower combined power budget.

Each complete three-board set now has seven two-position cable housings (five MAIN outputs plus POE/USB inputs), one three-position POE output housing, and sixteen populated JST contacts if all connections use this scheme. For ten sets this is 70 two-position housings,10 three-position housings and160 contacts before spares. Select contact sizes for actual wires and reconcile the final consolidated harness BOM; device-end connectors remain installation-specific.


D6 fabrication detail: the five narrow POE OPT traces are now 0.16 mm; configured clearance remains 0.20 mm. MAIN visible small board legends are enlarged to 1 mm. Individual via filling/capping flags and the per-board VIA_TREATMENT.csv schedules identify selective epoxy fill and copper capping; 0.635 mm POE vias remain ordinary. See FABRICATION_NOTES.md.
