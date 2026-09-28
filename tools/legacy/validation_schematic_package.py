"""Package generated flat UMI schematics on a 1.27 mm grid with local symbols.

Function: package_schematic(path, externally_driven_nets=()).
Original symbol/wire/label UUIDs are preserved. Added power flags get stable UUIDs.
Only supports the flat, unrotated generated circuit format; refuses conflicts.
"""
from pathlib import Path
import json
import re
import uuid
from collections import defaultdict
from validation_text_audit import parse, child, children, point


class Quoted(str): pass


def read(text):
    # Preserve string/atom distinction for KiCad S-expression serialization.
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text)
    stack=[];root=None
    for tok in tokens:
        if tok=='(':
            node=[]
            if stack:stack[-1].append(node)
            else:root=node
            stack.append(node)
        elif tok==')':stack.pop()
        else:stack[-1].append(Quoted(json.loads(tok)) if tok.startswith('"') else tok)
    assert not stack
    return root


def dump(x):
    if isinstance(x,list):return '('+' '.join(dump(i) for i in x)+')'
    return json.dumps(str(x)) if isinstance(x,Quoted) else str(x)


def snap(v):return round(round(float(v)/1.27)*1.27,6)
def fmt(v):return f'{v:.6f}'.rstrip('0').rstrip('.') or '0'


def package_schematic(path, externally_driven_nets=()):
    path=Path(path);s=read(path.read_text(encoding='utf-8'));root=child(s,'uuid')[1]
    if children(s,'sheet') or children(s,'bus'):raise ValueError('Flat schematic required')
    libs=child(s,'lib_symbols');libmap={x[1]:x for x in children(libs,'symbol')}
    moves={};graph=defaultdict(set)
    for wire in children(s,'wire'):
        a,z=[point(p) for p in children(child(wire,'pts'),'xy')]
        graph[a].add(z);graph[z].add(a)
    for inst in children(s,'symbol'):
        at=child(inst,'at')
        if float(at[3])!=0 or child(inst,'mirror'):raise ValueError('Unrotated symbols required')
        oldx,oldy=point(at);nx,ny=snap(oldx),snap(oldy)
        lib=libmap[child(inst,'lib_id')[1]]
        for sub in children(lib,'symbol'):
            for pin in children(sub,'pin'):
                pat=child(pin,'at');px,py=point(pat);npx,npy=snap(px),snap(py)
                old=(round(oldx+px,6),round(oldy-py,6));new=(round(nx+npx,6),round(ny-npy,6))
                moves[old]=(round(new[0]-old[0],6),round(new[1]-old[1],6))
                pat[1:3]=[fmt(npx),fmt(npy)]
        at[1:3]=[fmt(nx),fmt(ny)]
        for p in children(inst,'property'):
            pat=child(p,'at')
            if pat:pat[1:3]=[fmt(float(pat[1])+nx-oldx),fmt(float(pat[2])+ny-oldy)]
    translated={}
    for anchor,delta in moves.items():
        seen=set();todo=[anchor]
        while todo:
            p=todo.pop()
            if p in seen:continue
            seen.add(p);todo.extend(graph[p]-seen)
        for p in seen:
            if p in translated and translated[p]!=delta:raise ValueError('Shared wire has incompatible grid translations')
            translated[p]=delta
    for wire in children(s,'wire'):
        for p in children(child(wire,'pts'),'xy'):
            old=point(p);dx,dy=translated.get(old,(0,0));p[1:3]=[fmt(old[0]+dx),fmt(old[1]+dy)]
    for tag in ('label','global_label','no_connect','junction'):
        for item in children(s,tag):
            at=child(item,'at');old=point(at);dx,dy=translated.get(old,(0,0));at[1:3]=[fmt(old[0]+dx),fmt(old[1]+dy)]
    flaglib='UMI:PWR_FLAG'
    if externally_driven_nets and flaglib not in libmap:
        libs.append(read('(symbol "UMI:PWR_FLAG" (power) (pin_names (offset 0)) (in_bom no) (on_board no) (property "Reference" "#FLG" (at 0 0 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at 0 2.54 0) (effects (font (size 1 1)))) (symbol "PWR_FLAG_0_1" (polyline (pts (xy 0 0) (xy 0 1.27) (xy -1.27 1.905) (xy 0 2.54) (xy 1.27 1.905) (xy 0 1.27)) (stroke (width 0) (type default)) (fill (type none)))) (symbol "PWR_FLAG_1_1" (pin power_out line (at 0 0 90) (length 0) (name "pwr" (effects (font (size 1 1)))) (number "1" (effects (font (size 1 1)))))))'))
    existing={child(i,'uuid')[1] for i in children(s,'symbol')}
    for index,net in enumerate(externally_driven_nets,1):
        if not any(i[1]==net for tag in ('label','global_label') for i in children(s,tag)):raise ValueError(f'Power-flag net missing: {net}')
        ident=str(uuid.uuid5(uuid.NAMESPACE_URL,str(root)+'/powerflag/'+net))
        if ident in existing:continue
        x,y=762,snap(50+index*12.7);ref=f'#FLG{index:03d}'
        s.append(read(f'(symbol (lib_id "{flaglib}") (at {x} {y} 0) (unit 1) (in_bom no) (on_board no) (dnp no) (uuid "{ident}") (property "Reference" "{ref}" (at {x} {y} 0) (effects (font (size 1 1)) hide)) (property "Value" "PWR_FLAG" (at {x} {y-2.54} 0) (effects (font (size 1 1)))) (instances (project {json.dumps(path.stem)} (path "/{root}" (reference "{ref}") (unit 1)))))'))
        lid=str(uuid.uuid5(uuid.NAMESPACE_URL,ident+'/label'))
        label_kind='global_label' if any(i[1]==net for i in children(s,'global_label')) else 'label'
        shape='(shape input)' if label_kind=='global_label' else ''
        s.append(read(f'({label_kind} {json.dumps(net)} {shape} (at {x} {y} 0) (effects (font (size 1 1)) (justify left bottom)) (uuid "{lid}"))'))
    def textsize(node):
        if not isinstance(node,list):return
        if node and node[0]=='font':
            size=child(node,'size')
            if size:size[1:3]=['1','1']
        for x in node:textsize(x)
    textsize(s)
    library=['kicad_symbol_lib',['version','20241209'],['generator',Quoted('eeschema')]]
    for sym in children(libs,'symbol'):
        copied=read(dump(sym));copied[1]=Quoted(str(copied[1]).split(':',1)[-1]);library.append(copied)
    path.write_text(dump(s),encoding='utf-8')
    (path.parent/'UMI.kicad_sym').write_text(dump(library),encoding='utf-8')
    (path.parent/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "UMI") (type "KiCad") (uri "${KIPRJMOD}/UMI.kicad_sym") (options "") (descr "UMI local circuit symbols")))',encoding='utf-8')
    return {'schematic':str(path),'grid_mm':1.27,'power_flag_nets':list(externally_driven_nets)}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('schematic');ap.add_argument('--power-net',action='append',default=[])
    a=ap.parse_args();print(json.dumps(package_schematic(a.schematic,a.power_net),indent=2))
