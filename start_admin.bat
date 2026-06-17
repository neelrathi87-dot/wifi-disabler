@echo off
setlocal

:: net session requires ACTUAL UAC elevation to succeed.
:: Being "in" the admin group is not enough — this forces true elevation.
net session >nul 2>&1
if %errorLevel% == 0 goto :RUN

:: --- Not elevated: re-launch self with UAC prompt ---
echo Set UAC = CreateObject("Shell.Application") > "%TEMP%\elev.vbs"
echo UAC.ShellExecute "%~s0", "", "%~dps0", "runas", 1 >> "%TEMP%\elev.vbs"
wscript "%TEMP%\elev.vbs"
del /f /q "%TEMP%\elev.vbs" 2>nul
exit /b

:: --- Truly elevated from here ---
:RUN
cd /d "%~dp0"
echo.
echo  ====================================================
echo   Desactivateur - Serveur admin demarre
echo   Ouvrez: http://localhost:5000
echo  ====================================================
echo.
start "" "http://localhost:5000"
"C:\Users\neeln\AppData\Local\Programs\Python\Python312\python.exe" server.py
pause
