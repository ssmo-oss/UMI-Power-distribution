$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$kicadCli = Join-Path $env:ProgramFiles 'KiCad\10.0\bin\kicad-cli.exe'
if (-not (Test-Path -LiteralPath $kicadCli)) {
    throw "KiCad CLI not found at $kicadCli"
}

$boards = @(
    @{ Input = 'design/D8-2L/MAIN_POWER/MAIN_POWER.kicad_pcb'; Output = 'design/D8-2L/MAIN_POWER/MAIN_POWER_D8.step' },
    @{ Input = 'design/D8-2L-FASTON/MAIN_POWER/MAIN_POWER.kicad_pcb'; Output = 'design/D8-2L-FASTON/MAIN_POWER/MAIN_POWER_D8_FASTON.step' }
)
foreach ($board in $boards) {
    $inputPath = Join-Path $repo $board.Input
    $outputPath = Join-Path $repo $board.Output
    & $kicadCli pcb export step --force --include-soldermask --output $outputPath $inputPath
    if ($LASTEXITCODE -ne 0) {
        throw "STEP export failed for $inputPath (exit $LASTEXITCODE)"
    }
    $stepData = [System.IO.File]::ReadAllText($outputPath, [System.Text.Encoding]::ASCII)
    $stepData = [regex]::Replace($stepData, '(?m)[\t ]+$', '')
    [System.IO.File]::WriteAllText($outputPath, $stepData, [System.Text.Encoding]::ASCII)
}
