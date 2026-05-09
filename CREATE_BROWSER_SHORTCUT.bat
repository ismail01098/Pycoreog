@echo off
setlocal enabledelayedexpansion

REM Create a shortcut for quick browser access
REM This script creates a shortcut that opens the app in the default browser

echo Creating browser shortcut...

set SCRIPT_DIR=%~dp0
set TARGET_URL=http://localhost:5000
set SHORTCUT_PATH=%SCRIPT_DIR%OPEN_IN_BROWSER.vbs

REM Create VBScript to open browser
(
echo ' Farmers First - Open in Browser
echo Set oShell = CreateObject("WScript.Shell"^)
echo oShell.Run "http://localhost:5000"
) > "%SHORTCUT_PATH%"

if exist "%SHORTCUT_PATH%" (
    echo Shortcut created: OPEN_IN_BROWSER.vbs
    echo Double-click it to open the app in your browser
    echo.
    echo NOTE: Make sure Flask server is running first!
    echo.
) else (
    echo Failed to create shortcut
)

pause
