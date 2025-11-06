# Análise do Sistema de Teclas - BGT vs NVGT

## 📋 Data: 6 de outubro de 2025

## ❌ Problemas Críticos Encontrados

### 1. **Variáveis de Rede Antigas (game_net)**
**Localização:** `cliente/includes/comandos.nvgt` - 50+ ocorrências

**Problema:**
```nvgt
// ❌ ERRADO - Usa game_net (variável local vazia)
game_net.send(net_peer_id, "/pm "+msg, 1, true);
game_net.send(net_peer_id, "j1 "+player, 0, true);
game_net.send(net_peer_id, "/afk", 0, true);
```

**Deve ser:**
```nvgt
// ✅ CORRETO - Usa conexão global con
send_reliable(peer_id, "/pm "+msg, 1);
send_reliable(peer_id, "j1 "+player, 0);
send_reliable(peer_id, "/afk", 0);
```

**Impacto:** Todos os comandos de tecla (F1-F8, atalhos Shift, etc.) não funcionam porque enviam mensagens para variável vazia.

---

### 2. **Função alt_presionado() Ausente**
**Localização:** Nenhum arquivo .nvgt contém esta função

**Problema:**
- Sistema BGT usa `alt_presionado()` para detectar tecla Alt
- Necessário para atalhos como:
  - **Alt + Enter**: Entrar em portais
  - **Alt + C**: Copiar buffers
  - **Alt + outros**: Diversos comandos contextuais

**Deve implementar:**
```nvgt
bool alt_pressionado() {
    if(key_down(KEY_LMENU) || key_down(KEY_RMENU)) return true;
    return false;
}
```

---

### 3. **Conflito de Teclas F5**
**Localização:** `comandos.nvgt` linhas 755 e 806

**Problema:**
```nvgt
// Linha 755 - Shift + F5: Aumentar volume
if(shift_pressionado()) {
    if(key_pressed(KEY_F5)) {
        volumejogo = volumejogo + 1;
        // ...
    }
}

// Linha 806 - F5 (sem shift): Menu de jogadores
else {
    if(key_pressed(KEY_F5)) jogadoresmenu();
}
```

**Status:** ✅ Na verdade está correto! São dois contextos diferentes (com/sem shift).

---

### 4. **Estrutura key_hold Inconsistente**
**Localização:** Diversos arquivos

**Problema:**
- BGT usa `key_hold` para repetição contínua de teclas
- NVGT implementa a classe `key_hold` em alguns lugares
- Mas muitos menus não usam corretamente

**Verificar:**
- Navegação em menus
- Movimento com setas (já funciona em game())
- Campos de input

---

## 📊 Comparação BGT vs NVGT

### Métodos de Detecção de Teclas

| Método | BGT | NVGT | Status |
|--------|-----|------|--------|
| `key_pressed()` | ✅ Implementado | ✅ Implementado | ✅ OK |
| `key_down()` | ✅ Implementado | ✅ Implementado | ✅ OK |
| `key_released()` | ✅ Implementado | ⚠️ Não usado | ⚠️ Verificar |
| `key_hold` | ✅ Classe para repetição | ✅ Implementado | ✅ OK |

### Funções Auxiliares de Modificadores

| Função | BGT | NVGT | Status |
|--------|-----|------|--------|
| `shift_pressionado()` | ✅ Implementado | ✅ Implementado (linha 15) | ✅ OK |
| `alt_presionado()` | ✅ Implementado | ❌ AUSENTE | ❌ CRÍTICO |
| `ctrl_pressionado()` | ⚠️ Não documentado | ❌ AUSENTE | ⚠️ Verificar necessidade |

---

## 🎮 Exemplos de Teclas Específicas

### F5 - Ver Jogadores Conectados
**BGT:**
```bgt
if(key_pressed(KEY_F5)) {
    game_net.send("getplayers", 0, true);
}
```

**NVGT Atual (INCORRETO):**
```nvgt
else if(key_pressed(KEY_F5)) jogadoresmenu();
// ❌ Abre menu local sem consultar servidor
```

**NVGT Correto:**
```nvgt
else if(key_pressed(KEY_F5)) {
    // Primeiro solicita lista atualizada
    send_reliable(peer_id, "getplayers", 0);
    // Depois abre menu (quando receber resposta)
    jogadoresmenu();
}
```

---

### Shift + F2 - Modo Pacifista
**BGT:**
```bgt
if(shift_pressionado() && key_pressed(KEY_F2)) {
    game_net.send("/pacifista", 0, false); // unreliable
}
```

**NVGT Atual (COMENTADO):**
```nvgt
// else if(key_pressed(KEY_F2)) game_net.send(net_peer_id, "/pacifista", 0, true);
// ❌ Comentado e usa game_net
```

**NVGT Correto:**
```nvgt
else if(key_pressed(KEY_F2)) {
    send_unreliable(peer_id, "/pacifista", 0);
}
```

---

### Alt + Enter - Entrar em Portal
**BGT:**
```bgt
if(alt_presionado() && key_pressed(KEY_RETURN)) {
    game_net.send("enterportal", 0, true);
}
```

**NVGT Atual:**
```nvgt
// ❌ NÃO IMPLEMENTADO - função alt_pressionado() não existe
```

**NVGT Necessário:**
```nvgt
if(alt_pressionado() && key_pressed(KEY_RETURN)) {
    send_reliable(peer_id, "enterportal", 0);
}
```

---

## 🔧 Ações Necessárias

