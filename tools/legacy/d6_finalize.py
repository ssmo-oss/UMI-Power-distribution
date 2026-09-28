from pathlib import Path
import json
p=Path('work/d6_electrical_resolution.md');s=p.read_text(encoding='utf8').replace('The candidate is reasonable for engineering prototype evaluation with unchanged footprint.','Recommendation: adopt C4169838 for the prototype with unchanged footprint and retain the same measured-waveform/thermal validation required by the original design.')
s+='''

## Published rating comparison and geometry

Yageo RC2010 family specifies0.75W at70°C,derating to zero at155°C;body5.0×2.5mm, same2010land class. Family maximum working-voltage ceiling is200V and maximum overload-voltage ceiling500V, but rated working voltage must also satisfy sqrt(P·R), only~2.372V RMS at7.5Ω/0.75W. These ceiling numbers are not permission for sustained200V or500V across this low resistance. Short-time overload tests likewise do not establish the repeated snubber-pulse envelope. Original Panasonic2010 body/power/tolerance matches and has a wider asymmetric TCR(-100/+600ppm/K) than the candidate±200ppm/K. No claim of improved pulse handling is made.

The cap+frequency illustration is0.308643916×1.05×1.10=0.35648W,about47.5% of0.75W. The extra10% frequency is an engineering allowance, not a verified oscillator maximum. Additional ringing or higher actualfrequency may increase loss; measure at operating corners. Temperature at the resistor can exceed40°Cambient due to nearby power components.
''';p.write_text(s,encoding='utf8')
p=Path('work/d6_electrical_resolution.json');d=json.loads(p.read_text());d['R1']['recommendation']='Adopt C4169838 for prototype; retain same measured-waveform and thermal validation as original; no claim of proven pulse equivalence';d['snubber']['illustrative_Cplus5percent_fplus10percent_P_W']=d['snubber']['upper_static_P_W']*1.05*1.1;p.write_text(json.dumps(d,indent=2))
