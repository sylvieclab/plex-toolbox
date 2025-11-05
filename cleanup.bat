@echo off
echo ========================================
echo Plex Toolbox - Cleanup Script
echo ========================================
echo.
echo This will remove all installed dependencies and virtual environments.
echo You'll need to run setup-dev.bat again after this.
echo.
pause

cd /d "%~dp0"

echo.
echo Cleaning backend...
if exist "backend\venv\" (
    echo Removing Python virtual environment...
    rd /s /q "backend\venv"
)
if exist "backend\.env" (
    echo Removing backend .env file...
    del "backend\.env"
)
if exist "backend\plex_toolbox.db" (
    echo Removing SQLite database...
    del "backend\plex_toolbox.db"
)
if exist "backend\logs\" (
    echo Removing log files...
    rd /s /q "backend\logs"
)

echo.
echo Cleaning frontend...
if exist "frontend\node_modules\" (
    echo Removing node_modules...
    rd /s /q "frontend\node_modules"
)
if exist "frontend\.env" (
    echo Removing frontend .env file...
    del "frontend\.env"
)
if exist "frontend\build\" (
    echo Removing build directory...
    rd /s /q "frontend\build"
)

echo.
echo ========================================
echo Cleanup Complete!
echo ========================================
echo.
echo Run setup-dev.bat to set up again.
echo.
pause
