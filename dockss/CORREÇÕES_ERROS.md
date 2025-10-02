# 🔧 CORREÇÕES APLICADAS - Erros de Compilação NVGT

**Data:** 2 de outubro de 2025  
**Total de Erros Corrigidos:** ~65 erros

---

## ✅ CORREÇÕES REALIZADAS

### **1. logger.nvgt** - Funções BGT não existentes ✅
**Problema:** `string_trim_left()` e `string_replace()` não existem em NVGT

**Solução:**
```angelscript
// Antes (BGT):
year = string_trim_left(year, 2);
result = string_replace(result, "<d>", date, true);

// Depois (NVGT):
if(year.length() > 2) year = year.substr(year.length() - 2);
result.replace("<d>", date);  // replace() é método nativo
```

---

### **2. compban.nvgt** - get_peer_address não existe ✅
**Problema:** `net.get_peer_address()` não está disponível em NVGT

**Solução:**
```angelscript
// Usar endereço armazenado do array peer_addresses
string peer_address = "unknown";
for(uint i = 0; i < connected_peers.length(); i++) {
    if(connected_peers[i] == players[banindex].peer_id && i < peer_addresses.length()) {
        peer_address = peer_addresses[i];
        break;
    }
}
```

---

### **3. guarda.nvgt** - Sintaxe `server_//` incorreta ✅
**Problema:** Código tinha `server_// net.send_reliable()` que é sintaxe inválida

**Solução:**
```angelscript
// Antes:
server_// net.send_reliable(0, "play helicopteroarma.ogg");

// Depois:
server_broadcast("play helicopteroarma.ogg " + x + " " + y + " " + map);
```

**Arquivo recriado completamente** após corrupção.

---

### **4. helicoptero.nvgt** - Múltiplos erros ✅
**Problemas:**
1. `server_//` sintaxe incorreta
2. `helicopteros` vs `helicopteros_ativos` inconsistente

**Soluções:**
```angelscript
// 1. Corrigido server_//
server_broadcast("play bombaatomicaexplode.ogg " + x + " " + y + " " + map);

// 2. Padronizado para helicopteros_ativos em todo arquivo
helicopteros_ativos.insert_last(c);
```

---

### **5. boladefogo.nvgt** - Sintaxe `server_//` ✅
**Problema:** Mesma sintaxe incorreta

**Solução:**
```angelscript
server_broadcast("play boobytraphit1.ogg " + x + " " + y);
server_broadcast("play molotovatinge.ogg " + x + " " + y);
server_broadcast("inithurt " + voice + " " + x + " " + y);
```

---

### **6. maquinatempo.nvgt** - Sintaxe `server_//` ✅
**Problema:** Mesma sintaxe incorreta

**Solução:**
```angelscript
server_broadcast("spawnmaquinatempo " + id + " " + x + " " + y + " " + map);
```

---

### **7. combat.nvgt** - Múltiplos problemas ✅
**Problemas:**
1. `save_player_async()` não existe
2. Tipo `Player@` com P maiúsculo
3. `async<void>` e `yield_for()` não disponíveis
4. `db_statement` deveria ser `sqlite3statement`

**Soluções:**
```angelscript
// 1. Substituir save_player_async
save_player_to_database(@attacker);
save_player_to_database(@defender);

// 2. Corrigir tipo
Player@ player → player@ player

// 3. Remover async e usar timer
timer cleanup_combat_timer;
void cleanup_expired_combats() {
    if(cleanup_combat_timer.elapsed < 30000) return;
    cleanup_combat_timer.restart();
    // ... resto do código
}

// 4. Corrigir tipo de statement
db_statement@ stmt → sqlite3statement@ stmt
```

---

### **8. player.nvgt** - Conflitos de métodos ✅
**Problemas:**
1. Método `is_admin()` conflita com campo `is_admin`
2. Statements incompletos (faltava `}`)

**Soluções:**
```angelscript
// 1. Renomear método
bool is_admin() → bool check_admin()

// 2. Adicionar chaves faltantes
if (itemname.find("mm") == -1 && ...) {
    // net.send_reliable(...);
}  // ← Chave faltava aqui
```

---

### **9. objmagnet.nvgt** - string::npos não existe ✅
**Problema:** `string::npos` é conceito de C++, não existe em NVGT

