# KiCad verification and fabrication workflow findings

25 September 2026. Scope: KiCad 10.0.6 GUI plus official kicad-python 0.8.0 through the separate Codex Python runtime. No kicad-cli, KiCad bundled Python, GUI launches, or user configuration changes were performed by this investigation.

## What can be independently verified now

`validation_text_audit.py BOARD.kicad_pcb --out REPORT.json` independently parses the saved PCB and its sibling schematic. It does not import the design generator. It compares each symbol's actual wire-and-label net to the placed footprint pad net, checks the symbol/footprint UUID binding, and detects missing physical pads, conflicting repeated pad numbers, duplicate references and duplicate UUIDs. It supports the flat UMI schematics with unrotated custom symbols; it rejects unsupported sheets/buses/mirrored or rotated symbols. It does not validate pin functions or manufacturer pin numbering.

The existing D2 USB files passed this comparison: 32 symbols, 32 footprints, 122 logical pins, 124 physical copper pads, no net mismatches or UUID failures. That board still has only 26 tracks, no vias and no zones. The pass proves file consistency only.

`validation_ipc_audit.py --socket SOCKET --expected-board EXACT_FILENAME --out REPORT.json` uses KiCad's read-only `get_connected_items` for every pad. Union-find groups physical pads into copper-connected components per net. It rejects the connection if the loaded board name does not match. There are no hard-coded component counts. It does not launch KiCad, refill zones, save the board, or change anything in KiCad. The caller should fill zones in its controlled verification copy first, then run this audit. It records the serialized-board hash, KiCad version and time. At initial delivery this script has not been exercised against the temporary GUI endpoint because that editor was closed.

Physical copper groups remain separate even when two component pins may be internally common: that is deliberate. A designer must decide whether the layout needs external joining; the audit should not hide copper islands merely because pad numbers or internal functions match.

## Available API versus unsupported fabrication automation

The official [KiCad add-on developer documentation](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/) explicitly states:

- KiCad 9 and 10 IPC needs a running GUI.
- Plotting/exporting over IPC starts in KiCad 11.
- Schematic-editor IPC starts in KiCad 11.

Thus the `board_jobs.py` and protobuf export settings present in the installed Python client do **not** establish support in the running KiCad 10 server. The installed `Board` class has no DRC/plot/export job method. Using those newer protobuf commands against KiCad 10 is not a valid release strategy.

Supported and useful methods in the installed official client include `get_as_string`, `get_pads`, `get_tracks`, `get_vias`, `get_zones`, `get_footprints`, `get_connected_items`, `get_pad_shapes_as_polygons`, `get_bounding_box`, and `refill_zones`. The two last geometry calls can support further independent screens; none substitutes for full KiCad DRC.

`KiCad.run_action` exists but its official client docstring warns that it is unstable, intended for API developers, and may have unintended side effects. Opening a GUI DRC or plot dialog would still require a supported UI interaction route to configure, execute and retrieve results. Native UI automation is unavailable in this session. Consequently this is not a reliable unattended export mechanism.

## Instance selection

Official docs say default Windows named pipe is `api.sock`, with PID appended when occupied; observed behaviour in this session did not reliably expose the separately opened PCB editor. Root has already demonstrated a dedicated process TEMP/TMP directory produces a unique working endpoint. When using that method, always verify the connected board name before reads or edits. Do not assume an open editor window is the connected one.

## Release limits

The two audits can establish netlist consistency and copper connectivity independently of the generator. They cannot establish clearance, annular ring, mask sliver, solder paste, courtyard, edge clearance, creepage, thermal performance, switching behaviour, component orientation, circuit correctness, procurement validity or assembly capability.

Before calling any package ready to order, obtain genuine KiCad DRC and ERC results with actual configured rules; generate Gerber/drill outputs through a verified KiCad workflow; inspect those outputs in a CAM viewer; reconcile BOM and placement against exact orderable parts; and resolve electrical review findings. Electrical limits and thermal behaviour of these power boards still need prototype measurements. Under the present restriction against the previously crashing CLI/Python paths and without supported native UI access, unattended KiCad 10 fabrication export and full ERC/DRC have not been demonstrated. Do not fabricate replacement Gerbers with a custom writer and represent them as validated KiCad output.

## Existing alternative-runtime discovery

Read-only discovery also checked PATH, standard Program Files installation folders, the Windows uninstall registry, relevant services and the Downloads directory:

- `C:\Windows\system32\wsl.exe` exists, but `wsl.exe --list --verbose` explicitly reports that Windows Subsystem for Linux is **not installed**. There is no usable installed Linux distribution from this entry point.
- No Docker or Podman executable was found on PATH; no corresponding standard installation directory, installed-program record or service was found.
- No VMware or VirtualBox installed-program record or standard installation folder was found.
- The installed-program registry reports only KiCad 10.0.6 at `C:\Program Files\KiCad\10.0`. The only KiCad installer observed in Downloads is `kicad-10.0.6-x86_64.exe`, the same release.

