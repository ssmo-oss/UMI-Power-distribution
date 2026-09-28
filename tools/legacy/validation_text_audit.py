"""Independent read-only audit of flat KiCad schematic labels against PCB pad nets.

Supports the generated UMI single-sheet, unrotated-symbol schematic format.
Rejects unsupported schematic constructs instead of inventing connectivity.
Does not import design builders, pcbnew, or KiCad Python. Does not run DRC/ERC.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re


def parse(text):
    stack = []
    root = None
    for tok in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text):
        if tok == '(':
            node = []
            if stack:
                stack[-1].append(node)
            elif root is not None:
                raise ValueError('Multiple root expressions')
            else:
                root = node
            stack.append(node)
        elif tok == ')':
            if not stack:
                raise ValueError('Unmatched closing parenthesis')
            stack.pop()
        else:
            stack[-1].append(json.loads(tok) if tok.startswith('"') else tok)
    if stack or root is None:
        raise ValueError('Incomplete expression')
    return root


def children(node, tag):
    return [x for x in node if isinstance(x, list) and x and x[0] == tag]


def child(node, tag):
    return next(iter(children(node, tag)), None)


def prop(node, name):
    return next((x[2] for x in children(node, 'property') if x[1] == name), None)


def point(node):
    return tuple(round(float(x), 6) for x in node[1:3])


def ids(node):
    result = []
    if isinstance(node, list):
        if node and node[0] == 'uuid':
            result.append(node[1])
        for x in node:
            result.extend(ids(x))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('board')
    ap.add_argument('--schematic')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    bp = Path(args.board)
    sp = Path(args.schematic) if args.schematic else bp.with_suffix('.kicad_sch')
    bt, st = bp.read_text(encoding='utf-8-sig'), sp.read_text(encoding='utf-8-sig')
    b, s = parse(bt), parse(st)
    errors, unsupported = [], []
    for tag in ('sheet', 'bus', 'bus_entry', 'hierarchical_label'):
        if children(s, tag):
            unsupported.append(tag)
    graph = defaultdict(set)
    wires = []
    for wire in children(s, 'wire'):
        points = [point(x) for x in children(child(wire, 'pts'), 'xy')]
        if len(points) != 2:
            unsupported.append('wire with other than two endpoints')
            continue
        a, z = points
        graph[a].add(z); graph[z].add(a)
        wires.append((a, z))
    labels = defaultdict(set)
    for tag in ('label', 'global_label'):
        for label in children(s, tag):
            labels[point(child(label, 'at'))].add(label[1])
    ncs = {point(child(x, 'at')) for x in children(s, 'no_connect')}
    symbols = {x[1]: x for x in children(child(s, 'lib_symbols'), 'symbol')}
    expected, bindings, pin_pos, pin_functions = {}, {}, {}, {}
    refs = []
    for sym in children(s, 'symbol'):
        if child(sym, 'on_board') and child(sym, 'on_board')[1] == 'no':
            continue
        ref = prop(sym, 'Reference'); refs.append(ref)
        at = child(sym, 'at')
        if len(at) > 3 and float(at[3]) != 0 or child(sym, 'mirror'):
            unsupported.append(f'{ref}: rotated or mirrored symbol')
            continue
        bindings[ref] = child(sym, 'uuid')[1]
        lib_id = child(sym, 'lib_id')[1]
        if lib_id not in symbols:
            unsupported.append(f'{ref}: missing embedded symbol')
            continue
        unit = int(child(sym, 'unit')[1])
        lib = symbols[lib_id]
        for sub in children(lib, 'symbol'):
            m = re.search(r'_(\d+)_(\d+)$', sub[1])
            if m and int(m[1]) not in (0, unit):
                continue
            for pin in children(sub, 'pin'):
                num = child(pin, 'number')[1]
                px, py = point(child(pin, 'at'))
                pos = (round(float(at[1]) + px, 6), round(float(at[2]) - py, 6))
                pin_pos[(ref, num)] = pos
                pin_functions[(ref, num)] = child(pin, 'name')[1]
    # Attach endpoints, pin positions, labels and explicit junctions lying on wires.
    points = set(graph) | set(labels) | set(pin_pos.values())
    points |= {point(child(x, 'at')) for x in children(s, 'junction')}
    for a, z in wires:
        for p in points:
            cross = (p[0]-a[0])*(z[1]-a[1]) - (p[1]-a[1])*(z[0]-a[0])
            inside = min(a[0], z[0])-1e-6 <= p[0] <= max(a[0], z[0])+1e-6 and min(a[1], z[1])-1e-6 <= p[1] <= max(a[1], z[1])+1e-6
            if abs(cross) < 1e-6 and inside:
                graph[a].add(p); graph[p].add(a)
    for key, pos in pin_pos.items():
        seen, todo, names = set(), [pos], set()
        while todo:
            p = todo.pop()
            if p in seen:
                continue
            seen.add(p); names |= labels.get(p, set()); todo.extend(graph[p]-seen)
        if len(names) == 1:
            expected[key] = next(iter(names))
            if pos in ncs:
                errors.append(f'{key}: label and no-connect both present')
        elif not names and pos in ncs:
            expected[key] = None
        else:
            errors.append(f'{key}: expected one named net or explicit no-connect, got {sorted(names)}')
    actual, fp_refs, pad_count, bindings_bad = {}, [], 0, []
    for f in children(b, 'footprint'):
        ref = prop(f, 'Reference'); fp_refs.append(ref)
        path = child(f, 'path')
        if ref in bindings and (not path or not path[1].endswith('/'+bindings[ref])):
            bindings_bad.append(ref)
        for p in children(f, 'pad'):
            num = p[1]
            layers = child(p, 'layers')
            if not num or not layers or not any(x.endswith('.Cu') for x in layers[1:]):
                continue
            pad_count += 1
            n = child(p, 'net'); net = n[2] if n and len(n) > 2 else n[1] if n and len(n) == 2 else None
            key = (ref, num)
            if key in actual and actual[key] != net:
                errors.append(f'{key}: repeated physical pad has different nets')
            actual[key] = net
    missing = sorted(set(expected)-set(actual))
    extra = sorted(set(actual)-set(expected))
    def matches(k):
        if expected[k] == actual[k]:
            return True
        # KiCad assigns explicit no-connect pins their own diagnostic net names.
        # Accept only the exact ref/function/pad-derived name, not any arbitrary net.
        return expected[k] is None and actual[k] == f'unconnected-({k[0]}-{pin_functions[k]}-Pad{k[1]})'
    mismatches = [{'reference': k[0], 'pin': k[1], 'schematic_net': expected[k], 'pcb_net': actual[k]}
                  for k in sorted(set(expected)&set(actual)) if not matches(k)]
    # Purely mechanical footprints with no electrical symbol are allowed, but
    # their numbered copper pads remain visible for review in extra_pcb_pins.
    report = {'scope': 'Independent text parsing: flat schematic labels to PCB pad nets and UUID linkage; not ERC/DRC',
              'manufacturing_release': False, 'utc': datetime.now(timezone.utc).isoformat(),
              'board': str(bp.resolve()), 'schematic': str(sp.resolve()),
              'board_sha256': hashlib.sha256(bt.encode()).hexdigest(),
              'schematic_sha256': hashlib.sha256(st.encode()).hexdigest(),
              'schematic_symbols': len(refs), 'pcb_footprints': len(fp_refs),
              'schematic_pins': len(expected), 'physical_copper_pads': pad_count,
              'tracks': len(children(b, 'segment')), 'vias': len(children(b, 'via')), 'zones': len(children(b, 'zone')),
              'unsupported_constructs': unsupported, 'errors': errors,
              'duplicate_schematic_refs': [r for r, n in Counter(refs).items() if n > 1],
              'duplicate_pcb_refs': [r for r, n in Counter(fp_refs).items() if n > 1],
              'duplicate_schematic_uuids': [r for r, n in Counter(ids(s)).items() if n > 1],
              'duplicate_pcb_uuids': [r for r, n in Counter(ids(b)).items() if n > 1],
              'missing_pcb_pins': missing, 'extra_pcb_pins': extra,
              'pad_net_mismatches': mismatches, 'incorrect_symbol_footprint_uuid_bindings': bindings_bad,
              'limitations': ['Does not establish copper routing connectivity or clearance.',
                  'Does not verify symbol pin function, manufacturer pinout, component ratings or circuit behaviour.',
                  'This checker only supports one flat sheet and unrotated symbols with named nets.']}
    report['netlist_comparison_pass'] = not any(report[k] for k in (
        'unsupported_constructs', 'errors', 'duplicate_schematic_refs', 'duplicate_pcb_refs',
        'duplicate_schematic_uuids', 'duplicate_pcb_uuids', 'missing_pcb_pins',
        'pad_net_mismatches', 'incorrect_symbol_footprint_uuid_bindings'))
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
