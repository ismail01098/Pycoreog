@echo off
REM Farmers First - Simple Startup Script for Windows

echo.
echo ███████████████████████████████████████████████████████████
echo ███ Farmers First - Web Application Startup
echo ███████████████████████████████████████████████████████████
echo.

REM Check if virtual environment exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting Flask server...
echo.
echo Server will run at: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

python app.py

pause
