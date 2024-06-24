@echo off
cd %~dp0

IF NOT EXIST "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.
echo ¡Actualización completada!
pause