This bounded discovery did not search every byte on every disk, but it found no existing supported Linux/container/alternate KiCad runtime that can be used immediately. No WSL, distribution, VM, container engine or other OS-level component was installed or configured. Installing an OS-level environment would be a separate environmental change, not an available fallback already present on this machine.

## Controlled Windows CLI version-only probe

Root subsequently authorized a narrowly scoped fresh CLI test with process-local Windows error handling and isolated configuration. This supersedes the earlier no-CLI restriction **for the version query only**.

[Microsoft SetErrorMode documentation](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-seterrormode) confirms child processes inherit the parent's error mode. [Process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags) confirms `CREATE_DEFAULT_ERROR_MODE` would disable this inheritance; the wrapper deliberately does not set that flag. `CREATE_NO_WINDOW` avoids opening a console window. `SEM_NOGPFAULTERRORBOX` suppresses invoking Windows Error Reporting; this is process-local, not a machine configuration change.

`validation_cli_probe.py` runs in separate Codex Python, sets and confirms process error mode `0x8003`, sets TEMP/TMP and KICAD_CONFIG_HOME beneath `work/validation_cli_env`, and runs only the installed official `kicad-cli.exe --version` with a 20-second timeout.

Result: exit code **0 / 0x0**, stdout **10.0.6**, empty stderr, completed in **0.906 seconds**. Machine-readable record: `work/validation_cli_env/version_probe.json`. No design load, DRC, ERC or export has been attempted by this probe. A version-only success does not establish that the previously failing design operations now work.

## Controlled PCB DRC now demonstrated

Root then authorized a read-only USB PCB DRC snapshot. `validation_cli_controlled.py` generalizes the same process-local error mode and isolated environment, without automatic retries. Only expressly authorized CLI operations should be invoked through it.

`pcb drc --help` completed with exit 0. The USB_POWER PCB/project were copied to `work/validation_cli_env/input`; DRC ran with JSON output, all severities, all track errors and `--exit-code-violations`. It did **not** use `--save-board`, `--refill-zones` or schematic parity.

The actual PCB DRC completed in **0.828 seconds**, exit **5**, empty stderr, and produced `work/validation_cli_env/usb_drc.json`: **49 violations and 102 unconnected items**. Exit 5 reflects the requested nonzero result for design violations, not a process crash. The breakdown was 36 footprint-library warnings, 5 silk overlaps, 5 silk-over-copper warnings, 2 silk-edge warnings and 1 courtyard overlap (J2/H3). The footprint-library warnings arise because this narrowly specified first snapshot copied only PCB/project, not the local library table and library. Future complete snapshots must include those dependencies.

This establishes a working official DRC path under controlled invocation; it supersedes the earlier conclusion that DRC was unavailable. It does not establish DRC pass, schematic ERC functionality or export functionality. Those need separately authorized scoped tests and actual results.

## Iterative DRC and ERC snapshots authorized and functioning

Root authorized continued controlled read-only DRC/ERC snapshots for both active projects, still without fabrication exports. `validation_snapshot.py` copies PCB, schematic, project, rule and local library dependencies, records UTC/mtime/SHA256 in `snapshot_manifest.json`, and rejects any file changed during copying. Validation outputs are kept separate from source designs.

- USB snapshot 02, **2026-09-25 22:24:02 UTC**: real ERC completed normally in 2.796 seconds, exit 5, with 189 violations (152 off-grid endpoints, 36 missing symbol-library warnings, one undriven VIN power-input error). DRC completed normally in 0.734 seconds, exit 5: 126 violations and 68 unconnected items. DRC breakdown: 77 dangling vias, 17 undersized drills relative to project minimum, 17 undersized via diameters, 5 silk overlaps, 5 silk-over-copper, 3 local footprint mismatches and 2 silk-edge warnings. Zones were not filled for that USB DRC. H3/J2 courtyard overlap was fixed by this revision.
- Main snapshot 01, **2026-09-25 22:24:15 UTC**: real DRC with in-memory zone refill (`--refill-zones`, without `--save-board`) completed normally in 0.828 seconds, exit 5: 4 warnings for the absent global MountingHole library and 99 unconnected items; no clearance/courtyard violations were returned. Real ERC completed normally in 0.406 seconds, exit 5: 257 violations (201 off-grid endpoints, 55 missing UMI symbol-library warnings, one undriven VIN power-input error).

