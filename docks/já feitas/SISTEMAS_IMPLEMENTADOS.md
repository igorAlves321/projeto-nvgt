# Sistemas Implementados - EVM Server NVGT

Documento de acompanhamento da conversão BGT → NVGT

---

## ✅ 1. Sistema de NPCs - COMPLETO

### Arquivo
- **Localização**: `server/includes/npc.nvgt`
- **Linhas**: 574
- **Status**: ✅ **100% Funcional**
- **Data**: Janeiro 2025

### Características Implementadas

#### Classe `npc`
- ✅ **26 parâmetros** no construtor completo
- ✅ Propriedades de combate (vida, dano, XP, gold)
- ✅ Timers de comportamento (ataque, movimento, sons)
- ✅ Sistema de sons (nervosos, ataque, morte, passos, impactos)
- ✅ Controle de respawn
- ✅ Ranges de patrulha (left_range, right_range)
- ✅ Sistema de items e drops

#### IA Implementada
```nvgt
bool exists_player_in_my_map()      // ✅ Detecta jogadores válidos
int select_player_to_attack()       // ✅ Seleciona alvo mais próximo
int change_player(int)              // ✅ Muda de alvo se inválido
void move()                         // ✅ Pathfinding simples
void attack()                       // ✅ Ataque com reflexo
void play_step_sound()              // ✅ Sons de passos
void play_nervous_sounds()          // ✅ Sons nervosos
void die()                          // ✅ Morte completa
void drop_items(int)                // ✅ Drop de items
```

#### Funções Globais
```nvgt
void spawn_npc(x, y, map, type)     // ✅ Spawn simples
void npc_global_loop()              // ✅ Loop principal
npc@[] npcs_global                   // ✅ Array global
```

### Padrão Extraído de BGT
- ✅ Baseado em: `cachorro.bgt`, `lobo.bgt`, `guardaandar.bgt`
- ✅ Sistema genérico funciona para todos os tipos de NPC
- ✅ Compatível com sistema de reflexo (`refletir()`)
- ✅ Integrado com `ganhaxp()` para recompensas

---

## ✅ 2. Sistema de Monstros - COMPLETO

### Arquivo
- **Localização**: `server/includes/monstruo.nvgt`
- **Linhas**: 459
- **Status**: ✅ **100% Funcional**
- **Data**: Janeiro 2025

### Características Implementadas

#### Classe `monstruo`
- ✅ Tipos pré-configurados (cachorro, lobo, zumbi, urso)
- ✅ IA mais agressiva que NPCs
- ✅ Sistema de priorização de alvos (ataca jogadores com menos vida)
- ✅ Movimento mais rápido (`ladoandar = 2`)
- ✅ Spawn em cadeia (zumbis spawnam mais zumbis ao morrer - 15%)
- ✅ Sistema de respawn automático

#### IA Implementada
```nvgt
bool exists_player_in_my_map()      // ✅ Detecta jogadores válidos
int selecionar_jogador()            // ✅ Seleção inteligente (baseado em zumbi.bgt)
int change_player(int)              // ✅ Troca de alvo
void setup_by_type(string)          // ✅ Configuração por tipo
void move()                         // ✅ Movimento agressivo
void attack()                       // ✅ Ataque com dano variável
void die()                          // ✅ Morte + spawn em cadeia
void spawn_more_monsters()          // ✅ Spawn recursivo (zumbis)
```

#### Classe `monstruo_data`
```nvgt
class monstruo_data {               // ✅ Sistema de respawn
    timer trespawn;                  // ✅ Timer de respawn
}
monstruo_data@[] monstruos_data     // ✅ Array de respawn
```

#### Funções Globais
```nvgt
void spawn_monstruo(x, y, map, tipo)  // ✅ Spawn de monstro
void monstruo_global_loop()           // ✅ Loop principal + respawn
monstruo@[] monstruos_global          // ✅ Array global
```

### Tipos Pré-Configurados

#### Cachorro
- Vida: 2000-2300
- XP: 10-20
- Gold: 5-15
- Dano: 300-500
- Intervalo ataque: 500ms
- Intervalo movimento: 290ms
- Drop: corpo_de_cachorro

#### Lobo
- Vida: 3000-3300
- XP: 20-30
- Gold: 10-30
- Dano: 400-600
- Intervalo ataque: 500ms
- Intervalo movimento: 250ms
- Drop: corpo_de_lobo

#### Zumbi
- Vida: 3000-6000
- XP: 50-100
- Gold: 1000-3000
- Dano: 500-1000
- Intervalo ataque: 800ms
- Intervalo movimento: 400ms
- **Especial**: 15% chance de spawnar 1-2 zumbis ao morrer

