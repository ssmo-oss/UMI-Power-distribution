"""Generate auditable purchasing/assembly tables from the final design records."""
from pathlib import Path
import csv,json,re
from design_d2 import parse,all_,one,prop
BASE=Path.cwd(); ROOT=BASE/'outputs/UMI_D2'
CATALOG={
 'TPSM63610RDFR':('Texas Instruments','C7125816','LCSC only; JLC assembly sourcing needs confirmation'),
 'TPS2557DRBR':('Texas Instruments','C130056','JLC catalog matched; quote/stock unconfirmed'),
 'TPS2513ADBVR':('Texas Instruments','C473910','JLC catalog matched; quote/stock unconfirmed'),
 'AO4407A':('Alpha & Omega Semiconductor','C16072','Exact AOS part; no other manufacturer substitution'),
 'USBLC6-2SC6':('STMicroelectronics','C7519','Exact ST part; no other manufacturer substitution'),
 'LM5122MHX/NOPB':('Texas Instruments','C77241','JLC catalog matched; quote/stock unconfirmed'),
 'TPS259824ONRGER':('Texas Instruments','C2155766','Circuit-breaker O version; preserve exact MPN'),
 'BSC072N08NS5ATMA1':('Infineon Technologies','C3278732','JLC catalog matched; quote/stock unconfirmed'),
 'SER2915H-103KL':('Coilcraft','C19276042','Confirm support fixture for heavy SMT inductor'),
 'XAL4020-102MEB':('Coilcraft','','Exact MPN sourcing required'),
 'BZT52C12-7-F':('Diodes Incorporated','','Exact MPN sourcing required'),
 'SMBJ15A':('Littelfuse','','Unidirectional; exact manufacturer sourcing required'),
 'SS10P4-M3/86A':('Vishay','','Exact MPN sourcing required'),
 'MBR1H100SFT3G':('onsemi','','Exact MPN sourcing required'),
 '1709681':('Phoenix Contact','','User-fit through-hole'),
 '178.6165.0001':('Littelfuse','','Holder only; fuse insert purchased separately'),
 'B2P-VH(LF)(SN)':('JST','','User-fit through-hole'),
 'B3P-VH(LF)(SN)':('JST','','User-fit through-hole'),
 '614004190021':('Würth Elektronik','','User-fit through-hole'),
}
def sourcing(mpn):
 if mpn in CATALOG:return CATALOG[mpn]
 for prefix,mfr in [('GRM','Murata'),('GCM','Murata'),('CNA','TDK'),('RC0603','Yageo'),('RT0603','Yageo'),('CRCW','Vishay'),('ERJ','Panasonic'),('EEE','Panasonic'),('ESR03','ROHM')]:
  if mpn.startswith(prefix):return mfr,'','Exact MPN sourcing required'
 raise ValueError('Unidentified manufacturer for '+mpn)
def natural(s):return [int(t) if t.isdigit() else t for t in re.split('(\\d+)',s)]
def write(path,headers,rows):
 with path.open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(headers);w.writerows(rows)
def build(name):
 d=ROOT/name;parts=json.loads((d/'design.json').read_text());pcb=parse((d/(name+'.kicad_pcb')).read_text())
 footprints={str(prop(f,'Reference')[2]):f for f in all_(pcb,'footprint')}
 records=[];groups={};missing_attrs=[]
 for p in sorted(parts,key=lambda p:natural(p['ref'])):
  if p['ref'].startswith('H') and not p['pins']:continue
  f=footprints[p['ref']];attrs=one(f,'attr') or []
  types={str(a[2]) for a in all_(f,'pad') if a[2] in ('smd','thru_hole')}
  if types=={'smd'}:assembly='SMT';expected='smd'
  elif 'thru_hole' in types:assembly='MANUAL_THT';expected='through_hole'
  else:raise ValueError((p['ref'],types))
  if expected not in attrs:missing_attrs.append(p['ref'])
  mfr,code,status=sourcing(p['mpn'])
  row=[p['ref'],p['value'],1,mfr,p['mpn'],p['fp'],assembly,code,status]
  records.append(row)
  key=(p['mpn'],p['fp'],assembly)
  groups.setdefault(key,[]).append(row)
 headers=['Reference','Value','Quantity per board','Manufacturer','Manufacturer part number','Footprint','Assembly','LCSC/JLC code','Sourcing note']
 write(d/'BOM_by_reference.csv',headers,records)
 grouped=[]
 for rows in groups.values():
  r=list(rows[0]);r[0]=','.join(x[0] for x in rows);r[2]=len(rows);grouped.append(r)
 write(d/'BOM_grouped.csv',headers,grouped)
 # Missing catalog codes are deliberately blank, not invented. This is a draft
 # import table until the assembler resolves every exact MPN.
 write(d/'BOM_JLC_DRAFT.csv',['Comment','Designator','Footprint','LCSC Part #','Manufacturer','MPN'],[
  [r[1],r[0],r[5],r[7],r[3],r[4]] for r in grouped if r[6]=='SMT'])
 audit={'board':name,'electrical_components':len(records),'smt_components':sum(r[6]=='SMT' for r in records),'manual_tht_components':sum(r[6]=='MANUAL_THT' for r in records),'missing_assembly_attributes':missing_attrs,'assembly_quote_confirmed':False,'blank_catalog_groups':sum(not r[7] for r in grouped if r[6]=='SMT')}
 (d/'BOM_audit.json').write_text(json.dumps(audit,indent=2))
 print(json.dumps(audit))
if __name__=='__main__':
 import sys
 for name in sys.argv[1:] or ['USB_POWER','MAIN_POWER']:build(name)
