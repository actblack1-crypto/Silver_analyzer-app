SILVER ANALYZER — COMPLETE PROJECT
==================================

This is a completed SLV-focused Streamlit dashboard. The source was reconstructed
from the code excerpt supplied in chat, including the missing chart/dashboard end.

RUN FROM PYTHON
---------------
1. Install Python 3.10 or newer from https://www.python.org/downloads/.
2. Open this folder in Command Prompt.
3. Run: py -m pip install -r requirements.txt
4. Run: py -m streamlit run silver_analyzer.py

BUILD A WINDOWS DESKTOP APP
---------------------------
1. Use a Windows 10/11 computer with Python 3.10 or newer installed.
2. Double-click build_windows.bat.
3. Wait for PyInstaller to finish.
4. Run dist\SilverAnalyzer\SilverAnalyzer.exe.
5. The app opens the dashboard in your default web browser. Leave the app's
   console window open while using it.
6. To move the app to another Windows computer, copy the ENTIRE
   dist\SilverAnalyzer folder, not just the EXE.

IMPORTANT BUILD NOTE
--------------------
A Windows EXE must be built on Windows. This ZIP contains the source and Windows
build script; it does not contain a prebuilt EXE. The build script downloads
Python dependencies and therefore needs internet access.

FEATURES
--------
- SLV default ticker; ticker can be changed in the sidebar
- Historical periods from one month through maximum available history
- Candlestick price chart, volume and RSI panel
- SMA 20/50/200, EMA 12/26, MACD, Bollinger Bands, ATR and volatility
- Recent historical data table and CSV export
- Five-minute data cache and manual refresh

DATA / FINANCIAL DISCLAIMER
---------------------------
Market data is fetched from Yahoo Finance through yfinance and requires internet.
Provider data may be delayed, incomplete, or unavailable. SLV is an ETF and may
not track spot silver exactly. The app is educational, not financial advice,
and does not connect to Robinhood or place trades.