### 1. Corrigir todas referências game_net → send_reliable/send_unreliable
**Arquivos afetados:**
- `cliente/includes/comandos.nvgt` (50+ ocorrências)
- Outros arquivos includes (verificar)

**Comando de busca:**
```powershell
grep -r "game_net.send" cliente/includes/
```

---

### 2. Implementar função alt_pressionado()
**Localização:** `cliente/includes/comandos.nvgt` (ao lado de shift_pressionado())

**Código:**
```nvgt
bool alt_pressionado() {
    if(key_down(KEY_LMENU) || key_down(KEY_RMENU)) return true;
    return false;
}
```

---

### 3. Implementar atalhos com Alt faltantes
**Atalhos identificados:**
- Alt + Enter: Entrar em portal
- Alt + C: Copiar buffer
- (Verificar BGT para outros)

---

### 4. Verificar key_released()
**Necessidade:** Verificar se algum comando BGT usa key_released() e portar para NVGT.

---

### 5. Verificar key_hold em menus
**Necessidade:** Garantir que todos os menus usam key_hold corretamente para navegação repetitiva.

---

## 📝 Mapeamento Completo de Teclas (BGT Original)

### Teclas Principais (Sem Modificadores)

| Tecla | Ação | Canal | Tipo |
|-------|------|-------|------|
| F1 | Uptime do servidor | 0 | Reliable |
| F2 | Mensagem do dia (MOTD) | 0 | Reliable |
| F3 | Ping ao servidor | pingchannel | Reliable |
| F4 | Rastrear jogador | 0 | - |
| F5 | Menu de jogadores | - | Local |
| F6 | Menu de chat | - | Local |
| F8 | Toggle bipes | - | Local |
| V | Listar comandos | 0 | Reliable |
| C | Coordenadas (implementado) | - | Local |
| B | Localização (implementado) | - | Local |
| S | Status de saúde (implementado) | 0 | Unreliable |
| [ | Navegar adds (esquerda) | - | Local |
| ] | Navegar adds (direita) | - | Local |
| , | Item anterior add | - | Local |
| . | Próximo item add | - | Local |
| \ | Input de mensagem | 1 | Reliable |

### Teclas com Shift

| Combinação | Ação | Canal | Tipo |
|------------|------|-------|------|
| Shift + F1 | Toggle AFK | 0 | Reliable |
| Shift + F2 | Toggle Pacifista | 0 | Unreliable |
| Shift + F3 | Toggle mensagens outras janelas | - | Local |
| Shift + F4 | Diminuir volume | - | Local |
| Shift + F5 | Aumentar volume | - | Local |
| Shift + F6 | Toggle mute | - | Local |
| Shift + / | Quem está online | 0 | Reliable |
| Shift + = | Input de comando | 1 | Reliable |
| Shift + [ | Primeiro add | - | Local |
| Shift + ] | Último add | - | Local |
| Shift + , | Topo de adds | - | Local |
| Shift + . | Final de adds | - | Local |

### Teclas com Alt (FALTANTES EM NVGT)

| Combinação | Ação | Canal | Tipo |
|------------|------|-------|------|
| Alt + Enter | Entrar em portal | 0 | Reliable |
| Alt + C | Copiar buffer | - | Local |
| *Verificar BGT para outros* | | | |

---

## 🚨 Prioridade de Correção

### 🔴 URGENTE (Bloqueia funcionalidade básica)
1. ✅ Corrigir game_net → send_reliable em `comandos.nvgt` (50+ ocorrências)
2. ✅ Implementar função `alt_pressionado()`

### 🟡 IMPORTANTE (Melhora experiência)
3. ⏳ Implementar atalhos com Alt
4. ⏳ Descomentar/corrigir Shift + F2 (pacifista)
5. ⏳ Verificar comportamento de F5 com/sem shift

### 🟢 DESEJÁVEL (Polimento)
6. ⏳ Verificar uso de key_released()
7. ⏳ Auditar key_hold em todos os menus
8. ⏳ Documentar todos os atalhos para usuários

---

## 📄 Documentação de Referência

**Constantes de teclas NVGT:**
- `KEY_LSHIFT` / `KEY_RSHIFT` - Shift esquerdo/direito
- `KEY_LMENU` / `KEY_RMENU` - Alt esquerdo/direito (MENU = Alt no Windows)
- `KEY_LCONTROL` / `KEY_RCONTROL` - Ctrl esquerdo/direito
- `KEY_F1` até `KEY_F12` - Teclas de função
- `KEY_RETURN` - Enter
- `KEY_ESCAPE` - ESC

**Funções NVGT:**
- `key_pressed(KEY)` - Retorna true UMA vez quando tecla é pressionada
- `key_down(KEY)` - Retorna true ENQUANTO tecla está pressionada
- `key_released(KEY)` - Retorna true UMA vez quando tecla é solta
- `key_hold` - Classe para controlar repetição automática

---

## ✅ Conclusão

O sistema de teclas NVGT está **parcialmente implementado** mas tem problemas críticos:

1. **50+ chamadas game_net.send()** não funcionam (variável vazia)
2. **Função alt_pressionado() ausente** - bloqueia atalhos com Alt
3. **Atalhos com Alt não implementados** - funcionalidades faltantes
4. **Sistema base (key_pressed, key_down, shift_pressionado) funciona corretamente**

**Próximo passo:** Corrigir todas as chamadas de rede em `comandos.nvgt` e implementar suporte a Alt.
