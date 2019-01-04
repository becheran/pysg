echo off
title Setup
echo Setup reguirement files for example and api

:: Source folder
call .\venv\Scripts\activate.bat
pip freeze > requirements.txt
call .\venv\Scripts\deactivate.bat

:: Examples folder
cd examples
call .\venv\Scripts\activate.bat
pip freeze > requirements.txt
call .\venv\Scripts\deactivate.bat
pause