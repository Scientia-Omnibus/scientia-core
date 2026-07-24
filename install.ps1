#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

$App = "scientia-core"
$LocalBin = "$env:USERPROFILE\.local\bin"
$GitVersion = "2.47.1"
$GitUrl = "https://github.com/ryanwoodsmall/static-git/releases/download/v$GitVersion/git-win-x86_64-portable.zip"

function Info  { Write-Host ":: $_" -ForegroundColor Cyan }
function Ok    { Write-Host "==> $_" -ForegroundColor Green }
function Warn  { Write-Host "==> $_" -ForegroundColor Yellow }

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Warn "Git not found — installing MinGit to $LocalBin ..."
    [void](New-Item -ItemType Directory -Path $LocalBin -Force)
    $zip = "$env:TEMP\git-portable.zip"
    Info "Downloading git ..."
    curl.exe -# -fL $GitUrl -o $zip
    Info "Extracting ..."
    Expand-Archive -Path $zip -DestinationPath "$LocalBin\git" -Force
    $env:Path = "$LocalBin\git\cmd;$env:Path"
    Ok "Git installed ($(git --version))"
} else {
    Ok "Git already installed ($(git --version))"
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Warn "uv not found — installing ..."
    [void](New-Item -ItemType Directory -Path $LocalBin -Force)
    $env:Path = "$LocalBin;$env:Path"
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    & ([ScriptBlock]::Create((Invoke-WebRequest -Uri https://astral.sh/uv/install.ps1 -UseBasicParsing).Content)) -NoProfile:$true
    $env:Path = "$LocalBin;$env:Path"
    Ok "uv installed ($(uv --version))"
} else {
    Ok "uv already installed ($(uv --version))"
}

Info "Installing $App via uv ..."
uv tool install $App
Ok "$App installed! Run: $App"
