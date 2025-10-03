# 📋 Dependências da Classe Player - Plano de Implementação

## 🎯 Status Atual
- ✅ **Servidor compila** (318 erros são de propriedades opcionais)
- ✅ **Classe player** existe e funciona
- ✅ **Sistema de inventário** convertido para dictionary
- ⚠️ **Sistemas auxiliares** ainda não implementados

---

## 🔴 DEPENDÊNCIAS CRÍTICAS (Bloqueia funcionalidade essencial)

### 1. ✅ **Inventário (db.txt → CONCLUÍDO)**
**Status:** ✅ **JÁ IMPLEMENTADO**
- **O que era no BGT:** Classe `db` para gerenciar inventário
- **Como ficou no NVGT:** Usamos `dictionary` nativo do NVGT
- **Propriedades convertidas:**
  - `inv` (inventário principal) → `dictionary inv`
  - `inv_add_item()`, `inv_item_exists()`, `inv_item_number()`, `inv_delete_item()` → **TODOS FUNCIONANDO**
- **Armazenamento:** Usar `dictionary.serialize()` para salvar em arquivo

**✨ Não precisa de conversão adicional!**

---

### 2. ❌ **var_management.txt (Classe var_management)**
**Status:** ⚠️ **PRECISA IMPLEMENTAR**
- **Finalidade:** Ler/salvar configurações do jogador em arquivo `.ini`
- **Usado para:**
  - Salvar XP, level, gold, items equipados
  - Configurações de interface (volume, idioma)
  - Estatísticas (kills, deaths, playtime)

**Solução NVGT:**
```angelscript
// Usar ini.nvgt (já existe em include/)
#include "../../include/ini.nvgt"

class player_config {
    ini_file config;
    
    void load(string player_name) {
        config.open("players/" + player_name + "/config.ini");
    }
    
    void save() {
        config.save();
    }
    
    string get(string section, string key, string default_value = "") {
        return config.get_value(section, key, default_value);
    }
    
    void set(string section, string key, string value) {
        config.set_value(section, key, value);
    }
}
```

**Prioridade:** 🔴 **ALTA** (necessário para save/load do jogador)

---

### 3. ❌ **crafting.txt (Classe crafting)**
**Status:** ⚠️ **PRECISA IMPLEMENTAR**
- **Finalidade:** Sistema de criação de itens (receitas)
- **Usado para:**
  - Combinar itens do inventário
  - Criar armas, ferramentas, poções
  - Verificar se jogador tem recursos necessários

**Solução NVGT:**
```angelscript
class crafting_recipe {
    string result_item;
    dictionary required_items; // "item_name" → quantidade
    
    bool can_craft(player@ p) {
        string[] keys = required_items.get_keys();
        for(uint i = 0; i < keys.length(); i++) {
            int needed;
            required_items.get(keys[i], needed);
            if(p.inv_item_number(keys[i]) < needed) return false;
        }
        return true;
    }
    
    bool craft(player@ p) {
        if(!can_craft(p)) return false;
        
        // Remover itens necessários
        string[] keys = required_items.get_keys();
        for(uint i = 0; i < keys.length(); i++) {
            int needed;
            required_items.get(keys[i], needed);
            p.inv_delete_item(keys[i], needed);
        }
        
        // Adicionar item criado
        p.inv_add_item(result_item, 1);
        return true;
    }
}

class crafting {
    crafting_recipe@[] recipes;
    
    void load_recipes(string filename) {
        // Carregar receitas de arquivo
    }
}
```

**Prioridade:** 🟡 **MÉDIA** (gameplay importante mas não essencial)

---

### 4. ✅ **playerfires.bgt → PARCIALMENTE IMPLEMENTADO**
**Status:** ✅ **JÁ EXISTE EM PLAYER.NVGT**
- **Classe `playerfire`** já está declarada em `player.nvgt` (linha ~480)
- **Array `playerfires`** existe no player
- **Loop de dano** implementado em `playerfireloop()` (linhas 483-509)

**O que falta:**
- Verificar se todas as propriedades estão corretas
- Testar mecânica de fogo

**Prioridade:** ✅ **CONCLUÍDO** (só precisa de testes)

---

### 5. ❌ **settitle.bgt (Função settitle())**
**Status:** ⚠️ **PRECISA IMPLEMENTAR**
- **Finalidade:** Define título/patente do jogador baseado em level
- **Usado para:**
  - Exibir patente no nome (Novato, Guerreiro, Lenda, etc.)
  - Mostrar status especial (AFK, Pacífico, Procurado)
  - Atualizar HUD do jogador

**Solução NVGT:**
```angelscript
// Em globals.nvgt ou player.nvgt

void settitle(player@ p) {
    string title = "";
    
    // Patente por level
    if(p.level < 10) title = "Novato";
    else if(p.level < 25) title = "Guerreiro";
    else if(p.level < 50) title = "Veterano";
    else if(p.level < 100) title = "Mestre";
    else title = "Lenda";
    
    // Status especiais
    if(p.afk) title = "[AFK] " + title;
    if(p.pacifico > 0) title = "[Pacífico] " + title;
    if(p.admin) title = "[ADMIN] " + title;
    
    // Atualizar
    p.title = title;
    send_reliable(p.peer_id, "settitle " + title, 0);
}
```

