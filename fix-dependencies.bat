@echo off
echo Installing Python dependencies...
cd C:\Users\Administrator\Documents\Github\plex-toolbox\backend

REM Create virtual environment if it doesn't exist
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment and install dependencies
echo Activating virtual environment...
call venv\Scripts\activate

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Done! Now run:
echo   venv\Scripts\activate
echo   python migrate_integrations.py