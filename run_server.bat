@echo off
cd %~dp0
call venv\Scripts\activate
python server.py
pause
