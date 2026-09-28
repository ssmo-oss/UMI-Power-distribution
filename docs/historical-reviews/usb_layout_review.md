# USB_POWER physical layout review — 2026-09-25

Reviewed current USB_POWER/design.json, route_usb_power.py and the usb_review_04 top render and copper PDF. Root reports native DRC and schematic parity clean; this review does not independently repeat those checks.

## Recommended ESD revision before prototype

Increase board height from 45 to 50 mm, preserving 80 mm width. Move USB connectors J2/J3 pin rows from y=42 to y=47. Place U5 at (25.5, 43.5) and U6 at (68.5, 43.5). Existing orientation is acceptable if routed deliberately. Rotating arrays 90 degrees could align their two channels with connector pins, but is optional and requires routing transform support.

Move C6/C7 to (30.5, 43.5) / (73.5, 43.5), retaining their current orientation so the VBUS pad faces the ESD array. This places each VBUS capacitor pad about 2.4 mm from its array VBUS pad. Proposed courtyards appear separated from the USB shell and ESD courtyards; regenerate native DRC to establish this on actual copper.

Route connector D− and D+ to the ESD array first, then continue from the array to U4. Avoid a distant T-junction with ESD on a long stub. Two same-channel pins can remain joined locally for native connectivity, but external routing should place the protection point along the current path. Direct front traces from connector through-hole pads to the array are preferable to detouring around shell holes.

The ESD VBUS pin has little DC load but carries transient clamp current. Use a short broad connection to the nearby port capacitor and VBUS copper; approximately 0.5 mm where it fits is preferable to an arbitrary 0.25 mm signal route. Give pin 2 a direct ground connection and adjacent vias to the continuous ground plane. Do not route ESD ground through the charging controller's ground return.

These recommendations interpret ST's short I/O, VBUS and ground path guidance and connector proximity recommendation. They do not establish a withstand level. [ST USBLC6-2 datasheet, section 2.3 and Figure 6](https://www.st.com/resource/en/datasheet/usblc6-2.pdf).

## Other observations

- Power connectivity uses parallel vias and explicitly wide paths. No additional definite pin mapping or power-net error was found in this review.
- The render omits models for custom parts. Exposed buck pads and missing USB shells do not mean those parts are absent. Final mechanical review must include actual body geometry.
- C6/C7 relocation lengthens the connector feed slightly. Keep 3 A VBUS traces wide and check copper resistance after rerouting.
- Preserve dedicated buck feedback routing and separation from switch-node/bootstrap copper. Sense near output capacitors; a shared distribution plane can include load-dependent voltage drop.
- Thermal vias underneath the module require the selected filled-and-capped fabrication process. Via count alone does not prove full-load operation at 40°C.
- Measure simultaneous 3 A electronic loads, then actual headset/cable behavior. Check startup, short recovery, hot-plugging, converter temperature and voltage overshoot. Layout improvement does not replace ESD testing.
