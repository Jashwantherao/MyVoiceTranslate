@echo off
echo Starting MyVoiceTranslate Application...
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if required packages are installed
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Streamlit not installed
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting Streamlit application...
echo.
echo The application will open in your default browser.
echo If it doesn't open automatically, go to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run app.py

pause
