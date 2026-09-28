# Main board final independent electrical review

Reviewed current MAIN_POWER/design.json and main_power_d2.py. Primary sources: https://www.ti.com/lit/ds/symlink/tps25982.pdf ; https://www.ti.com/lit/ds/symlink/lm5122.pdf ; https://www.vishay.com/docs/88983/ss10p4.pdf .

## Required layout and rating attention

D4 SS10P4-M3/86A is correctly oriented: pins1/2 anode GND, pin3 cathode BOOST_IN. Its40V reverse rating exceeds normal12V bus and eFuse16.9V OVLO. Its10A rating and0.56V maximum forward drop at10A/25°C support it as the candidate catch diode. They do not guarantee protection against dynamic undershoot. TPS25982 OUT absolute minimum is−0.8V. TI explicitly requires the Schottky physically close to OUT with minimal parasitic inductance. Current D4(90,55) versus U2(79,60) is~12mm between centres. Move beside OUT bank if practical and give it short, broad output and ground paths. There is only0.24V nominal static margin at the diode's stated10A test point, before inductive overshoot, temperature and current variation. Measure worst-case fault turnoff at the eFuse pins; no−0.8V guarantee is claimed.

18A is not a conservative simultaneous12V input requirement. At nominal output powers and90% conversion efficiencies: Jetson5A + SG4A4A + fan0.14A + USB30W/(12V×0.9) + switch70.085W/(12V×0.9) =18.407A, excluding auxiliary losses. Using raised USB voltage and upper switch voltage raises this to~18.54A. Use at least20A continuous bus/connector/fuse thermal design at12V, with separate minimum-input-voltage and startup/fault analysis. This is a design load estimate, not a measured operating current or recommendation to arbitrarily replace fuses.

## Circuit checks

TPS259824ONRGER input/output/exposed-pad mapping, 182Ω ILIM,511Ω IMON, open ITIMER, RETRY_DLY=GND, NRETRY open and LDSTRT=GND match intended latching fast-trip operation. PG is connected to LM5122 UVLO with49.9k upper/8.45k lower divider from BOOST_IN; nominal divider level is1.738V at12V and2.447V at16.9V, below PG6V recommended maximum. Pulling PG low inhibits boost; there is no inappropriate12V PG pullup. Unpowered PG low specification at26µA is below LM5122 UVLO threshold. Actual fault dynamics still need bench verification.

182Ω produces~8.13A nominal threshold, with wider IC current-limit tolerance previously documented. Near10V full boost load may approach the lower limit; full rated output at undervoltage is not guaranteed. Input/output transient suppression is necessary even though eFuse interrupts the otherwise persistent inductor/body-diode fault path.

## Output voltage

R19=84.5k and R20=931Ω sum85.431k, R18=1.96k, all0.1%. LM5122 FB reference1.188–1.212V gives nominal53.50469V and static extreme52.86619–54.14550V. These exclude feedback bias current, trace effects, ripple and startup overshoot. The switch's53.5V adapter marking alone does not establish its maximum accepted supply voltage. Acceptance of54.15V plus transient margin must be supported by switch documentation or appropriate system testing before production qualification.

No additional definite pin-map error was found in this fault network. Bench release tests must include output short while fully loaded, latched shutdown/reset, startup into actual switch capacitance, minimum input, worst-case negative OUT undershoot and positive IN surge. This remains a prototype candidate, not a production-qualified release.
