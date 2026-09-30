"""Create the D8 MAIN layout candidate from D7-2L and a millimetre DXF profile.

This intentionally leaves the D7 source untouched. The input DXF is deduplicated,
checked as one closed line/arc contour, and mapped without scaling. Board objects
are rotated as a rigid layout so the existing electrical placement and routing
are preserved for review; the resulting revision is still a prototype candidate.
"""

from __future__ import annotations

import argparse
import math
import re
import uuid
from collections import Counter, defaultdict
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+')


def parse_sexpr(source: str):
    tokens = TOKEN.findall(source)
    index = 0

    def parse_one():
        nonlocal index
        token = tokens[index]
        index += 1
        if token != "(":
            return token
        node = []
        while tokens[index] != ")":
            node.append(parse_one())
        index += 1
        return node

    result = parse_one()
    if index != len(tokens):
        raise ValueError("Unexpected trailing tokens in KiCad board")
    return result


def dump_sexpr(value, indent=0):
    if not isinstance(value, list):
        return value
    if all(not isinstance(child, list) for child in value):
        return "(" + " ".join(value) + ")"
    head = value[0] if value else ""
    lines = ["(" + head]
    for child in value[1:]:
        lines.append(" " * (indent + 2) + dump_sexpr(child, indent + 2))
    lines.append(" " * indent + ")")
    return "\n".join(lines)


def child(node, name):
    if isinstance(node, list):
        for value in node:
            if isinstance(value, list) and value and value[0] == name:
                return value
    return None


def walk(node):
    if isinstance(node, list):
        yield node
        for value in node:
            yield from walk(value)


def unquote(value):
    return value[1:-1] if isinstance(value, str) and value.startswith('"') else value


def number(value):
    return float(value)


def fmt(value):
    return f"{value:.6f}".rstrip("0").rstrip(".") or "0"


def new_uuid():
    return '"' + str(uuid.uuid4()) + '"'


def parse_dxf(path: Path):
    lines = path.read_text(encoding="cp1252").splitlines()
    if len(lines) % 2:
        raise ValueError("Malformed DXF code/value pairs")
    pairs = [(lines[i].strip(), lines[i + 1].strip()) for i in range(0, len(lines), 2)]
    insunits = None
    for i, pair in enumerate(pairs[:-1]):
        if pair[0] == "9" and pair[1] == "$INSUNITS":
            insunits = pairs[i + 1][1]
            break
    if insunits != "4":
        raise ValueError(f"Expected DXF millimetres ($INSUNITS=4); received {insunits!r}")

    entity_index = next(i for i, p in enumerate(pairs) if p == ("2", "ENTITIES")) + 1
    entities = []
    current = None
    for code, value in pairs[entity_index:]:
        if code == "0":
            if current:
                entities.append(current)
            if value == "ENDSEC":
                break
            current = {"type": value}
        elif current is not None:
            current.setdefault(code, []).append(value)

    def val(entity, group):
        return float(entity[group][0])

    lines_by_key = {}
    arcs_by_key = {}
    circles = {}
    for entity in entities:
        kind = entity["type"]
        if kind == "LINE":
            a = (val(entity, "10"), val(entity, "20"))
            b = (val(entity, "11"), val(entity, "21"))
            key = ("LINE", *sorted((tuple(round(q, 6) for q in a), tuple(round(q, 6) for q in b))))
            lines_by_key[key] = (a, b)
        elif kind == "ARC":
            cx, cy, radius = val(entity, "10"), val(entity, "20"), val(entity, "40")
            start_angle, end_angle = val(entity, "50"), val(entity, "51")
            point = lambda a: (cx + radius * math.cos(math.radians(a)), cy + radius * math.sin(math.radians(a)))
            start, end = point(start_angle), point(end_angle)
            ends = tuple(sorted(tuple(round(q, 6) for q in p) for p in (start, end)))
            key = ("ARC", round(cx, 6), round(cy, 6), round(radius, 6), ends)
            arcs_by_key[key] = (cx, cy, radius, start_angle, end_angle, start, end)
        elif kind == "CIRCLE":
            key = (round(val(entity, "10"), 6), round(val(entity, "20"), 6), round(val(entity, "40"), 6))
            circles[key] = circles.get(key, 0) + 1

    segments = []
    for a, b in lines_by_key.values():
        segments.append(("LINE", a, b))
    for cx, cy, radius, start_angle, end_angle, start, end in arcs_by_key.values():
        segments.append(("ARC", (cx, cy, radius, start_angle, end_angle), start, end))

    adjacency = defaultdict(list)
    for i, segment in enumerate(segments):
        if segment[0] == "LINE":
            a, b = segment[1], segment[2]
        else:
            a, b = segment[2], segment[3]
        a_key = tuple(round(q, 5) for q in a)
        b_key = tuple(round(q, 5) for q in b)
        adjacency[a_key].append((b_key, i))
        adjacency[b_key].append((a_key, i))
    degrees = Counter(len(v) for v in adjacency.values())
    if len(degrees) != 1 or degrees.get(2) != len(adjacency):
        raise ValueError(f"DXF line/arc endpoints do not form a closed contour: {degrees}")
    pending = set(adjacency)
    components = 0
    while pending:
        components += 1
        queue = [pending.pop()]
        while queue:
            for neighbor, _ in adjacency[queue.pop()]:
                if neighbor in pending:
                    pending.remove(neighbor)
                    queue.append(neighbor)
    if components != 1:
        raise ValueError(f"Expected one closed board outline; found {components}")

    if len(circles) != 6 or any(count != 2 for count in circles.values()):
        raise ValueError(f"Expected six double-drawn mounting-hole circles; found {circles}")
    holes = sorted((x, y, r) for x, y, r in circles)
    if any(abs(r - 1.75) > 1e-6 for _, _, r in holes):
        raise ValueError("Expected 3.5 mm diameter mounting holes")

    xs, ys = [], []
    for segment in segments:
        if segment[0] == "LINE":
            points = segment[1:]
        else:
            cx, cy, radius, a0, a1 = segment[1]
            points = [segment[2], segment[3]]
            sweep = (a1 - a0) % 360
            for angle in (a0, a0 + sweep / 2, a0 + sweep):
                points.append((cx + radius * math.cos(math.radians(angle)), cy + radius * math.sin(math.radians(angle))))
        xs.extend(p[0] for p in points)
        ys.extend(p[1] for p in points)
    return segments, holes, (min(xs), min(ys), max(xs), max(ys))


