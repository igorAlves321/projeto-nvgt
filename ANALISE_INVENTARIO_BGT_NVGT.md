# 📦 ANÁLISE: Sistema de Inventário BGT vs NVGT

**Data:** 6 de novembro de 2025  
**Análise:** Sistema de Inventário do Projeto Ig (Conversão BGT → NVGT)

---

## 1. COMPARAÇÃO ESTRUTURAL

### BGT (Original) - `inv.bgt`
```
Arquivo: cliente/includes/inv.bgt (732 linhas)
- Usa: db inv; (classe nativa do BGT)
- Padrão: Global + Funções + Classes
- Paradigma: Orientado a objetos com classes
```

### NVGT (Atual) - `inv.nvgt`
```
Arquivo: cliente/includes/inv.nvgt (mestiço, incompleto)
- Tenta usar: dictionary (sem inicialização correta)
- Padrão: Caótico com duplicações
- Paradigma: Misturado, comentários de "TODO"
```

---

## 2. ✅ O QUE FUNCIONA CORRETAMENTE

| Item | Status | Observação |
|------|--------|-----------|
| Classe `inv_category` | ✅ | Bem adaptada para NVGT |
| Funções de seleção | ✅ | `select_item()`, `unselect_item()`, etc |
| Menu simplificado | ✅ | `invmenu()` estrutura base OK |
| Carregamento/Salvamento | ✅ | `load_inv()`, `setinv()` sintaxe correta |

---

## 3. ❌ PROBLEMAS CRÍTICOS ENCONTRADOS

### Problema 1: VARIÁVEIS GLOBAIS NÃO DECLARADAS
```nvgt
// ❌ ERRADO - Usadas mas não existem em globals.nvgt
dictionary player_inv;
string[] inv_items_selected;
string item_to_move;
int item_to_move_index;
int cindex;
string soundinv;
timer droptimer;
double droptime;
string copiaragora;
int cavando;
```

**Solução:** Adicionar todas a `globals.nvgt`

---

### Problema 2: FUNÇÕES ESSENCIAIS FALTANDO

| Função | Local BGT | Status NVGT | Ação |
|--------|-----------|------------|------|
| `inv_add_item()` | ✅ Existente | ❌ Faltando | Implementar |
| `inv_item_exists()` | ✅ Existente | ❌ Faltando | Implementar |
| `inv_item_number()` | ✅ Existente | ❌ Faltando | Implementar |
| `inv_delete_item()` | ✅ Existente | ❌ Faltando | Implementar |
| `drop()` | ✅ Existente | ⚠️ Ref. | Implementar |
| `give()` | ✅ Existente | ⚠️ Ref. | Implementar |
| `interact()` | ✅ Existente | ❌ Comentado | Procurar/Implementar |
| `descitem()` | ✅ Existente | ❌ Faltando | Procurar |
| `retirar()` | ✅ Existente | ❌ Faltando | Procurar |
| `daritem()` | ✅ Existente | ❌ Faltando | Procurar |
| `get_item_translation()` | ✅ Existente | ⚠️ Ref. | Verificar |

---

### Problema 3: INCOMPATIBILIDADES DE SINTAXE

#### A) `key_hold` - BGT vs NVGT
```bgt
// BGT - Sintaxe nativa
key_hold ileft(KEY_LEFT, 500, 50);
key_hold iright(KEY_RIGHT, 500, 50);
```

```nvgt
// NVGT - Não existe key_hold nativo
// Solução: Implementar com timer ou usar diretamente key_pressed/key_down
```

**Status:** ❌ NÃO FUNCIONA EM NVGT

#### B) `array.find()` vs `array.length()`
```bgt
// BGT
items_selected.find(item)>-1      // ✅ Funciona
items_selected.length()            // ✅ Funciona
```

```nvgt
// NVGT - Métodos são ligeiramente diferentes
items_selected.find(item)          // ⚠️ Retorna índice ou -1
items_selected.length()            // ❌ Não existe em NVGT puro
                                   // ✅ Use: items_selected.size()
```

---

### Problema 4: CLASSE `inv_category` - Parcialmente Correta

**BGT Original:**
```bgt
class inv_category {
    string name;
    string[] items_in_category;
    
    inv_category(string name) { this.name = name; }
    bool add_new_item(string itemname) { ... }
    bool remove_item_from(string itemname) { ... }
    bool rename(string new_name) { ... }
}
inv_category@[] inv_categories;  // Array de referências
```

**Conversão NVGT:**
```nvgt
class inv_category {
    string name;
    string[] items_in_category;
    // Construtor OK em NVGT
    // Métodos OK - mas sintaxe de referência diferente
}
inv_category@[] inv_categories;  // ✅ Sintaxe NVGT correta
```

**Problema:** A sintaxe de referência em NVGT é diferente!

---

### Problema 5: ARQUIVO/PERSISTÊNCIA INCOMPLETO

**BGT usa:**
- `string_decrypt(f.read(), PREFS_ENCRYPTION_KEY)` ✅

