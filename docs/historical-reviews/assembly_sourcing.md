# Critical SMT assembly sourcing — UMI D2

Checked 2026-09-25 against current design.json files in MAIN_POWER and USB_POWER. This review identifies exact catalog matches. It is not a purchasable BOM or a stock reservation. No files were uploaded and no purchases or account changes were made.

| Board / refs | Exact manufacturer and MPN | Catalog | Evidence / action |
|---|---|---|---|
| USB_POWER / U1 | Texas Instruments — TPSM63610RDFR | [C7125816](https://www.lcsc.com/product-detail/C7125816.html) | LCSC page exposed stock 64; JLC catalog fetch failed/rate-limited. Assembly route unverified. |
| USB_POWER / U2, U3 | Texas Instruments — TPS2557DRBR | [C130056](https://jlcpcb.com/partdetail/C130056) | JLC Extended, SMT Assembly, Economic and Standard; inventory not exposed in current readable page. |
| USB_POWER / U4 | Texas Instruments — TPS2513ADBVR | [C473910](https://jlcpcb.com/partdetail/TexasInstruments-TPS2513ADBVR/C473910) | JLC Extended, SMT Assembly, Economic and Standard; inventory not exposed. |
| USB_POWER / Q1 | Alpha & Omega Semiconductor — AO4407A | [C16072](https://jlcpcb.com/partdetail/Alpha_OmegaSemicon-AO4407A/C16072) | JLC exact AOS manufacturer identity verified; do not substitute another vendor sharing the MPN. |
| USB_POWER / U5, U6 | STMicroelectronics — USBLC6-2SC6 | [C7519](https://jlcpcb.com/partdetail/C7519) | JLC exact ST manufacturer identity verified; do not use GOODWORK/UMW clones without electrical review. |
| MAIN_POWER / U1 | Texas Instruments — LM5122MHX/NOPB | [C77241](https://jlcpcb.com/partdetail/TexasInstruments-LM5122MHXNOPB/C77241) | JLC catalog entry and SMT Assembly verified; cached inventory counts deliberately not accepted as live. |
| MAIN_POWER / U2 | Texas Instruments — TPS259824ONRGER | [C2155766](https://jlcpcb.com/partdetail/TexasInstruments-TPS259824ONRGER/C2155766) | JLC Extended, SMT Assembly, Economic and Standard; inventory not exposed. |
| MAIN_POWER / Q1, Q2, Q3 | Infineon Technologies — BSC072N08NS5ATMA1 | [C3278732](https://jlcpcb.com/partdetail/3841630-BSC072N08NS5ATMA1/C3278732) | JLC catalog match verified. Old indexed result showed only one in stock; current count not exposed, so shortage cannot be confirmed or dismissed. |
| MAIN_POWER / L1 | Coilcraft — SER2915H-103KL | [C19276042](https://jlcpcb.com/partdetail/Coilcraft-SER2915H103KL/C19276042) | JLC catalog match verified. Older indexed JLC page said assembly support fixture required; current extracted page omits this. Confirm fixture service before ordering. |

## Procurement gates

- TPSM63610RDFR: part exists, TI marks it active, and LCSC exposes catalog C7125816. The retrieved LCSC page displayed 64 units. This is LCSC inventory, not proof that JLC can source and assemble it. Request JLC pre-order/global-sourcing confirmation or arrange approved consignment if direct JLC sourcing is unavailable. No such request has been submitted. [TI manufacturer page](https://www.ti.com/product/TPSM63610/part-details/TPSM63610RDFR).
- JLC inventory for the other eight critical parts is unverified. Some search-index snapshots contained quantities, but current readable pages either omitted quantity or returned stale crawls. None of those counts is presented as available stock.
- The Coilcraft inductor is approximately 30 g and large. Its older JLC listing mentioned a support fixture. Confirm assembly handling and fixture costs with the assembler; user willingness to fit through-hole parts does not cover an unassembled SMT inductor.
- The selected SOIC MOSFET and USB ESD device share names with parts from other manufacturers. Preserve AOS C16072 and ST C7519 identities. Catalog substitutions are not approved substitutes.
- Passive-component catalog mapping, feeder-loss quantities, board count, full assembly capability, stencil thermal-pad windows and final placement orientation are outside this critical-parts check and remain required.
- Confirm final sourcing only after layout/DRC and manufacturing exports are complete. A catalog entry establishes an offered component, not an approved assembly order.

## Evidence quality

JLC and LCSC links above are distributor/assembler primary catalog evidence. The module manufacturer link establishes active production only. Stock changes continuously; check the actual order quote immediately before any purchase. Search engine cached counts and related-product recommendations were not treated as live inventory.