def transform_layout_xy(x, y, old_center, new_center):
    ox, oy = old_center
    nx, ny = new_center
    # KiCad's positive 90-degree footprint rotation maps local +X toward -Y.
    return nx + (y - oy), ny - (x - ox)


def rotate_at(node, old_center, new_center, angle_delta=90):
    if len(node) < 3:
        return
    x, y = transform_layout_xy(number(node[1]), number(node[2]), old_center, new_center)
    node[1], node[2] = fmt(x), fmt(y)
    if len(node) > 3:
        node[3] = fmt((number(node[3]) + angle_delta) % 360)


def transform_global_nodes(node, old_center, new_center):
    if not isinstance(node, list):
        return
    head = node[0] if node else None
    if head in {"at", "xy", "start", "end", "mid", "center", "aux_axis_origin"} and len(node) >= 3:
        x, y = transform_layout_xy(number(node[1]), number(node[2]), old_center, new_center)
        node[1], node[2] = fmt(x), fmt(y)
        if head == "at" and len(node) > 3:
            node[3] = fmt((number(node[3]) + 90) % 360)
        return
    for value in node:
        transform_global_nodes(value, old_center, new_center)


def footprint_reference(fp):
    node = child(fp, "property")
    while node:
        if len(node) > 2 and unquote(node[1]) == "Reference":
            return unquote(node[2])
        node = None
    return ""


def is_mounting_footprint(fp):
    return isinstance(fp, list) and fp and fp[0] == "footprint" and "MountingHole_4.5mm" in unquote(fp[1])


def collect_uuids(node, result):
    for value in walk(node):
        if isinstance(value, list) and value and value[0] == "uuid" and len(value) > 1:
            result.add(value[1])


def make_hole_footprint(index, x, y):
    ref = f'H{index}'
    ref_uuid, value_uuid, pad_uuid, fp_uuid = [new_uuid() for _ in range(4)]
    return [
        "footprint", '"UMI_D2:MountingHole_3.5mm"',
        ["layer", '"F.Cu"'], ["uuid", fp_uuid], ["at", fmt(x), fmt(y), "0"],
        ["property", '"Reference"', f'"{ref}"', ["at", "0", "-3", "0"], ["layer", '"F.Fab"'], ["hide", "yes"], ["uuid", ref_uuid], ["effects", ["font", ["size", "1", "1"], ["thickness", "0.15"]]]],
        ["property", '"Value"', '"DXF 3.5mm NPTH"', ["at", "0", "3", "0"], ["layer", '"F.Fab"'], ["hide", "yes"], ["uuid", value_uuid], ["effects", ["font", ["size", "1", "1"], ["thickness", "0.15"]]]],
        ["attr", "exclude_from_pos_files", "exclude_from_bom"],
        ["pad", '""', "np_thru_hole", "circle", ["at", "0", "0"], ["size", "3.5", "3.5"], ["drill", "3.5"], ["layers", '"*.Cu"', '"*.Mask"'], ["uuid", pad_uuid]],
        ["embedded_fonts", "no"],
    ]


