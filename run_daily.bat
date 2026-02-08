@echo off
REM Script batch para executar o download diário + Git push
REM Este arquivo será chamado pelo Agendador de Tarefas do Windows

cd /d "%~dp0"

REM Executa o script Python (com download + git push)
python download_and_push.py >> logs\daily_run.log 2>&1

REM Adiciona timestamp no log
echo. >> logs\daily_run.log
echo ---------------------------------------- >> logs\daily_run.log
echo. >> logs\daily_run.log
