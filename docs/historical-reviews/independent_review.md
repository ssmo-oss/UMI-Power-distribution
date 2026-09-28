# Independent electrical review — UMI D2

Reviewed source capture in work/design_d2.py and work/main_power_d2.py on 2026-09-25. This is an independent circuit review, not ERC/DRC, a manufactured-board test, or a release authorization. Scripts are being changed concurrently; observations refer to the versions read during this review.

## Corrections identified

1. USB nominal voltage margin: original 100k/24.9k feedback gives 5.01606 V, with reference and 0.1% resistor extremes 4.93292–5.09947 V. Recommend 102k/24.9k: 5.09639 V nominal, 5.01188–5.18116 V. These limits assume FPWM; connect SYNC/MODE to VCC if using them. They exclude transient ripple and FB bias error. TI gives 50 nA typical FB current, no maximum; approximately 5.1 mV output shift at the typical value with 102k top resistance. Treat the 68.8 mV upper allowance to 5.25 V as a test budget, not guaranteed overshoot immunity. [TI TPSM63610](https://www.ti.com/lit/ds/symlink/tpsm63610.pdf), tables 5-1 and 6.5.
2. USB C12 EEEFK1E470P is 6.3 mm diameter, 5.8 mm height. Use Capacitor_SMD:CP_Elec_6.3x5.8. Panasonic recommends identical copper lands for its D (5.8 mm) and D8 (7.7 mm) case heights, so the original height error was not independently proven to invalidate the copper lands. [Panasonic part specification](https://industrial.panasonic.com/ww/products/pt/aluminum-cap-smd/models/EEEFK1E470P), [FK case and land tables](https://industrial.panasonic.com/cdbs/www-data/pdf/RDE0000/ABA0000C1181.pdf).
3. Main R19 85.4k / RT0603BRD0785K4L was unverified and not a standard E96 value. Main agent notified; 84.5k plus 931 ohm with 1.96k bottom gives nominal 53.50469 V. Exact assembled MPN sourcing still required.

## USB power and interface assessment

TPS2557 pin schedule and enable polarity match the capture. 32.4k/0.1% gives approximately 3.08453 A minimum, 3.67898 A maximum per port using TI current-limit equations. Two maximum limits total 7.35796 A, below the buck's 8 A continuous nameplate. A 3 A load dissipates up to 0.315 W in each switch at its 35 milliohm maximum resistance. Exposed-pad grounding and useful copper area are necessary. Its reverse leakage specification at VIN=0 does not establish active reverse blocking with VIN powered. Do not describe the ports as generally backfeed-protected. [TI TPS2557](https://www.ti.com/lit/ds/symlink/tps2557.pdf), sections 7.5, 10.2.1.2 and 12.3.

At 3 A, that switch can lose 105 mV. The selected connector's 30 milliohm maximum per contact permits another 180 mV across supply and return contacts. With the proposed 5.096 V nominal bus, the computed minimum after those elements is 4.72688 V before board/cable losses. This does not by itself prove USB-source noncompliance: the exact measurement interface matters. It does preclude claiming guaranteed 5 V at the attached device. Acceptance must measure voltage at the actual load through the intended cable. Connector pins 1/4 are rated 3 A; the other contacts 1 A. [Würth 614004190021](https://www.we-online.com/components/products/datasheet/614004190021.pdf).

TPS2513A implements BC1.2 and proprietary divider/short signatures; physical 3 A capacity is distinct from a negotiated 3 A charging mode. In particular, it is not a USB-PD controller. No assertion of sustained Quest charging power can be made without the actual headset and cable. Its captured DP/DM assignment agrees with the TI pin table. [TI TPS2513A](https://www.ti.com/lit/ds/symlink/tps2513a.pdf).

USBLC6-2SC6 has leakage specified at 5.25 V and minimum breakdown 6 V. A 5.181 V steady rail is not incompatible. It is ESD protection, not a precision overvoltage disconnect; a shorted buck high-side device could still expose downstream components to excessive voltage. No system-level single-fault overvoltage protection has been demonstrated or promised. [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf).

## Main power assessment

PMP21274 is a useful engineering starting point. Keeping its inductor, switch arrangement and compensation while changing output by less than 1 V is preferable to unreviewed major power-stage changes, but this is not proof of stability on a new layout. Input fuse alone has not been shown to interrupt output shorts before damage to the boost conduction path. Disabling switching does not isolate the output from input through L1 and Q1's body diode. The separate work/main_efuse_candidate.md develops a candidate input breaker and highlights remaining validation needs. [TI PMP21274](https://www.ti.com/tool/PMP21274).

## Release gates that remain substantive

- PCB copper completion and a genuine KiCad clearance/unconnected check, followed by schematic-to-layout connectivity agreement. A text parser or successful API load is not a DRC pass.
- Vendor land-pattern verification for custom buck, input terminal and large boost inductor; exact fuse insertion and board thickness compatibility.
- Current-path and connector temperature at simultaneous load, 40 C ambient, intended enclosure and copper weight. Neither module nameplate current nor evaluation-board thermal resistance proves this board's temperature.
- Start/stop, simultaneous load steps, individual USB shorts, boost-output short and recovery, input brownout, cable insertion and voltage overshoot measurements.
- Full resistor/capacitor/semiconductor order codes and assembly stock. Unverified ordering strings must not silently become an order BOM.
- Fabrication plots, drill data and SMT placement orientation review only after electrical and geometric completion. There is not enough evidence to label the present boards ready for ordering.
