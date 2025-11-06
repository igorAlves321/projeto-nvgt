# ✅ CHECKLIST RÁPIDO DE DEPLOY

**Versão:** v1.0  
**Data:** 6 de novembro de 2025  
**Tempo estimado:** 45-60 minutos  

---

## 🚀 EXECUTE AGORA (Passo a Passo)

### PASSO 1: PREPARAÇÃO (5 min)
```
⏳ [ ] Abrir PowerShell em: c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\
⏳ [ ] Verificar NVGT instalado: nvgt --version
⏳ [ ] Fazer backup de inv.nvgt
⏳ [ ] Fazer backup de globals.nvgt
```

**Comando rápido:**
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\"
nvgt --version
Copy-Item "cliente/includes/inv.nvgt" "cliente/includes/inv.nvgt.backup"
Copy-Item "cliente/includes/globals.nvgt" "cliente/includes/globals.nvgt.backup"
```

---

### PASSO 2: VALIDAÇÃO (10 min)
```
⏳ [ ] Verificar inv.nvgt.novo existe
⏳ [ ] Verificar globals.nvgt contém "SISTEMA DE INVENTÁRIO"
⏳ [ ] Verificar comandos.nvgt existe
⏳ [ ] Verificar menu.nvgt existe
```

**Comando rápido:**
```powershell
Test-Path "cliente/includes/inv.nvgt.novo"
Select-String -Path "cliente/includes/globals.nvgt" -Pattern "SISTEMA DE INVENTÁRIO" -Quiet
Test-Path "cliente/includes/comandos.nvgt"
Test-Path "cliente/includes/menu.nvgt"
```

---

### PASSO 3: DEPLOY (5 min)
```
✅ [ ] Remover inv.nvgt antigo
✅ [ ] Mover inv.nvgt.novo para inv.nvgt
✅ [ ] Verificar arquivo está no lugar
```

**Comando rápido:**
```powershell
Remove-Item "cliente/includes/inv.nvgt" -Force
Move-Item "cliente/includes/inv.nvgt.novo" "cliente/includes/inv.nvgt"
Test-Path "cliente/includes/inv.nvgt"
```

---

### PASSO 4: COMPILAÇÃO (10-15 min)
```
⏳ [ ] Compilar client.nvgt
⏳ [ ] Verificar sem erros
⏳ [ ] Se erro, consultar ANALISE_INVENTARIO_BGT_NVGT.md
```

**Comando rápido:**
```powershell
nvgt --compile cliente/client.nvgt 2>&1 | Tee-Object -FilePath "compile_log.txt"
$LASTEXITCODE
# Se $LASTEXITCODE = 0, sucesso!
```

---

### PASSO 5: TESTES BÁSICOS (15-20 min)
```
⏳ [ ] Executar cliente.nvgt
⏳ [ ] Abrir inventário (tecla de atalho)
⏳ [ ] Tentar adicionar item
⏳ [ ] Tentar usar item
⏳ [ ] Fechar inventário sem crash
```

---

## 📊 STATUS CHECKLIST

| Fase | Etapa | Status | Tempo |
|------|-------|--------|-------|
| 1 | Preparação | ⏳ Pendente | 5 min |
| 2 | Validação | ⏳ Pendente | 10 min |
| 3 | Deploy | ⏳ Pendente | 5 min |
| 4 | Compilação | ⏳ Pendente | 15 min |
| 5 | Testes | ⏳ Pendente | 20 min |

---

## 🆘 SE ALGO DER ERRADO

### Erro "file not found"
```
❌ inv.nvgt.novo não existe?
→ Verificar em: cliente/includes/inv.nvgt.novo
→ Se não existir, voltar a ANALISE_INVENTARIO_BGT_NVGT.md
```

### Erro "undefined reference"
```
❌ Função não encontrada?
→ Verificar em: ANALISE_INVENTARIO_BGT_NVGT.md (seção Funções externas)
→ Procurar função em: cliente/includes/comandos.nvgt
```

### Erro "syntax error"
```
❌ Erro de sintaxe NVGT?
→ Consultar: PADROES_NVGT_DESCOBERTOS.md
→ Verificar: Uso de . (dictionary), .size() (arrays), @ (referências)
```

---

## 🔄 ROLLBACK DE EMERGÊNCIA

**Se der problema, volta atrás assim:**
```powershell
# 1. Parar cliente se rodando
# 2. Remover inv.nvgt com erro
Remove-Item "cliente/includes/inv.nvgt" -Force

# 3. Restaurar backup
Copy-Item "cliente/includes/inv.nvgt.backup" "cliente/includes/inv.nvgt"

# 4. Recompilar
nvgt --compile cliente/client.nvgt

Write-Host "✅ Rollback completo!"
```

---

## ✅ SUCESSO!

Se chegou aqui sem erros:
```
✅ Compilação OK
✅ Testes funcionais OK
✅ Inventário respondendo OK
✅ Pronto para produção!
```

**Próximo passo:** Validar com servidor e fazer deploy final

---

## 📚 DOCUMENTOS DE REFERÊNCIA

| Problema | Documento |
|----------|-----------|
| Não sei o que fazer | RESUMO_VISUAL_FINAL.md |
| Tenho erro compilação | ANALISE_INVENTARIO_BGT_NVGT.md |
| Como usar novo código | CORRECAO_INVENTARIO_NVGT.md |
| Preciso fazer testes | CHECKLIST_INTEGRACAO_INVENTARIO.md |
| Padrões NVGT | PADROES_NVGT_DESCOBERTOS.md |
| Resumo gerencial | SUMARIO_EXECUTIVO_INVENTARIO.md |
| Índice de tudo | INDICE_CONSOLIDADO.md |

---

**Status: ⏳ Aguardando execução**  
**Tempo total: 45-60 minutos**  
**Dificuldade: Fácil (Passo a passo)**  

