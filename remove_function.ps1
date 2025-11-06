# Remove linhas 623-684 (função antiga) de globals.nvgt
$file = "cliente\includes\globals.nvgt"
$lines = Get-Content $file
$newLines = $lines[0..622] + "// FUNÇÃO ANTIGA REMOVIDA - usamos o método do Batalha Constante agora" + "// (abrir pack diretamente no client.nvgt)" + "" + $lines[684..($lines.Count-1)]
$newLines | Set-Content $file -Encoding UTF8
Write-Host "Função removida com sucesso!"
