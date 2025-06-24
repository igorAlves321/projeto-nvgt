# Script para corrigir problemas de codificação UTF-8 em mapas do jogo
# Baseado na correção feita no mapa casa_de_sinistro
# Uso: .\fix_map_encoding.ps1 -MapPath "caminho\para\mapa.map"

param(
    [Parameter(Mandatory=$true)]
    [string]$MapPath
)

# Verifica se o arquivo existe
if (-not (Test-Path $MapPath)) {
    Write-Error "Arquivo não encontrado: $MapPath"
    exit 1
}

Write-Host "Corrigindo codificação do mapa: $MapPath"

# Lê o conteúdo do arquivo
$content = Get-Content -Path $MapPath -Raw

# Define os mapeamentos de caracteres corrompidos para caracteres corretos
$replacements = @{
    'ï¿½' = 'ê'    # Para maioria dos casos de 'ê'
    'vocï¿½' = 'você'
    'Vocï¿½' = 'Você' 
    'ï¿½rea' = 'área'
    'ï¿½rvore' = 'árvore'
    'ï¿½s ' = 'às '
    'ï¿½ ' = 'é '
    'nï¿½o' = 'não'
    'estï¿½' = 'está'
    'estï¿½o' = 'estão'
    'serï¿½' = 'será'
    'terï¿½' = 'terá'
    'saï¿½da' = 'saída'
    'mï¿½sica' = 'música'
    'trï¿½s' = 'trás'
    'prï¿½xima' = 'próxima'
    'sï¿½o' = 'são'
    'olï¿½' = 'olá'
    'silï¿½ncio' = 'silêncio'
    'escritï¿½rio' = 'escritório'
    'papï¿½is' = 'papéis'
    'minï¿½sculo' = 'minúsculo'
    'dï¿½' = 'dá'
    'hï¿½' = 'há'
    'vï¿½' = 'vê'
    'apï¿½s' = 'após'
    'avanï¿½a' = 'avança'
    'permiï¿½ï¿½o' = 'permissão'
    'alguï¿½m' = 'alguém'
    'serto' = 'certo'
    'avansa' = 'avança'
    'diante' = 'à frente'
}

# Aplica todas as substituições
foreach ($old in $replacements.Keys) {
    $new = $replacements[$old]
    $content = $content.Replace($old, $new)
}

# Correções adicionais específicas
$content = $content.Replace('Às águas', 'às águas')
$content = $content.Replace('retorna as escadas', 'retorna às escadas')
$content = $content.Replace('a entrada', 'à entrada')

# Cria backup do arquivo original
$backupPath = $MapPath + ".backup"
Copy-Item -Path $MapPath -Destination $backupPath
Write-Host "Backup criado: $backupPath"

# Salva o arquivo corrigido
$content | Out-File -FilePath $MapPath -Encoding UTF8
Write-Host "Arquivo corrigido salvo: $MapPath"

# Mostra estatísticas
$originalContent = Get-Content -Path $backupPath -Raw
$problematicCharsOriginal = ($originalContent | Select-String -Pattern 'ï¿½' -AllMatches).Matches.Count
$problematicCharsFixed = ($content | Select-String -Pattern 'ï¿½' -AllMatches).Matches.Count

Write-Host "Caracteres problemáticos encontrados: $problematicCharsOriginal"
Write-Host "Caracteres problemáticos restantes: $problematicCharsFixed"
Write-Host "Caracteres corrigidos: $($problematicCharsOriginal - $problematicCharsFixed)"

if ($problematicCharsFixed -eq 0) {
    Write-Host "✅ Codificação corrigida com sucesso!" -ForegroundColor Green
} else {
    Write-Warning "⚠️  Ainda há $problematicCharsFixed caracteres problemáticos. Pode ser necessário correção manual."
}