Reports use names `usb_{drc,erc}_02.json` and `main_{drc,erc}_01.json` beneath `work/validation_cli_env`. These are historical snapshots while routing is ongoing, not final release checks. Normal completion with exit 5 demonstrates usable validators, never a clean design.

## USB schematic packaging: zero real ERC violations

`validation_schematic_package.py` provides `package_schematic(path, externally_driven_nets=())`. This separate helper normalizes generated flat schematic symbol/pin/wire locations to a 1.27 mm grid, preserves existing symbol/wire/label UUIDs, makes text 1 mm, writes the actual local UMI symbol library and library table, and adds stable-ID boardless power flags only on explicitly provided existing net names. It does not change PCB files or ignore rule checks.

On a controlled USB test copy, with power flags on `12V_PROTECTED` and `GND`, the independent text comparison still passed all 122 logical pins and UUID bindings. Official KiCad ERC then returned **exit 0, zero violations**, in **0.422 seconds**. Evidence: `work/validation_cli_env/usb_grid_erc.json`; test copy: `work/validation_cli_env/usb_grid_test`. This validates the helper on that snapshot. Root must invoke the helper in the production builder and rerun release checks after later circuitry changes.

Main snapshot 02 at **22:28:32 UTC** independently passed all **194 logical pins**, with **65 circuit symbols / 69 footprints / 232 physical copper pads**. Its main-specific schematic reflow and legitimate power flags yielded **zero official ERC violations, exit 0**, in **0.375 seconds**. DRC completed normally in 0.797 seconds with in-memory zone refill: 4 missing MountingHole library warnings and **137 unconnected items**, no clearance/courtyard violations returned. This revision includes the captured input eFuse circuit but still needs its routing. Evidence: `main_text_02.json`, `main_erc_02.json`, `main_drc_02.json` beneath `work/validation_cli_env`.

## USB completed copper connectivity and internal review exports

USB snapshot 03 could not load into DRC because a new graphic used undefined layer `F.Silkscreen`; KiCad returned a normal error code 3, not a crash. Root corrected it to canonical `F.SilkS`. ERC on snapshot 03 was clean and its schematic hash was unchanged in snapshot 04.

USB snapshot 04 at **22:33:08 UTC**: official DRC with in-memory refill returned **zero unconnected items and no clearance/electrical geometry errors**. Only **three footprint-library mismatch warnings** remained for rotated C1, C3 and R1. Root reported these already used actual rotation; incrementing text angles in snapshot 05 did not remove the mismatch. Exact cause was not established by this stream. Exit 5 correctly reflected these warnings. This is a major routing milestone but not a full clean release.

Root authorized internal visual review exports. Official `pcb export pdf --mode-multipage ... --check-zones` produced `usb_review_04.pdf` successfully (exit 0, 0.75 seconds), with filled copper polygons in the exported review. Official `pcb render` produced `usb_review_04_top.png` successfully (exit 0, 1.5 seconds). The PDF front-copper page was rasterized and inspected. The top 3D render was inspected; the module, USB connectors and some IC bodies are absent because their custom/local footprints do not have 3D models. The PNG came from the saved, unfilled snapshot and is a placement visual only. No Gerber, drill or supplier order package was generated by this stream.

Inspected exact export command syntax is in `work/validation_export_commands.md` and the corresponding `*_help.json` captures.

## Native schematic parity identified additional metadata/name issues

An additional official DRC run on USB snapshot 05 with `--schematic-parity` identified **164 parity issues**: 124 net conflicts, 36 missing MPN footprint fields and 4 mounting-hole BOM exclusion differences. Local schematic labels produce canonical names such as `/GND`, whereas the generated PCB used `GND`. Two explicitly unconnected pins also need KiCad's unique diagnostic net names (`unconnected-(U1-SW-Pad4)` and `unconnected-(U1-NC-Pad16)`) for native parity.

The earlier independent text audit checked logical label names and therefore did not establish native KiCad canonical name parity. Root/main agents were informed and are fixing this without changing intended topology. Final validation should include `--schematic-parity`. The text audit now accepts the exact KiCad-generated no-connect name when a pin is explicitly marked unconnected, but it remains complementary to the native parity check. Evidence: `usb_parity_05.json`.

USB snapshot 06 at **22:38:13 UTC** achieved **full official DRC pass** with all severities, all track errors, zone refill and schematic parity enabled: **zero violations, zero unconnected items, zero schematic parity issues, exit 0**. Independent 122-pin comparison also passed. ERC had only two label-scope warnings because power-flag labels were still local while circuit labels had become global. The packaging helper was updated so new power-flag labels follow the existing net's global/local scope; source rebuild and final ERC are pending. Evidence: `usb_drc_06.json`, `usb_erc_06.json`, `usb_text_06.json`.

## USB physical ESD revision 07 — all CAD checks clean

