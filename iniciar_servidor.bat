@echo off
echo ========================================
echo   API Bienestar Estudiantil
echo   Iniciando servidor FastAPI...
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar si las dependencias están instaladas
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
)

REM Iniciar el servidor
echo Servidor iniciando en http://localhost:8000
echo Documentacion: http://localhost:8000/docs
echo.
echo Presiona CTRL+C para detener el servidor
echo.

python run.py
