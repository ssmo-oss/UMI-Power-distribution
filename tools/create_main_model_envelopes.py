from pathlib import Path
from create_faston_proxy_step import step_box

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'design/D8-2L-FASTON/MAIN_POWER/3d'


def write_assembly(name, description, boxes):
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
        f"#4=PRODUCT('{name}','{name}','{description}',(#3));",
        "#5=PRODUCT_DEFINITION_FORMATION('','',#4);",
        "#6=PRODUCT_DEFINITION_CONTEXT('part definition',#1,'design');",
        "#7=PRODUCT_DEFINITION('design','',#5,#6);",
        "#8=PRODUCT_DEFINITION_SHAPE('','',#7);",
        f"#9=SHAPE_REPRESENTATION('{name}',(#15,{','.join(f'#{n}' for n in solid_ids)}),#10);",
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
    path = OUT / f'{name}.step'
    header = [
        'ISO-10303-21;', 'HEADER;',
        f"FILE_DESCRIPTION(('{description}'),'2;1');",
        f"FILE_NAME('{name}.step','2026-10-01T00:00:00',('Codex'),('OpenAI'),'','','');",
        "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));", 'ENDSEC;', 'DATA;'
    ]
    path.write_text('\n'.join([*header,*entities,'ENDSEC;','END-ISO-10303-21;','']),encoding='ascii')
    print(f'{path}: {len(boxes)} envelope solids')


def main():
    # JST B2P-VH body envelope follows the maker's 7.86 x 8.5 mm housing,
    # 9.4 mm insulation height, 3.96 mm pitch, and 3.7 mm PCB posts.
    jst_boxes = [
        (-1.95,-4.25,0, 5.91,4.25,9.4),
        (-0.57,-0.57,-3.7, 0.57,0.57,0),
        (3.39,-0.57,-3.7, 4.53,0.57,0),
    ]
    write_assembly('JST_VH_B2P-VH_ENVELOPE',
                   'Dimensioned JST VH header envelope; simplified housing and PCB tails, not vendor detail',jst_boxes)
    # Littelfuse FLR 178.6165 holder envelope uses the 20 x 6 mm body and
    # the published 21.6 mm maximum height envelope.
    holder_boxes=[(-3.6,-1.75,0,16.4,4.25,21.6)]
    write_assembly('Littelfuse_FLR_1786165_ENVELOPE',
                   'Dimensioned Littelfuse FLR ATO holder envelope; simplified body envelope, not vendor detail',holder_boxes)
    for variant in ('D8-2L', 'D8-2L-FASTON'):
        target = ROOT / 'design' / variant / 'MAIN_POWER' / '3d'
        target.mkdir(parents=True, exist_ok=True)
        for model in ('JST_VH_B2P-VH_ENVELOPE.step', 'Littelfuse_FLR_1786165_ENVELOPE.step'):
            (target / model).write_bytes((OUT / model).read_bytes())

if __name__ == '__main__':
    main()
