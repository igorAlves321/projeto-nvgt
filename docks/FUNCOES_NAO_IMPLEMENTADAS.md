# Funções Não Implementadas - Análise Completa 📋

**Data:** 2025-10-03
**Arquivo Principal:** `stubs.nvgt` + outros arquivos

---

## 📊 Resumo Executivo

Foram identificadas **52 funções/sistemas** que estão como stubs (temporários) ou marcados para implementação futura. Estas estão categorizadas por prioridade e sistema.

---

## 🔴 PRIORIDADE CRÍTICA (11 itens)

### 1. Sistema de Histórico de Ações
**Arquivo:** `stubs.nvgt:4-34`
**Status:** Stub

#### Funções Afetadas:
```cpp
void log_action(string player, string action, string description,
                string map, int x, int y, int z, string extra = "")
// Atualmente: apenas debug_log

string get_recent_actions(string player, int limit = 10)
// Retorna: "Histórico ainda não implementado"

string[] get_recent_actions(int limit, string category, string player)
// Retorna: Array com mensagem de não implementado
```

#### Por que implementar:
- **Auditoria:** Rastrear ações de jogadores
- **Anti-cheat:** Detectar padrões suspeitos
- **Admin:** Investigar reportes
- **Analytics:** Estatísticas de gameplay

#### Implementação Sugerida:
```cpp
// Criar history.nvgt
class action_log {
    string player;
    string action;
    string description;
    string map;
    int x, y, z;
    uint64 timestamp;
    string extra_data;
}

action_log@[] action_history;
int MAX_HISTORY = 10000;

void log_action(...) {
    action_log@ log = action_log();
    // preencher dados
    action_history.insert_last(log);

    // Limitar tamanho
    if(action_history.length() > MAX_HISTORY) {
        action_history.remove_at(0);
    }
}
```

---

### 2. Sistema de Estatísticas
**Arquivo:** `stubs.nvgt:10-19`
**Status:** Stub

#### Funções Afetadas:
```cpp
void update_statistics(string stat_name)
// Atualmente: apenas debug_log

string get_current_statistics_report()
// Retorna: "Estatísticas ainda não implementadas"
```

#### Por que implementar:
- **Leaderboards:** Rankings de jogadores
- **Achievements:** Conquistas baseadas em stats
- **Balance:** Ajustar gameplay baseado em dados
- **Eventos:** Criar eventos baseados em métricas

#### Implementação Sugerida:
```cpp
// Criar statistics.nvgt
dictionary player_stats; // player_name => dictionary de stats

void update_statistics(string stat_name) {
    // Incrementar contador global
    global_stats.set(stat_name, get_stat(stat_name) + 1);
}

string get_current_statistics_report() {
    string report = "=== ESTATÍSTICAS DO SERVIDOR ===\n";
    report += "Total de mortes: " + get_stat("deaths") + "\n";
    report += "Total de kills: " + get_stat("kills") + "\n";
    // ... mais stats
    return report;
}
```

---

### 3. Sistema de Experiência (XP)
**Arquivo:** `stubs.nvgt:76-91`
**Status:** Stub básico

#### Funções Afetadas:
```cpp
void apply_doublexp(string player, int amount)
// Atualmente: apenas debug_log

void ganhaxp(string player_name, int exp_amount, int gold_amount)
// Atualmente: apenas debug_log
```

#### Por que implementar:
- **Progressão:** Sistema de níveis
- **Recompensas:** Ganho de XP por ações
- **Eventos:** XP dobrado em períodos especiais
- **Economia:** Vincular XP com gold

#### Implementação Sugerida:
```cpp
void ganhaxp(string player_name, int exp_amount, int gold_amount) {
    int index = get_player_index_from(player_name);
    if(index < 0) return;

    // Aplicar multiplicadores
    if(enable_double_emeralds > 0) {
        exp_amount *= 2;
    }

    // Adicionar XP
    players[index].exp += exp_amount;
    players[index].gold += gold_amount;

    // Verificar level up
    check_level_up(index);

    // Notificar
    send_reliable(players[index].peer_id,
        "msg2 +"+exp_amount+" XP, +"+gold_amount+" Gold!", 0);
}
```

---

### 4. Sistema de NPC (IA)
**Arquivo:** `stubs.nvgt:243-249`
**Status:** Stubs vazios