**Solução:**
```angelscript
// Antes:
if (get_tile_at(dir, y, map).find_first("wall") != string::npos)

// Depois:
if (get_tile_at(dir, y, map).find("wall") != -1)
```

---

### **10. stubs.nvgt** - Campos faltantes em guardacofre ✅
**Problema:** `guardacofre_placeholder` não tinha campos `vida` e `golpeado`

**Solução:**
```angelscript
class guardacofre_placeholder { 
    int x, y; 
    string map;
    int vida = 1000;       // Adicionado
    string golpeado = "";  // Adicionado
}
```

---

## 📊 RESUMO DAS CORREÇÕES

| Arquivo | Erros | Status |
|---------|-------|--------|
| `logger.nvgt` | 25 | ✅ Corrigido |
| `compban.nvgt` | 1 | ✅ Corrigido |
| `guarda.nvgt` | 4 | ✅ Corrigido |
| `helicoptero.nvgt` | 6 | ✅ Corrigido |
| `boladefogo.nvgt` | 4 | ✅ Corrigido |
| `maquinatempo.nvgt` | 2 | ✅ Corrigido |
| `combat.nvgt` | 12 | ✅ Corrigido |
| `player.nvgt` | 4 | ✅ Corrigido |
| `objmagnet.nvgt` | 3 | ✅ Corrigido |
| `stubs.nvgt` | 2 | ✅ Corrigido |
| **TOTAL** | **~65** | **✅ 100%** |

---

## 🎯 PRINCIPAIS LIÇÕES APRENDIDAS

### **1. BGT → NVGT Diferenças Chave:**

#### **Funções de String:**
- ❌ BGT: `string_replace(text, search, replace, case_insensitive)`
- ✅ NVGT: `text.replace(search, replace)` (método)

- ❌ BGT: `string_trim_left(text, count)`
- ✅ NVGT: `text.substr(start, length)`

- ❌ BGT: `string::npos`
- ✅ NVGT: `-1`

#### **Tipos de Banco de Dados:**
- ❌ BGT: `db_statement@`
- ✅ NVGT: `sqlite3statement@`

#### **Networking:**
- ❌ BGT: `net.get_peer_address(peer_id)`
- ✅ NVGT: Armazenar manualmente em arrays

#### **Async/Threading:**
- ❌ BGT: `async<void>`, `yield_for(ms)`
- ✅ NVGT: Usar `timer` e verificar no loop principal

#### **Nomes de Variáveis:**
- ⚠️ Conflito: Método `is_admin()` vs campo `is_admin`
- ✅ Solução: Renomear método para `check_admin()`

---

## 🚀 PRÓXIMOS PASSOS

### **1. Testar Compilação:**
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\server"
nvgt -c server.nvgt
```

### **2. Se houver mais erros:**
- Me envie a lista completa
- Vou corrigir imediatamente

### **3. Se compilar com sucesso:**
- Executar servidor
- Testar conexão com cliente
- Verificar logs

---

## 💡 DICAS PARA CONVERSÃO BGT → NVGT

### **1. Sempre verificar documentação NVGT para:**
- Métodos de string (são diferentes!)
- APIs de rede (sintaxe mudou)
- Tipos de dados (alguns mudaram)

### **2. Padronizar nomes de variáveis:**
- Escolher um nome e usar consistentemente
- Exemplo: `helicopteros_ativos` em vez de misturar com `helicopteros`

### **3. Evitar conflitos de nomes:**
- Não usar nome de método igual a campo
- Preferir prefixos: `check_admin()` vs `is_admin`

### **4. Usar find() retorna -1 em NVGT:**
- Sempre comparar com `-1`, não com `npos`

### **5. Replace é método, não função:**
- `texto.replace(a, b)` ← correto
- `string_replace(texto, a, b)` ← errado no NVGT

---

## ✅ STATUS FINAL

**🎉 TODOS OS ERROS REPORTADOS FORAM CORRIGIDOS!**

O servidor deve compilar agora. Se houver novos erros, me envie e eu corrijo imediatamente.

---

*Corrigido por: GitHub Copilot*  
*Especialista em: BGT, NVGT, Conversão de Código, AudioGames*
