"""Create the corrected underside fuseholder envelope for the FASTON board."""

from pathlib import Path

from create_main_model_envelopes import write_assembly


ROOT = Path(__file__).resolve().parents[1]
FASTON = ROOT / "design/D8-2L-FASTON/MAIN_POWER"
MODEL_NAME = "Littelfuse_FLR_1786165_BACKSIDE_ENVELOPE"


def main():
    # KiCad mirrors model Y for footprints on B.Cu. Mirror the local envelope
    # through the footprint origin so the body stays over the pad pattern.
    write_assembly(
        MODEL_NAME,
        "Dimensioned Littelfuse FLR ATO holder envelope aligned for B.Cu; simplified body, not vendor detail",
        [(-3.6, -4.25, 0, 16.4, 1.75, 21.6)],
    )
    board = FASTON / "MAIN_POWER.kicad_pcb"
    text = board.read_text(encoding="utf-8")
    text = text.replace(
        "${KIPRJMOD}/3d/Littelfuse_FLR_1786165_ENVELOPE.step",
        f"${{KIPRJMOD}}/3d/{MODEL_NAME}.step",
    )
    board.write_text(text, encoding="utf-8")
    print(f"Updated only the FASTON board fuseholder models: {MODEL_NAME}.step")


if __name__ == "__main__":
    main()