#### Funções Afetadas:
```cpp
void die(int npc_index)                        // Apenas log
void attack(int npc_index, int target_player)  // Apenas log
void move(int npc_index, int direction)        // Vazio
bool exists_player_in_my_map(int npc_index)    // Retorna false
int select_player_to_attack(int npc_index)     // Retorna -1
void change_player(int npc_index)              // Vazio
```

#### Por que implementar:
- **PvE:** Inimigos para combater
- **Quests:** NPCs para missões
- **Economia:** Merchants e shops
- **Gameplay:** Adicionar desafios

#### Implementação Sugerida:
```cpp
void attack(int npc_index, int target_player) {
    if(npc_index < 0 || target_player < 0) return;

    npc@ n = npcs[npc_index];
    player@ p = players[target_player];

    // Calcular dano
    int damage = n.attack_power - p.defense;
    if(damage < 1) damage = 1;

    // Aplicar dano
    p.health -= damage;

    // Notificar
    send_reliable(p.peer_id, "msg2 " + n.name + " atacou você! -"+damage+" HP", 0);
}
```

---

### 5. Sistema de Inventário Real (item_take/item_give)
**Arquivo:** `stubs.nvgt:397-413`
**Status:** Apenas logs

#### Funções Afetadas:
```cpp
bool item_take(int player_index, string item_name, int quantity)
// Atualmente: apenas debug_log, sempre retorna true

bool item_give(int player_index, string item_name, int quantity)
// Atualmente: apenas debug_log, sempre retorna true
```

#### Por que implementar:
- **Gameplay:** Sistema essencial
- **Economia:** Transferência de itens
- **Crafting:** Consumir/criar itens
- **Loot:** Pegar itens do chão

#### Implementação Sugerida:
```cpp
bool item_take(int player_index, string item_name, int quantity) {
    if(player_index < 0) return false;

    // Verificar se jogador tem o item
    if(!players[player_index].inv_item_exists(item_name)) {
        return false;
    }

    int current = players[player_index].inv_item_number(item_name);
    if(current < quantity) {
        return false; // Não tem quantidade suficiente
    }

    // Remover item
    players[player_index].inv_remove_item(item_name, quantity);
    return true;
}

bool item_give(int player_index, string item_name, int quantity) {
    if(player_index < 0) return false;

    // Verificar se tem espaço (peso/slots)
    if(!can_add_to_inventory(player_index, item_name, quantity)) {
        send_reliable(players[player_index].peer_id,
            "msg2 Inventário cheio!", 0);
        return false;
    }

    // Adicionar item
    players[player_index].inv_add_item(item_name, quantity);
    return true;
}
```

---

### 6. Sistema de Mudança de Mapa
**Arquivo:** `stubs.nvgt:46-50`
**Status:** Apenas log

#### Função Afetada:
```cpp
void changemap(string player, string new_map)
// Atualmente: apenas debug_log
```

#### Por que implementar:
- **Navegação:** Essencial para mundo aberto
- **Teleportes:** Portais entre mapas
- **Comandos Admin:** /changemap
- **Eventos:** Mover jogadores para arenas

#### Implementação Sugerida:
```cpp
void changemap(string player_name, string new_map) {
    int index = get_player_index_from(player_name);
    if(index < 0) return;

    // Salvar posição atual
    save_player_position(index);

    // Mudar mapa
    players[index].map = new_map;
    players[index].x = 0;  // Spawn do novo mapa
    players[index].y = 0;

    // Notificar cliente
    send_reliable(players[index].peer_id,
        "changemap " + new_map + " 0 0", 0);

    // Log
    log_action(player_name, "changemap", new_map,
               new_map, 0, 0, 0);
}
```

---

### 7. Sistema Temporal (Uptime)
**Arquivo:** `stubs.nvgt:52-58`
**Status:** Retorna 0

#### Funções Afetadas:
```cpp
int upw()  // Uptime weeks
int upd()  // Uptime days
int uph()  // Uptime hours
int upm()  // Uptime minutes
int ups()  // Uptime seconds
// Todos retornam 0
```

#### Por que implementar:
- **Info:** Mostrar tempo de servidor online
- **Stats:** Calcular métricas por período
- **Eventos:** Agendar por uptime
- **Admin:** Monitorar estabilidade

#### Implementação Sugerida:
```cpp
timer server_start_time;

int ups() { return int(server_start_time.elapsed / 1000); }
int upm() { return ups() / 60; }
int uph() { return upm() / 60; }
int upd() { return uph() / 24; }
int upw() { return upd() / 7; }
```

---

### 8. Sistema de Equipes
**Arquivo:** `stubs.nvgt:120-124`
**Status:** Retorna false

