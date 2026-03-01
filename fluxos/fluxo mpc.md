# Fluxo de MPC no Jogo (NVGT)

Este documento cobre o fluxo completo de MPC/NPC no jogo, comparando com o BGT e explicando o que foi ajustado no NVGT.

## 1. Permissao para construir MPC

Para abrir o menu administrativo no cliente (F9), o jogador precisa ser um destes:
- dev
- admin
- moderador
- builder

No servidor, para aceitar construcao com `add_line::`, a validacao real e:
- `rank >= 3`, ou
- `constructor`, ou
- `dev`, ou
- `admin`

Resumo: abrir F9 nao garante construcao. Quem manda e a validacao do servidor.

## 2. Entrada no fluxo in-game

1. Entrar no jogo e logar.
2. Pressionar `F9`.
3. Entrar em `Construtor de Mapas`.
4. Escolher `Bots` (MPC).
5. O cliente chama `builder_create_bot()`.

## 3. Criacao de MPC (cliente -> servidor)

O builder de MPC no cliente abre 3 formularios e 2 confirmacoes (sim/nao), depois envia:
- `add_line::npc:<25 campos>`

Ordem do payload `npc:`:
1. x
2. y
3. vida
4. xp
5. attack_dist
6. damage_received
7. damage_dealt
8. mirror_damage
9. attack_time
10. walk_time
11. calm_time
12. items_drop
13. attack_sounds
14. calm_sounds
15. death_sound
16. npc_name
17. death_msg
18. respawn_time
19. multi_respawn (0/1)
20. bomb_damage (0/1)
21. footsteps
22. x_min
23. x_max
24. hit_sounds
25. degradation

## 4. Recepcao no servidor

Fluxo de rede:
1. servidor recebe `add_line::...`
2. chama `req_builder_create_element(...)`
3. identifica `element_type == "npc"`
4. chama `builder_create_npc(...)`
5. cria objeto `npc` e adiciona em `current_map.npcs`
6. persiste a linha no mapdata (`current_map.add_line(element_data)`)

## 5. Compatibilidade BGT x NVGT (estado atual)

Os dois agora estao alinhados no fluxo principal de criacao de MPC:
- mesma estrutura de payload `npc:`
- mesma ordem de campos de construcao
- mesmo formato de linha em mapa (`npc:...`)

Ajustes aplicados no NVGT:
- Correcao da ordem dos parametros em `builder_create_npc`.
  Antes estava mapeando campos em posicoes erradas.
- Compatibilidade de separadores para listas de MPC:
  - aceita `,` (BGT) e `|` (NVGT)
  - aplicado para itens, sons de ataque, sons calmos, passos e hit_sounds
- Drops aceitando os dois formatos:
  - `item:quantidade` (NVGT)
  - `item.quantidade` (BGT)
- Sons de ataque/calm/death normalizados para `.ogg` quando necessario.
- Passos no estilo BGT:
  - `default` usa piso atual do mapa
  - lista de passos escolhe aleatorio e monta `stepN.ogg`
- Hit sounds de bala agora tratados como lista (igual comportamento BGT).

## 6. Atualizacao e salvamento

Depois de construir MPC:
1. usar `/savemap`
2. usar `/mapupdate` (ou `/mapupdate <nome_mapa>`)

Sem salvar, alteracoes podem sumir ao reiniciar.

## 7. Edicao e exclusao de MPC

Hoje nao existe comando dedicado para "deletar MPC por id" diretamente.

Mas agora existe undo funcional do ultimo elemento criado via builder:
- cliente envia `undo_last::<linha>`
- servidor remove do array em memoria e de `mapdata`
- tipos suportados no undo: `npc`, `item`, `p/platform/sc`, `w/wall/pwall`, `z`, `sz`, `rt`, `lv`, `ex`, `dr/door`, `ss`, `txt`, `tp`, `maxx`, `maxy`, `teto`, `dv`

Para MPC especificamente:
1. criar MPC
2. se precisar desfazer imediato, usar `Desfazer` no builder (usa `undo_last::`)
3. salvar (`/savemap`) e atualizar (`/mapupdate`)

Regra para tipos globais:
- em `maxx`, `maxy`, `teto` e `dv`, o servidor remove a linha e recompõe o estado runtime a partir do `mapdata` restante.

## 8. Arquivos chave do fluxo MPC

Cliente:
- `cliente/includes/buildermenu.nvgt`

Servidor:
- `server/server.nvgt`
- `server/includes/builder.nvgt`
- `server/includes/server_map.nvgt`
- `server/includes/npc.nvgt`

Referencia BGT para comparacao:
- `cliente/includes/buildermenu.bgt`
- `server/includes/map.bgt`
- `server/includes/bots/npc.bgt`
