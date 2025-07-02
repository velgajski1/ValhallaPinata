@echo off
echo Starting SpriteBuilder in watch mode...
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Please run install_requirements.bat first.
    pause
    exit /b 1
)

call .venv\Scripts\activate.bat
python watch_and_build.py