# D6 loose manual-part procurement

Ten three-board systems. Every specified board-mounted manual part, fuse insert and listed JST mating component has an exact-part source with observed stock exceeding the recommended quantity. No substitute footprints are needed for this batch. No order has been placed.

Quantities include 20% spares rounded to the selected supplier pack multiple, except the obsolete 80 V fuse: 10 installed plus 10 spares. Stock was checked on 26 September 2026 through supplier web pages; it is unreserved and may change.

| Exact MPN | Use | Installed | Buy | Supplier/code | Observed stock | MOQ / multiple |
|---|---|---:|---:|---|---:|---|
| 1709681 | MAIN J1 | 10 | 12 | [DigiKey exact part](https://www.digikey.com/en/products/detail/phoenix-contact/1709681/2511044) | 78 | 1 / 1 |
| 178.6165.0002 | MAIN F1-F5; POE F6 holders | 60 | 72 | [LCSC C207061](https://www.lcsc.com/product-detail/Fuse-Holders_Littelfuse-178-6165-0002_C207061.html) | 617 | 1 / 1 |
| B2P-VH(LF)(SN) | MAIN J2-J6; POE J1; USB J1 | 70 | 90 | [LCSC C160315](https://www.lcsc.com/product-detail/C160315.html) | 296,150 | 10 / 10 |
| B3P-VH(LF)(SN) | POE J6 | 10 | 15 | [LCSC C160316](https://www.lcsc.com/product-detail/C160316.html) | 31,215 | 5 / 5 |
| 614004190021 | USB J2,J3 | 20 | 24 | [DigiKey 732-10012-ND](https://www.digikey.com/en/products/detail/w%C3%BCrth-elektronik/614004190021/5956436) | 4,651 | 1 / 1 |
| 028707.5PXCN | MAIN F1,F2 inserts 7.5A32V | 20 | 24 | [DigiKey F4198-ND](https://www.digikey.com/en/products/detail/littelfuse-inc/028707-5PXCN/2519829) | 21,020 | 1 / 1 |
| 0287001.PXCN | MAIN F3 insert 1A32V | 10 | 15 | [LCSC C142679](https://www.lcsc.com/product-detail/C142679.html) | 3,750 | 5 / 5 |
| 0287005.PXCN | MAIN F4 insert 5A32V | 10 | 15 | [LCSC C142682](https://www.lcsc.com/product-detail/PTC-Fuse_Littelfuse_0287005-PXCN_5A-32V_C142682.html) | 5,895 | 5 / 5 |
| 0287010.PXCN | MAIN F5 insert 10A32V | 10 | 15 | [LCSC C142683](https://www.lcsc.com/product-detail/C142683.html) | 14,670 | 5 / 5 |
| 166.7000.4302 | POE F6 insert 3A80V | 10 | 20 | [DigiKey exact part](https://www.digikey.com/en/products/detail/littelfuse-inc/166-7000-4302/2515899) | 378 | 1 / 1 |
| VHR-2N-BK | Two-position cable housings | 70 | 90 | [LCSC C595405](https://www.lcsc.com/product-detail/C595405.html) | 30,640 | 10 / 10 |
| VHR-3N | POE output cable housing; middle cavity empty | 10 | 20 | [LCSC C157899](https://www.lcsc.com/product-detail/C157899.html) | 49,960 | 10 / 10 |
| SVH-41T-P1.1 | AWG20-16 cable contacts; gauge must match actual wires | 160 | 200 | [LCSC C160350](https://www.lcsc.com/product-detail/C160350.html) | 136,100 | 100 / 100 |

## Procurement decisions

- Phoenix 1709681: exact part available from DigiKey (78 observed). Buy 12; JLC preorder is unnecessary for hand assembly.
- F6 166.7000.4302: exact 3 A / 80 V part available from DigiKey (378 observed). Buy 20. Do not replace it with a 32 V insert.
- F6 lifecycle is now established: [Littelfuse notice A0377, hosted by TTI](https://www.ttieurope.com/content/dam/tti-europe/products/PCN/Littelfuse/Littelfuse-A0377.pdf) names this part, with last order 6 August 2026 and last shipment 30 December 2026. DigiKey also marks it obsolete. This corrects the earlier D5 statement that manufacturer obsolescence was not established.
- JST two-position headers and housings: 84 pieces would provide 20% spares, but the selected LCSC listings sell in multiples of 10, so buy 90.
- LCSC is preferred where its exact loose-part page was readable. DigiKey is the fallback for Phoenix, USB-A receptacles, 7.5 A inserts and the 80 V insert. These links concern loose procurement, not JLC assembly inventory.

## Remaining installation details

- Device-end plugs, wire lengths, source-input cable/protection, mounting hardware and crimp-tool arrangement remain installation-dependent.
- 160 contacts assumes all 16 contacts per system use SVH-41T-P1.1. If thinner fan leads require SVH-21T-P1.1, split quantities after wire selection.
- No purchases, baskets or board edits were made.

The holder suffix .0002 denotes the 500-piece manufacturer package; the selected LCSC listing allows individual pieces. Do not confuse a manufacturer full-pack size with the retailer minimum order.
