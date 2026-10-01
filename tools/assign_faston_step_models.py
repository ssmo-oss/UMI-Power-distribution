"""Assign local dimensioned envelopes to the connector/fuse models in both D8 MAIN variants."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
replacements = {
    '${KICAD6_3DMODEL_DIR}/Connector_JST.3dshapes/JST_EH_B2B-EH-A_1x02_P2.50mm_Vertical.step': '${KIPRJMOD}/3d/JST_VH_B2P-VH_ENVELOPE.step',
    '${KICAD6_3DMODEL_DIR}/Connector_JST.3dshapes/JST_VH_B2P-VH_1x02_P3.96mm_Vertical.wrl': '${KIPRJMOD}/3d/JST_VH_B2P-VH_ENVELOPE.step',
    '${KICAD7_3DMODEL_DIR}/Fuse.3dshapes/Fuseholder_Blade_Mini_Keystone_3568.step': '${KIPRJMOD}/3d/Littelfuse_FLR_1786165_ENVELOPE.step',
    '${KICAD7_3DMODEL_DIR}/Fuse.3dshapes/FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165.wrl': '${KIPRJMOD}/3d/Littelfuse_FLR_1786165_ENVELOPE.step',
}
paths = [
    ROOT / 'design/D8-2L/MAIN_POWER/MAIN_POWER.kicad_pcb',
    ROOT / 'design/D8-2L-FASTON/MAIN_POWER/MAIN_POWER.kicad_pcb',
]
for variant in ('D8-2L', 'D8-2L-FASTON'):
    pretty = ROOT / 'design' / variant / 'MAIN_POWER/UMI_D2.pretty'
    paths.extend([
        pretty / 'JST_VH_B2P-VH_1x02_P3.96mm_Vertical.kicad_mod',
        pretty / 'FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165.kicad_mod',
    ])
for path in paths:
    text = path.read_text(encoding='utf-8')
    for source, target in replacements.items():
        text = text.replace(source, target)
    path.write_text(text, encoding='utf-8')
print('Assigned dimensioned JST VH and Littelfuse envelopes to both D8 MAIN variants')
