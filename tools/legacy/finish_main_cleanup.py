from pathlib import Path
from design_d2 import parse,all_,one,write
p=Path('outputs/UMI_D2/MAIN_POWER/MAIN_POWER.kicad_pcb')
b=parse(p.read_text());ids={'e9e83dfa-cb40-525f-b502-c0fb79677859','f4f95612-56fd-5d8c-a275-6208624b38b9','e3564a8b-91e4-5525-9dfc-6642e1989cb8'}
removed=[a for a in all_(b,'segment') if str(one(a,'uuid')[1]) in ids]
assert len(removed)==3
for a in removed:b.remove(a)
write(p,b)
print('Removed three dangling segments')
