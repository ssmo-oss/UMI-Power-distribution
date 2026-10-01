"""Bring the direct-solder MAIN schematic's six mechanical holes in sync."""

from pathlib import Path
import re

from create_d8_main import dump_sexpr, parse_sexpr

ROOT = Path(__file__).resolve().parents[1]
DIRECT = ROOT / "design/D8-2L/MAIN_POWER/MAIN_POWER.kicad_sch"
FASTON = ROOT / "design/D8-2L-FASTON/MAIN_POWER/MAIN_POWER.kicad_sch"


def balanced_end(text, start):
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        ch = text[pos]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("Unbalanced schematic S-expression")


def matched_blocks(text, pattern):
    blocks = []
    for match in re.finditer(pattern, text):
        start = match.start()
        end = balanced_end(text, start)
        blocks.append((start, end, text[start:end]))
    return blocks


def reference(block):
    found = re.search(r'\(reference\s+"(H[1-6])"\)', block)
    return found.group(1) if found else None


direct_text = DIRECT.read_text(encoding="utf-8")
faston_text = FASTON.read_text(encoding="utf-8")
direct_root = re.search(r'\(kicad_sch\s+\(version\s+\d+\)\s+\(generator\s+"[^"]+"\)\s+\(uuid\s+"([^"]+)"\)', direct_text).group(1)
faston_root = re.search(r'\(kicad_sch\s+\(version\s+\d+\)\s+\(generator\s+"[^"]+"\)\s+\(uuid\s+"([^"]+)"\)', faston_text).group(1)

direct_by_ref = {reference(block): (start, end, block) for start, end, block in matched_blocks(direct_text, r"\(symbol\s+\(lib_id") if reference(block)}
faston_by_ref = {reference(block): block for _, _, block in matched_blocks(faston_text, r"\(symbol\s+\(lib_id") if reference(block)}

# Copy the six complete mechanical instances, which keeps all symbol fields and
# footprint properties consistent with the FASTON schematic's resolved records.
instance_replacements = []
for ref in (f"H{i}" for i in range(1, 7)):
    block = faston_by_ref[ref].replace(f'"{faston_root}"', f'"{direct_root}"')
    if ref in direct_by_ref:
        start, end, _ = direct_by_ref[ref]
        instance_replacements.append((start, end, block))
    else:
        instance_replacements.append((None, None, block))
for start, end, block in sorted((item for item in instance_replacements if item[0] is not None), reverse=True):
    direct_text = direct_text[:start] + block + direct_text[end:]
extras = [block for start, _, block in instance_replacements if start is None]
direct_text = direct_text.rstrip()
assert direct_text.endswith(")")
direct_text = direct_text[:-1] + "\n" + "\n".join(extras) + "\n)\n"

DIRECT.write_text(direct_text, encoding="utf-8")

# The board holes carry a non-purchasable MPN field, and their Value matches
# the mechanical symbol value used by the schematic.
board_path = ROOT / "design/D8-2L/MAIN_POWER/MAIN_POWER.kicad_pcb"
board = parse_sexpr(board_path.read_text(encoding="utf-8"))
for node in board[1:]:
    if not isinstance(node, list) or not node or node[0] != "footprint":
        continue
    ref_prop = next((p for p in node if isinstance(p, list) and p[:2] == ["property", '"Reference"']), None)
    if not ref_prop or ref_prop[2].strip('"') not in {f"H{i}" for i in range(1, 7)}:
        continue
    at = next((p for p in node if isinstance(p, list) and p and p[0] == "at"), None)
    x, y = at[1], at[2]
    value_prop = next((p for p in node if isinstance(p, list) and p[:2] == ["property", '"Value"']), None)
    if value_prop:
        value_prop[2] = '"DXF 3.5mm NPTH"'
    if not any(isinstance(p, list) and p[:2] == ["property", '"MPN"'] for p in node):
        node.append(["property", '"MPN"', '"MECHANICAL - NO PURCHASE"', ["at", x, y, "0"],
                     ["effects", ["font", ["size", "1", "1"]], ["hide", "yes"]]])
board_path.write_text(dump_sexpr(board) + "\n", encoding="utf-8")
print("Updated direct-solder schematic and PCB mechanical-hole records for H1-H6")
