@echo off
echo Installing Python dependencies in virtual environment...
echo.

echo Step 1: Activating virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Creating one...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated

echo.
echo Step 2: Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

echo.
echo Step 3: Installing core dependencies...
pip install onnxruntime
if %errorlevel% neq 0 (
    echo ❌ Failed to install onnxruntime
    pause
    exit /b 1
)

echo.
echo Step 4: Installing rembg and other dependencies...
pip install rembg watchdog pillow tqdm
if %errorlevel% neq 0 (
    echo ❌ Failed to install rembg or other dependencies
    pause
    exit /b 1
)

echo.
echo Step 5: Verifying installation...
python -c "import onnxruntime; print('✅ onnxruntime version:', onnxruntime.__version__)"
if %errorlevel% neq 0 (
    echo ❌ onnxruntime verification failed
    pause
    exit /b 1
)

python -c "import rembg; print('✅ rembg version:', rembg.__version__)"
if %errorlevel% neq 0 (
    echo ❌ rembg verification failed
    pause
    exit /b 1
)

echo.
echo ✅ All dependencies installed successfully in virtual environment!
echo.
echo To run the scripts, use:
echo   .venv\Scripts\python.exe watch_and_build.py
echo   .venv\Scripts\python.exe force_rebuild.py
echo   .venv\Scripts\python.exe test_dependencies.py
echo.
echo Or activate the environment first:
echo   .venv\Scripts\activate.bat
echo   python watch_and_build.py
pause
