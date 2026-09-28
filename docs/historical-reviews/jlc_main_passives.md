# MAIN_POWER JLC passive availability audit

Counts are live public JLC page purchasing metadata (overseasStockCount); coordinating browser checks established this field matches displayed In Stock. Not reserved, final order quantity/attrition and assembly eligibility must be confirmed at ordering. Zero differs from search not found and HTTP429 unknown.

No PCB, schematic or BOM substitutions have been applied. R2 shunt is handled by the parallel critical-parts review.

| References | Original MPN | JLC code | Library | Live stock | Status |
|---|---|---|---|---:|---|
| C1 | GRM2165C2A471JA01D | â€” | Unknown | Unknown | not_found_in_search |
| C2, C3, C4, C5, C6, C7, C8 | GRM32ER71K475KE14L | [C711060](https://jlcpcb.com/partdetail/C711060) | Extended | 1941 | live_jlc_in_stock |
| C9, C16 | GRM188R71E104KA01D | [C77050](https://jlcpcb.com/partdetail/C77050) | Extended | 161914 | live_jlc_in_stock |
| C10, C13 | GRM1885C1H101JA01D | [C71664](https://jlcpcb.com/partdetail/C71664) | Unknown | Unknown | retrieval_failed |
| C11 | GCM188R71C105KA64D | [C161212](https://jlcpcb.com/partdetail/C161212) | Extended | 57409 | live_jlc_in_stock |
| C14 | GRM188R71E473KA01D | [C97893](https://jlcpcb.com/partdetail/C97893) | Extended | 0 | live_jlc_zero_stock |
| C15 | GRM21BR72A474KA73L | â€” | Unknown | Unknown | not_found_in_search |
| C17 | GRM1885C1H152JA01D | [C162204](https://jlcpcb.com/partdetail/C162204) | Extended | 26554 | live_jlc_in_stock |
| C18 | GRM188R71H153KA01D | [C86021](https://jlcpcb.com/partdetail/C86021) | Extended | 0 | live_jlc_zero_stock |
| C19, C20 | EEE-FK1K470P | â€” | Unknown | Unknown | not_found_in_search |
| C21 | GRM21BR71H105KA12L | [C77083](https://jlcpcb.com/partdetail/C77083) | Extended | 122926 | live_jlc_in_stock |
| C22 | GRM188R71H104KA93D | [C77055](https://jlcpcb.com/partdetail/C77055) | Extended | 1386623 | live_jlc_in_stock |
| C23 | GRM1885C1H682JA01D | [C162241](https://jlcpcb.com/partdetail/C162241) | Extended | 110602 | live_jlc_in_stock |
| R1 | ERJ-12ZYJ7R5U | â€” | Unknown | Unknown | not_found_in_search |
| R3, R4 | ESR03EZPJ101 | [C253328](https://jlcpcb.com/partdetail/C253328) | Extended | 12799 | live_jlc_in_stock |
| R5, R8, R12, R21 | ERJ-3GEY0R00V | [C122704](https://jlcpcb.com/partdetail/C122704) | Extended | 365980 | live_jlc_in_stock |
| R10 | CRCW060349K9FKEA | [C844789](https://jlcpcb.com/partdetail/C844789) | Extended | 4823 | live_jlc_in_stock |
| R11 | CRCW06033R30JNEA | â€” | Unknown | Unknown | not_found_in_search |
| R13 | CRCW06038K45FKEA | [C2076762](https://jlcpcb.com/partdetail/C2076762) | Extended | 5 | live_jlc_in_stock |
| R14 | CRCW060330K0JNEA | [C2076641](https://jlcpcb.com/partdetail/C2076641) | Extended | 3633 | live_jlc_in_stock |
| R16 | CRCW060340K2FKEA | [C844784](https://jlcpcb.com/partdetail/C844784) | Extended | 5321 | live_jlc_in_stock |
| R17 | CRCW060320K5FKEA | â€” | Unknown | Unknown | not_found_in_search |
| R18 | RT0603BRD071K96L | [C861213](https://jlcpcb.com/partdetail/C861213) | Extended | 2298 | live_jlc_in_stock |
| R19 | RT0603BRD0784K5L | â€” | Unknown | Unknown | not_found_in_search |
| R20 | RT0603BRD07931RL | â€” | Unknown | Unknown | not_found_in_search |
| R22 | RT0603BRD07100KL | [C122538](https://jlcpcb.com/partdetail/C122538) | Extended | 1241622 | live_jlc_in_stock |
| R23 | RT0603BRD0713K7L | [C861119](https://jlcpcb.com/partdetail/C861119) | Extended | 1868 | live_jlc_in_stock |
| R24 | RT0603BRD07182RL | [C705731](https://jlcpcb.com/partdetail/C705731) | Extended | 2535 | live_jlc_in_stock |
| R25 | RT0603BRD07511RL | â€” | Unknown | Unknown | not_found_in_search |

## Substitution candidates, not approved

| Ref | Candidate | JLC | Live stock | Assessment |
|---|---|---|---:|---|
| R5,R8,R12,R21 | ERJ3GEY0R00V | [C122704](https://jlcpcb.com/partdetail/C122704) | 365980 | Exact part after manufacturer hyphen normalization. |
| R17 | 0603WAF2052T5E | [C22910](https://jlcpcb.com/partdetail/C22910) | 38124 | 20.5k 1%100mW75V0603; same value/tolerance/power, verify resistor pulse/environment spec. |
| R11 | 0603WAF330KT5E | [C22979](https://jlcpcb.com/partdetail/C22979) | 347223 | 3.3ohm1%100mW0603; improved tolerance over5%, verify startup resistor pulse behavior. |
| R1 | 201007F750KT4E | [C421781](https://jlcpcb.com/partdetail/C421781) | 8 | 7.5ohm1%750mW2010; verify repetitive snubber pulse curve before approval. |
| R19 | RT0603BRC0784K5L | [C861034](https://jlcpcb.com/partdetail/C861034) | Unknown | 84.5k0.1%15ppm0603; sameYageoRTfamily with improvedTCR vs25ppm. |
| R20 | RT0603BRC07931RL | [C861054](https://jlcpcb.com/partdetail/C861054) | 0 | 931ohm0.1%15ppm0603; sameYageoRTfamily with improvedTCR vs25ppm. |
| R25 | ERA-3AEB5110V | [C2075538](https://jlcpcb.com/partdetail/C2075538) | 0 | 511ohm0.1%25ppm100mW0603; same nominal specification; exact datasheet/package verify. |
| R25 | RQ73C1J511RBTD | [C3959727](https://jlcpcb.com/partdetail/C3959727) | 0 | 511ohm0.1%10ppm150mW0603; alternative pending manufacturer verification. |
| C1 | GCM2165C2A471GA16D | [C17565246](https://jlcpcb.com/partdetail/C17565246) | Unknown | 470pF100VC0G0805 2%; improved tolerance; same dielectric, noDCbias concern. |
| C1 | VJ0805A471GXBPW1BC | [C2254220](https://jlcpcb.com/partdetail/C2254220) | 0 | 470pF100VC0G0805 2%; manufacturer dimensions and voltage coefficient verify. |
| C15 | CC0805KKX7R0BB474 | [C596323](https://jlcpcb.com/partdetail/C596323) | Unknown | 470nF100VX7R10%0805; IC_VIN decoupling around12V, compareDCbias effectivecapacitance. |
| C15 | 08051C474KAT2A | [C597304](https://jlcpcb.com/partdetail/C597304) | Unknown | 470nF100VX7R10%0805; compareDCbias at12V and footprint height. |
| C19,C20 | EEHZC1K470P | [C178648](https://jlcpcb.com/partdetail/C178648) | 12 | 47uF80V10x10.2 hybrid 36mohm versusold700mohm. NOTdropinapproved: outputfilterdamping/stability changes, land drawing required. |
| C18 | CC0603KRX7R9BB153 | [C107076](https://jlcpcb.com/partdetail/C107076) | 403038 | 15nF50VX7R10%0603; same compensationvalue; verifyDCbias atCOMP/FB (~fewV). |
| C18 | 0603B153K500NT | [C1596](https://jlcpcb.com/partdetail/C1596) | 40770 | 15nF50VX7R10%0603; same compensationvalue, compareeffectivecapacitance. |

## Engineering constraints

- C2â€“C8 should retain the exact Murata 80 V, 4.7 ÂµF, 1210 part where possible. Nominal capacitance alone does not establish effective capacitance at 53.5 V. A different 80/100 V ceramic requires DC-bias data and control-loop review.
- C1 is the snubber capacitor: preserve 470 pF, C0G/NP0, at least100 V and +/-5% or better. Do not substitute X7R or a50 V part.
- R1 needs repetitive snubber pulse capability, not merely matching 7.5 ohm/2010/wattage. The stocked UniRoyal candidate is not approved until its pulse curve is checked.
- C19/C20 hybrid candidate has much lower ESR than the original Panasonic FK electrolytic. The changed output-filter damping and converter stability need review; matching body size and voltage is insufficient. EEE-FN1K470UL is rejected as a direct replacement:8 mm body,1.3 ohm ESR and130 mA ripple differ from the10 mm original.
- R18/R19/R20 feedback divider and R22/R23/R24/R25 protection components retain0.1% requirements. Do not silently substitute generic1% parts. Same-value15ppm Yageo alternatives improve TCR but currently have unknown/zero stock.
- C18 compensation capacitor: YageoC107076 has matching15 nF50 VX7R10%0603 nominal specs and substantial live stock; compare effective capacitance in its low-voltage compensation application before final substitution.
- C14 alternate C107093 (CC0603KRX7R9BB473) has matching47 nF/X7R/10%/0603 and higher50 V rating; live inventory still needs browser confirmation.
- The exact8.45 kohm R13 has only5 reported parts; this is not enough for a comfortable small assembly order including attrition.

HTTP429 occurred on C71664, C861034, C17565246, C596323 and C597304. Their stock remains unknown; no claim of out-of-stock follows from rate limiting. Raw live page evidence is retained in work/jlc_main_passive_pages/.

Update: Root live JLC browser found the exact bulk capacitors as normalized EEEFK1K470P / C178556, stock259 minimum1. Retain the original FK electrolytic. The hybrid candidate is unnecessary and not approved.

## Additional exact parts confirmed in live JLC browser

|Ref|Code|Stock|Minimum|
|---|---|---:|---:|
|C1|[C97904](https://jlcpcb.com/partdetail/C97904)|0|317|
|C15|[C97926](https://jlcpcb.com/partdetail/C97926)|12424|1|
|R1|[C2086794](https://jlcpcb.com/partdetail/C2086794)|0|734|
|R11|[C4212014](https://jlcpcb.com/partdetail/C4212014)|0|388|
|R17|[C844143](https://jlcpcb.com/partdetail/C844143)|155|1|
|R19|[C705797](https://jlcpcb.com/partdetail/C705797)|10|1|
|R20|[C861600](https://jlcpcb.com/partdetail/C861600)|7|1|
|R25|[C861455](https://jlcpcb.com/partdetail/C861455)|678|1|

All Extended. R1 original rating is 750 mW. R19/R20 stocks are low; do not equate listed stock with sufficient assembly quantity.

## Manufacturer-reviewed capacitor alternatives

C14: Yageo CC0603KRX7R9BB473, C107093, live JLC stock1,574,400. C18: Yageo CC0603KRX7R9BB153, C107076, live403,038. Both 50V X7R10%,0603; manufacturer dimensions1.6x0.8x0.8mm +/-0.1. C14 preserves47nF with higher voltage rating; C18 preserves15nF. Prototype timing/loop checks remain required.

Primary sources: https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB473 and https://www.yageogroup.com/download/specsheet/CC0603KRX7R9BB153

C1 alternative C17565246 now verified zero stock. R1 VO SCR2010J7R5 C5140273 live235 stock, but not approved: manufacturer PDF inaccessible and repetitive snubber-pulse rating unverified.

## Applied-change research handoff (10 boards)

Manufacturer-reviewed alternatives are recorded in `jlc_main_approved_substitutes.json`: C1 KEMET C23481145 (15 stock), R11 Yageo C137725 (159032), R13 Yageo C163417 (529), R19 Panasonic C4295220 (694), R20 Yageo C861604 (903). C1 has only five parts beyond the ten placements, so assembler attrition remains a purchasing gate.

R20 changes931Ω to953Ω explicitly. Nominal output53.518163V versus53.504694V before; static extremes52.879495–54.159133V from reference±1% and divider±0.1%, excluding bias/ripple/thermal/overshoot.

R1 remains unresolved. BournsCRM2010-JW-7R5ELF has only1stock, originalPanasoniczero stock/preorder734minimum, UNI-ROYAL201007F750KT4E only8stock, VO SCR2010J7R5 has235stock but manufacturer pulse information inaccessible. A pulse-rated7.32Ω1% or7.68Ω1% alternative would stay completely within the original7.5Ω±5% tolerance envelope;8.2Ω does not. Two15Ωpulse-ratedresistors inparallel is an exact7.5Ω redesign option requiring an added footprint. No unverifiedVO substitute approved.
