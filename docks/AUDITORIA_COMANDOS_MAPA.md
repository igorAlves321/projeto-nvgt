# 🗺️ Auditoria Completa de Comandos de Mapa

## Data: 6 de novembro de 2025

### 📋 Lista de Todos os Comandos Encontrados nos Mapas

Análise de **4658 arquivos `.map`** no servidor.

---

## ✅ Comandos Implementados

| Comando | Aliases | Status | Função | Linha |
|---------|---------|--------|--------|-------|
| `map` | - | ✅ | Nome do mapa | 149 |
| `maxx` | - | ✅ | Limite X | 218 |
| `maxy` | - | ✅ | Limite Y | 222 |
| `x` | - | ✅ | Posição X inicial | 226 |
| `y` | - | ✅ | Posição Y inicial | 230 |
| `platform` | `p` | ✅ | Plataformas | 174 |
| `wall` | `w`, `pwall` | ✅ | Paredes | 183 |
| `zone` | `z` | ✅ | Zonas | 192 |
| `door` | `dr`, `porta` | ✅ | Portas | 209 |
| `sound_source` | `ss`, `som` | ✅ | Sons 3D | 234 |
| `staircase` | `sc` | ✅ | Escadas | 243 |
| `texto` | `txt` | ✅ | Textos descritivos | 254 |
| `areia_movedissa` | `am` | ✅ | Areia movediça | 261 |
| `desc` | `dv` | ✅ | Disable View | 269 |
| `safezone` | `safez` | ✅ | Zonas seguras | 302 |
| `teto` | - | ✅ | Teto/ceiling | 171 |
| `dialog` | `dlg` | ✅ | Diálogos | 265 |
| `ss2` | - | ✅ | Streams de áudio | 277 |
| `url` | - | ✅ | URL de stream | 158 |

---

## ⚠️ Comandos Parcialmente Implementados

| Comando | Aliases | Status | Implementação | Impacto |
|---------|---------|--------|---|---|
| `store` | - | ⚠️ | Não procurado | Itens de loja não carregam |
| `item` | - | ⚠️ | Não procurado | Itens do mapa não carregam |

---

## ❌ Comandos NÃO Implementados

### 🔴 CRÍTICOS (causam erros)

| Comando | Uso | Status | Alternativa |
|---------|-----|--------|---|
| `tp` | Travel Point (Teleportes) | ❌ Ignorado | Usar `tp:...` para entrar/sair de mapas |
| `travelpoint` | Teleportes (nome completo) | ❌ Ignorado | Alias para `tp` |
| `where` | Descrição de localização | ❌ Ignorado | TTS ao entrar no mapa |
| `pm2` | Plataforma 2 (tipo especial) | ❌ Ignorado | Ignorar silenciosamente |
| `w2` | Parede 2 (tipo especial) | ❌ Ignorado | Ignorar silenciosamente |
| `ex` | Saída de emergência? | ❌ Ignorado | Investigar uso |

### 🟡 INCOMUNS (aparição rara ou obsoletos)

| Comando | Uso | Status | Notas |
|---------|-----|--------|-------|
| `arbol` | Árvore | ❌ Não procurado | Similar a `sc` (escada) - BGT suporta |
| `npc` | NPC | ❌ Não procurado | Pode ser para NPCs dinâmicos |
| `pnpc` | NPC posição | ❌ Não procurado | Similiar a `npc` |
| `monstruo` | Monstro | ❌ Não procurado | Para spawnar inimigos |
| `cpm` | Desconhecido | ❌ Não procurado | Padrão desconhecido |
| `ptm` | Desconhecido | ❌ Não procurado | Padrão desconhecido |
| `rt` | Desconhecido | ❌ Não procurado | Padrão desconhecido |
| `pm` | Mensagem privada? | ❌ Ignorado | Pode ser duplicado com chat |
| `lv` | Level/nível | ❌ Não procurado | Para definir nível do mapa? |
| `darmas` | Desabilitar armas | ⚠️ Parcial | BGT tem `dv:armas`, não `darmas:` |
| `congelar` | Congelar movimento | ❌ Ignorado | Efeito ambiental |
| `disable_game` | Desabilitar jogo | ❌ Não procurado | Efeito especial |
| `newymap` | Novo mapa? | ❌ Não procurado | Desconhecido |
| `asfixiar` | Asfixiar | ❌ Não procurado | Dano ambiental |
| `death` | Morte | ❌ Não procurado | Zona de morte? |

---

## 📊 Resumo Estatístico

**Total de comandos únicos encontrados**: 50

| Categoria | Quantidade | Percentual |
|-----------|-----------|-----------|
| ✅ Implementados | 19 | 38% |
| ⚠️ Parcialmente | 2 | 4% |
| ❌ Não implementados | 29 | 58% |

---

## 🎯 Prioridade de Implementação

### 1️⃣ IMEDIATO (Essenciais para gameplay)
- [ ] `tp` / `travelpoint` - Sem isso, não há navegação entre mapas
- [ ] `where` - Sem isso, player não sabe onde está
- [ ] `item` / `store` - Sem isso, não há objetos/itens

### 2️⃣ PRÓXIMAS (Importantes para features)
- [ ] `arbol` - Semelhante a `sc` (já parcialmente suportado)
- [ ] `pm` - Para marcar pontos de entrada
- [ ] `monstruo` / `npc` - Para inimigos e NPCs dinâmicos

### 3️⃣ FUTUROS (Enhancements)
- [ ] `congelar` / `asfixiar` / `death` - Efeitos ambientais
- [ ] `cpm`, `ptm`, `rt`, `lv`, `newymap` - Investigar uso

---

## 🔍 Investigação Adicional Necessária

1. **`arbol`**: Aparece em mapas? Se sim, implementar
2. **`pm`, `pm2`, `ptm`, `cpm`**: Definir padrão
3. **`monstruo`, `npc`, `pnpc`**: Suportar spawning de inimigos?
4. **`congelar`, `asfixiar`, `death`**: Investigar uso real
5. **`item` vs `store`**: Qual a diferença?

---

## 📝 Próximas Etapas

1. **Implementar `tp`** (Travel Points) - CRÍTICO
2. **Implementar `where`** - CRÍTICO
3. **Implementar `item`** - ALTO
4. **Investigar** outros 26 comandos

---

**Última Atualização**: 6 de novembro de 2025
**Status**: Em análise
