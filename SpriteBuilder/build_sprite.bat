@echo off
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
set input=%1

if "%input%"=="" (
    echo ❌ Please provide a folder name. Example: build_sprite.bat myvideo
    exit /b 1
)

set framePath=tmp\%input%

REM Ensure frame path exists
if not exist "%framePath%" (
    echo ❌ Frame path "%framePath%" does not exist.
    exit /b 1
)

echo 🔍 Debug: Checking files in %framePath%
dir "%framePath%\*.png" /b

REM Check if there are any _no_bg.png frames
dir "%framePath%\*_no_bg.png" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ No *_no_bg.png frames found in "%framePath%".
    echo 🔍 Did you run remove_background_parallel.py on this folder?
    exit /b 1
)

echo ✅ Found *_no_bg.png files in %framePath%

echo 🧹 Cleaning up original PNG files (with background)...
for %%f in ("%framePath%\*.png") do (
    echo "%%f" | findstr /v "_no_bg.png" >nul
    if !errorlevel! equ 0 (
        del "%%f"
        echo   ✅ Removed: %%~nxf
    )
)

echo ✅ Done. All frames are ready in %framePath% with backgrounds removed.