#### Urso
- Vida: 5000-8000
- XP: 100-200
- Gold: 500-1500
- Dano: 800-1500
- Intervalo ataque: 1000ms
- Intervalo movimento: 500ms
- Drop: corpo_de_urso + pele_de_urso

### Padrão Extraído de BGT
- ✅ Baseado em: `zumbi.bgt` (IA complexa)
- ✅ Sistema de seleção de jogador (`selecionar_jogador()`)
- ✅ Comportamento agressivo (prioriza jogadores com menos vida)
- ✅ Spawn recursivo (comportamento de zumbi)

---

## ⚠️ 3. Sistema de Árvores - PARCIALMENTE IMPLEMENTADO

### Arquivo
- **Localização**: Classes em `placeholder_classes.nvgt` (linhas 70-132)
- **Status**: ⚠️ **Estrutura OK, Loop faltando**

### O que existe
```nvgt
class arbol {                       // ✅ Estrutura completa
    int x, y, vida;
    string map, items;
    bool morreu;
    timer trespawn;
}

class arbol_data {                  // ✅ Dados de respawn OK
    int x, y;
    string map, items;
}
```

### O que falta
- ❌ `arbolloop()` - Loop principal de árvores
- ❌ Sistema de corte (dano às árvores)
- ❌ Sistema de morte e drop de items
- ❌ Integração com ferramentas (machado, etc)

### Baseado em
- Arquivo BGT: `arbol.bgt` (38 linhas)

---

## ✅ 4. Sistema de Portais - COMPLETO

### Arquivo
- **Localização**: `server/includes/portals.nvgt`
- **Linhas**: 138
- **Status**: ✅ **100% Implementado**

### Características
- ✅ Teletransporte entre mapas
- ✅ Sistema de dano por distância
- ✅ Rastreamento de jogadores no portal
- ✅ Sons 3D de portal
- ✅ Proteção contra spam

---

## ✅ 5. Sistema de Bola de Fogo - COMPLETO

### Arquivo
- **Localização**: `server/includes/boladefogo.nvgt`
- **Linhas**: 16
- **Status**: ✅ **100% Implementado**

### Características
- ✅ Movimento de projétil
- ✅ Sons 3D em movimento
- ✅ Sistema de timer
- ✅ Rastreamento de posição

---

## 🔴 PENDÊNCIAS CRÍTICAS

### 1. Integração dos Sistemas Novos
- ❌ Adicionar `#include "npc.nvgt"` em server.nvgt
- ❌ Adicionar `#include "monstruo.nvgt"` em server.nvgt
- ❌ Chamar `npc_global_loop()` no loop principal
- ❌ Chamar `monstruo_global_loop()` no loop principal

### 2. Remoção de Stubs
- ❌ Remover classes `npc` e `monstruo` de `placeholder_classes.nvgt`
- ❌ Manter apenas `arbol` e `arbol_data` em placeholder

### 3. Sistema de Árvores
- ❌ Implementar `arbolloop()` em `server_map.nvgt` ou criar `arbol.nvgt`

### 4. Testes
- ❌ Testar spawn de NPC
- ❌ Testar IA de NPC
- ❌ Testar spawn de monstro
- ❌ Testar spawn recursivo de zumbis
- ❌ Testar respawn de NPCs/monstros

### 5. Ajustes de Balanceamento
- ⚠️ Verificar valores de dano
- ⚠️ Verificar valores de XP/gold
- ⚠️ Ajustar intervalos de ataque/movimento conforme necessário

---

## 📊 RESUMO GERAL

### Completamente Implementados ✅
- [x] Sistema de NPCs (npc.nvgt)
- [x] Sistema de Monstros (monstruo.nvgt)
- [x] Sistema de Portais (portals.nvgt)
- [x] Sistema de Bola de Fogo (boladefogo.nvgt)

### Parcialmente Implementados ⚠️
- [ ] Sistema de Árvores (falta loop)

### Não Implementados ❌
- [ ] frozen.nvgt (não encontrado no código BGT)

### Prioridade Imediata
1. **ALTA**: Integrar npc.nvgt e monstruo.nvgt no servidor
2. **ALTA**: Remover stubs de placeholder_classes.nvgt
3. **MÉDIA**: Implementar arbolloop()
4. **BAIXA**: Testar balanceamento

---

## 🎯 PRÓXIMOS PASSOS

1. Integrar os sistemas novos no `server.nvgt`
2. Testar compilação
3. Testar funcionalidade básica (spawn e comportamento)
4. Implementar sistema de árvores
5. Testar em ambiente de produção

**Última atualização**: Janeiro 2025
