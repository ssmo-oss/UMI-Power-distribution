"""Apply the owner's V3 DXF contour and mounting-hole centers to D8 MAIN variants."""

from pathlib import Path

from create_d8_main import dump_sexpr, make_edge, parse_dxf, parse_sexpr


ROOT = Path(__file__).resolve().parents[1]
DXF = ROOT / "design/D8-2L-FASTON/source/10052938_AA-UMI POWER PCB OUTLINE V3.dxf"
SEGMENTS, HOLES, _ = parse_dxf(DXF)
DXF_ORIGIN_ON_BOARD = (139.6, 97.131981)


def child(node, name):
    return next((v for v in node if isinstance(v, list) and v and v[0] == name), None)


def quoted(value):
    return '"' + value + '"'


def apply(board_path):
    root = parse_sexpr(board_path.read_text(encoding="utf-8"))
    old_edges = [n for n in root[1:] if isinstance(n, list) and n and n[0].startswith("gr_")
                 and child(n, "layer") and child(n, "layer")[1] == '"Edge.Cuts"']
    root[:] = [root[0], *[n for n in root[1:] if n not in old_edges]]

    for seg in SEGMENTS:
        root.append(make_edge(seg, DXF_ORIGIN_ON_BOARD))

    # Keep footprints keyed by drawing circle position, so reference numbering
    # remains stable while following the V3 hole centers.
    # Retain the existing reference-to-location convention: H1/H6 are the
    # outside pair, H2/H5 the upper inner pair, and H3/H4 the lower pair.
    by_xy = {(round(x, 3), round(y, 3)): (x, y) for x, y, _radius in HOLES}
    ref_positions = {
        "H1": by_xy[(-56.9, 20.522)], "H2": by_xy[(-16.0, 38.0)],
        "H3": by_xy[(-16.0, -14.5)], "H4": by_xy[(16.0, -14.5)],
        "H5": by_xy[(16.0, 38.0)], "H6": by_xy[(56.9, 20.522)],
    }
    target_by_ref = {ref: (DXF_ORIGIN_ON_BOARD[0] + x, DXF_ORIGIN_ON_BOARD[1] - y)
                     for ref, (x, y) in ref_positions.items()}
    for footprint in (n for n in root[1:] if isinstance(n, list) and n and n[0] == "footprint"):
        prop = next((p for p in footprint if isinstance(p, list) and p[:2] == ["property", '"Reference"']), None)
        if not prop:
            continue
        ref = prop[2].strip('"')
        if ref not in target_by_ref:
            continue
        at = child(footprint, "at")
        if at:
            x, y = target_by_ref[ref]
            at[1], at[2] = f"{x:.6f}".rstrip("0").rstrip("."), f"{y:.6f}".rstrip("0").rstrip(".")

    board_path.write_text(dump_sexpr(root) + "\n", encoding="utf-8")
    print(f"{board_path}: replaced {len(old_edges)} Edge.Cuts objects with {len(SEGMENTS)} V3 segments; updated six mounting-hole centers")


for variant in ("D8-2L", "D8-2L-FASTON"):
    apply(ROOT / f"design/{variant}/MAIN_POWER/MAIN_POWER.kicad_pcb")
