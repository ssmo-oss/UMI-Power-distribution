# D6 fabrication instructions

Use separate builds for MAIN (1.2 mm), POE (1.2 mm) and USB (1.6 mm). All are four-layer ENIG, 2 oz outer and 1 oz inner copper; green soldermask and white legend. Maintain exact outlines and mounting holes. Use the source stackup and MANUFACTURING_SPECIFICATION.md; quote any stackup change explicitly.

POE and USB require epoxy resin-filled, copper-capped vias at all positions marked in manufacturing/VIA_TREATMENT.csv. This is a coordinate schedule, not a drill program. Plot coordinates share the Gerber/drill origin; Y is inverted relative to KiCad coordinates. Drill files remain authoritative for hole geometry. Corresponding KiCad via objects explicitly carry filling/capping flags. Filling is not tenting or soldermask plugging.

POE smaller vias (0.254, 0.35 and 0.40 mm) are filled/capped. Its 0.635 mm vias are ordinary plated vias and must not be included in the fill process. USB 0.25/0.30 mm vias are filled/capped. MAIN has no vias requiring this process. All through-hole component and mounting holes remain open.

The POE Coilcraft SER2915H-103KL inductor requires an assembly support fixture. Include it in the SMT quotation. Assemble only the SMT BOM/CPL; connectors, holders and inserts are user-fitted. Preserve the original footprint pad geometry and paste openings. Review every supplier rotation/pin-1 preview before accepting assembly.

The requested construction has published capability support, but the exact selective-fill/copper/thickness combination and fixture still require manufacturer engineering acceptance. No quote is represented as accepted.
