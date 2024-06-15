@echo off

:: Check for Python 3 and pip installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python 3 could not be found. Please install Python 3.
    exit /b 1
)

where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo pip could not be found. Please install pip.
    exit /b 1
)

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate

:: Upgrade pip
pip install --upgrade pip

:: Install required dependencies
pip install -r requirements.txt

echo Setup complete. To run the application, use 'venv\Scripts\activate' and then 'python game.py'.
pause
