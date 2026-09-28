p='work/d5_poe_extract.py'
s=open(p).read();s=s.replace("write(D/(NAME+'.kicad_pcb'),b)","# Remove exact duplicated conductor segments introduced at the input junction.\nseen=set()\nfor seg in list(all_(b,'segment')):\n key=(str(one(seg,'net')[1]),str(one(seg,'layer')[1]),float(one(seg,'width')[1]),tuple(sorted([tuple(map(float,one(seg,k)[1:3])) for k in ('start','end')])))\n if key in seen:b.remove(seg)\n else:seen.add(key)\nwrite(D/(NAME+'.kicad_pcb'),b)")
open(p,'w').write(s)