Root delegated the physical review changes to this stream. USB-only sections of `design_d2.py` and `route_usb_power.py` now produce an **80 × 50 mm board**, move the connector pin rows to y=47, place each ESD array immediately behind its connector, put the VBUS capacitor adjacent to the array, route connector signals through the ESD protection point before controller connections, use a direct **0.5 mm VBUS clamp-reference connection**, and provide an adjacent direct ground via for each array. Bottom mounting holes moved down with the enlarged outline. The root-provided exact D1 MPN `BZT52C12-7-F` is captured. Shared main-board helpers were preserved.

Snapshot 07 at **22:47:55 UTC** has **263 copper segments, 103 vias and 5 zones**. Genuine DRC with zone refill and schematic parity: **zero violations, zero unconnected items, zero parity issues, exit 0**. Genuine ERC: **zero violations, exit 0**. Independent 122-pin netlist/UUID comparison passed. Evidence: `usb_drc_07.json`, `usb_erc_07.json`, `usb_text_07.json`, and snapshot manifest under `work/validation_cli_env`.

Internal seven-layer PDF and top 3D PNG were regenerated successfully (`usb_review_07.pdf`, `usb_review_07_top.png`). The PNG was visually inspected, with ESD arrays now immediately behind connector pins and capacitors adjacent. Custom USB/module/limiter bodies still lack 3D models. The design remains ENGINEERING HOLD pending final electrical/thermal/procurement review and assembly/fabrication decisions; clean CAD checks alone are not prototype measurement evidence. No manufacturing exports were made.

## USB output-capacitance margin revision 09

Electrical review identified inadequate margin between the three-capacitor reference's approximately 78 µF typical effective capacitance and the converter's 75 µF minimum at 1 MHz. Root chose **five GRM32ER71A476ME15L 47 µF / 10 V X7R output capacitors** and no feed-forward capacitor because the TI table/body CFF guidance needs further reconciliation.

C13 and C14 are at (44,37) and (50,37) mm beside the buck/output-capacitor area, each with **four 5 V vias and four ground vias connected by 1.2 mm traces**. The existing low-inductance first row remains immediately next to the module. The added row joins the same inner 5 V plane and ground planes. Total nominal capacitance is 235 µF. Scaling the manufacturer's cited three-capacitor typical effective value gives approximately 130 µF, **not a guaranteed minimum**: actual DC bias at the configured output voltage, production tolerance, temperature and aging remain relevant. Bench startup, load-step/loop stability and capacitor temperature tests are required, particularly at both ports loaded and 40°C enclosure ambient.

Snapshot 08 ERC passed zero violations. After a C13 reference-text collision was corrected, snapshot 09 at **22:54:52 UTC** passed full native DRC/refill/parity with **zero violations, zero unconnected items and zero parity issues**. The schematic is identical between 08 and 09. Independent text validation also passed. Final source now has **38 footprints, 126 logical pins, 277 segments, 119 vias and 5 zones**. No manufacturing exports were generated; root will refill and save its final deliverable copy.

## Main snapshot05 — 2026-09-25 23:01 UTC
Stable 40-file snapshot, native KiCad 10 controlled subprocess validation completed normally. Initial relative-path invocation returned ordinary load error 3; corrected absolute paths (wrapper working directory differs). Final DRC child exit5 means violations, ERC exit0. No crash.

ERC0; schematic parity0; DRC108; unconnected3. Counts: clearance5, courtyard1, hole clearance3, shorts8, solder-mask bridges5, crossing1, dangling8, silk-over-copper36, silk-overlap41. Imported reference plus added distribution reduced unconnected92→3. Detailed non-silk and opens: `validation_cli_env/main_geometry_05.json`. Main design owner has exact UUID/position findings and is correcting routes; no validation-agent edits to design.

## Main snapshot06 — 2026-09-25 23:04 UTC
Native DRC process completed, exit5 with13violations and1unconnected; ERC0 andparity0. All snapshot05shorts, courtyard andsilkscreen findings resolved. Remaining:7clearances,1hole-to-hole,4danglingtracks,1danglingvia; F6inputpadapproach stillunconnected. Detailed work/validation_cli_env/main_geometry_06.json sentdesignowner. Low-current sense corridor may benefit narrower tracks instead of cascaded displacement; no designchanges byvalidationagent.

## Main snapshot07 — 2026-09-25 23:09 UTC
Native refill DRC/parity: zero errors, zero unconnected, zero parity issues. Three dangling-track warnings remain (VCC, FB_HIGH, HO imported option stubs); exact UUIDs delivered to main owner. ERC0. Source has explicit1.2mm four-layer2/1/1/2oz stack and0.15mm OPT corridor. These checks establish software rule/connectivity agreement; they do not qualify boost loop stability, thermal performance or assembly.
