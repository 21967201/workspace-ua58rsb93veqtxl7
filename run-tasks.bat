@echo off
REM Task Runner Batch File
REM Generated: 2026-06-18T11:00:31.584141
REM 
REM This file runs all due tasks from auto-tasks.json

echo ========================================
echo QClaw Auto Task Runner
echo ========================================
echo.

cd /d "%~dp0"

echo Running Task Runner...
python task_runner.py --tasks-file auto-tasks.json

echo.
echo ========================================
echo Task Runner Complete
echo ========================================
pause
