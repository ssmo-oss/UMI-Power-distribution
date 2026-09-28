# Final USB electrical review — snapshot07 and proposed capacitor update

Reviewed current outputs/UMI_D2/USB_POWER/design.json against TI TPSM63610 SLVSGU1A (December2023), https://www.ti.com/lit/ds/symlink/tpsm63610.pdf. Root reports native DRC/ERC/parity pass; this review does not independently repeat those checks.

## Action before prototype

Increase local output capacitors from3 to5 of GRM32ER71A476ME15L, as root approved. TI Table7-1 requires75µF EFFECTIVE for5V at500–1400kHz. Current15.8k RT is1MHz. The33µF figure elsewhere is for2.2MHz and must not be applied here. TI's example using3×47µF gives approximately78µF effective at5V25°C and57µF at−40°C; this is slim nominal margin, not a certified tolerance-inclusive minimum. Three capacitors are explicitly listed in TI's example, so no assertion of demonstrated instability is warranted. Five provides more useful margin. The illustrative bound78×5/3×0.8×0.85=88.4µF is NOT a verified guaranteed combined-bias/tolerance/temperature curve. Exact5.18V/40°C effectiveness and loop response remain verification items.

TI Table7-1 lists22pF feedforward capacitance across upper feedback resistor. Section8.2.1.2.6 requires4.99kΩ in series to limit injected noise and says its zero should exceed fsw/5. With102kΩ and22pF the zero is~71kHz, conflicting with200kHz target at1MHz.6.8pF gives~229kHz but is not the tabulated recommendation. Do not silently populate a feedforward network based on one conflicting sentence. Provision DNP if useful; with increased output capacitance the near-minimum-capacitance justification is weaker. No explicit maximum COUT was found in reviewed datasheet; startup and load-step behavior still require measurement.

## Confirmed component ratings

TDK CNA6P1X7R1H106K is explicitly listed in TI Table8-2 as10µF50V X7R1210. Two are required; current design has two. Murata GRM32ER71A476ME15L is explicitly listed in TI Tables7-3/8-2 as47µF10V X7R1210. Their names and ratings therefore have direct primary-source support. Capacitor nameplate sums must not be presented as effective operating capacitance.

TPSM63610 recommended VIN3–36V (3.7V required for startup), IOUT0–8A, ambient−40..105°C, junction−40..125°C.150°C is absolute maximum, not the release thermal target despite a less conservative layout-text sentence.40°C ambient is within recommended range but requires board-specific temperature validation; stay below125°C junction. TI example94.3% efficiency is at12V→5V4A and must not be extrapolated as guaranteed6A efficiency. Thermal vias, planes and copper thickness materially change temperature rise.

Current JSON correctly has SYNC/MODE=VCC,102k/24.9k0.1% feedback, revised6.3×5.8 electrolytic footprint, and intended power/ESD pin mappings. Nominal output5.09639V; reference/resistor extrema5.01188–5.18116V exclude FB bias and ripple/transients. Only~68.8mV remains to5.25V upper source target. Scope startup, disconnect and load-step peaks at both USB ports.3A connector contact and TPS2557 losses mean5V at remote device is not guaranteed. No negotiated3A claim is justified.

## Remaining validation and sourcing

At40°C soak, test0/3/6A loads and asymmetricportloading, USBhotplug, short/recovery, outputovershoot/ripple, inputplug-inringing and cable-endvoltage. These are prototype tests, not evidence that current circuit has a demonstrated fault. Inputbulk47µF must be assessed with actual harness; TI general recommendation68–100µF is damping guidance, not a fixedminimum in its2×10µF applicationexample.

Live capacitor lifecycle not verified: TDK official productpage returns403; Murata official page returned only application shell; web search tool unavailable dueauthenticationerror. TI datasheet confirms existence/specification in its publication, not current inventory/active lifecycle. Do not mark either capacitor currently available without assembly-house confirmation. Existing assembly_sourcing.md separates catalog IDs from live assembly inventory.
