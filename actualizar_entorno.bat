@echo off
cd %~dp0

IF NOT EXIST "venv_3-10-10\" (
    echo Creando entorno virtual...
    python -m venv venv_3-10-10
)
echo ¡1!
pause

IF EXIST "venv_3-10-10\" (
    call venv_3-10-10\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo ¡Actualización completada!
)
echo ¡1.5!
pause


IF NOT EXIST "venv_2-7-12\" (
    .\Python27\python.exe -m pip install --upgrade pip
    .\Python27\python.exe -m pip install virtualenv
    echo Creando entorno virtual...
    .\Python27\python.exe -m venv venv_2-7-12
)
echo ¡2!
pause

IF EXIST "venv_2-7-12\" (
    .\Python27\python.exe -m pip install virtualenv
    call venv_2-7-12\Scripts\activate
    .\Python27\python.exe -m pip install -r requirements_fiscal.txt
    echo.
    echo ¡Actualización completada!
)
echo ¡2.5!
pause
