# ✅ CHECKLIST: Integração do Sistema de Inventário Corrigido

**Objetivo:** Integrar o novo `inv.nvgt` corrigido ao projeto  
**Data:** 6 de novembro de 2025  
**Status:** ⏳ PRONTO PARA INTEGRAÇÃO

---

## 📋 PRÉ-INTEGRAÇÃO

### Verificação de Arquivos

- [ ] **Backup de segurança**
  ```
  cliente/includes/inv.nvgt → cliente/includes/inv.nvgt.backup
  cliente/includes/globals.nvgt → cliente/includes/globals.nvgt.backup
  ```

- [ ] **Novo arquivo existe**
  ```
  cliente/includes/inv.nvgt.novo ✅ (criado)
  ```

- [ ] **Globals atualizado**
  ```
  cliente/includes/globals.nvgt ✅ (atualizado com variáveis)
  ```

---

## 🔧 ETAPA 1: SUBSTITUIÇÃO DE ARQUIVO

### Passo 1.1: Remover arquivo antigo (ou arquivar)
```powershell
# Opção A: Mover para backup (recomendado)
Move-Item -Path "cliente\includes\inv.nvgt" -Destination "cliente\includes\inv.nvgt.v1.bak"

# Opção B: Manter como referência
Rename-Item -Path "cliente\includes\inv.nvgt" -NewName "inv.nvgt.old"
```

**Status:** [ ] Concluído

### Passo 1.2: Renomear novo arquivo
```powershell
Rename-Item -Path "cliente\includes\inv.nvgt.novo" -NewName "inv.nvgt"
```

**Status:** [ ] Concluído

### Passo 1.3: Verificar includes no cliente
```powershell
# Procurar por "inv.nvgt" em client.nvgt
grep -n "inv.nvgt\|include.*inv" cliente\client.nvgt

# Deve mostrar:
# #include "includes/inv.nvgt"
```

**Status:** [ ] Verificado

---

## 🧪 ETAPA 2: TESTES DE COMPILAÇÃO

### Teste 2.1: Compilação Básica
```powershell
cd cliente
nvgt client.nvgt
```

**Esperado:**
- ✅ Sem erros de sintaxe
- ✅ Sem referências undefined
- ✅ Compilação bem-sucedida

**Status:** [ ] ✅ Compilou

**Se falhar:**
```
Erro típico 1: "dictionary não tem método size()"
Solução: Verificar versão NVGT (v2.0+)

Erro típico 2: "player_inv não declarado"
Solução: Verificar se globals.nvgt foi atualizado

Erro típico 3: "Função get_number2 não existe"
Solução: Procurar definição em client.nvgt ou adicionar
```

### Teste 2.2: Verificar Referências
```powershell
# Procurar por funções que podem não existir:
grep -rn "get_number2\|daritem\|interact\|descitem" cliente/includes/

# Deve encontrar:
# - daritem em menu.nvgt
# - interact em comandos.nvgt
# - descitem em comandos.nvgt
```

**Status:** [ ] ✅ Referências OK

---

## 🎮 ETAPA 3: TESTES FUNCIONAIS

### Teste 3.1: Inicialização
```
1. Conectar ao servidor
2. Verificar console: "[📦]" (emoji de inventário)
3. Verificar se init_inventory() é chamado

Esperado:
✅ Sem erros de inicialização
✅ Categorias carregadas
✅ Inventário vazio ou com itens corretos
```

**Status:** [ ] ✅ Testado

### Teste 3.2: Abrir Inventário
```
1. Pressionar tecla de inventário (padrão: I ou similar)
2. Ouvir som "abrirziper.ogg" ou similar
3. Ouvir anúncio de categoria (ex: "Compartimento Geral, 5 itens")

Esperado:
✅ Menu abre sem erros
✅ Som toca corretamente
✅ Fala anúncio em português/espanhol
```

**Status:** [ ] ✅ Testado

### Teste 3.3: Navegação Básica
```
1. No menu de inventário:
   - Pressionar UP: deve ir ao item anterior
   - Pressionar DOWN: deve ir ao próximo item
   - Pressionar HOME: deve ir ao primeiro
   - Pressionar END: deve ir ao último

Esperado:
✅ Navegação funciona
✅ Sons de menu tocam ("invclick.ogg")
✅ Items são falados corretamente
```

**Status:** [ ] ✅ Testado

### Teste 3.4: Ações de Inventário
```
1. Testar cada ação:

   A) SPACE (usar item):
      - Comando: interact(itemname)
      - Esperado: Item é usado

   B) ENTER (dar item):
      - Comando: give(itemname)
      - Esperado: Pede para digitar nome de pessoa
      - Esperado: Envia comando ao servidor

   C) DELETE (dropar item):
      - Comando: drop(itemname, 1)
      - Esperado: Item é removido do inventário
      - Esperado: Item aparece no chão (objeto)

   D) SHIFT + DELETE (dropar quantidade):
      - Esperado: Pede quantidade
      - Esperado: Remove quantidade especificada

   E) CTRL + DELETE (dropar tudo):
      - Esperado: Remove toda quantidade do item
```

**Status:** [ ] ✅ Todos testados

### Teste 3.5: Recebimento de Itens (Servidor)
```
1. Servidor envia: "inv item1=10 item2=5"
2. Verificar se load_inv() é chamado
3. Verificar se items aparecem no inventário

Esperado:
✅ Items são recebidos corretamente
✅ Quantidades são precisas
✅ Podem ser usados/dropados
```

**Status:** [ ] ✅ Testado

