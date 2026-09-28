# Historical engineering scripts

These are development and audit scripts preserved for traceability, not an installed or supported build pipeline. They were written against a Windows working directory with `work/`, `outputs/UMI_D2` through `outputs/UMI_D6`, KiCad 10 and various temporary dependencies. Many have absolute local paths and top-level mutations. Do not run them indiscriminately or against the only copy of a design.

The editable projects in `design/D6` are authoritative. Generated current manufacturing files are already included. No Python runtimes, dependency environments, credentials or browser caches are bundled.

STEP generation used `build_simple_steps.py`, text parsing helpers in `design_d2.py` and `cadquery-ocp-novtk==8.0.1.0.0`. Original native board-only STEP inputs are in `../step-native-inputs/`. The script adds the documented proxies and corrects only the native bare model Z thickness. Adapt its source/output/delivery paths before execution. It is not necessary to run it to use the delivered STEP files.

Native validation used `validation_cli_controlled.py` with official KiCad CLI commands, isolated configuration and fault handling. Earlier bundled KiCad Python/CLI executions crashed on the source workstation; review the wrapper and command scope before any rerun. Original verification logs retain provenance paths that may not exist on your computer.
