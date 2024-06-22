@echo off
cd %~dp0

IF NOT EXIST "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
)

call venv\Scripts\activate
python -m pip install --upgrade pip

REM Verifica si el archivo requirements.txt existe
IF NOT EXIST "requirements.txt" (
    echo Creando archivo requirements.txt vacío...
    echo. > requirements.txt
)

pip install -r requirements.txt

echo.
echo ¡Actualización completada!
pause

