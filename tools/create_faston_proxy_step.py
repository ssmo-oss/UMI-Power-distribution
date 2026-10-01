"""Write a simple solid STEP envelope for the two TE 63951-4 terminals.

This is a dimension-based envelope proxy, not the manufacturer's detailed CAD.
"""

from pathlib import Path
import math


OUTPUT = Path(__file__).resolve().parents[1] / "design/D8-2L-FASTON/MAIN_POWER/3d/FASTON_63951-4_PAIR_PROXY.step"


def fmt(value):
    return f"{value:.9f}".rstrip("0").rstrip(".")


def step_box(x1, y1, z1, x2, y2, z2, start_id):
    entities = []
    next_id = start_id

    def add(line):
        nonlocal next_id
        entity_id = next_id
        next_id += 1
        entities.append(f"#{entity_id}={line};")
        return entity_id

    points = [
        (x1, y1, z1), (x2, y1, z1), (x2, y2, z1), (x1, y2, z1),
        (x1, y1, z2), (x2, y1, z2), (x2, y2, z2), (x1, y2, z2),
    ]
    vertex_ids = []
    for xyz in points:
        point_id = add(f"CARTESIAN_POINT('',({fmt(xyz[0])},{fmt(xyz[1])},{fmt(xyz[2])}))")
        vertex_ids.append(add(f"VERTEX_POINT('',#{point_id})"))

    face_cycles = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
                   (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    edge_pairs = sorted({tuple(sorted((cycle[i], cycle[(i + 1) % 4])))
                         for cycle in face_cycles for i in range(4)})
    edge_ids = {}
    for a, b in edge_pairs:
        pa, pb = points[a], points[b]
        delta = tuple(pb[i] - pa[i] for i in range(3))
        length = math.sqrt(sum(v * v for v in delta))
        direction = tuple(v / length for v in delta)
        point_id = add(f"CARTESIAN_POINT('',({fmt(pa[0])},{fmt(pa[1])},{fmt(pa[2])}))")
        dir_id = add(f"DIRECTION('',({fmt(direction[0])},{fmt(direction[1])},{fmt(direction[2])}))")
        vector_id = add(f"VECTOR('',#{dir_id},1.)")
        line_id = add(f"LINE('',#{point_id},#{vector_id})")
        edge_ids[(a, b)] = add(f"EDGE_CURVE('',#{vertex_ids[a]},#{vertex_ids[b]},#{line_id},.T.)")

    face_ids = []
    for cycle in face_cycles:
        oriented = []
        for i in range(4):
            a, b = cycle[i], cycle[(i + 1) % 4]
            lo, hi = sorted((a, b))
            oriented.append(add(f"ORIENTED_EDGE('',*,*,#{edge_ids[(lo, hi)]},{'.T.' if (a, b) == (lo, hi) else '.F.'})"))
        loop_id = add(f"EDGE_LOOP('',({','.join(f'#{v}' for v in oriented)}))")
        bound_id = add(f"FACE_OUTER_BOUND('',#{loop_id},.T.)")

        p0, p1, p2 = (points[cycle[i]] for i in range(3))
        u = tuple(p1[i] - p0[i] for i in range(3))
        v = tuple(p2[i] - p0[i] for i in range(3))
        normal = (u[1] * v[2] - u[2] * v[1],
                  u[2] * v[0] - u[0] * v[2],
                  u[0] * v[1] - u[1] * v[0])
        norm = math.sqrt(sum(x * x for x in normal))
        normal = tuple(x / norm for x in normal)
        xnorm = math.sqrt(sum(x * x for x in u))
        xdir = tuple(x / xnorm for x in u)
        origin_id = add(f"CARTESIAN_POINT('',({fmt(p0[0])},{fmt(p0[1])},{fmt(p0[2])}))")
        zdir_id = add(f"DIRECTION('',({fmt(normal[0])},{fmt(normal[1])},{fmt(normal[2])}))")
        xdir_id = add(f"DIRECTION('',({fmt(xdir[0])},{fmt(xdir[1])},{fmt(xdir[2])}))")
        placement_id = add(f"AXIS2_PLACEMENT_3D('',#{origin_id},#{zdir_id},#{xdir_id})")
        plane_id = add(f"PLANE('',#{placement_id})")
        face_ids.append(add(f"ADVANCED_FACE('',(#{bound_id}),#{plane_id},.T.)"))

    shell_id = add(f"CLOSED_SHELL('',({','.join(f'#{face}' for face in face_ids)}))")
    solid_id = add(f"MANIFOLD_SOLID_BREP('63951-4 terminal envelope',#{shell_id})")
    return entities, solid_id, next_id


def main():
    # KiCad mirrors 3D-model Y for an F.Cu footprint. Author the shape with
    # positive model Y so the installed blades point toward board top (global
    # negative Y), and mirror the through-hole pin coordinates for the same
    # transform. Each terminal has two solder tails at 5.08 mm pitch.
    boxes = []
    for cx in (-5.08, 5.08):
        boxes.append((cx - 0.4, 5.08, 0, cx + 0.4, 11.43, 8.89))
        boxes.append((cx - 0.4, 0, 0, cx + 0.4, 5.08, 0.8))
        for cy in (0.0, 5.08):
            boxes.append((cx - 0.5, cy - 0.5, -3.81, cx + 0.5, cy + 0.5, 0.8))

    entities = []
    solid_ids = []
    next_id = 101
    for box in boxes:
        new_entities, solid, next_id = step_box(*box, next_id)
        entities.extend(new_entities)
        solid_ids.append(solid)

    entities.extend([
        "#1=APPLICATION_CONTEXT('automotive design');",
        "#2=APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#1);",
        "#3=PRODUCT_CONTEXT('',#1,'mechanical');",
        "#4=PRODUCT('FASTON_63951-4_PAIR_PROXY','FASTON 63951-4 pair proxy','Dimension-based proxy, not vendor CAD',(#3));",
        "#5=PRODUCT_DEFINITION_FORMATION('','',#4);",
        "#6=PRODUCT_DEFINITION_CONTEXT('part definition',#1,'design');",
        "#7=PRODUCT_DEFINITION('design','',#5,#6);",
        "#8=PRODUCT_DEFINITION_SHAPE('','',#7);",
        f"#9=SHAPE_REPRESENTATION('FASTON 63951-4 pair proxy',(#15,{','.join(f'#{n}' for n in solid_ids)}),#10);",
        "#10=(GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNIT_ASSIGNED_CONTEXT((#11,#12,#13)) REPRESENTATION_CONTEXT('Context #1','3D Context with UNIT and UNCERTAINTY'));",
        "#11=(LENGTH_UNIT() NAMED_UNIT(*) SI_UNIT(.MILLI.,.METRE.));",
        "#12=(NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.));",
        "#13=(NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT());",
        "#14=SHAPE_DEFINITION_REPRESENTATION(#8,#9);",
        "#15=AXIS2_PLACEMENT_3D('',#16,#17,#18);",
        "#16=CARTESIAN_POINT('',(0.,0.,0.));",
        "#17=DIRECTION('',(0.,0.,1.));",
        "#18=DIRECTION('',(1.,0.,0.));",
    ])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "ISO-10303-21;", "HEADER;",
        "FILE_DESCRIPTION(('Dimension-based FASTON 63951-4 envelope proxy'),'2;1');",
        "FILE_NAME('FASTON_63951-4_PAIR_PROXY.step','2026-10-01T00:00:00',('Codex'),('OpenAI'),'','','');",
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));", "ENDSEC;", "DATA;",
        *entities, "ENDSEC;", "END-ISO-10303-21;", "",
    ]
    OUTPUT.write_text("\n".join(lines), encoding="ascii")
    print(f"Wrote {OUTPUT} with {len(boxes)} solid blocks")


if __name__ == "__main__":
    main()
