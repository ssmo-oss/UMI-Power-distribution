# Verified fuse candidates

Manufacturer primary source: https://www.eska-fuses.de/fileadmin/produkte/datenblaetter/ESKA_KFZ_Sicherungen.pdf . Retrieved2026-09-26 from the catalog link in ESKA's current official product navigation. Saved as work/datasheets/eska_auto.pdf. Pages16 and19 were text-extracted and visually inspected. This verifies manufacturer listing and specifications; it does not verify distributor stock or constitute a lifecycle guarantee.

| Ref | Manufacturer MPN | Rating | Quantity | Catalog page |
|---|---|---|---|---|
| F1,F2 | ESKA340.026 |7.5A32VDC|2|16|
| F3 | ESKA340.017 |1A32VDC|1|16|
| F4 | ESKA340.024 |5A32VDC|1|16|
| F5 | ESKA340.027 |10A32VDC|1|16|
| F6 | ESKA340.022-80V |3A80VDC|1|19|

All have1000A breaking capacity at their rated voltage. F6 is specifically the80V suffix; standard340.022 is only32V and must not be substituted on the53.5V output. Retain the manufacturer punctuation in the BOM even if distributors normalize it. TME's candidate listing is https://www.tme.eu/en/details/340022-80v/standard-automotive-fuses/eska/ ; direct retrieval was blocked, so no stock claim is made.

The32V series time windows:110% minimum100h;135%0.75–600s;200%0.15–5s;350%0.04–0.5s;600%0.02–0.1s. Its40°C derating graph reads approximately97% (graph estimate, not exact tabulated value). Operating ambient range−40..125°C. Fuse rating is not an exact trip threshold; coordination with wiring, source current limitation and inrush still needs validation.

The80V series time windows:110% minimum100h;150%0.5–300s;200%0.15–20s;350%0.04–0.5s;600%0.02–0.1s. No40°C correction curve or explicit temperature range is provided on this series page. Do not transfer the32V derating curve to80V as a certified value. At1.31A nominal load, a3A fuse has substantial current margin, but switch startup/inrush is still unverified.

Both are standard blade geometry.32V: body19×4.5mm, overall20mm, blade6.5mm exposed length,5.25mm width,0.63mm thickness,14.5mm outer span.80V: body19±0.2×4.9±0.2mm, overall19.5±0.5mm, blade6.4±0.3mm length,5.1±0.1mm width,0.6±0.05mm thickness,14.4±0.2mm outer span. These are nominally compatible with the same standard ATO-style holder family, but actual178.6165.0001 contact tolerance/insertion fit remains a sample/mechanical check. Holder maximum PCB thickness1.5mm and80V rating are tracked separately by root.

The older Littelfuse166.7000.4302 is also verified from manufacturer2012 catalog mirrored at https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_16670004402_apr22_xonlink.pdf :3A80V,500-pack; suffix4306 is100-pack. That source explicitly limits continuous operation to0.7×rating at23°C. Root has distributor end-of-life indications, so ESKA's currently manufacturer-listed80V candidate is preferred for sourcing follow-up. Do not infer Littelfuse lifecycle from the old PDF.

Machine-readable entries, curves and dimensions are in work/fuse_verification.json. No board scripts were changed.
