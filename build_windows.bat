@echo off
setlocal
cd /d "%~dp0"
echo Building Silver Analyzer for Windows...
py -m pip install --upgrade pip
if errorlevel 1 goto failed
py -m pip install -r requirements.txt
if errorlevel 1 goto failed
py -m PyInstaller --noconfirm --clean --onedir --name SilverAnalyzer --collect-all streamlit --collect-all plotly --collect-all ta --collect-all yfinance --collect-all pandas --collect-all numpy --add-data "silver_analyzer.py;." launcher.py
if errorlevel 1 goto failed
echo.
echo Build complete: dist\SilverAnalyzer\SilverAnalyzer.exe
echo Keep the entire SilverAnalyzer folder together when copying or sharing.
pause
exit /b 0
:failed
echo Build failed. Check the error messages above.
pause
exit /b 1
