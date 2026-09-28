# D5 independent electrical review — three boards

Reviewed2026-09-26. No PCB changes. Intended boards are MAIN12V distribution, separate POE53.5V converter, and unchanged USB5V board. **PoE switch and SENSING GMSL are mutually exclusive configurations.** This is a configuration rule, not a demonstrated hardware interlock.

## Power budget

Assumptions:12V at the MAIN input,90% conversion efficiency for each converter, Jetson60W allowance, fan1.68W, USB6A total at5.0963855V. Efficiency is a design assumption, not measured or a guaranteed minimum.

| Configuration | Nominal source demand | Current at12V |
|---|---:|---:|
|Jetson+fan+USB+PoE|173.5546W|14.4629A|
|Same, PoE output at54.159133V static upper bound|174.4875W|14.5406A|
|Jetson+fan+USB+GMSL4A provisional allowance|143.6559W|11.9713A|
|GMSL3A alternative, only if confirmed|131.6559W|10.9713A|

USB input33.9759W; PoE input77.8987W nominal. Take the larger configuration rather than adding PoE and GMSL. For the same modeled powers at a different board input voltage, I=P/V. No minimum input voltage was specified;10.8V is not a validated operating limit. Upper static PoE calculation is not a full worst case: USB output tolerance, efficiency variation, harness drop, startup and other auxiliaries remain. Keep20A continuous supply-path design/test capability if already implemented; the lower nominal budget does not justify reducing copper or connector ratings before tests.

## Jetson fuse

**Keep7.5A provisionally. It is not established as the unique necessary value.** A12V5A adapter/branch allowance specifies available power, not continuous consumption or startup surge. A5A fuse supplying5A has insufficient demonstrated thermal/startup margin. The manufacturer's typical derating table allows only4A on its5A fuse at65C, while7.5A permits6A. At40C a precise guaranteed interpolated trip/load limit is not given. Measure actual cold/hot startup and sustained peripheral-loaded operation before considering a smaller fuse. Fuse choice must protect the weakest actual branch cable/connector;7.5A is not automatically suitable for an unknown thin device pigtail.

NVIDIA's official Orin Nano developer-kit guide lists a19V supply; NVIDIA staff state12V5A is within the supported developer-kit voltage range. This does not identify the user's exact carrier or prove a5A load. Do not confuse module5V input specifications with the carrier DC jack. The user's12V5A remains a branch design basis, not independently measured consumption.

Sources: [NVIDIA guide](https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/quick_start.html), [NVIDIA staff12V5A clarification](https://forums.developer.nvidia.com/t/about-power-supply-of-jetson-orin-nano/343709/2), [Littelfuse287 primary datasheet](https://www.littelfuse.com/assetdocs/littelfuse-datasheet-287-atof?assetguid=43dcdce8-8ca2-426f-8998-7e566f048d40).

## GMSL rating

SENSING's primary SG4A-NONX-G2Y-A1 page verifies12V DC input and camera PoC9–16V, but does **not** specify a3A or4A aggregate maximum. CN3 is described with modelDC-005-2.5A-2.0; the embedded2.5A string must not be treated as a proven assembly input rating without its own connector sheet. Actual load depends on the connected cameras. The prior4A is a conservative design allowance, not a verified manufacturer rating; the3A original diagram remains unconfirmed. Keep current fuse pending camera/adapter/connector verification, rather than assert3A and reduce it automatically.

Source: [SENSING manufacturer wiki](https://wiki.sensing-world.com/docs/2_1_NVIDIA_Jetson/Getting_Started/NVIDIA_Jetson_Orin_Nano_NX/Adapter_Board/SG4A-NONX-G2Y-A1).

## Fuse disposition and placement

| Position | Recommendation | Reason |
|---|---|---|
|MAIN Jetson F1|retain7.5A provisional|5A design allowance and unknown startup|
|MAIN GMSL F2|retain7.5A provisional|current/camera aggregate unverified; reassess against actual harness|
|MAIN fan F3|retain1A|0.14A fan does not justify exposing thin branch wiring to whole PSU fault current|
|MAIN USB F4|retain5A|protects12V cable and input before USB output switches; nominal2.83A input|
|MAIN PoE feed F5|retain10A at source|protects MAIN-to-POE12V cable; nominal6.49A converter input|
|POE output F6|retain3A80V|output branch protection has not been shown redundant by coordinated fault analysis|

Do not duplicate F5 at the POE input when the source fuse already protects the entire feed and the local TPS259824 remains. A fuse only at the remote POE board cannot interrupt a cable short ahead of that fuse. The diagram's input-fuse function is therefore better located on MAIN at the cable source. Separate source cable upstream of MAIN still needs installation-specific protection.

The TPS259824 input eFuse can disconnect the boost body-diode path and limits the duration of severe converter faults. However, it senses12V input current, not53.5V cable current, and its delayed overcurrent/fast-trip response, component faults and output-capacitor discharge differ from output-fuse operation. At90% efficiency8.13A nominal input threshold corresponds roughly1.64A output at53.5V in regulated steady state, but this arithmetic is **not** a guarantee of output short protection or a reason to remove F6. Demonstrate fault coordination, cable ratings, capacitor discharge and recovery before removing F6. Never replace80V output fuse with32V insert.

Sources: [TI TPS25982](https://www.ti.com/lit/ds/symlink/tps25982.pdf), [TI LM5122](https://www.ti.com/lit/ds/symlink/lm5122.pdf), [Littelfuse FKS80 manufacturer-sheet mirror](https://xonstorage.z8.web.core.windows.net/pdf/littelfuse_16670004402_apr22_xonlink.pdf).

No physical tests have been performed. Required checks remain startup/inrush, actual camera and Jetson load, cable voltage drop, all allowed configurations at40C, controlled eFuse overload/output-short response, and fuse/connector temperatures. No fuse removal is approved by this review.
