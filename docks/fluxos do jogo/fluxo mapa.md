# Fluxo de Mapa no Jogo (NVGT)

Este documento explica o fluxo completo de mapa dentro do jogo, do jeito que esta implementado hoje no codigo:

1. permissao para construir
2. abertura do menu no cliente
3. criacao de mapa
4. edicao de elementos (piso, parede, som, etc.)
5. salvamento
6. atualizacao/reload para jogadores
7. exclusao de mapa

## 1. Quem pode usar o Builder

Para abrir o menu administrativo (`F9`), o cliente aceita:
- dev
- admin
- moderador
- builder

No login, o servidor envia flags para o cliente:
- `djogador` => dev
- `ajogador` => admin
- `bjogador` => builder

Ponto importante:
- abrir `F9` nao significa que todas acoes de builder vao passar no servidor
- o servidor valida builder com:
  - `rank >= 3`, ou
  - `constructor`, ou
  - `dev`, ou
  - `admin`

Entao, um moderador pode abrir F9, mas pode receber erro de permissao nas operacoes de mapa.

## 2. Como entrar no fluxo (in-game)

1. Jogador loga normalmente.
2. Pressiona `F9`.
3. Abre `Menu Administrativo`.
4. Escolhe `Construtor de Mapas`.
5. O cliente chama o `buildermenu()`.

## 3. Criacao de mapa novo

No menu builder:
- opcao: `Novo mapa`

O cliente envia:
- `/newmap <nome> <largura> <altura> <som_piso>`

Exemplo:
- `/newmap arena_teste 120 80 1`

O servidor:
- valida permissao
- valida nome/dimensoes
- cria arquivo `.map`
- adiciona mapa na memoria (`server_maps`)
- cria base minima do mapa (maxx/maxy/plataforma/parede/safezone/zone)

## 4. Edicao de mapa (elementos)

Depois de criar (ou em mapa existente):

1. Entre no mapa que voce quer editar.
2. F9 -> Construtor de Mapas.
3. Use as opcoes do builder.

A maioria das opcoes manda pacote no formato:
- `add_line::<dados>`

Tipos principais aceitos no servidor hoje:
- `p` / `platform`: piso/plataforma
- `w` / `wall` / `pwall`: parede
- `sc` / `staircase`: escada
- `z` / `zone`: zona
- `sz` / `safezone`: zona segura
- `npc`: npc
- `item`: item dropavel
- `rt`: banheiro
- `lv`: pia
- `ex`: zona de extracao
- `dr` / `door`: porta
- `ss`: som ambiente
- `txt` / `texto`: texto no mapa
- `tp`: travelpoint/passagem
- `maxx`, `maxy`: limites do mapa
- `teto`: som de teto/chuva do mapa
- `dv`: desativar elemento no mapa

Obs:
- algumas opcoes antigas do menu podem existir visualmente, mas se o tipo nao tiver handler no servidor novo, retorna erro de tipo desconhecido.

## 5. Salvar alteracoes (obrigatorio)

Comando de salvar:
- `/savemap`

Sem salvar:
- alteracoes podem ficar so em memoria
- reiniciar o servidor pode perder mudancas nao salvas

## 6. Atualizar/recarregar mapa

Comandos:
- `/mapupdate` (mapa atual)
- `/mapupdate <nome_mapa>` (mapa especifico)

Compatibilidade:
- `/rawdata <nome_mapa>` tambem foi ligado para atualizar mapa

Comportamento atual:
- servidor recarrega o mapa do disco
- jogadores no mapa sao forcados a recarregar via `changemap`

## 7. Excluir mapa

No menu builder:
- opcao: `Deletar mapa`

Comando:
- `/delmap <nome_mapa>`

Regras atuais:
- nao permite deletar o mapa inicial (`mapainicial`)
- remove da memoria (`server_maps`)
- remove arquivo `.map` (em `maps/` e/ou `server/maps/`)
- jogadores que estiverem nesse mapa vao para o mapa inicial

## 8. Fluxo recomendado para equipe

Sequencia segura para construir sem perder trabalho:

1. `F9 -> Construtor de Mapas`
2. criar mapa (`Novo mapa` / `/newmap ...`)
3. entrar no mapa
4. construir elementos (`add_line::...` via menu)
5. salvar (`/savemap`)
6. atualizar (`/mapupdate`)
7. testar no cliente
8. repetir ciclo (editar -> salvar -> atualizar)

## 9. Como dar permissao de builder

Via comando admin/dev:
- `/addcargo <jogador> builder`

Depois, no login, o servidor envia a flag de builder e o cliente libera acesso correspondente.

## 10. Erros comuns

- `Permissao negada`
  - jogador sem rank/cargo necessario no servidor

- `Mapa nao encontrado`
  - nome incorreto
  - mapa inexistente em memoria/arquivo

- construi e "sumiu"
  - faltou `/savemap`

- atualizei e cliente nao refletiu
  - confirmar `/mapupdate` no mapa certo
  - confirmar que salvou antes
