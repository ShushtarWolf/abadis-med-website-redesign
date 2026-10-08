# Full Abadis site test suite (Windows). Requires Node 18+, Python 3, and deps from npm i.
$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "../..")
$env:BASE = if ($env:BASE) { $env:BASE } else { "http://127.0.0.1:8080" }
$env:TEST_SHA = (git -C $Root rev-parse HEAD).Trim()

# Prefer bash if available (Git Bash / WSL); else run pieces via npm scripts.
$bash = Get-Command bash -ErrorAction SilentlyContinue
if ($bash) {
  & bash (Join-Path $PSScriptRoot "run-all.sh")
  exit $LASTEXITCODE
}

Write-Host "bash not found; starting server + playwright only. Run linkinator/lighthouse manually if needed."
$out = Join-Path $PSScriptRoot "out"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$server = Start-Process -PassThru -WindowStyle Hidden -FilePath "python" -ArgumentList @("-m","http.server","8080","--directory",(Join-Path $Root "site"))
try {
  Push-Location $PSScriptRoot
  npx playwright test site.spec.mjs --reporter=list
  node .\write-report.mjs
} finally {
  Stop-Process -Id $server.Id -Force -ErrorAction SilentlyContinue
  Pop-Location
}
