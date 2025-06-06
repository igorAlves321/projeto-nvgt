@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   REINO ELEMENTAL 4.0 - CONVERSOR DE MOEDAS
echo ========================================
echo.
echo Iniciando conversão das moedas...
echo.

set "baseDir=%~dp0"
set "errorOccurred=0"

echo [1/5] Convertendo "elementales" para "dólares"...
powershell -Command "Get-ChildItem -Path '%baseDir%' -Recurse -Include '*.bgt', '*.map', '*.txt', '*.md', '*.db' | Where-Object { $_.DirectoryName -notlike '*\logs\*' } | ForEach-Object { try { $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8; if ($content -and $content.Contains('elementales')) { $newContent = $content -replace [regex]::Escape('elementales'), 'dólares'; Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8; Write-Host '  ✓ '$_.Name } } catch { Write-Host '  ✗ Erro: '$_.Name; exit 1 } }" 2>nul
if %errorlevel% neq 0 set "errorOccurred=1"

echo [2/5] Convertendo "mgerems" para "reais"...
powershell -Command "Get-ChildItem -Path '%baseDir%' -Recurse -Include '*.bgt', '*.map', '*.txt', '*.md', '*.db' | Where-Object { $_.DirectoryName -notlike '*\logs\*' } | ForEach-Object { try { $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8; if ($content -and $content.Contains('mgerems')) { $newContent = $content -replace [regex]::Escape('mgerems'), 'reais'; Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8; Write-Host '  ✓ '$_.Name } } catch { Write-Host '  ✗ Erro: '$_.Name; exit 1 } }" 2>nul
if %errorlevel% neq 0 set "errorOccurred=1"

echo [3/5] Convertendo "gemas mágicas" para "reais"...
powershell -Command "Get-ChildItem -Path '%baseDir%' -Recurse -Include '*.bgt', '*.map', '*.txt', '*.md', '*.db' | Where-Object { $_.DirectoryName -notlike '*\logs\*' } | ForEach-Object { try { $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8; if ($content -and $content.Contains('gemas mágicas')) { $newContent = $content -replace [regex]::Escape('gemas mágicas'), 'reais'; Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8; Write-Host '  ✓ '$_.Name } } catch { Write-Host '  ✗ Erro: '$_.Name; exit 1 } }" 2>nul
if %errorlevel% neq 0 set "errorOccurred=1"

echo [4/5] Convertendo "esmeraldas" para "créditos"...
powershell -Command "Get-ChildItem -Path '%baseDir%' -Recurse -Include '*.bgt', '*.map', '*.txt', '*.md', '*.db' | Where-Object { $_.DirectoryName -notlike '*\logs\*' } | ForEach-Object { try { $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8; if ($content -and $content.Contains('esmeraldas')) { $newContent = $content -replace [regex]::Escape('esmeraldas'), 'créditos'; Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8; Write-Host '  ✓ '$_.Name } } catch { Write-Host '  ✗ Erro: '$_.Name; exit 1 } }" 2>nul
if %errorlevel% neq 0 set "errorOccurred=1"

echo [5/5] Convertendo "celestiums" para "libras"...
powershell -Command "Get-ChildItem -Path '%baseDir%' -Recurse -Include '*.bgt', '*.map', '*.txt', '*.md', '*.db' | Where-Object { $_.DirectoryName -notlike '*\logs\*' } | ForEach-Object { try { $content = Get-Content -Path $_.FullName -Raw -Encoding UTF8; if ($content -and $content.Contains('celestiums')) { $newContent = $content -replace [regex]::Escape('celestiums'), 'libras'; Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8; Write-Host '  ✓ '$_.Name } } catch { Write-Host '  ✗ Erro: '$_.Name; exit 1 } }" 2>nul
if %errorlevel% neq 0 set "errorOccurred=1"

echo.
echo ========================================

if "%errorOccurred%"=="0" (
    echo   ✅ CONVERSÃO CONCLUÍDA COM SUCESSO!
    echo.
    echo   Todas as moedas foram convertidas:
    echo   • elementales     → dólares
    echo   • mgerems         → reais
    echo   • gemas mágicas   → reais    echo   • esmeraldas      → créditos
    echo   • celestiums      → libras
    echo.
    echo   O sistema de moedas do Reino Elemental 4.0
    echo   agora está atualizado com os novos nomes!
) else (
    echo   ❌ ERRO DURANTE A CONVERSÃO!
    echo.
    echo   Ocorreu um erro durante o processo.
    echo   Verifique as permissões dos arquivos
    echo   e tente executar como administrador.
)

echo ========================================
echo.
pause
