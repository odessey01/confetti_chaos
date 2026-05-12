param(
    [switch]$SkipTests,
    [switch]$DemoMode
)

$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot
$demoFlagDir = Join-Path $PSScriptRoot "build_flags"
$demoFlagPath = Join-Path $demoFlagDir "demo_mode.flag"

# Ensure stale marker does not leak into non-demo builds.
if (Test-Path $demoFlagPath) {
    Remove-Item -Force $demoFlagPath
}
if ($DemoMode) {
    New-Item -ItemType Directory -Path $demoFlagDir -Force | Out-Null
    Set-Content -Path $demoFlagPath -Value "demo_mode=true" -Encoding utf8
    Write-Host "Demo mode marker enabled for this build."
}

if (-not $SkipTests) {
    Write-Host "Running unit tests..."
    python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw "Unit tests failed." }
}

Write-Host "Cleaning previous build artifacts..."
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }

Write-Host "Building standalone executable..."
python -m PyInstaller --noconfirm --clean confetti-chaos.spec
if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

# Cleanup temporary marker after packaging completes.
if (Test-Path $demoFlagPath) {
    Remove-Item -Force $demoFlagPath
}
if ((Test-Path $demoFlagDir) -and -not (Get-ChildItem -Path $demoFlagDir -Force | Select-Object -First 1)) {
    Remove-Item -Force $demoFlagDir
}

Write-Host "Build complete. Output expected at .\\dist\\confetti-chaos.exe"
