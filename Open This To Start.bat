@echo off
echo Installing required Python libraries...

:: Install external Python libraries
pip install pystyle psutil

:: Clear the console
cls

echo Launching Roblox Cleaner...
python spoofermain.py

:: Pause to keep the console window open
pause