### Teste 3.6: Categorias
```
1. Se suportar categorias:
   - Pressionar LEFT/RIGHT para mudar categoria
   - Verificar se items filtram corretamente

2. Esperado:
   ✅ Menu muda de categoria
   ✅ Items mostrados correspondem à categoria
```

**Status:** [ ] ✅ Testado (se aplicável)

---

## 💾 ETAPA 4: TESTES DE PERSISTÊNCIA

### Teste 4.1: Salvar/Carregar Categorias
```
1. Criar categoria customizada:
   - Usar menu de ações (ALT+A?)
   - Nomear categoria

2. Salvar e sair:
   - Desconectar/Sair do jogo
   - Fechar cliente

3. Reabrir e verificar:
   - Conectar novamente
   - Abrir inventário
   - Categoria deve existir

Esperado:
✅ Arquivo "categories.db" criado
✅ Arquivo é criptografado
✅ Categoria persiste entre sessões
```

**Status:** [ ] ✅ Testado

### Teste 4.2: Dados Criptografados
```
1. Verificar arquivo: categories.db
2. Tentar ler com editor de texto:
   - Se ilegível = criptografia OK ✅
   - Se legível = problema de criptografia ⚠️

Esperado:
✅ Arquivo é binário/criptografado
✅ Não é humano-legível
```

**Status:** [ ] ✅ Verificado

---

## 🐛 ETAPA 5: TRATAMENTO DE ERROS

### Teste 5.1: Inventário Vazio
```
1. Quando não há itens:
   - Abrir inventário
   - Deve falar "Inventário vazio"
   - Deve sair do menu

Esperado:
✅ Sem crash
✅ Mensagem clara
✅ Retorna ao jogo
```

**Status:** [ ] ✅ Testado

### Teste 5.2: Item Inexistente
```
1. Tentar usar item que não existe
2. Tentar dropar item que não existe

Esperado:
✅ Sem crash
✅ Mensagem de erro clara
✅ Continua funcionando
```

**Status:** [ ] ✅ Testado

### Teste 5.3: Arquivo Corrompido
```
1. Deletar "categories.db"
2. Abrir inventário

Esperado:
✅ Sem crash
✅ Cria novo arquivo
✅ Categorias resetam para "all"
```

**Status:** [ ] ✅ Testado

---

## 🔐 ETAPA 6: SEGURANÇA

### Teste 6.1: Validação de Input
```
1. No menu "Dar Item":
   - Tentar nomes inválidos
   - Tentar quantidades negativas
   - Tentar strings vazias

Esperado:
✅ Rejeita inputs inválidos
✅ Pede novamente
✅ Sem crash
```

**Status:** [ ] ✅ Testado

### Teste 6.2: Limites de Quantidade
```
1. Testar limites internos:
   - Máximo de drop: 100000000000
   - Quantidade negativa: rejeitada
   - Quantidade zerada: item removido

Esperado:
✅ Responde corretamente
✅ Sem overflow de números
```

**Status:** [ ] ✅ Testado

---

## 📊 ETAPA 7: PERFORMANCE

### Teste 7.1: Inventário Grande
```
1. Adicionar muitos itens (~100+)
2. Navegação deve ser responsiva

Esperado:
✅ Menu abre em <1 segundo
✅ Navegação fluid
✅ Sem travamentos
```

**Status:** [ ] ✅ Testado

### Teste 7.2: Muitas Categorias
```
1. Criar ~20 categorias
2. Trocar entre elas (LEFT/RIGHT)

Esperado:
✅ Sem delay
✅ Mudanças instantes
```

**Status:** [ ] ✅ Testado

---

## 📝 ETAPA 8: DOCUMENTAÇÃO

### Documentação Criada
- [x] `ANALISE_INVENTARIO_BGT_NVGT.md` - Análise completa
- [x] `CORRECAO_INVENTARIO_NVGT.md` - Implementação
- [x] `CHECKLIST.md` - Este arquivo

**Status:** [ ] ✅ Documentado

### Comentários no Código
```
Verificar:
[ ] inv.nvgt tem comentários explicativos
[ ] globals.nvgt tem seção de inventário documentada
[ ] Funções têm propósitos documentados
```

**Status:** [ ] ✅ Verificado

---

## 🎯 RESUMO FINAL

### Checklist Geral

| Item | Status | Responsável |
|------|--------|-------------|
| Backup criado | [ ] | Você |
| Arquivo substituído | [ ] | Você |
| Compilação OK | [ ] | Você |
| Testes funcionais OK | [ ] | Você |
| Persistência OK | [ ] | Você |
| Erros tratados | [ ] | Você |
| Performance OK | [ ] | Você |
| Documentado | [ ] | Você |

### Aprovação Final

- [ ] **Todos os testes passaram**
- [ ] **Nenhum erro crítico**
- [ ] **Sistema estável**
- [ ] **Pronto para produção**

**Assinado por:** _____________  
**Data:** _____ / _____ / _____

---

## 📞 SUPORTE

Se encontrar problemas:

1. **Verifique logs:**
   ```
   debug/client_log.txt
   ```

2. **Consulte análise:**
   ```
   ANALISE_INVENTARIO_BGT_NVGT.md
   ```

3. **Referência de implementação:**
   ```
   CORRECAO_INVENTARIO_NVGT.md
   ```

4. **Arquivo de backup:**
   ```
   cliente/includes/inv.nvgt.backup
   ```

---

**Checklist de Integração** ✅  
**Pronto para Implementação** 🚀
