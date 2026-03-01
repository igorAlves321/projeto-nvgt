@echo off
title Servidor EVM - Auto Rebuild
color 0A

echo ========================================
echo    SERVIDOR EVM - Auto Rebuild System
echo ========================================
echo.

:loop
echo [%time%] Verificando servidor...

REM Limpar sinais antigos
if exist rebuild_signal.txt del rebuild_signal.txt
if exist restart_signal.txt del restart_signal.txt

REM Compilar se source for mais novo que exe
REM Nota: ajuste o caminho do nvgtw.exe conforme sua instalação
set NVGT_COMPILER=nvgtw.exe

echo [%time%] Compilando servidor...
%NVGT_COMPILER% -c server.nvgt
if errorlevel 1 (
    echo [%time%] ERRO na compilacao!
    timeout /t 5
    goto loop
)

echo [%time%] Iniciando servidor...
start /wait server.exe

echo [%time%] Servidor encerrou.

REM Verificar sinais
if exist rebuild_signal.txt (
    echo [%time%] Rebuild solicitado, recompilando...
    del rebuild_signal.txt
    goto loop
)

if exist restart_signal.txt (
    echo [%time%] Restart solicitado...
    del restart_signal.txt
    goto loop
)

echo [%time%] Reiniciando em 2 segundos...
timeout /t 2
goto loop
