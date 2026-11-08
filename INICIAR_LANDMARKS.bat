@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente virtual nao encontrado. Leia o README.md e execute a instalacao.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" src\main.py --modo maos
pause
