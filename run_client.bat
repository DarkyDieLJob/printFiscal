@echo off
cd %~dp0

IF EXIST "venv_3-10-10\" (
    call venv_3-10-10\Scripts\activate
    python cliente.py
)
pause
