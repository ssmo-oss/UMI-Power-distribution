# USB_POWER JLCPCB availability audit

All 16 intended SMT parts have live stocked JLC catalog matches; complete TDK orderable suffix required. Stock is not reserved and assembly order acceptance not yet tested.

31 SMT placements, 16 distinct parts. All catalog entries are Extended. Checked 26 September 2026 UTC. No board or BOM source was edited.

| References | Qty | Full catalog MPN | JLC code | Package | Displayed stock |
|---|---:|---|---|---|---:|
| C1,C2 | 2 | CNA6P1X7R1H106KT000A | [C694544](https://jlcpcb.com/partdetail/C694544) | 1210 | 1,024 |
| C12 | 1 | EEEFK1E470P | [C178545](https://jlcpcb.com/partdetail/C178545) | 6.3x5.8mm | 12,963 |
| C3,C9,C10,C13,C14 | 5 | GRM32ER71A476ME15L | [C415541](https://jlcpcb.com/partdetail/C415541) | 1210 | 741 |
| C4,C5,C8,C11 | 4 | GRM188R71E104KA01D | [C77050](https://jlcpcb.com/partdetail/C77050) | 0603 | 161,914 |
| C6,C7 | 2 | GRM31CR71A226KE15L | [C91604](https://jlcpcb.com/partdetail/C91604) | 1206 | 101,994 |
| D1 | 1 | BZT52C12-7-F | [C124196](https://jlcpcb.com/partdetail/C124196) | SOD-123 | 9,099 |
| Q1 | 1 | AO4407A | [C16072](https://jlcpcb.com/partdetail/C16072) | SOIC-8 | 24,090 |
| R1 | 1 | RT0603BRD0724K9L | [C136967](https://jlcpcb.com/partdetail/C136967) | 0603 | 6,436 |
| R2,R3 | 2 | RT0603BRD0732K4L | [C861323](https://jlcpcb.com/partdetail/C861323) | 0603 | 22,326 |
| R4,R5,R6,R9 | 4 | RC0603FR-07100KL | [C14675](https://jlcpcb.com/partdetail/C14675) | 0603 | 8,590,459 |
| R7 | 1 | RT0603BRD07102KL | [C861068](https://jlcpcb.com/partdetail/C861068) | 0603 | 10,762 |
| R8 | 1 | RC0603FR-0715K8L | [C155689](https://jlcpcb.com/partdetail/C155689) | 0603 | 26 |
| U1 | 1 | TPSM63610RDFR | [C7125816](https://jlcpcb.com/partdetail/C7125816) | B3QFN-22(6.5x7.5) | 64 |
| U2,U3 | 2 | TPS2557DRBR | [C130056](https://jlcpcb.com/partdetail/C130056) | SON-8(3x3) | 1,957 |
| U4 | 1 | TPS2513ADBVR | [C473910](https://jlcpcb.com/partdetail/C473910) | SOT-23-6 | 37 |
| U5,U6 | 2 | USBLC6-2SC6 | [C7519](https://jlcpcb.com/partdetail/C7519) | SOT-23-6L | 45,071 |

## Required sourcing correction

C1/C2: replace incomplete base CNA6P1X7R1H106K with **CNA6P1X7R1H106KT000A**, C694544. [TDK product record](https://product.tdk.cn/zh/search/capacitor/ceramic/mlcc/info?part_no=CNA6P1X7R1H106K250AE) explicitly gives delivery MPN pattern CNA6P1X7R1H106KT***A, 10µF±10%, 50V, X7R, 3.2×2.5×2.5mm. The alternative electrical-record code C2182452 is zero-stock; use stocked delivery code C694544. Panasonic EEE-FK1E470P is the same punctuation-normalized catalog MPN EEEFK1E470P.

## Stock and evidence limits

R8 has 26 pieces displayed and zero presale count; U4 has 37 and U1 has 64. These are the limiting per-board parts and must be reconfirmed for the intended order quantity and assembly attrition. No unsupported substitute is proposed: current exact parts are stocked, and no batch quantity is specified.

Displayed stock comes from the JLC field overseasStockCount, verified against root browser rows. canPresaleNumber is retained separately in JSON and is not displayed stock. preMinPurchaseNum is a pre-order minimum, not assembly minimum. Root live browser confirmed minimum 1 for the four additional parts and TPSM63610RDFR/TPS2557DRBR. Public page evidence for the initial twelve parts is saved under work/jlc_evidence; the other four are root browser observations. Stock alone does not reserve inventory or establish final assembly-order acceptance.

J1 and J2/J3 remain user-fit through-hole parts and are excluded from this SMT audit. The old U1 BOM note saying LCSC-only is obsolete: live JLC C7125816 explicitly shows stock64.
