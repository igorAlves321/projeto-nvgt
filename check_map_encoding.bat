@echo off
REM Script para buscar mapas com problemas de codificação
REM Baseado na correção feita no mapa casa_de_sinistro

echo Procurando mapas com problemas de codificação...
echo.

set "searchDir=servidor\maps"
set "problemFound=0"

for %%f in ("%searchDir%\*.map") do (
    findstr /C:"ï¿½" "%%f" >nul 2>&1
    if !errorlevel! equ 0 (
        echo Problema encontrado em: %%f
        set "problemFound=1"
    )
)

if %problemFound% equ 0 (
    echo ✅ Nenhum problema de codificação encontrado nos mapas!
) else (
    echo.
    echo ⚠️  Problemas de codificação encontrados.
    echo Use o script PowerShell fix_map_encoding.ps1 para corrigir:
    echo.
    echo Exemplo:
    echo PowerShell -ExecutionPolicy Bypass -File fix_map_encoding.ps1 -MapPath "servidor\maps\nome_do_mapa.map"
)

echo.
pause
