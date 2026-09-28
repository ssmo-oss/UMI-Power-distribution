from pathlib import Path
import sys,struct,json
sys.path.insert(0,'work/main_lib');import olefile
f=olefile.OleFileIO('work/datasheets/PMP21274_REVA.PcbDoc')
def properties(stream):
 b=f.openstream(stream+'/Data').read();o=0;r=[]
 while o<len(b):
  n=struct.unpack_from('<I',b,o)[0];s=b[o+4:o+4+n].decode('latin1').rstrip('\0');o+=4+n
  r.append(dict(v.split('=',1) for v in s.split('|') if '=' in v))
 return r
c=properties('Components6');n=properties('Nets6');data=f.openstream('Pads6/Data').read();i=0;pads=[]
while i<len(data):
 typ=data[i];i+=1;assert typ==2,typ;subs=[]
 for j in range(6):
  z=struct.unpack_from('<I',data,i)[0];subs.append(data[i+4:i+4+z]);i+=4+z
 name=subs[0][1:1+subs[0][0]].decode('latin1');p=subs[4];cid=struct.unpack_from('<H',p,7)[0];net=struct.unpack_from('<H',p,3)[0]
 vals=struct.unpack_from('<9i',p,13)
 pads.append(dict(ref=c[cid]['SOURCEDESIGNATOR'] if cid!=65535 else None,pin=name,layer=p[0],net=n[net]['NAME'] if net!=65535 else None,xy_mm=[v*.00000254 for v in vals[:2]],size_mm=[v*.00000254 for v in vals[2:4]],rotation=struct.unpack_from('<d',p,52)[0]))
Path('work/datasheets/pmp_reference_geometry.json').write_text(json.dumps(dict(components=c,pads=pads,nets=n),indent=2))
print('Components',len(c),'pads',len(pads))
for r in ['Q1','Q2','Q3','U1','C5','L1']:
 print(r,[p for p in pads if p['ref']==r])