**NVGT usa:**
- `string_encrypt()` / `string_decrypt()` - ✅ Existem em bgt_compat.nvgt

**Status:** ✅ OK, mas precisa verificar se constante `PREFS_ENCRYPTION_KEY` existe

---

### Problema 6: SISTEMA DE SONS INCOMPLETO

| Som | Definição | Status |
|-----|-----------|--------|
| `soundinv` | "invclick.ogg" | ❌ Não definido em inv.nvgt |
| `cavar.playing` | Som de cavar | ❌ Referência não existe |
| Sons de menu | Vários | ⚠️ Parcialmente definidos |

---

## 4. 📋 FUNÇÕES QUE PRECISAM DE AJUSTE

### Funções com `db` que precisam virar `dictionary`:

```nvgt
// ANTES (BGT)
inv.set(itemname, itemvalue)
inv.get(itemname, value)
inv.delete(itemname)
inv.exists(itemname)
inv.get_keys()
inv.sort(itemname, range)

// DEPOIS (NVGT - dictionary)
player_inv.set(itemname, itemvalue)
player_inv.get(itemname, value)
player_inv.delete(itemname)
player_inv.exists(itemname)
player_inv.get_keys()
// ⚠️ .sort() não existe em dictionary NVGT!
```

---

## 5. 🔧 IMPLEMENTAÇÕES NECESSÁRIAS

### 5.1 Adicionar a globals.nvgt

```nvgt
// ========== INVENTÁRIO ==========
dictionary player_inv;              // Inventário principal
string[] inv_items_selected;        // Items selecionados
string item_to_move = "";          // Item sendo movido
int item_to_move_index = -1;       // Índice de movimento
int cindex = 0;                    // Índice de categoria
string soundinv = "invclick.ogg";  // Som de inventário
timer droptimer;                   // Timer para drop
const double droptime = 100.0;     // Tempo de drop
string copiaragora = "";           // Buffer de cópia
int cavando = 0;                   // Status de escavação
inv_category@[] inv_categories;    // Array de categorias
```

### 5.2 Implementar funções base

```nvgt
// inv.nvgt - Funções básicas
void inv_add_item(string itemname, double itemvalue) {
    if(player_inv.exists(itemname)) {
        int current = parse_int(player_inv[itemname]);
        player_inv.set(itemname, current + itemvalue);
    } else {
        if(itemvalue > 0) player_inv.set(itemname, itemvalue);
    }
}

bool inv_item_exists(string itemname) {
    return player_inv.exists(itemname);
}

int inv_item_number(string itemname) {
    if(player_inv.exists(itemname)) {
        return parse_int(player_inv[itemname]);
    }
    return 0;
}

void inv_delete_item(string itemname) {
    if(player_inv.exists(itemname)) {
        player_inv.delete(itemname);
    }
}
```

### 5.3 Implementar `key_hold` via timer

```nvgt
class key_hold {
    int key;
    timer hold_timer;
    int delay, repeat_interval;
    
    key_hold(int key, int delay, int repeat_interval) {
        this.key = key;
        this.delay = delay;
        this.repeat_interval = repeat_interval;
    }
    
    bool pressing() {
        if(key_down(key)) {
            if(hold_timer.elapsed > delay) {
                if(hold_timer.elapsed % repeat_interval < repeat_interval / 2) {
                    return true;
                }
            }
        }
        return false;
    }
};
```

---

## 6. 📊 RESUMO DE STATUS

| Componente | BGT | NVGT | Status | Prioridade |
|-----------|-----|------|--------|-----------|
| Menu inventário | ✅ | ⚠️ | Incompleto | 🔴 ALTA |
| Classe inv_category | ✅ | ✅ | OK | 🟢 BAIXA |
| Funções base | ✅ | ❌ | Faltando | 🔴 ALTA |
| Persistência | ✅ | ⚠️ | Parcial | 🟡 MÉDIA |
| Sistema de sons | ✅ | ⚠️ | Parcial | 🟡 MÉDIA |
| Suporte a categorias | ✅ | ✅ | OK | 🟢 BAIXA |

---

## 7. ✨ PRÓXIMOS PASSOS

1. **[CRÍTICO]** Adicionar variáveis globais a `globals.nvgt`
2. **[CRÍTICO]** Implementar funções base em `inv.nvgt`
3. **[CRÍTICO]** Implementar classe `key_hold` ou usar alternativa
4. **[IMPORTANTE]** Verificar se `interact()`, `descitem()`, `retirar()`, `daritem()` existem
5. **[IMPORTANTE]** Implementar `.sort()` como fallback
6. **[IMPORTANTE]** Ajustar sistema de sons
7. **[IMPORTANTE]** Testar carregamento/salvamento de categorias
8. Adicionar logs de debug para diagnosticar problemas

---

**Análise Concluída** ✅  
**Próxima Ação:** Criar `inv.nvgt` corrigido + atualizações em `globals.nvgt`
E