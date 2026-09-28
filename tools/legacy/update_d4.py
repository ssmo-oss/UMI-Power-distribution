"""Apply reviewed procurement substitutions to a fresh D4 copy, without rerouting."""
from pathlib import Path
import json, shutil, csv, copy
from design_d2 import parse, all_, one, prop, Q, write
BASE=Path.cwd(); SRC=BASE/'outputs/UMI_D3'; DST=BASE/'outputs/UMI_D4'
manifest=json.loads((BASE/'work/d4_substitutions.json').read_text(encoding='utf-8'))
for name in ['MAIN_POWER','USB_POWER']:
    src=SRC/name; dst=DST/name; dst.mkdir(parents=True,exist_ok=True)
    # Re-running is safe only before any D4 geometry edits.
    assert not (dst/'GEOMETRY_EDITED').exists(), 'Do not overwrite edited D4 copper'
    for p in src.iterdir():
        if p.is_file() and (p.suffix in ['.kicad_pcb','.kicad_sch','.kicad_pro','.kicad_sym'] or p.name in ['fp-lib-table','sym-lib-table','design.json','pin_schedule.csv']): shutil.copy2(p,dst/p.name)
    shutil.copytree(src/'UMI_D2.pretty',dst/'UMI_D2.pretty',dirs_exist_ok=True)
    pcb=parse((dst/(name+'.kicad_pcb')).read_text(encoding='utf-8'))
    sch=parse((dst/(name+'.kicad_sch')).read_text(encoding='utf-8'))
    parts=json.loads((dst/'design.json').read_text(encoding='utf-8'))
    footprints={str(prop(x,'Reference')[2]):x for x in all_(pcb,'footprint')}
    symbols={str(prop(x,'Reference')[2]):x for x in all_(sch,'symbol') if prop(x,'Reference')}
    changes=[r for r in manifest if r['board']==name]
    for change in changes:
        for ref in change['refs']:
            p=next(p for p in parts if p['ref']==ref)
            assert p['mpn']==change['old_mpn'], (ref,p['mpn'],change)
            p['mpn']=change['mpn']
            if 'value' in change:p['value']=change['value']
            for obj in [footprints[ref],symbols[ref]]:
                assert str(prop(obj,'MPN')[2])==change['old_mpn']
                prop(obj,'MPN')[2]=Q(change['mpn'])
                if 'value' in change:prop(obj,'Value')[2]=Q(change['value'])
            # Embedded library default value stays consistent with instance.
            if 'value' in change:
                libid=str(one(symbols[ref],'lib_id')[1])
                lib=next(x for x in all_(one(sch,'lib_symbols'),'symbol') if x[1]==libid)
                if prop(lib,'Value'):prop(lib,'Value')[2]=Q(change['value'])
    for item in all_(pcb,'gr_text'):
        if 'REV D3 ' in str(item[1]) or 'USB POWER - D3 ' in str(item[1]):item[1]=Q(str(item[1]).replace('D3','D4'))
    title=one(sch,'title_block')
    if title and one(title,'rev'):one(title,'rev')[1]=Q('D4 - PROCUREMENT PROTOTYPE')
    write(dst/(name+'.kicad_pcb'),pcb);write(dst/(name+'.kicad_sch'),sch)
    (dst/'design.json').write_text(json.dumps(parts,indent=2),encoding='utf-8')
    with (src/'pin_schedule.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    byref={p['ref']:p for p in parts}
    for row in rows:row['MPN']=byref[row['Reference']]['mpn']
    with (dst/'pin_schedule.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    # Procurement edits must not move parts, pads, tracks, vias or zones.
    old=parse((src/(name+'.kicad_pcb')).read_text(encoding='utf-8'))
    for kind in ['segment','via','zone']:assert all_(old,kind)==all_(pcb,kind),kind
    for oldfp in all_(old,'footprint'):
        fp=footprints[str(prop(oldfp,'Reference')[2])]
        assert one(oldfp,'at')==one(fp,'at') and all_(oldfp,'pad')==all_(fp,'pad')
    print(name,len(changes),'substitution groups; copper unchanged')
(DST/'PROCUREMENT_CHANGES.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
