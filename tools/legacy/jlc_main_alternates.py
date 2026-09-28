import json,concurrent.futures
from pathlib import Path
# Reuse only the function definitions, without rerunning the baseline audit.
source=Path('work/jlc_main_passive_audit.py').read_text();exec(source[:source.index('found=dict(')])
candidates={
'ERJ3GEY0R00V':('C122704','R5,R8,R12,R21','Exact part after manufacturer hyphen normalization.'),
'0603WAF2052T5E':('C22910','R17','20.5k 1%100mW75V0603; same value/tolerance/power, verify resistor pulse/environment spec.'),
'0603WAF330KT5E':('C22979','R11','3.3ohm1%100mW0603; improved tolerance over5%, verify startup resistor pulse behavior.'),
'201007F750KT4E':('C421781','R1','7.5ohm1%750mW2010; verify repetitive snubber pulse curve before approval.'),
'RT0603BRC0784K5L':('C861034','R19','84.5k0.1%15ppm0603; sameYageoRTfamily with improvedTCR vs25ppm.'),
'RT0603BRC07931RL':('C861054','R20','931ohm0.1%15ppm0603; sameYageoRTfamily with improvedTCR vs25ppm.'),
'ERA-3AEB5110V':('C2075538','R25','511ohm0.1%25ppm100mW0603; same nominal specification; exact datasheet/package verify.'),
'RQ73C1J511RBTD':('C3959727','R25','511ohm0.1%10ppm150mW0603; alternative pending manufacturer verification.'),
'GCM2165C2A471GA16D':('C17565246','C1','470pF100VC0G0805 2%; improved tolerance; same dielectric, noDCbias concern.'),
'VJ0805A471GXBPW1BC':('C2254220','C1','470pF100VC0G0805 2%; manufacturer dimensions and voltage coefficient verify.'),
'CC0805KKX7R0BB474':('C596323','C15','470nF100VX7R10%0805; IC_VIN decoupling around12V, compareDCbias effectivecapacitance.'),
'08051C474KAT2A':('C597304','C15','470nF100VX7R10%0805; compareDCbias at12V and footprint height.'),
'EEHZC1K470P':('C178648','C19,C20','47uF80V10x10.2 hybrid 36mohm versusold700mohm. NOTdropinapproved: outputfilterdamping/stability changes, land drawing required.'),
'CC0603KRX7R9BB153':('C107076','C18','15nF50VX7R10%0603; same compensationvalue; verifyDCbias atCOMP/FB (~fewV).'),
'0603B153K500NT':('C1596','C18','15nF50VX7R10%0603; same compensationvalue, compareeffectivecapacitance.'),
}
items=[]
for mpn,result in concurrent.futures.ThreadPoolExecutor(max_workers=5).map(fetch,[(m,c[0])for m,c in candidates.items()]):
 c=candidates[mpn];d=dict(mpn=mpn,references=c[1],assessment=c[2],**result);items.append(d);i=d.get('live_jlc_metadata',{});print(mpn,c[0],i.get('componentModelEn'),i.get('componentLibraryType'),i.get('overseasStockCount'))
Path('work/jlc_main_alternates.json').write_text(json.dumps(items,indent=2),encoding='utf8')
