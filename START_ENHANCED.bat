@echo off
echo ========================================
echo Starting ENHANCED AI Data Analyst
echo 15-Stage Analysis with AI Insights
echo ========================================
echo.
echo Stopping any running Flask apps...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting enhanced app on port 5000...
start http://localhost:5000
python app_enhanced.py
pause
