# Plano de refatoracao NVGT

Este documento guia a refatoracao incremental do projeto IG em NVGT/AngelScript. A prioridade e melhorar legibilidade, coerencia arquitetural e manutencao sem alterar comportamento de jogo por acidente.

## Principios

- Fazer mudancas pequenas, compilaveis e commitadas separadamente.
- Preservar comportamento existente antes de mudar regra de negocio.
- Preferir separacao por dominio em vez de arquivos genericos gigantes.
- Reduzir globais dispersos gradualmente, sem quebrar includes existentes.
- Usar handles `@` para objetos compartilhados e checar nulidade quando aplicavel.
- Manter codigo compativel com os padroes atuais enquanto a estrutura nova nasce.
- Validar cada etapa com compilacao do cliente e do servidor.

## Diagnostico atual

Arquivos NVGT ainda concentrados demais:

- `server/server.nvgt`: inicializacao, banco, rede, comandos legados e loop principal.
- `server/includes/server_map.nvgt`: dados de mapa, carregamento, interacao, objetos e regras de ambiente.
- `cliente/includes/menu.nvgt`: menu principal, opcoes, lojas, midia, social, inventario e formularios.
- `cliente/includes/net.nvgt`: login, mensagens de mapa, inventario, social, audio, combate e fallback.
- `server/includes/commands.nvgt`: registro e execucao de comandos de muitos dominios.
- `cliente/includes/globals.nvgt`: grande volume de estado global do cliente.
- `cliente/client.nvgt`: bootstrap, loop de jogo, input, movimento, audio e heartbeat.

## Etapas

### 1. Mapa arquitetural

Criar este plano e manter nele o estado das decisoes de refatoracao. Nenhuma mudanca de comportamento deve acontecer nesta etapa.

### 2. Estado global do cliente

Extrair grupos de variaveis de `cliente/includes/globals.nvgt` para arquivos menores, mantendo os mesmos nomes globais inicialmente para reduzir risco.

Arquivos alvo iniciais:

- `cliente/includes/state/client_config.nvgt`
- `cliente/includes/state/client_session.nvgt`
- `cliente/includes/state/client_audio_state.nvgt`
- `cliente/includes/state/client_movement_state.nvgt`
- `cliente/includes/state/client_ui_state.nvgt`

Aceite:

- O cliente compila.
- O servidor compila.
- Nenhum nome global usado pelo codigo atual desaparece.

### 3. Menus do cliente

Separar `cliente/includes/menu.nvgt` por dominio, mantendo `menu.nvgt` como fachada temporaria.

Arquivos alvo:

- `cliente/includes/menus/main_menu.nvgt`
- `cliente/includes/menus/options_menu.nvgt`
- `cliente/includes/menus/social_menu.nvgt`
- `cliente/includes/menus/store_menu.nvgt`
- `cliente/includes/menus/media_menu.nvgt`
- `cliente/includes/menus/inventory_menu.nvgt`

Aceite:

- Menus existentes continuam chamaveis pelos mesmos nomes de funcao.
- Navegacao principal, opcoes e social compilam sem mudanca de protocolo.

### 4. Loop principal do cliente

Extrair partes de `cliente/client.nvgt` para controladores simples.

Arquivos alvo:

- `cliente/includes/client_loop/input_loop.nvgt`
- `cliente/includes/client_loop/movement_controller.nvgt`
- `cliente/includes/client_loop/audio_listener.nvgt`
- `cliente/includes/client_loop/heartbeat_client.nvgt`

Aceite:

- `game()` fica menor e mais legivel.
- Movimento, rotacao, heartbeat e audio posicional continuam compilando.

### 5. Rede do cliente

Dividir handlers de `cliente/includes/net.nvgt` por dominio e centralizar nomes de protocolo.

Arquivos alvo:

- `cliente/includes/net/login_handlers.nvgt`
- `cliente/includes/net/map_handlers.nvgt`
- `cliente/includes/net/inventory_handlers.nvgt`
- `cliente/includes/net/social_handlers.nvgt`
- `cliente/includes/net/combat_handlers.nvgt`
- `cliente/includes/net/protocol_names.nvgt`

Aceite:

- Protocolos modernos como `FRIEND:list` ficam centralizados.
- Fallbacks continuam visiveis e rastreaveis.

### 6. Servidor principal e comandos

Reduzir `server/server.nvgt` para inicializacao, roteamento e loop principal. Depois dividir `server/includes/commands.nvgt` por dominio.

Arquivos alvo:

- `server/includes/commands/player_commands.nvgt`
- `server/includes/commands/social_commands.nvgt`
- `server/includes/commands/inventory_commands.nvgt`
- `server/includes/commands/store_commands.nvgt`
- `server/includes/commands/combat_commands.nvgt`

Aceite:

- Registro de comandos permanece centralizado ou claramente roteado.
- Comandos publicos e administrativos preservam aliases existentes.

### 7. Mapa e jogador

Refatorar `server/includes/server_map.nvgt` e `server/includes/player.nvgt` em fatias pequenas, por comportamento.

Possiveis dominios:

- objetos no chao
- zonas/interacoes
- portas/elevadores
- dano/morte
- persistencia de player
- estado social do player

Aceite:

- Cada mudanca deve tocar um dominio por vez.
- Compilacao obrigatoria a cada commit.

### 8. Padronizacao e limpeza

Padronizar nomes, comentarios, encoding e remover codigo morto com aprovacao quando houver risco.

Alvos:

- comentarios antigos de task/debug que nao ajudam manutencao
- arquivos `.bgt` que sejam apenas referencia e possam sair do fluxo principal
- mensagens sem acento ou com mojibake
- includes e nomes inconsistentes

## Rotina de cada etapa

1. Fazer a menor mudanca coerente.
2. Compilar cliente.
3. Compilar servidor.
4. Revisar `git diff`.
5. Commitar com mensagem clara.
6. Avancar para a proxima etapa.
