@echo off
echo ========================================
echo   AI Data Analyst - Starting Server
echo ========================================
echo.
echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting Flask server...
echo.
python app_final.py
pause