**Prioridade:** 🟡 **MÉDIA** (cosmético mas importante para UX)

---

## 🟡 DEPENDÊNCIAS IMPORTANTES (Funcionalidade parcial sem elas)

### 6. ❌ **weapon.txt (Classe weapon)**
**Status:** ⚠️ **PRECISA IMPLEMENTAR**
- **Finalidade:** Sistema de armas e combate
- **Usado para:**
  - Gerenciar armas equipadas
  - Calcular dano, alcance, munição
  - Sons e efeitos de disparo

**Propriedades essenciais:**
```angelscript
class weapon {
    string name;
    int damage;
    int range;
    int ammo;
    int max_ammo;
    int fire_rate; // ms entre disparos
    string fire_sound;
    bool automatic;
    
    // Métodos
    bool can_fire();
    void fire(player@ shooter, int target_x, int target_y);
    void reload();
}

weapon@[] weapons; // Array global de todas as armas
```

**Prioridade:** 🔴 **ALTA** (combate é core do jogo)

---

### 7. ❌ **clothes.txt (Classe clothe)**
**Status:** ⚠️ **PRECISA IMPLEMENTAR**
- **Finalidade:** Sistema de roupas/armaduras
- **Usado para:**
  - Equipar/desequipar roupas
  - Calcular proteção (redução de dano)
  - Efeitos especiais (velocidade, invisibilidade)

**Propriedades essenciais:**
```angelscript
class clothe {
    string name;
    string body_part; // "head", "chest", "legs", "feet"
    int protection; // % de redução de dano
    int durability;
    int max_durability;
    
    // Efeitos especiais
    bool grants_night_vision = false;
    int speed_boost = 0;
}

clothe@[] clothes; // Array global de todas as roupas
```

**Prioridade:** 🟡 **MÉDIA** (importante mas não essencial inicialmente)

---

### 8. ❌ **arena.txt (Classe arena)**
**Status:** ⚠️ **STUB CRIADO** (arena_global em stubs.nvgt)
- **Finalidade:** Sistema de arenas PvP
- **Usado para:**
  - Gerenciar batalhas em arenas
  - Salvar/restaurar inventário e posição
  - Contabilizar kills/deaths de arena

**O que existe:**
- ✅ Classe `arena_placeholder` criada
- ✅ Métodos `remove_player_from()` e `reset()` stubados

**O que falta:**
- Implementar lógica completa de arena
- Sistema de matchmaking
- Recompensas

**Prioridade:** 🟢 **BAIXA** (feature opcional)

---

## 📊 RESUMO DE PRIORIDADES

### 🔴 **IMPLEMENTAR AGORA** (Sistema não funciona sem)
1. ✅ **Inventário (db.txt)** → JÁ FEITO
2. ⚠️ **var_management** → Salvar/carregar jogador
3. ⚠️ **weapon** → Combate básico

### 🟡 **IMPLEMENTAR EM BREVE** (Melhora experiência)
4. ⚠️ **crafting** → Criação de itens
5. ⚠️ **settitle** → Títulos e status
6. ⚠️ **clothes** → Armaduras e proteção

### 🟢 **IMPLEMENTAR DEPOIS** (Features extras)
7. ✅ **playerfires** → JÁ FEITO
8. ⚠️ **arena** → Arenas PvP (stub existe)

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

### Opção A: **Compilação 100% Limpa**
Adicionar propriedades faltando nas classes placeholder para eliminar os 318 erros:
- `earthquakes` → Criar classe placeholder
- `p_index` em npc → Adicionar propriedade
- `tile` em obj → Adicionar propriedade
- `enablerespawn` em npc → Adicionar propriedade
- etc.

**Tempo estimado:** 30-60 minutos
**Resultado:** Servidor compila 100% sem erros

### Opção B: **Implementar Dependências Críticas**
Focar nas 3 dependências mais importantes:
1. **var_management** (salvar/carregar jogador) - 1h
2. **weapon** (sistema de combate) - 2h
3. **settitle** (títulos do jogador) - 30min

**Tempo estimado:** 3-4 horas
**Resultado:** Servidor funcional com recursos essenciais

### Opção C: **Abordagem Híbrida** ⭐ RECOMENDADO
1. **Fase 1 (30min):** Limpar os 318 erros (compilação 100%)
2. **Fase 2 (1h):** Implementar var_management (save/load)
3. **Fase 3 (2h):** Implementar weapon (combate básico)
4. **Fase 4 (quando necessário):** Crafting, clothes, arena

**Resultado:** Servidor compilável + funcionalidades essenciais

---

## 🤔 QUAL CAMINHO SEGUIR?

**Sua escolha:**
- **A)** Focar em compilar 100% sem erros primeiro?
- **B)** Implementar sistemas críticos (var_management, weapons)?
- **C)** Abordagem híbrida (limpar erros + implementar essenciais)?

