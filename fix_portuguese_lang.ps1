# Script para corrigir o arquivo portuguese.lang
# Separa as traduções que estão todas em uma linha

Write-Host "Corrigindo arquivo portuguese.lang..."

# Fazer backup
$originalFile = "cliente\lang\portuguese.lang"
$backupFile = "cliente\lang\portuguese_backup.lang"

if (Test-Path $originalFile) {
    Copy-Item $originalFile $backupFile
    Write-Host "Backup criado: $backupFile"
    
    # Ler o conteúdo
    $content = Get-Content $originalFile -Raw
    
    # Separar as linhas que não têm quebra
    # Procurar por padrões como "palavra=tradução" e adicionar quebra de linha
    $fixed = $content -replace '([^=\r\n]+=[^=\r\n]+?)(?=[a-zA-Z_][^=]*=)', '$1`r`n'
    
    # Salvar o arquivo corrigido
    $fixed | Out-File $originalFile -Encoding UTF8
    
    Write-Host "Arquivo corrigido! As traduções agora estão em linhas separadas."
    Write-Host "Teste o jogo para ver se 'general' agora aparece como 'tudo'."
} else {
    Write-Host "Erro: Arquivo $originalFile não encontrado!"
}
