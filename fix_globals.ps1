# Corrigir globals.nvgt removendo código órfão da função antiga
$file = "cliente\includes\globals.nvgt"
$lines = Get-Content $file

# Manter linhas 0-625 (até comentário "// FUNÇÃO ANTIGA REMOVIDA")
# Pular linhas 626-655 (código órfão)
# Retomar linha 656 em diante
$newLines = $lines[0..625] + $lines[656..($lines.Count-1)]
$newLines | Set-Content $file -Encoding UTF8
Write-Host "Código órfão removido com sucesso!"
