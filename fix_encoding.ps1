$filePath = "d:\programação\bgt\projetoIg\cliente\lang\portuguese.lang"

# Ler o arquivo com a codificação atual
$content = Get-Content -Path $filePath -Raw

# Substituir caracteres com encoding incorreto
$content = $content -replace "р", "á"
$content = $content -replace "с", "ã"
$content = $content -replace "у", "ç"
$content = $content -replace "Ж", "ê"
$content = $content -replace "ж", "é"
$content = $content -replace "н", "í"
$content = $content -replace "з", "ó"
$content = $content -replace "Щ", "ú"
$content = $content -replace "ш", "õ"

# Salvar o arquivo com codificação UTF-8 com BOM
$content | Out-File -FilePath $filePath -Encoding utf8
Write-Host "Encoding corrigido para UTF-8 com caracteres especiais corretamente mapeados."
