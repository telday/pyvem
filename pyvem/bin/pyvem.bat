@echo off
Rem Main entry point for the pyvem application.

if "%PYVEMHOME%" == "" goto setpyvemhome

if "%1" == "" goto fail
if "%1" == "activate" goto activateenv

python -m pyvem %*
goto end

:activateenv

if "%2" == "" goto environmentfail
%PYVEMHOME%\%2\Scripts\activate.bat
set ERRORLEVEL=0
goto end


:setpyvemhome
if not EXIST %USERPROFILE%\.pyvem goto createpyvemhome
:contuesetuphome
set PYVEMHOME=%USERPROFILE%\.pyvem
goto end

:createpyvemhome
goto continuesetuphome

:environmentfail
echo usage: pyvem activate "environment name"
goto end

:fail
python -m pyvem -h
set ERRORLEVEL=1
goto end

:end
