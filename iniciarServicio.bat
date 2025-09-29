@echo off
cd %~dp0

IF EXIST "venv_2-7-12\" (
    call venv_2-7-12\Scripts\activate
    .\Python27\python.exe server.py
)
pause