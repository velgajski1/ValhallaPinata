@echo off
echo Installing missing dependencies in virtual environment...
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing onnxruntime...
pip install onnxruntime

echo Installing rembg...
pip install rembg

echo Installing other dependencies...
pip install pillow tqdm

echo.
echo Testing installations...
python test_deps.py

echo.
echo Done!
pause