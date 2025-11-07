# 🚀 Próximas Implementações - Comandos Críticos

## Data: 6 de novembro de 2025

### 📊 Análise de Uso nos Mapas

| Comando | Ocorrências | Prioridade | Status |
|---------|------------|-----------|--------|
| `ptm` | **473** | 🔴 CRÍTICO | ❌ NÃO IMPL. |
| `npc` | **432** | 🔴 CRÍTICO | ❌ NÃO IMPL. |
| `death` | 101 | 🟠 ALTO | ❌ NÃO IMPL. |
| `pm` | 43 | 🟡 MÉDIO | ❌ NÃO IMPL. |
| `cpm` | 29 | 🟡 MÉDIO | ❌ NÃO IMPL. |
| `disable_game` | ? | 🟡 MÉDIO | ❌ NÃO IMPL. |
| `darmas` | ? | 🟡 MÉDIO | ❌ NÃO IMPL. |
| `arbol` | ? | 🟢 BAIXO | ❌ NÃO IMPL. |
| `congelar` | 2 | 🟢 BAIXO | ❌ NÃO IMPL. |
| `reverb` | 0 | ⚫ IGNORAR | ❌ N/A |

---

## 🎯 Estratégia de Implementação

### 1️⃣ FASE 1 - CRÍTICO (473 + 432 = 905 ocorrências)

#### `ptm` - Portal/Teleporte Customizado
**Ocorrências: 473**
**Formato**: `ptm:x1:y1:x2:y2:dest_x:dest_y:dest_map:mensagem:som`

Similar a `tp` mas com som customizado. Exemplo:
```
ptm:15:15:45:45:17:71:cueva_de_anelyem:Gusto conocerte, pero....:fire2
```

**Impacto**: Sem isso, 473 teleportes não funcionam!

#### `npc` - Inimigos/NPCs
**Ocorrências: 432**
**Formato**: `npc:x:y:hp:mp:atk:def:speed:x_range:y_range:z_range:rewards:sounds:animations:drops:name:message:exp:drops_gold:drops_item:drops_special:stance:respawn_time:difficulty:scale`

Muito complexo. Requer:
- Sistema de combat
- Pathfinding
- Item drops
- Animations

**Impacto**: Sem isso, 432 inimigos não aparecem!

---

### 2️⃣ FASE 2 - ALTO (101 ocorrências)

#### `death` - Zona de Morte
**Ocorrências: 101**
**Formato**: `death:x1:y1:x2:y2:dest_x:dest_y:dest_z:mensagem:som:unk1:unk2`

Zona que mata player e o teleporta para spawn.

**Impacto**: Sem isso, 101 zonas de morte não funcionam!

---

### 3️⃣ FASE 3 - MÉDIO (43 + 29 = 72 ocorrências)

#### `pm` - Ponto de Entrada/Pickup
**Ocorrências: 43**
**Formato**: `pm:x1:y1:x2:y2:dest_x:dest_y:dest_map:mensagem:som:item_type:unk1`

Similar a `ptm` mas com sistema de items.

#### `cpm` - Customized Portal/Message
**Ocorrências: 29**
**Formato**: `cpm:x1:y1:x2:y2:dest_x:dest_y:dest_map:travel_msg:color:travel_time:arrival_msg:effect`

Com tempo de viagem customizado.

---

## ⚡ Recomendação

### Implementação Rápida (Prioridade)
1. **`ptm`** - Cópia de `tp` com som customizado (30 min)
2. **`death`** - Zona de morte com teleporte (20 min)
3. **`pm`** - Modificação de `ptm` com item (20 min)

### Implementação Futura (Complexa)
4. **`npc`** - Sistema completo de inimigos (2-3 horas)
5. **`cpm`** - Viagem customizada com tempo (30 min)

### Implementação Opcional
6. **`disable_game`**, **`darmas`**, **`arbol`**, **`congelar`** - Verificar uso

---

## 📝 Próximas Etapas

1. Implementar `ptm` (copiar lógica de `tp`)
2. Implementar `death` (zona com teleporte)
3. Implementar `pm` (combinação de `ptm` + item)
4. Testar compilação
5. Depois investigar `npc` e `cpm`

---

**Status**: 🟡 PLANEJAMENTO COMPLETO

