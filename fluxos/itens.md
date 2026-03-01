# Fluxo de Itens no Jogo (NVGT)

Este documento descreve como o sistema de itens funciona hoje no projeto NVGT, compara com o legado BGT e aponta o que esta completo e o que ainda falta.

## 1. Visao geral (tipos de item no projeto)

No projeto atual existem 3 fluxos diferentes relacionados a itens:

1. Itens de inventario do jogador
- Ex.: `reais`, `euro`, consumiveis, armas, materiais.
- Ficam associados ao usuario/jogador.

2. Itens de mapa (objetos coletaveis com respawn)
- Ex.: linhas `item:x:y:...` dentro do mapa.
- Nao pertencem a um usuario ate serem coletados.

3. Definicao/cadastro de item (catalogo do jogo)
- Itens cadastrados no banco (`items`) e armas em `weapons_list.db`.
- Usado pelo construtor de itens administrativo.

## 2. Onde os itens sao armazenados hoje (NVGT)

### 2.1 Inventario por usuario

Servidor (fonte principal atual):
- Tabela `players.inventory` (JSON) no banco SQLite `server/database/ig.db`.
- Carregamento no login via `server/includes/load_player.nvgt`:
  - `load_player_inventory(...)`
  - `send_inventory_to_client(...)` (pacote `setinv ...`)

Servidor (legado ainda presente no codigo):
- `players/<usuario>/inv.md` em `server/includes/player.nvgt` (`load_inv`/`setinv`).
- Existe como compatibilidade, mas o fluxo principal ativo esta no SQLite.

Cliente:
- Inventario em memoria no `dictionary player_inv` (`cliente/includes/globals.nvgt`).
- Atualizacao por rede:
  - incremental: `inv ...` -> `load_inv(...)`
  - completo: `setinv ...` -> `setinv(...)`
- Categorias de inventario sao locais do cliente em `categories.db` (`cliente/includes/inv.nvgt`).

### 2.2 Itens de mapa (respawn/objeto)

Mapa:
- Persistidos como linha `item:...` no mapdata do mapa.
- Criados pelo builder do mapa (cliente envia `add_line::item:...`).

Servidor:
- Parse da linha `item` no carregamento de mapa em `server/includes/server_map.nvgt`.
- Objetos em runtime em arrays do mapa (`objs`, `objs_data`) com respawn/timeout.

### 2.3 Catalogo de itens (definicao global)

Servidor:
- Tabela `items` (SQLite) em `server/includes/items.nvgt`.
- Tabela `world_items` e `player_inventories` tambem sao criadas.
- Armas de fogo do construtor vao para `weapons_list.db` (`cmd_create_weapon_tool`).

## 3. Relacao item x usuario (fluxo funcional)

Fluxo principal:
1. Usuario loga.
2. Servidor carrega inventario do banco.
3. Servidor envia `setinv` apos `changemap`.
4. Cliente atualiza `player_inv`.
5. Durante o jogo, servidor envia atualizacoes `inv ...` quando ha alteracao.

Operacoes principais de item no jogador:
- Adicionar/remover: `player.inv_add_item(...)`, `inv_remove_item(...)` em `server/includes/player.nvgt`.
- Uso de consumivel: `use_item(...)` em `server/includes/consumables.nvgt`.
- Loja, trade e outras features usam `inv_add_item(...)` como base.

## 4. Construcao de itens (o que existe no NVGT)

## 4.1 Construcao de item de mapa (respawnavel)

Cliente:
- `F9` -> `Construtor de Mapas` -> `colocar itens respawnaveis no mapa`.
- Implementado em `cliente/includes/buildermenu.nvgt` (`builder_create_respawn_items`).
- Envia `add_line::item:x:y:timeout:0:qty:name:sound:respawn_time`.

Servidor:
- Recebe em `req_builder_create_element(...)` (`server/includes/builder.nvgt`).
- Roteia para `builder_create_item(...)`.
- Persiste no mapdata e passa a existir no mapa em runtime.

Status: completo para fluxo de item de mapa.

## 4.2 Construcao de item de inventario (catalogo)

Cliente:
- `F9` -> `Construtor de Itens` (`cliente/includes/item_builder.nvgt`).
- Cria:
  - arma de fogo (`/create_weapon_tool ...`)
  - arma melee, armadura, consumivel, misc (`/create_item_tool ...`)
- Lista itens (`/list_items`).

Servidor:
- `cmd_create_item_tool(...)` e `cmd_create_weapon_tool(...)` em `server/includes/admin_commands.nvgt`.
- `cmd_list_items(...)` lista itens do SQLite + `weapons_list.db`.

Status: parcial (criar e listar funciona; excluir/editar nao foi portado nesse fluxo).

## 5. Comparacao NVGT x BGT (diferencas reais)

No BGT:
- Havia menu `itemsmenu()` no builder (`cliente/includes/buildermenu.bgt`) com:
  - criar item (`newitem::...`)
  - listar (`list_items`)
  - excluir (`delete_item::...`)
- Definicoes de item de uso ficavam em `items.db` (`server/includes/item_in_inv.bgt`).

No NVGT:
- `itemsmenu()` do builder de mapas esta stubado:
  - `cliente/includes/buildermenu.nvgt:1389`
  - fala "Menu de itens ainda nao implementado"
- O fluxo novo foi separado para `Construtor de Itens` (admin menu), mas:
  - tem criar/listar
  - nao tem excluir/editar no mesmo nivel que o BGT antigo
- Parte da logica de `item_in_inv.bgt` foi migrada para `consumables.nvgt`, mas nao em formato 1:1 de editor legado.

## 6. O sistema de itens esta completo?

Resposta objetiva: nao, ainda nao esta 100% completo em relacao ao BGT legado.

### 6.1 O que esta funcional/estavel

- Inventario base por usuario (carregar, sincronizar, atualizar, usar, dar/remover via comandos).
- Itens de mapa respawnaveis via builder (`add_line::item`).
- Criacao de itens no banco (SQLite) e criacao de armas em `weapons_list.db`.
- Listagem administrativa de itens.

### 6.2 O que ainda falta ou esta parcial

1. Paridade total do `itemsmenu` legado do builder (BGT) no NVGT:
- criar/listar/excluir diretamente nesse menu ainda nao existe.

2. Exclusao/edicao de item no construtor novo:
- hoje ha `create` e `list`, sem `delete/edit` equivalente completo.

3. Inventario secundario (`invsec`) no cliente:
- `load_secondary_inventory(...)` esta TODO em `cliente/includes/stubs.nvgt`.

4. Partes de inventario avancado:
- `inventory_advanced.nvgt` tem funcoes com `TODO` (peso/slots calculados de forma incompleta).

5. Leilao novo:
- `auction.nvgt` ainda tem `TODO` para validacao/entrega real de item em alguns pontos.

## 7. Conclusao pratica

Se a pergunta for "o jogador consegue usar itens e jogar normalmente?":
- Sim, o nucleo de inventario e uso de item funciona.

Se a pergunta for "a construcao de itens esta completa como no BGT?":
- Ainda nao.
- Falta fechar paridade de edicao/exclusao e finalizar stubs/partes incompletas do fluxo administrativo e de inventario secundario.

