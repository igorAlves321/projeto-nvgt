@echo off
echo ========================================
echo Encerrando servidores NVGT antigos...
echo ========================================
echo.

taskkill /F /IM nvgtw.exe 2>nul
if %errorlevel% == 0 (
    echo [OK] Processos nvgtw encerrados com sucesso!
) else (
    echo [INFO] Nenhum processo nvgtw encontrado.
)

echo.
echo Aguarde 2 segundos...
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo Pronto! Agora você pode rodar o servidor.
echo ========================================
pause
