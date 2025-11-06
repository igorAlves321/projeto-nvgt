# PRÓXIMAS AÇÕES - Deploy inv.nvgt.novo

**Data:** 6 de novembro de 2025  
**Tarefa:** Preparar e testar inv.nvgt.novo para produção  
**Prioridade:** ALTA  

---

## 🎯 OBJETIVO

Validar `inv.nvgt.novo` através de compilação NVGT e testes funcionais básicos antes do deploy final.

---

## ✅ CHECKLIST DE AÇÕES

### FASE 1: Preparação (5 minutos)

- [ ] **1.1** Abrir terminal PowerShell no VS Code
- [ ] **1.2** Navegar até: `c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\`
- [ ] **1.3** Verificar se NVGT compiler está instalado (`nvgt --version`)
- [ ] **1.4** Backup de segurança:
  ```powershell
  Copy-Item -Path "cliente/includes/inv.nvgt" -Destination "cliente/includes/inv.nvgt.backup.$(Get-Date -f 'yyyyMMdd_HHmm')"
  Copy-Item -Path "cliente/includes/globals.nvgt" -Destination "cliente/includes/globals.nvgt.backup.$(Get-Date -f 'yyyyMMdd_HHmm')"
  ```

---

### FASE 2: Validação Pré-Compilação (10 minutos)

**2.1** Verificar existência de arquivos críticos:
```powershell
# Verificar inv.nvgt.novo existe
Test-Path "cliente/includes/inv.nvgt.novo"

# Verificar globals.nvgt foi atualizado
$content = Get-Content "cliente/includes/globals.nvgt" | Select-String "SISTEMA DE INVENTÁRIO"
Write-Host "Seção de inventário encontrada: $($content.Matches.Count -gt 0)"

# Verificar arquivos de suporte existem
@("comandos.nvgt", "menu.nvgt", "bgt_compat.nvgt") | ForEach-Object {
    Write-Host "Arquivo $_: $(Test-Path "cliente/includes/$_")"
}
```

**2.2** Verificar sintaxe básica:
```powershell
# Procurar por erros óbvios
$errors = Select-String -Path "cliente/includes/inv.nvgt.novo" -Pattern "❌|TODO|FIXME|ERROR" -ErrorAction SilentlyContinue
if ($errors.Count -gt 0) {
    Write-Host "⚠️  Encontrados marcadores de erro: $($errors.Count)"
    $errors | ForEach-Object { Write-Host "  - $_" }
} else {
    Write-Host "✅ Nenhum marcador de erro encontrado"
}
```

---

### FASE 3: Deploy (5 minutos)

**3.1** Substituir arquivo:
```powershell
# Mover novo arquivo para produção
Remove-Item "cliente/includes/inv.nvgt" -Force -ErrorAction SilentlyContinue
Move-Item -Path "cliente/includes/inv.nvgt.novo" -Destination "cliente/includes/inv.nvgt"
Write-Host "✅ inv.nvgt.novo movido para inv.nvgt"

# Verificar
if (Test-Path "cliente/includes/inv.nvgt") {
    Write-Host "✅ Novo arquivo em lugar: OK"
} else {
    Write-Host "❌ ERRO: Arquivo não encontrado!"
    exit 1
}
```

**3.2** Verificar globals.nvgt contém variáveis:
```powershell
$vars = @(
    "player_inv",
    "inv_items_selected",
    "item_to_move",
    "soundinv",
    "droptimer"
)

$found = 0
$missing = @()

foreach ($var in $vars) {
    if (Select-String -Path "cliente/includes/globals.nvgt" -Pattern $var -Quiet) {
        $found++
        Write-Host "  ✅ $var"
    } else {
        $missing += $var
        Write-Host "  ❌ $var"
    }
}

Write-Host ""
Write-Host "Variáveis encontradas: $found/$($vars.Count)"
if ($missing.Count -gt 0) {
    Write-Host "⚠️  Variáveis faltando: $($missing -join ', ')"
    exit 1
}
```

---

### FASE 4: Compilação (10-15 minutos)

**4.1** Teste de compilação básica:
```powershell
# Tentar compilar apenas o arquivo inv.nvgt
Write-Host "🔨 Iniciando compilação..."
nvgt --compile cliente/includes/inv.nvgt --output temp_inv.o 2>&1 | Tee-Object -Variable compile_output

