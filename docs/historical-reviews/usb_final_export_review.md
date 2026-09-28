# Independent USB final export review

Reviewed outputs/UMI_TWO_BOARD_DESIGN/USB_POWER on2026-09-26 using a separate read-only parser script, work/review_usb_exports.py. No deliverable files changed.

Result: no definite BOM/CPL reference, position or pin-orientation error found.

-34 electrical components:31 SMT plus3 manual through-hole connectors J1/J2/J3. Every SMT reference appears exactly in both by-reference BOM and exploded grouped JLC draft BOM and in the CPL; no extra/missing references. C3/C9/C10/C13/C14 are all the intended47µF10V Murata output capacitors.
- All31 CPL coordinates and rotations match the actual filled board footprints. Native KiCad coordinates use auxiliary origin(10,60), X right/Y up in placement export. This transformation is consistent with the80×50mm board. CPL is native KiCad format; assembler import/orientation preview remains required, especially custom module packaging.
- U1 custom TPSM63610 pin1 is upper-left at local(−2.75,−2.925); VIN1 and VIN2 are top corners, VOUT1/VOUT2 bottom corners. Current pad functions match the previously reviewed TI pinout, with MODE tiedVCC and RBOOT/CBOOT joined. CPL U1 rotation0 is consistent with the actual footprint geometry. This does not certify a particular assembler's library zero-angle convention.
- Q1 pin1 is upper-left, source pins1–3 protected input, gate4, drain5–8 raw input. C12 positive pad1 is left/protected input and negative2 right/GND. No polarity reversal found.
- Manual USB J2/J3 retain pin1VBUS,2D−,3D+,4GND left-to-right in their custom board footprint, matching previously reviewed manufacturer land pattern. Both shell pads GND. They are correctly excluded from SMT placement/BOM and remain included in full BOM as user-fit parts.
- Stored stackup has1.6mm total,0.07/0.035/0.035/0.07mm copper (2/1/1/2oz nominal), ENIG. VIPPO instructions must accompany the board order; stackup metadata alone does not order filled/capped vias.
- Export audit independently records137 expected/exported drills and matching centres/sizes; this review read that result rather than rerunning Gerbonara. Four copper Gerbers, masks, outline and plated/nonplated drill files exist; top paste exists in assembly directory. No bottom assembly is listed.

Remaining ordering limitations are already explicit:13 grouped BOM catalog fields blank, no confirmed assembly quote/inventory; TPSM63610 C7125816 is LCSC-only evidence and does not establish JLC assembly availability. Draft JLC BOM labeling is appropriate. The package is suitable for assembly quoting/prototype review with these conditions, not an automatically accepted or production-qualified order. No external upload was performed.
