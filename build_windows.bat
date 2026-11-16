@echo off
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\pyinstaller --noconsole --onefile main.py
echo.
echo Build selesai. Lihat folder dist\main.exe
pause
