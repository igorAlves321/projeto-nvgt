# start_server.ps1 - Script de inicialização com auto-rebuild
# Monitora sinais de rebuild/restart e recompila automaticamente

$ServerPath = $PSScriptRoot
$NvgtCompiler = "nvgtw.exe"  # Ajuste para o caminho do compilador NVGT
$ServerSource = "server.nvgt"
$ServerExe = "server.exe"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SERVIDOR EVM - Auto Rebuild System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Função para compilar o servidor
function Compile-Server {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Compilando servidor..." -ForegroundColor Yellow
    
    # Tentar encontrar o compilador NVGT
    $nvgtPaths = @(
        "C:\nvgt\nvgtw.exe",
        "C:\Program Files\nvgt\nvgtw.exe",
        "C:\Program Files (x86)\nvgt\nvgtw.exe",
        "$env:USERPROFILE\nvgt\nvgtw.exe",
        "nvgtw.exe"
    )
    
    $compiler = $null
    foreach ($path in $nvgtPaths) {
        if (Test-Path $path) {
            $compiler = $path
            break
        }
    }
    
    if ($compiler -eq $null) {
        Write-Host "[ERRO] Compilador NVGT não encontrado!" -ForegroundColor Red
        Write-Host "Caminhos tentados:" -ForegroundColor Red
        $nvgtPaths | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
        return $false
    }
    
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Usando compilador: $compiler" -ForegroundColor Gray
    
    # Compilar
    $startTime = Get-Date
    $process = Start-Process -FilePath $compiler -ArgumentList "-c", $ServerSource -WorkingDirectory $ServerPath -Wait -PassThru -NoNewWindow
    $elapsed = (Get-Date) - $startTime
    
    if ($process.ExitCode -eq 0) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Compilação concluída em $($elapsed.TotalSeconds.ToString('F1'))s" -ForegroundColor Green
        return $true
    } else {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ERRO na compilação! Código: $($process.ExitCode)" -ForegroundColor Red
        return $false
    }
}

# Função para iniciar o servidor
function Start-GameServer {
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Iniciando servidor..." -ForegroundColor Green
    
    $exePath = Join-Path $ServerPath $ServerExe
    if (-not (Test-Path $exePath)) {
        Write-Host "[ERRO] Executável não encontrado: $exePath" -ForegroundColor Red
        return $null
    }
    
    $process = Start-Process -FilePath $exePath -WorkingDirectory $ServerPath -PassThru
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Servidor iniciado (PID: $($process.Id))" -ForegroundColor Green
    return $process
}

# Limpar sinais antigos
Remove-Item -Path (Join-Path $ServerPath "rebuild_signal.txt") -ErrorAction SilentlyContinue
Remove-Item -Path (Join-Path $ServerPath "restart_signal.txt") -ErrorAction SilentlyContinue

# Loop principal
while ($true) {
    # Compilar se necessário
    $exePath = Join-Path $ServerPath $ServerExe
    $sourcePath = Join-Path $ServerPath $ServerSource
    
    $needCompile = $false
    if (-not (Test-Path $exePath)) {
        $needCompile = $true
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Executável não existe, compilando..." -ForegroundColor Yellow
    } elseif ((Get-Item $sourcePath).LastWriteTime -gt (Get-Item $exePath).LastWriteTime) {
        $needCompile = $true
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Código fonte modificado, recompilando..." -ForegroundColor Yellow
    }
    
    if ($needCompile) {
        if (-not (Compile-Server)) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Aguardando 5 segundos antes de tentar novamente..." -ForegroundColor Yellow
            Start-Sleep -Seconds 5
            continue
        }
    }
    
    # Iniciar servidor
    $serverProcess = Start-GameServer
    if ($serverProcess -eq $null) {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Falha ao iniciar servidor. Aguardando 5 segundos..." -ForegroundColor Red
        Start-Sleep -Seconds 5
        continue
    }
    
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Monitorando servidor..." -ForegroundColor Cyan
    Write-Host "Comandos no jogo: /rb (rebuild) ou /restart" -ForegroundColor Gray
    Write-Host ""
    
    # Monitorar processo e sinais
    while (-not $serverProcess.HasExited) {
        Start-Sleep -Milliseconds 500
        
        $rebuildSignal = Join-Path $ServerPath "rebuild_signal.txt"
        $restartSignal = Join-Path $ServerPath "restart_signal.txt"
        
        # Verificar sinal de rebuild
        if (Test-Path $rebuildSignal) {
            Write-Host ""
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sinal de REBUILD detectado!" -ForegroundColor Yellow
            Remove-Item $rebuildSignal -Force
            
            # Aguardar servidor encerrar
            if (-not $serverProcess.HasExited) {
                $serverProcess.WaitForExit(5000)
            }
            
            # Recompilar
            if (Compile-Server) {
                Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Rebuild concluído!" -ForegroundColor Green
            }
            break
        }
        
        # Verificar sinal de restart simples
        if (Test-Path $restartSignal) {
            Write-Host ""
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sinal de RESTART detectado!" -ForegroundColor Yellow
            Remove-Item $restartSignal -Force
            
            # Aguardar servidor encerrar
            if (-not $serverProcess.HasExited) {
                $serverProcess.WaitForExit(5000)
            }
            break
        }
    }
    
    # Servidor encerrou
    $exitCode = $serverProcess.ExitCode
    Write-Host ""
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Servidor encerrou (código: $exitCode)" -ForegroundColor Yellow
    
    # Pequena pausa antes de reiniciar
    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Reiniciando em 2 segundos..." -ForegroundColor Cyan
    Start-Sleep -Seconds 2
}
