@echo off
cd %~dp0
call venv\Scripts\activate
python cliente.py
pause
