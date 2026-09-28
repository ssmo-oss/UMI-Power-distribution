# D6 manufacturing resolution review

Read-only review of D5 sources and official JLCPCB pages, 26 September 2026. No PCB edits, uploads, messages or orders were made.

Subsequent authorized action: repaired D6 MAIN/POE stackup names and widened five POE OPT tracks to 0.20 mm; changed POE minimum track rule to 0.16 mm. USB already had correct stackup metadata and was unchanged. Audit: `work/d6_manufacturing_repairs.json`. Root owns subsequent refill/DRC; this report does not claim the widened tracks passed until that check returns.

## Ordering specification that preserves the electrical design

| Board | Quantity | Construction | Assembly |
|---|---:|---|---|
| MAIN_POWER | 10 | 4 layers, 1.2 mm, 2 oz outer / 1 oz inner, ENIG, green mask | Bare PCB; 11 user-fit through-hole parts |
| POE_POWER | 10 | 4 layers, 1.2 mm, 2 oz outer / 1 oz inner, ENIG, green mask; epoxy-filled and copper-capped solder-pad vias | Top-side SMT, 53 placements; heavy-inductor carrier/fixture required; 3 user-fit parts |
| USB_POWER | 10 | 4 layers, 1.6 mm, 2 oz outer / 1 oz inner, ENIG, green mask; epoxy-filled and copper-capped solder-pad vias | Top-side SMT, 31 placements; 3 user-fit connectors |

These options have published support individually. The exact combination still requires the order configurator/engineering quotation; this review does not establish an accepted quote. Do not substitute the default 0.5 oz inner copper or convert the 1.2 mm boards to 1.6 mm: the fuse-holder limit drove their thickness. Use routed individual outlines. Ask the assembler to add removable handling rails if needed rather than alter the delivered mounting holes. JLC's stackup selector exposes four-layer, 1.2/1.6 mm, 2 oz outer and 1 oz inner options. [Official stackup selector](https://jlcpcb.com/impedance)

## Concrete source discrepancies to resolve in D6

1. **MAIN and POE inner copper stackup naming is wrong.** Their enabled layer tables and Gerbers have four copper layers, but the saved stackup calls the two 0.035 mm copper layers `dielectric 2` and `dielectric 4`, with dielectric material properties. Name them `In1.Cu` and `In2.Cu`, retain copper thickness, and use three actual dielectric entries. USB's stackup is correctly named. This is a metadata repair, not an instruction to reroute. Reopen/save and recheck the persisted stackup and total thickness before final export.
2. **POE has five 0.15 mm F.Cu OPT tracks.** JLC's capability table permits 0.15 mm for two-ounce multilayers, but its newer copper-weight guide specifies 0.16 mm, while the FR4 product page says 0.16 mm width / 0.20 mm spacing. Treat this as a conflicting published limit, not proof of rejection. The conservative resolution is widen the five tracks to at least 0.16 mm and rerun DRC at 0.20 mm clearance where feasible. Locations are in `work/d6_geometry_stats.json`, around X125–128, Y68–69. MAIN minimum actual width is 1 mm; USB is 0.20 mm. [Copper-weight guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight), [FR4 product specification](https://jlcpcb.com/pcb-fabrication/fr4-pcb)
3. **Saved POE/USB via fabrication flags say filling/capping off.** The written fabrication specification requires filled/capped pad vias; the KiCad flags and generic tenting defaults do not encode that instruction. Ensure the fabrication drawing/order explicitly requests epoxy-filled, copper-capped VIPPO and identifies only the relevant hole sizes. Tenting and soldermask plugging are not interchangeable with that process. POE also has 0.635 mm ordinary power vias, outside the published 0.55 mm filling range; do not ask to fill every via blindly. USB holes are 0.25/0.30 mm. POE smaller via holes are 0.254/0.35/0.40 mm. [Official via-covering explanation](https://jlcpcb.com/help/article/pcb-via-covering)
4. **MAIN has thirteen visible board-level labels/symbols below 1 mm height.** Examples include the 0.85 mm fuse warning and 0.9 mm polarity marks. Increase important visible legends to 1 mm where space permits and recheck silkscreen clearance. The published guide recommends 1 mm text and 0.15 mm stroke. Treat this as legibility improvement, not an electrical defect. [Capabilities](https://jlcpcb.com/capabilities/Capab)

Current PTH pad annuli checked against 0.254 mm have no failures. USB's smallest vias are 0.45/0.25 mm, POE's 0.508/0.254 mm; these satisfy published drill/diameter capability. Via limits differ from through-hole component pad annular requirements. Existing native DRC is valuable but does not prove all manufacturing process choices, mask bridges, fixture requirements or stackup acceptance.

## Assembly and ten-board inventory

JLC's exact **SER2915H-103KL / C19276042** product listing explicitly calls for an assembly fixture. Keep that fixture in the POE quotation; do not omit L1 from the CPL or assume top-only placement eliminates the requirement. The general fixture guidance also covers mechanical support during assembly. [Exact JLC inductor listing](https://jlcpcb.com/partdetail/Coilcraft-SER2915H103KL/C19276042), [Fixture policy](https://jlcpcb.com/help/article/pcb-assembly-fixtures)

The consolidated list's 1,310 pieces are installed quantities for ten full sets, not purchase quantities. Require the assembler's part-specific minimum and attrition quantities in its quote. Do not invent a universal percentage. Existing observations leave five spare C1 capacitors (15 stock for 10), seven inductors (17 for 10), and zero spare 80 V F6 fuse inserts (10 for 10). These buffers are not reservations. F6 is manually fitted; its spare need is separate from SMT attrition. [Assembly minimum/attrition policy](https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2)

Root's later public metadata gives C1 minimum5/loss4 and L1 minimum0/loss0: ten placements suggest14 C1 and10 L1 under either common arithmetic interpretation. The official public pages do not specify whether loss is added before or after the minimum is applied. For installed10/minimum20/loss10, plausible totals are20 or30. Use30 only as a clearly labeled conservative planning allowance pending the supplier's actual BOM-match quantity; do not call that formula verified JLC policy. The metadata refresh did not supply live stock counts for every part, so the dated D5 stock observations must remain labeled as such.

MAIN J1 Phoenix 1709681 and POE R1 ERJ-12ZYJ7R5U remain exact-part preorder items, not stocked items. R1's recorded minimum is 734 pieces for a ten-piece installed requirement; price/arrival and inventory acceptance must be confirmed before committing. No need to introduce an unvalidated replacement solely to avoid that minimum. Preordered stock can be assembled only once received. [Preorder terms](https://jlcpcb.com/help/article/pre-ordering-parts-terms-conditions)

Keep the authorized user-fit route for connectors, holders, fuse inserts and harness parts. JLC component-library inventory is for PCBA, so it is not an ordinary loose-parts supply. Practical paths are independent authorized-distributor/LCSC purchase for manual parts, or an explicitly agreed JLC through-hole/hand-assembly service. Cable crimping and fuse insertion need a specific scope; merely selecting a library code is insufficient. The inductor listing itself states the PCBA-only restriction.

## Release decision

Complete the file corrections above, refill/revalidate/export D6, obtain a quote retaining copper/stackup/VIPPO/fixture requirements, and reconcile actual purchasable quantities including attrition. These steps can make the package manufacturing-review ready. Physical converter stability, thermal, overload and real-device tests remain prototype qualification; an accepted fabrication order would not complete them.