#### Função Afetada:
```cpp
bool emequipe(string player1, string player2)
// Sempre retorna false
```

#### Por que implementar:
- **PvP:** Friendly fire control
- **Parties:** Grupos de jogadores
- **Raids:** Times para dungeons
- **Social:** Sistema de clãs/guildas

#### Implementação Sugerida:
```cpp
// Criar teams.nvgt
class team {
    string name;
    string[] members;
    string leader;

    bool is_member(string player) {
        for(uint i = 0; i < members.length(); i++) {
            if(members[i] == player) return true;
        }
        return false;
    }
}

team@[] teams;

bool emequipe(string player1, string player2) {
    for(uint i = 0; i < teams.length(); i++) {
        if(teams[i].is_member(player1) &&
           teams[i].is_member(player2)) {
            return true;
        }
    }
    return false;
}
```

---

### 9. Sistema de Guardacofres (Safes)
**Arquivo:** `stubs.nvgt:96-102`
**Status:** Placeholder

#### Classe Afetada:
```cpp
class guardacofre_placeholder {
    int x, y;
    string map;
    int vida = 1000;
    string golpeado = "";
}
guardacofre_placeholder@[] guardacofres;
```

#### Por que implementar:
- **Armazenamento:** Baús/cofres seguros
- **Economia:** Guardar itens valiosos
- **Proteção:** Sistema de senhas/chaves
- **Gameplay:** Objetivos para roubo/defesa

---

### 10. Sistema de Roupas/Armaduras
**Arquivo:** `stubs.nvgt:183-194`
**Status:** Placeholder

#### Funções Afetadas:
```cpp
bool has_clothe(int player_index, string clothe_name)
// Sempre retorna false

class clothes_placeholder {
    string name = "";
    int protection = 0;
    bool enable_degradation = false;
    int degradation = 0;
}
```

#### Por que implementar:
- **Defesa:** Sistema de proteção
- **Visual:** Customização de personagem
- **Economia:** Items de valor
- **Durabilidade:** Degradação de equipamento

---

### 11. Sistema de Descrições de Itens
**Arquivo:** `stubs.nvgt:275-276, 341-344`
**Status:** Retorna string vazia

#### Funções Afetadas:
```cpp
string getdesc(string map, int x, int y)  // Retorna ""
string getdesc(string item_name)         // Retorna ""
```

#### Por que implementar:
- **UX:** Informações sobre itens
- **Tooltip:** Descrições detalhadas
- **Localização:** Descrições de lugares
- **Tutorial:** Ajudar novos jogadores

---

## 🟠 PRIORIDADE MÉDIA (15 itens)

### 12. Sistema de Mensagens Admin
**Arquivo:** `stubs.nvgt:60-74`
**Status:** Funcional básico

```cpp
string[] msgadm_array;
void msgadm(string message)
```

**Melhorias:** Adicionar persistência, filtros, categorias

---

### 13. Sistema de Objetos Magnéticos
**Arquivo:** `stubs.nvgt:104-109`
**Status:** Stubs vazios

```cpp
void update()
void update(string map)
void update2()
void update2(string map)
timer tmina2;
```

**Funcionalidade:** Puxar itens para jogador com imã

---

### 14. Seleção Inteligente de Jogador
**Arquivo:** `stubs.nvgt:111-118`
**Status:** Retorna primeiro jogador

```cpp
string selecionar_jogador(string criteria)
```

**Melhorias:** Implementar critérios (mais próximo, mais fraco, etc)

---

### 15. Loop de Rede para Objetos
**Arquivo:** `stubs.nvgt:137-141`
**Status:** Vazio

```cpp
void netloop()
```

**Funcionalidade:** Sincronizar objetos do mundo pela rede

---

### 16. Sistema de Arena
**Arquivo:** `stubs.nvgt:168-179`
**Status:** Placeholder

```cpp
class arena_placeholder {
    int counter_deaths = 0;
    void remove_player_from(int player_index)
    void reset()
}
```

**Funcionalidade:** Arena PvP completa com ranking

---

### 17. Eventos de Mensagem
**Arquivo:** `stubs.nvgt:163-167`
**Status:** Retorna vazio

```cpp
string get_event_message()
```

**Funcionalidade:** Sistema de eventos/notícias do servidor

---

### 18. Sistema de Moderação
**Arquivo:** `stubs.nvgt:288-289`
**Status:** Retorna false

```cpp
bool is_mod(int player_index)
```

