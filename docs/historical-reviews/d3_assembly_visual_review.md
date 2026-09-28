# D3 assembly and routing visual review

Final reference-only PDF/SVG overview and enlarged detail generated for both boards from their filled, saved D3 sources. Source hashes and annotation counts are recorded in each `review/*_assembly_review.json`; source files remained unchanged.

Main: 69 reference labels; boost control detail is readable with values removed, thin body outlines, and vertical lettering fitted inside narrow vertical passives. Main native snapshot05 has zero DRC violations, opens or schematic parity findings. The final bottom Gerber visual shows the long control route in a clean orthogonal corridor with short 45-degree transitions, and the broad distribution route has chamfered corners.

USB: 38 reference labels; overview identifies both connectors, mounting holes, diode and power sections without overlapping values. Buck detail is provided separately. Final bottom Gerber visual confirms the charging-signal shield-hole detour has been removed; the remaining pair has a short, orderly path and matched direction changes.

The assembly drawings intentionally show body outlines/reference designators, not solder pad numbering or manufacturer assembly orientation. Use normalized CPL, footprints and BOM for actual placement. Custom-body absence in 3D renders remains a known limitation.

Reusable command: `python work/export_reference_assembly.py BOARD --output-dir REVIEW_DIR --detail-box X0 Y0 X1 Y1`. It uses isolated text-only board copies and the controlled native CLI; copper and source placement are not modified.
