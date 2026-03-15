$originalFile = "portuguese.lang"
$backupFile = "portuguese.lang.backup"
$correctedFile = "portuguese.lang.corrected"

# Cria backup antes de qualquer modificação
Copy-Item -Path $originalFile -Destination $backupFile -Force

# Lê o arquivo com a codificação correta
$content = Get-Content -Path $originalFile -Encoding Default

# Corrige caracteres malformados e erros de sintaxe comuns
$correctedContent = $content -replace 'cartсo_de_crжdito', 'cartão_de_crédito' `
    -replace 'estр', 'está' `
    -replace 'histзria', 'história' `
    -replace 'estaусo', 'estação' `
    -replace 'estсo', 'estão' `
    -replace 'observaусo', 'observação' `
    -replace 'proteусo', 'proteção' `
    -replace 'sсo', 'são' `
    -replace 'forуa', 'força' `
    -replace 'tecnolзgica', 'tecnológica' `
    -replace 'vocЖ', 'você' `
    -replace 'ж', 'é' `
    -replace 'jр', 'já' `
    -replace 'construусo', 'construção' `
    -replace 'nсo', 'não' `
    -replace 'serр', 'será' `
    -replace 'рgua', 'água' `
    -replace 'graуas', 'graças' `
    -replace 'tЩmulo', 'túmulo' `
    -replace 'atж', 'até' `
    -replace 'lЩcifer', 'lúcifer' `
    -replace 'eletrЗnica', 'eletrônica' `
    -replace 'cabaыa', 'cabana' `
    -replace 'rрpido', 'rápido' `
    -replace 'prзximo', 'próximo' `
    -replace 'comeуa', 'começa' `
    -replace 'serviуo', 'serviço' `
    -replace 'poрa', 'poça' `
    -replace 'transferЖncia', 'transferência' `
    -replace 'eletrЗnico', 'eletrônico' `
    -replace 'tambжm', 'também' `
    -replace 'inclinaусo', 'inclinação' `
    -replace 'imobiliрria', 'imobiliária' `
    -replace 'agЖncia', 'agência' `
    -replace 'janrdin', 'jardim' `
    -replace 'vocЖs', 'vocês' `
    -replace 'lanуa', 'lança' `
    -replace 'fantrрstico', 'fantástico' `
    -replace 'Эtil', 'útil' `
    -replace 'avanуa', 'avança' `
    -replace 'elusi', 'ilusi' `
    -replace 'assesуria', 'assessoria' `
    -replace 'balсo', 'balcão' `
    -replace 'espaуo', 'espaço' `
    -replace 'Praуa', 'Praça' `
    -replace 'coraусo', 'coração' `
    -replace 'dragсo', 'dragão' `
    -replace 'birzn', 'visão' `
    -replace 'atЖnусo', 'atenção' `
    -replace 'doenуa', 'doença' `
    -replace 'vрrias', 'várias'

# Escreve o conteúdo corrigido para o arquivo de saída com codificação ANSI
$encoding = [System.Text.Encoding]::GetEncoding('windows-1252')
[System.IO.File]::WriteAllLines($correctedFile, $correctedContent, $encoding)

Write-Output "Arquivo corrigido criado: $correctedFile"
