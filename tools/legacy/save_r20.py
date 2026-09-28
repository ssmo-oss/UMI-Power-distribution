import json
from pathlib import Path
upper=84500+953;lower=1960;t=.001;v=1.2
calc=dict(nominal=v*(1+upper/lower),minimum=v*.99*(1+upper*(1-t)/(lower*(1+t))),maximum=v*1.01*(1+upper*(1+t)/(lower*(1-t))),previous_nominal=v*(1+(84500+931)/lower),assumptions='LM5122 reference±1%, all divider resistors±0.1%; excludes bias current,ripple,thermal drift and overshoot')
row=dict(ref='R20',mpn='RT0603BRD07953RL',manufacturer='Yageo',code='C861604',stock=903,approved=True,assessment='Explicit value change931→953ohm; same0603,0.1%,25ppm,100mW75V. Nominal output increases13.47mV.',datasheet='https://www.yageogroup.com/component-documentation/download/specsheet/RT0603BRD07953RL',url='https://jlcpcb.com/partdetail/C861604',output_calculation=calc)
p=Path('work/jlc_main_approved_substitutes.json');d=json.loads(p.read_text());d.append(row);p.write_text(json.dumps(d,indent=2));print(json.dumps(calc))
