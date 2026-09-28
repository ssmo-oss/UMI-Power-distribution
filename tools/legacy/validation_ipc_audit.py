"""Read-only KiCad IPC copper-connectivity audit. Never starts KiCad or writes its documents.

Run only after the caller has refilled zones in its controlled verification copy.
This reports copper connectivity, NOT DRC/ERC or manufacturing readiness.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent / 'ipc_client'))
from kipy import KiCad
from kipy.proto.common.types import KiCadObjectType


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--socket', required=True)
    ap.add_argument('--expected-board', required=True, help='Exact filename, e.g. USB_POWER.kicad_pcb')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    k = KiCad(socket_path=args.socket, timeout_ms=15000)
    b = k.get_board()
    if b.name != args.expected_board:
        raise SystemExit(f'Wrong connected board: expected {args.expected_board!r}, received {b.name!r}; no changes made.')
    text = b.get_as_string()
    pads = b.get_pads()
    pad_by_id = {p.id.value: p for p in pads}
    names = {}
    footprints = b.get_footprints()
    for f in footprints:
        ref = f.reference_field.text.text
        for p in f.definition.pads:
            names[p.id.value] = f'{ref}.{p.number}'
    parent = {key: key for key in pad_by_id}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def join(a, z):
        parent[find(z)] = find(a)

    cross_net_contacts = set()
    # Visit every pad: the server may return direct neighbours rather than a full
    # transitive closure; union-find works for either behaviour.
    for p in pads:
        connected = b.get_connected_items(p, types=[KiCadObjectType.KOT_PCB_PAD])
        for q in connected:
            if q.id.value not in pad_by_id:
                continue
            join(p.id.value, q.id.value)
            if p.net.name and q.net.name and p.net.name != q.net.name:
                cross_net_contacts.add(tuple(sorted((names.get(p.id.value, p.id.value), names.get(q.id.value, q.id.value)))))
    nets = defaultdict(lambda: defaultdict(list))
    for p in pads:
        if p.net.name:
            nets[p.net.name][find(p.id.value)].append(names.get(p.id.value, p.id.value))
    net_report = {}
    for net, components in sorted(nets.items()):
        groups = sorted([sorted(group) for group in components.values()])
        net_report[net] = {'copper_component_count': len(groups), 'pad_count': sum(map(len, groups)), 'components': groups}
    report = {
        'scope': 'KiCad IPC copper-connected pad graph only; not DRC/ERC, no current capacity or electrical function validation',
        'manufacturing_release': False,
        'utc': datetime.now(timezone.utc).isoformat(),
        'version': str(k.get_version()), 'board': b.name,
        'serialized_board_sha256': hashlib.sha256(text.encode()).hexdigest(),
        'footprints': len(footprints), 'pads': len(pads),
        'tracks': len(b.get_tracks()), 'vias': len(b.get_vias()), 'zones': len(b.get_zones()),
        'copper_layers': b.get_copper_layer_count(),
        'disconnected_nets': [n for n, v in net_report.items() if v['copper_component_count'] > 1],
        'cross_net_contacts_returned_by_api': sorted(cross_net_contacts),
        'nets': net_report,
        'limitations': ['Zones must already be filled by caller; this script does not refill or save.',
            'GetConnectedItems may filter by net and is not a short-circuit detector.',
            'Repeated pad numbers may represent internally common component pins, but copper components are reported separately.',
            'No clearance, courtyard, mask, hole, thermal, creepage, ERC or fabrication checks.'],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k != 'nets'}, indent=2))


if __name__ == '__main__':
    main()
