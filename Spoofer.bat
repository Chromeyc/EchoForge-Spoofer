��&cls
@echo off
:: Check for Administrator Privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Add-Type -AssemblyName PresentationCore,PresentationFramework; [System.Windows.MessageBox]::Show('This script must be run as Administrator.','Administrator Required',[System.Windows.MessageBoxButton]::OK,[System.Windows.MessageBoxImage]::Warning)" 
    exit /b
)

:: Set up colors
color 0A
title Roblox Cleaner

:menu
cls
echo ==============================
echo          Roblox Cleaner
echo      Made By "admin_x2"
echo ==============================
echo.
echo 1. Start Cleaning
echo 2. Quit
echo 3. IP Change
echo.
set /p choice="Please choose an option: "

if "%choice%"=="1" goto start_cleaning
if "%choice%"=="2" goto quit
if "%choice%"=="3" goto ip_change
goto menu

:start_cleaning
cls
echo Starting cleaning process...

echo.
echo Deleting Roblox data in Local AppData...
timeout /t 2 >nul

:: Deleting the Roblox folder in Local AppData
if exist "%LocalAppData%\Roblox" (
    rmdir /S /Q "%LocalAppData%\Roblox"
    echo Roblox data in Local AppData deleted successfully.
) else (
    echo No Roblox data found in Local AppData.
)

echo.
echo Deleting .rbx files in LocalLow...
timeout /t 2 >nul

:: Deleting .rbx files in LocalLow
for /r "%LocalAppData%\..\LocalLow" %%f in (*.rbx) do (
    del /f /q "%%f"
)

echo .rbx files in LocalLow deleted successfully.
echo.

:: Prompt to reinstall Roblox
set /p reinstall="Would you like to reinstall Roblox? Type 1 for Yes, Type 2 for No: "
if "%reinstall%"=="1" goto download_roblox
if "%reinstall%"=="2" goto end_cleaning
goto start_cleaning

:download_roblox
cls
echo Downloading Roblox installer...
timeout /t 2 >nul

:: Generate a random file name and download location
set "randomfilename=RobloxInstaller_%random%.exe"
set "downloadpath=%userprofile%\Documents\%randomfilename%"

:: Download the Roblox installer
powershell -Command "Invoke-WebRequest -Uri 'https://www.roblox.com/download/client?os=win' -OutFile '%downloadpath%'"

echo.
echo Download complete! Installing Roblox...
timeout /t 2 >nul

:: Launch the installer and wait until it closes
start /wait "" "%downloadpath%"

echo.
echo Installation completed! The program will now close.
timeout /t 3 >nul
exit

:end_cleaning
echo.
echo Cleaning process complete! The program will close in 3 seconds...
timeout /t 3 >nul
exit

:quit
echo Exiting the program...
timeout /t 1 >nul
exit

:ip_change
cls
echo IP Change option selected.
echo.

:: Generating Random MAC Address
echo Generating random MAC Address...
setlocal enabledelayedexpansion
set "hexchars=0123456789ABCDEF"
set "newmac="

for /l %%i in (1,1,12) do (
    set /a "rand=!random! %% 16"
    for /f %%h in ('echo !rand!') do (
        set "newmac=!newmac!!hexchars:~%%h,1!"
        if %%i==2 set "newmac=!newmac!:"
        if %%i==4 set "newmac=!newmac!:"
        if %%i==6 set "newmac=!newmac!:"
        if %%i==8 set "newmac=!newmac!:"
        if %%i==10 set "newmac=!newmac!:"
    )
)

echo Generated MAC Address: !newmac!
echo.

:: Getting Network Adapter
set "adapter="
for /f "tokens=2 delims=:" %%a in ('getmac /v /fo list ^| findstr "Physical"') do (
    set adapter=%%a
)
set adapter=!adapter: =!

:: Changing MAC Address
echo Adapter found: !adapter!
echo Disabling the adapter...
netsh interface set interface name="Ethernet" admin=disable

reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}\0001" /v "NetworkAddress" /d !newmac! /f >nul

echo Enabling the adapter...
netsh interface set interface name="Ethernet" admin=enable

echo MAC Address changed to: !newmac!
echo.

:: Releasing and Renewing IP Address
echo Releasing and Renewing IP Address...
ipconfig /release
ipconfig /renew
echo IP Address changed successfully!
echo.

echo Done! The program will return to the main menu in 3 seconds...
timeout /t 3 >nul
goto menu
