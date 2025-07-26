@echo off
echo Starting MyVoiceTranslate Setup...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo Python found. Checking version...
python -c "import sys; print(f'Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo.
echo Installing requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Install OpenVoice separately
echo.
echo Setting up OpenVoice...
echo Note: OpenVoice requires manual installation from GitHub
echo.
echo Please run the following commands manually after this setup:
echo 1. git clone https://github.com/myshell-ai/OpenVoice.git
echo 2. cd OpenVoice
echo 3. pip install -e .
echo.
echo For now, the app will use mock voice cloning functionality.
echo.

REM Run setup script
echo.
echo Running setup script...
python setup.py

echo.
echo Setup complete! 
echo.
echo To start the application:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the app: streamlit run app.py
echo.
pause
