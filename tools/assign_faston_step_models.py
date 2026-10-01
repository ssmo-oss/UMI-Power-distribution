"""Set installed proxy STEP models for both D8 MAIN board variants."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "design/D8-2L-FASTON/MAIN_POWER/MAIN_POWER.kicad_pcb"
replacements = {
    '${KICAD6_3DMODEL_DIR}/Connector_JST.3dshapes/JST_VH_B2P-VH_1x02_P3.96mm_Vertical.wrl': '${KICAD6_3DMODEL_DIR}/Connector_JST.3dshapes/JST_EH_B2B-EH-A_1x02_P2.50mm_Vertical.step',
    '${KICAD7_3DMODEL_DIR}/Fuse.3dshapes/FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165.wrl': '${KICAD7_3DMODEL_DIR}/Fuse.3dshapes/Fuseholder_Blade_Mini_Keystone_3568.step',
}
direct_board = ROOT / "design/D8-2L/MAIN_POWER/MAIN_POWER.kicad_pcb"
files = [BOARD, direct_board,
         BOARD.parent / 'UMI_D2.pretty/JST_VH_B2P-VH_1x02_P3.96mm_Vertical.kicad_mod',
         BOARD.parent / 'UMI_D2.pretty/FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165.kicad_mod',
         direct_board.parent / 'UMI_D2.pretty/JST_VH_B2P-VH_1x02_P3.96mm_Vertical.kicad_mod',
         direct_board.parent / 'UMI_D2.pretty/FuseHolder_Blade_ATO_Littelfuse_FLR_178.6165.kicad_mod']
for path in files:
    text = path.read_text(encoding='utf-8')
    for source, target in replacements.items():
        text = text.replace(source, target)
    path.write_text(text, encoding='utf-8')
print('Assigned STEP proxy models for J1, J2-J6, and F1-F5')
