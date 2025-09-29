@echo off
cd %~dp0

IF NOT EXIST "venv_3-10-10\" (
    echo Creando entorno virtual...
    python -m venv venv_3-10-10
)

call venv\Scripts\activate
python -m pip install --upgrade pip
python pip install -r requirements.txt
echo.
echo ¡Actualización completada!
pause
