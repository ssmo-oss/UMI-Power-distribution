# Official KiCad 10.0.6 export command reference for this task

All commands below were inspected with `--help` through `validation_cli_controlled.py`. Help probes returned exit 0. Actual exports require coordinating-agent authorization and are not implied by this reference.

Use absolute paths for OUT and BOARD. Wrap every actual invocation with the controlled runner; stop on crashes instead of retrying. Preserve a source snapshot and its hashes. Always inspect generated outputs; successful export does not mean electrical or manufacturing validation passed.

## Board review

Combined SVG:

```
pcb export svg --mode-single --fit-page-to-board --exclude-drawing-sheet --layers F.Cu,F.SilkS,F.Mask,Edge.Cuts --check-zones --output OUT.svg BOARD.kicad_pcb
```

Individual copper-layer SVGs with shared outline:

```
pcb export svg --mode-multi --fit-page-to-board --exclude-drawing-sheet --layers F.Cu,In1.Cu,In2.Cu,B.Cu --common-layers Edge.Cuts --check-zones --output OUTPUT_DIRECTORY BOARD.kicad_pcb
```

PDF copper/assembly review:

```
pcb export pdf --mode-multipage --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,F.Fab,Edge.Cuts --common-layers Edge.Cuts --check-zones --output OUT.pdf BOARD.kicad_pcb
```

In single mode, `--output` is a full file path and common layers do not apply. In SVG multi mode, output is a directory. SVG `--fit-page-to-board` avoids a large blank page. PDF supports `--scale 0` for autoscale. `--check-zones` explicitly checks/refills zones for output. A DRC-only in-memory refill does not persist zone polygons for a separate export process.

3D PNG review:

```
pcb render --side top --width 1600 --height 900 --quality basic --output OUT.png BOARD.kicad_pcb
```

Custom footprints lacking models will appear without their component bodies; 3D render is not a complete mechanical clearance check. The tool supports `--rotate X,Y,Z`, `--perspective`, and optional stackup colours.

## Future manufacturing output (not yet authorized/run)

Gerber output needs an explicit layer list for the intended stackup; example four-layer list:

```
pcb export gerbers --layers F.Cu,In1.Cu,In2.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,F.Paste,B.Paste,Edge.Cuts --check-zones --output OUTPUT_DIRECTORY BOARD.kicad_pcb
```

X2/netlist attributes are enabled unless explicitly disabled. Coordinate precision defaults to six decimal places. Default Protel extensions are supported. No outline repetition on copper layers should be added accidentally. Keep the selected drill origin consistent with Gerbers and placement.

```
pcb export drill --format excellon --drill-origin absolute --excellon-units mm --excellon-zeros-format decimal --excellon-separate-th --generate-map --map-format pdf --generate-report --output OUTPUT_DIRECTORY BOARD.kicad_pcb
```

Position export for supplier-assembled SMT parts:

```
pcb export pos --format csv --units mm --side both --smd-only --exclude-fp-th --exclude-dnp --output OUT.csv BOARD.kicad_pcb
```

Review every footprint's SMD/through-hole attributes. Thermal pad soldering and through-hole pins affect filtering. Native KiCad placement CSV is not automatically supplier-specific CPL; map headers/rotations and review against assembly preview.

Native schematic BOM:

```
sch export bom --fields Reference,Value,Footprint,MPN,QUANTITY --labels Reference,Value,Footprint,MPN,Quantity --group-by MPN,Value,Footprint --exclude-dnp --output OUT.csv SCHEMATIC.kicad_sch
```

Manufacturer part numbers still require procurement/availability checks. The CLI does not invent LCSC/JLC part identifiers or assembly availability.

## Required evidence before release

Genuine final ERC and DRC with actual project rules, copper connectivity and schematic parity, BOM/MPN and placement reconciliation, exported CAM/drill visual inspection, board stackup/order constraints, and unresolved electrical/thermal review disposition. Prototype thermal and fault testing remains separate from CAD validation.
