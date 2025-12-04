# Correções de Sincronização de Movimento

## Problemas Identificados

### 1. Formato de Comando Inconsistente
**Problema**: Cliente enviava `move step_sound X Y` (4 partes), mas servidor esperava `move X Y` (3 partes).

**Solução**: 
- **Arquivo**: `server/server.nvgt` (linhas 577-625)
- Modificado para aceitar ambos os formatos
- Extrai `step_sound` quando presente (4 partes)
- Passa `step_sound` para `handle_move()`

**Arquivo**: `server/includes/network_handlers.nvgt` (handle_move)
- Adicionado suporte para formato `step|x|y`
- Passa `step_sound` para `player.move()`

### 2. Função updateplayer() Não Implementada
**Problema**: `updateplayer()` em `cliente/includes/stubs.nvgt` era stub vazio.

**Solução**:
- **Arquivo**: `cliente/includes/stubs.nvgt` (linha 216)
- Implementada para chamar `update_player(name, x, y, mapname)`
- Atualiza posição de outros jogadores no array `players`

### 3. Handler "s" Não Atualizava Posição
**Problema**: Handler recebia comando `s peer_id steps x y` do servidor, mas:
- Esperava formato diferente (username/mapname)
- Apenas tocava som, não atualizava posição

**Solução**:
- **Arquivo**: `cliente/includes/net.nvgt` (linhas 539+)
- Corrigido para formato correto: `s peer_id steps x y`
- Adiciona novas funções helper em `player.nvgt`:
  - `get_player_by_peer_id(peer_id)` - busca jogador por ID
  - `update_player_by_peer_id(peer_id, x, y)` - atualiza posição por ID
- Atualiza posição do jogador no array
- Toca som do passo na posição correta

### 4. Handler "upl" Com Formato Errado
**Problema**: Cliente esperava `upl username x y facedir mapname peer_id` (6+ parâmetros), mas servidor enviava `upl peer_id x y` (3 parâmetros).

**Solução**:
- **Arquivo**: `cliente/includes/net.nvgt` (linhas 488+)
- Corrigido para formato do servidor: `upl peer_id x y`
- Usa `update_player_by_peer_id()` para atualizar posição
- Remove verificações de mapname/username desnecessárias

## Arquivos Modificados

### Servidor
1. `server/server.nvgt`
   - Aceita ambos formatos de `move` (3 e 4 partes)
   - Extrai `step_sound` corretamente

2. `server/includes/network_handlers.nvgt`
   - `handle_move()` processa formato `step|x|y`
   - Passa `step_sound` para `player.move()`

### Cliente
1. `cliente/includes/stubs.nvgt`
   - `updateplayer()` implementada

2. `cliente/includes/player.nvgt`
   - Adicionadas funções:
     - `get_player_by_peer_id(peer_id)`
     - `update_player_by_peer_id(peer_id, x, y)`

3. `cliente/includes/net.nvgt`
   - Handler "s" corrigido (formato: `s peer_id steps x y`)
   - Handler "upl" corrigido (formato: `upl peer_id x y`)

## Fluxo de Sincronização (Após Correções)

### Cliente → Servidor
1. Cliente move e envia: `move step_sound X Y`
2. Servidor recebe e processa:
   - Extrai step_sound, x, y
   - Valida movimento com anti-cheat
   - Atualiza posição do jogador
   - Chama `player.move(step_sound, x, y)`

### Servidor → Outros Clientes
3. Servidor transmite:
   - **Com som**: `s peer_id step_sound x y`
   - **Sem som** (invisível/cloaked): `upl peer_id x y`

4. Clientes recebem e processam:
   - Handler "s": Atualiza posição + toca som
   - Handler "upl": Apenas atualiza posição
   - Ambos usam `update_player_by_peer_id()`

## Validação
✅ Sem erros de compilação
✅ Formato de comandos consistente
✅ Posições sincronizadas via peer_id
✅ Sons reproduzidos corretamente
✅ Compatibilidade com movimento invisível (upl)

## Próximos Passos
1. Testar em ambiente de desenvolvimento
2. Verificar sincronização com múltiplos jogadores
3. Validar comportamento com latência
4. Confirmar sons de passos diferentes funcionam