def make_edge(segment, source_center):
    cx, cy = source_center
    def xy(point):
        return (fmt(cx + point[0]), fmt(cy - point[1]))
    if segment[0] == "LINE":
        a, b = xy(segment[1]), xy(segment[2])
        return ["gr_line", ["start", *a], ["end", *b], ["stroke", ["width", "0.05"], ["type", "solid"]], ["layer", '"Edge.Cuts"'], ["uuid", new_uuid()]]
    arc, a, b = segment[1], segment[2], segment[3]
    acx, acy, radius, angle0, angle1 = arc
    sweep = (angle1 - angle0) % 360
    angle_mid = angle0 + sweep / 2
    mid = (acx + radius * math.cos(math.radians(angle_mid)), acy + radius * math.sin(math.radians(angle_mid)))
    return ["gr_arc", ["start", *xy(a)], ["mid", *xy(mid)], ["end", *xy(b)], ["stroke", ["width", "0.05"], ["type", "solid"]], ["layer", '"Edge.Cuts"'], ["uuid", new_uuid()]]


def make_library_footprint(path: Path):
    path.write_text('''(footprint "MountingHole_3.5mm"
\t(version 20240108)
\t(generator "pcbnew")
\t(layer "F.Cu")
\t(descr "Non-plated 3.5 mm mounting hole from UMI Power PCB outline V2")
\t(property "Reference" "H" (at 0 -3 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))
\t(property "Value" "DXF 3.5mm NPTH" (at 0 3 0) (layer "F.Fab") (hide yes) (effects (font (size 1 1) (thickness 0.15))))
\t(attr exclude_from_pos_files exclude_from_bom)
\t(pad "" np_thru_hole circle (at 0 0) (size 3.5 3.5) (drill 3.5) (layers "*.Cu" "*.Mask"))
\t(embedded_fonts no)
)
''', encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-board", type=Path, required=True)
    parser.add_argument("--dxf", type=Path, required=True)
    parser.add_argument("--output-board", type=Path, required=True)
    parser.add_argument("--footprint-library", type=Path, required=True)
    args = parser.parse_args()

    segments, holes, bounds = parse_dxf(args.dxf)
    root = parse_sexpr(args.source_board.read_text(encoding="utf-8"))
    if root[0] != "kicad_pcb":
        raise ValueError("Input is not a KiCad PCB")

    old_center = (139.6, 97.131981)
    new_center = (139.6, 85.381981)
    deleted_uuids = set()
    retained = []
    for item in root[1:]:
        if isinstance(item, list) and item and item[0] == "footprint" and is_mounting_footprint(item):
            collect_uuids(item, deleted_uuids)
            continue
        if isinstance(item, list) and item and item[0] == "gr_arc":
            layer = child(item, "layer")
            if layer and unquote(layer[1]) == "Edge.Cuts":
                collect_uuids(item, deleted_uuids)
                continue
        if isinstance(item, list) and item and item[0] == "gr_line":
            layer = child(item, "layer")
            if layer and unquote(layer[1]) == "Edge.Cuts":
                collect_uuids(item, deleted_uuids)
                continue
        retained.append(item)
    root[1:] = retained

    for item in root[1:]:
        if not isinstance(item, list) or not item:
            continue
        if item[0] == "footprint":
            at = child(item, "at")
            if at:
                rotate_at(at, old_center, new_center, angle_delta=90)
        elif item[0] in {"segment", "via", "zone", "gr_text", "gr_line", "gr_arc", "gr_rect", "gr_circle", "gr_poly", "dimension", "target", "image", "pcb_text", "pcb_shape", "setup"}:
            transform_global_nodes(item, old_center, new_center)

    for group in [value for value in root[1:] if isinstance(value, list) and value and value[0] == "group"]:
        for member_list in walk(group):
            if isinstance(member_list, list) and member_list and member_list[0] == "members":
                member_list[1:] = [member for member in member_list[1:] if member not in deleted_uuids]

    for value in walk(root):
        if isinstance(value, list) and value and value[0] == "gr_text" and len(value) > 1 and isinstance(value[1], str):
            value[1] = value[1].replace("D7-2L", "D8-2L")

    source_center = (old_center[0], old_center[1])
    for segment in segments:
        root.append(make_edge(segment, source_center))
    for index, (x, y, _) in enumerate(holes, start=1):
        # DXF origin is the source origin; retain the established MAIN sheet position.
        root.append(make_hole_footprint(index, source_center[0] + x, source_center[1] - y))

    args.footprint_library.mkdir(parents=True, exist_ok=True)
    make_library_footprint(args.footprint_library / "MountingHole_3.5mm.kicad_mod")
    args.output_board.parent.mkdir(parents=True, exist_ok=True)
    args.output_board.write_text(dump_sexpr(root) + "\n", encoding="utf-8")

    w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
    print(f"Wrote {args.output_board}")
    print(f"Profile: {w:.3f} x {h:.3f} mm; {len(segments)} unique outline segments; {len(holes)} holes at 3.5 mm")
    print(f"Source contour bounds: x={bounds[0]:.3f}..{bounds[2]:.3f}, y={bounds[1]:.3f}..{bounds[3]:.3f} mm")
    print("Layout transform: 90 degrees; D7-2L component footprints, traces, and copper zones preserved")


if __name__ == "__main__":
    main()
