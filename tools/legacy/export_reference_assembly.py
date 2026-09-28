"""Make readable reference-only native assembly plots from a disposable board copy.

Does not import design builders or KiCad Python. Source board is hash-checked unchanged.
"""
import argparse, copy, hashlib, json, math, re, shutil, subprocess, sys
from pathlib import Path

class Q(str): pass
def parse(text):
    stack=[]; root=None
    for t in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text):
        if t=='(':
            n=[]
            if stack: stack[-1].append(n)
            else: root=n
            stack.append(n)
        elif t==')': stack.pop()
        else: stack[-1].append(Q(json.loads(t)) if t.startswith('"') else t)
    assert not stack
    return root
def dump(n): return '('+' '.join(map(dump,n))+')' if isinstance(n,list) else json.dumps(str(n)) if isinstance(n,Q) else str(n)
def one(n,k): return next((v for v in n if isinstance(v,list) and v and v[0]==k),None)
def all_(n,k): return [v for v in n if isinstance(v,list) and v and v[0]==k]
def set_(n,k,v): n[:]=[a for a in n if not(isinstance(a,list) and a and a[0]==k)]; n.append(v)

def clean(board):
    labels=[]
    # Dedicated assembly copy intentionally excludes board legends and copper.
    board[:]=[n for n in board if not(isinstance(n,list) and n[0] in ('segment','via','zone','gr_text','gr_text_box'))]
    for fp in all_(board,'footprint'):
        p=next(v for v in all_(fp,'property') if v[1]=='Reference'); ref=str(p[2])
        fp[:]=[n for n in fp if not(isinstance(n,list) and (n[0]=='fp_text' or (n[0]=='property' and n[1]!='Reference')))]
        pts=[]
        for n in fp:
            if not isinstance(n,list) or not one(n,'layer') or one(n,'layer')[1]!='F.Fab': continue
            stroke=one(n,'stroke')
            if stroke and one(stroke,'width'):one(stroke,'width')[1]='0.04'
            if n[0] in ('fp_line','fp_rect','fp_arc'):
                for k in ('start','end','mid'):
                    a=one(n,k)
                    if a: pts.append(tuple(map(float,a[1:3])))
            elif n[0]=='fp_circle':
                c=one(n,'center'); e=one(n,'end')
                if c and e:
                    x,y=map(float,c[1:3]); r=math.dist((x,y),tuple(map(float,e[1:3])))
                    pts.extend([(x-r,y-r),(x+r,y+r)])
        vertical=False
        if pts:
            x0=min(a for a,b in pts);x1=max(a for a,b in pts);y0=min(b for a,b in pts);y1=max(b for a,b in pts)
            cx=(x0+x1)/2;cy=(y0+y1)/2
            width=x1-x0;height=y1-y0
            vertical=height>width*1.4 and ref.startswith(('R','C'))
            if vertical:width,height=height,width
            size=max(.18,min(1.1,width/(1.3*len(ref)),height*.50))
        else: cx=cy=0.;size=.8
        # Diode symbols and mounting drill fills obscure centred lettering.
        if ref.startswith(('D','F')) and pts: cy=y0-size*1.2
        if ref=='D2' and pts: cx=x1+size*(len(ref)*.5+.6);cy=(y0+y1)/2
        if ref.startswith('H'): cy=-3.;size=.8
        if ref.startswith('J') and pts: cy=y1-size*1.2
        at=one(fp,'at'); angle=float(at[3]) if at and len(at)>3 else 0.
        set_(p,'at',['at',str(cx),str(cy),str(-angle+(90 if vertical else 0))])
        set_(p,'layer',['layer',Q('F.Fab')]);set_(p,'effects',parse(f'(effects (font (size {size} {size}) (thickness {max(.03,size*.10)})))'))
        p[:]=[v for v in p if v!='hide' and not(isinstance(v,list) and v[0]=='hide')]
        labels.append({'reference':ref,'local_label_center_mm':[cx,cy],'font_mm':size})
    set_(board,'paper',['paper',Q('A3')])
    return labels

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('board',type=Path);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--detail-box',type=float,nargs=4,metavar=('X0','Y0','X1','Y1'))
    args=ap.parse_args();src=args.board.resolve();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    before=hashlib.sha256(src.read_bytes()).hexdigest(); b=parse(src.read_text());labels=clean(b)
    work=Path(__file__).resolve().parent/'assembly_review_temp'/src.stem;work.mkdir(parents=True,exist_ok=True)
    pcb=work/src.name;pcb.write_text(dump(b),encoding='utf-8')
    if src.with_suffix('.kicad_pro').exists():shutil.copy2(src.with_suffix('.kicad_pro'),pcb.with_suffix('.kicad_pro'))
    wrapper=Path(__file__).with_name('validation_cli_controlled.py')
    def export(board,stem):
        for typ in ('pdf','svg'):
            dest=out/(stem+'.'+typ);report=work/(stem+'_'+typ+'_process.json')
            flags=['--mode-single','--layers','F.Fab,Edge.Cuts','--black-and-white']
            flags+=['--exclude-value','--scale','0'] if typ=='pdf' else ['--fit-page-to-board','--exclude-drawing-sheet']
            subprocess.run([sys.executable,str(wrapper),'--timeout','60','--report',str(report),'--','pcb','export',typ,*flags,'--output',str(dest),str(board)],check=True,capture_output=True)
            result=json.loads(report.read_text())
            if result.get('exit_code')!=0:raise RuntimeError(result)
    export(pcb,src.stem+'_assembly_references')
    if args.detail_box:
        x0,y0,x1,y1=args.detail_box;d=copy.deepcopy(b)
        d[:]=[n for n in d if not(isinstance(n,list) and ((n[0]=='footprint' and not(x0<=float(one(n,'at')[1])<=x1 and y0<=float(one(n,'at')[2])<=y1)) or n[0].startswith('gr_')))]
        for fp in all_(d,'footprint'):
            at=one(fp,'at');at[1]=str(float(at[1])-x0);at[2]=str(float(at[2])-y0)
        d.append(parse(f'(gr_rect (start 0 0) (end {x1-x0} {y1-y0}) (stroke (width .05) (type default)) (fill none) (layer "Edge.Cuts"))'))
        detail=work/(src.stem+'_detail.kicad_pcb');detail.write_text(dump(d),encoding='utf-8');export(detail,src.stem+'_assembly_detail')
    assert hashlib.sha256(src.read_bytes()).hexdigest()==before,'Source changed while plotting'
    report={'source':str(src),'source_sha256':before,'source_unchanged':True,'label_count':len(labels),'labels':labels,'detail_box_mm':args.detail_box,'scope':'Reference-only assembly visualization; disposable copy is not a manufacturing board'}
    (out/(src.stem+'_assembly_review.json')).write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='labels'},indent=2))
if __name__=='__main__':main()
