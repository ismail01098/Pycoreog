#!/usr/bin/env pwsh
<#
.SYNOPSIS
Farmers First - Web Application Startup Script for PowerShell

.DESCRIPTION
This script starts the Flask development server for the Farmers First web application.

.EXAMPLE
.\START.ps1
#>

Write-Host "
███████████████████████████████████████████████████████████
███ Farmers First - Web Application Startup
███████████████████████████████████████████████████████████
" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv .venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Starting Flask server..." -ForegroundColor Cyan
Write-Host ""
Write-Host "Server will run at: http://localhost:5000" -ForegroundColor Yellow
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py

Read-Host "Press Enter to exit"