**Funcionalidade:** Permissões de moderador (entre player e admin)

---

### 19. Configurações do Servidor
**Arquivo:** `stubs.nvgt:313-318`
**Status:** Placeholder

```cpp
class sconfigs_placeholder {
    int max_players = 100;
    string server_name = "EVM Server";
}
```

**Melhorias:** Carregar de arquivo config.ini

---

### 20. Funções de Config (ge/gc)
**Arquivo:** `stubs.nvgt:320-322, 346-349`
**Status:** Retorna vazio

```cpp
string ge(string key)
string gc(string key)
string gc(string key, int default_value)
```

**Funcionalidade:** Get config/Get emerald settings

---

### 21-26. Outros stubs médios
- `save_transfer()` - Log de transferências (271-273)
- `eadm()` - Log admin especial (279-281)
- `log()` - Log categorizado (284-286)
- `game_disabled_data` - Jogo desabilitado global (307-311)
- `changename()` - Mudar nome de jogador (258)
- `exists_player_in_my_map()` - Verificar jogadores (336-339)

---

## 🟡 PRIORIDADE BAIXA (26 itens)

### 27-52. Comandos não implementados
**Arquivo:** `commands.nvgt:383-796`

#### Comandos Stub:
- `/time` - Ver tempo de jogo (431)
- `/quit` - Sair graciosamente (444)
- `/inventory` - Ver inventário (491)
- `/freeze` - Congelar jogo (513)
- `/backup` - Backup manual (520)
- `/forcedc` - Desconectar forçado (556)
- `/defend` - Sistema de defesa (795-796)

#### Sistemas não integrados:
- Sistema de equipamentos detalhado (combat.nvgt:162)
- Spawn de maxbomba em helicoptero (helicoptero.nvgt:67)
- Zonas desabilitadas em globals (globals.nvgt:344)
- Reload de world_items (items.nvgt:565)
- Player direction para som 3D (msound.nvgt:117)
- Verificação de mapa em network (network.nvgt:110)
- Sistema de fogo contínuo em player (player.nvgt:2118)
- Timer concatenation em server_map (server_map.nvgt:587)
- Acesso a weapons array (server_map.nvgt:890,919,939,1036,1050)
- Construtor NPC compatível (server_map.nvgt:1260,1282)
- Reload de configs do jogador (var_management.nvgt:240)
- Verificação de ban (auth.nvgt:128)
- Cópia de arquivos (admin_commands.nvgt:134)
- Timer com callback (admin_commands.nvgt:158)

---

## 📈 Estatísticas

| Categoria | Quantidade | % |
|-----------|------------|---|
| Crítica | 11 | 21% |
| Média | 15 | 29% |
| Baixa | 26 | 50% |
| **TOTAL** | **52** | **100%** |

---

## 🎯 Roadmap de Implementação Sugerido

### Fase 1 - Sistemas Essenciais (2-3 semanas)
1. Sistema de Inventário Real (item_take/item_give)
2. Sistema de Experiência (ganhaxp, level up)
3. Sistema de Mudança de Mapa (changemap)
4. Funções de Uptime (ups, upm, uph, etc)

### Fase 2 - Gameplay Core (2-3 semanas)
5. Sistema de NPC (IA básica)
6. Sistema de Histórico (action logs)
7. Sistema de Estatísticas
8. Sistema de Equipes

### Fase 3 - Features Avançadas (3-4 semanas)
9. Sistema de Guardacofres
10. Sistema de Roupas/Armaduras
11. Sistema de Arena
12. Sistema de Descrições

### Fase 4 - Polimento (1-2 semanas)
13. Todos os comandos pendentes
14. Integrações faltantes
15. Otimizações
16. Testes completos

---

## 💡 Próximos Passos

1. **Priorizar:** Escolher 3-5 funções mais críticas
2. **Planejar:** Definir arquitetura de cada sistema
3. **Implementar:** Código + testes
4. **Integrar:** Conectar com sistemas existentes
5. **Documentar:** Atualizar docs

---

## 🔧 Template de Implementação

Para cada função stub, seguir:

```cpp
// 1. Remover stub de stubs.nvgt
// 2. Criar arquivo dedicado (ex: history.nvgt)
// 3. Implementar funcionalidade completa
// 4. Adicionar ao server.nvgt (#include)
// 5. Integrar com sistemas existentes
// 6. Testar + documentar
```

---

**Status:** ✅ Análise completa
**Última atualização:** 2025-10-03
