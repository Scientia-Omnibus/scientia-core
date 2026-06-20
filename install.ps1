#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$AppName = "scientia-core"
$AppPyPI = "scientia-core"

function Write-Info  { Write-Host ":: $_" -ForegroundColor Cyan }
function Write-Ok    { Write-Host "==> $_" -ForegroundColor Green }
function Write-Warn  { Write-Host "==> $_" -ForegroundColor Yellow }

function Install-Git-IfMissing {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $ver = git --version
        Write-Ok "Git already installed ($ver)"
        return
    }
    Write-Warn "Git not found — installing via winget..."
    $result = winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Git installation failed. Install manually: https://git-scm.com"
        exit 1
    }
    # Refresh PATH so git is available in this session
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "Error: Git installed but not found in PATH. Restart your terminal and try again."
        exit 1
    }
    $ver = git --version
    Write-Ok "Git installed ($ver)"
}

function Install-UV-IfMissing {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $ver = uv --version
        Write-Ok "uv already installed ($ver)"
        return
    }
    Write-Warn "uv not found — installing..."
    $result = & powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" 2>&1
    # uv adds itself to PATH but might not be available immediately in this session
    $env:Path = [System.Environment]::GetEnvironmentVariable("USERPROFILE") + "\.local\bin;" + $env:Path
    $env:Path = [System.Environment]::GetEnvironmentVariable("USERPROFILE") + "\.cargo\bin;" + $env:Path
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Host "Error: uv installation failed. Restart your terminal and try again, or install manually: https://docs.astral.sh/uv"
        exit 1
    }
    $ver = uv --version
    Write-Ok "uv installed ($ver)"
}

function Main {
    Write-Info "Installing $AppName..."
    ""
    Install-Git-IfMissing
    Install-UV-IfMissing
    Write-Info "Installing $AppName via uv..."
    uv tool install $AppPyPI
    ""
    Write-Ok "$AppName installed! Run: $AppName"
}

Main
