# UMI D6 simplified STEP models

Six files: BARE and SIMPLIFIED for MAIN_POWER, POE_POWER and USB_POWER. Units are millimetres.

BARE files retain the native KiCad board outline, rounded corners, mounting and component holes. Small via holes are intentionally omitted. The native board-only export omits outer conductor/mask thickness; its Z dimension was scaled to the specified finished 1.2 mm MAIN/POE and 1.6 mm USB thickness. X/Y geometry is unchanged. No tracks, pads, copper zones or text are modelled.

SIMPLIFIED files add a rectangular body proxy for every board-mounted electrical component, including the through-hole parts intended for manual assembly. They also show simple fuse-insert proxies. Component X/Y outlines derive from the saved footprint fabrication graphics and placements. Heights are approximate visual allowances, not verified manufacturer maximum dimensions. Leads, solder joints, connector internals, mating plugs, cables and standoffs are omitted. These models are useful for arrangement and visualisation, but NOT final enclosure-clearance signoff. Consult COMPONENT_PROXY_DIMENSIONS.json for each assumption.

Origin: each board's Gerber/drill origin. X points right, Y points upward when viewed from the component side, Z points upward. Bare PCB bottom is Z=0; component bodies start at the finished PCB top. All boards are exported separately; their relative installation positions are not defined.

Every file was reimported with Open CASCADE and checked for valid solid geometry and expected solid count. Bare PCB dimensions were checked against the design. MAIN: 68 × 100.263962 × 1.2 mm; POE: 106 × 100 × 1.2 mm; USB: 80 × 50 × 1.6 mm. The original KiCad/manufacturing files were not modified.
