@echo off
echo Installing OpenVoice for MyVoiceTranslate...
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    if exist "venv\Scripts\activate.bat" (
        echo Activating virtual environment...
        call venv\Scripts\activate.bat
    ) else (
        echo Error: Virtual environment not found
        echo Please run setup.bat first
        pause
        exit /b 1
    )
)

echo Current directory: %CD%
echo.

REM Create models directory if it doesn't exist
if not exist "models" (
    mkdir models
    echo Created models directory
)

REM Check if OpenVoice directory already exists
if exist "OpenVoice" (
    echo OpenVoice directory already exists
    echo Do you want to update it? (y/n)
    set /p choice=
    if /i "%choice%"=="y" (
        echo Updating OpenVoice...
        cd OpenVoice
        git pull
        cd ..
    ) else (
        echo Skipping OpenVoice download
        goto install
    )
) else (
    REM Clone OpenVoice repository
    echo Cloning OpenVoice repository...
    git clone https://github.com/myshell-ai/OpenVoice.git
    if %errorlevel% neq 0 (
        echo Error: Failed to clone OpenVoice repository
        echo Please check your internet connection and git installation
        pause
        exit /b 1
    )
)

:install
REM Install OpenVoice
echo.
echo Installing OpenVoice package...
cd OpenVoice
pip install -e .
if %errorlevel% neq 0 (
    echo Error: Failed to install OpenVoice
    echo You may need to install additional dependencies
    cd ..
    pause
    exit /b 1
)

cd ..

REM Download checkpoints (if available)
echo.
echo Checking for OpenVoice checkpoints...
if exist "OpenVoice\checkpoints" (
    echo Checkpoints directory found
) else (
    echo.
    echo Important: You need to download OpenVoice checkpoints manually
    echo Please follow the instructions in the OpenVoice README:
    echo https://github.com/myshell-ai/OpenVoice#quick-start
    echo.
)

echo.
echo OpenVoice installation completed!
echo.
echo Next steps:
echo 1. Download required checkpoints (see OpenVoice documentation)
echo 2. Update config.py to set mock_voice_cloning = False
echo 3. Run the application: streamlit run app.py
echo.
pause