# Verificar resultado
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilação bem-sucedida!"
    Remove-Item "temp_inv.o" -ErrorAction SilentlyContinue
} else {
    Write-Host "❌ Erros de compilação encontrados:"
    Write-Host $compile_output
    exit 1
}
```

**4.2** Se erro, analisar e corrigir:
```powershell
# Procurar tipos de erro comuns
$errors = $compile_output | Select-String -Pattern "error|undefined|declaration" -CaseSensitive

if ($errors.Count -gt 0) {
    Write-Host "Erros encontrados:"
    $errors | ForEach-Object {
        Write-Host "  [ERRO] $_"
    }
    
    # Sugestões de correção
    if ($compile_output -match "undefined reference") {
        Write-Host "💡 Sugestão: Verificar se todas as funções externas existem"
    }
    if ($compile_output -match "syntax error") {
        Write-Host "💡 Sugestão: Verificar sintaxe NVGT (@ para referências, .size() para arrays)"
    }
}
```

---

### FASE 5: Testes Funcionais (15-20 minutos)

**5.1** Teste de inicialização:
```
✓ Executar cliente
✓ Pressionar tecla de inventário
✓ Verificar se menu abre sem erros de runtime
✓ Verificar se lista de itens carrega
✓ Fechar inventário sem crash
```

**5.2** Teste de operações básicas:
```
✓ Adicionar item ao inventário
✓ Selecionar item
✓ Usar item (interact)
✓ Dar item para outro player
✓ Dropar item
✓ Remover item
```

**5.3** Teste com servidor:
```
✓ Conectar ao servidor
✓ Carregar inventário do servidor
✓ Enviar item via rede
✓ Receber item via rede
✓ Sincronizar estado
```

---

## 📋 DOCUMENTOS DE REFERÊNCIA

Durante o deploy, consulte:

1. **ANALISE_INVENTARIO_BGT_NVGT.md** - Se encontrar problemas de conversão
2. **PADROES_NVGT_DESCOBERTOS.md** - Se tiver dúvidas sobre sintaxe NVGT
3. **CHECKLIST_INTEGRACAO_INVENTARIO.md** - Para testes mais abrangentes
4. **SUMARIO_EXECUTIVO_INVENTARIO.md** - Para visão geral

---

## 🚨 TROUBLESHOOTING

### Cenário 1: Erro "undefined reference to X"
**Solução**: Verificar se função existe em `comandos.nvgt` ou `menu.nvgt`
```bash
grep -r "void interact" cliente/includes/
grep -r "void descitem" cliente/includes/
```

### Cenário 2: Erro "expected ';' before '@'"
**Solução**: Verificar sintaxe de referência na linha indicada
```nvgt
// ❌ ERRADO
string items[];

// ✅ CORRETO
string@[] items;  // Array de referências
```

### Cenário 3: Erro "'.size()' is not a valid method"
**Solução**: Verificar se é array (usar `.size()`) ou string (usar `.length()`)
```nvgt
// ✅ CORRETO
int count = player_inv.get_keys().size();  // Array de chaves
```

### Cenário 4: Inventário não carrega do arquivo
**Solução**: Verificar se arquivo de save existe e está acessível
```powershell
# Listar arquivos de save
Get-ChildItem "cliente/saves/" -Filter "*.inv" -ErrorAction SilentlyContinue
```

---

## ✅ VALIDAÇÃO FINAL

Após completar todas as fases, confirmar:

- [ ] **Compilação**: ✅ Sem erros
- [ ] **Variáveis globais**: ✅ Todas presentes
- [ ] **Menu do inventário**: ✅ Abre corretamente
- [ ] **Operações básicas**: ✅ Funciona
- [ ] **Rede (cliente-servidor)**: ✅ Sincroniza
- [ ] **Persistência**: ✅ Salva/carrega arquivo

---

## 📞 SUPORTE

Se encontrar problemas não listados acima:

1. Verificar arquivo de log: `client.log` ou `debug.log`
2. Revisar `ANALISE_INVENTARIO_BGT_NVGT.md` seção "Problemas Encontrados"
3. Fazer rollback para backup: `inv.nvgt.backup`

```powershell
# Rollback de emergência
Copy-Item "cliente/includes/inv.nvgt.backup.latest" -Destination "cliente/includes/inv.nvgt" -Force
```

---

## 🎯 CONCLUSÃO

Após completar este checklist, o sistema de inventário estará totalmente operacional em NVGT e pronto para uso em produção.

**Tempo estimado: 45-60 minutos**

---

*Guia prático para deploy de inv.nvgt.novo*  
*Data: 6 de novembro de 2025*  

