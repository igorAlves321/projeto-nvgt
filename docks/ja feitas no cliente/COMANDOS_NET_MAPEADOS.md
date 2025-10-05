# 📡 MAPEAMENTO COMPLETO - COMANDOS DE REDE (net.bgt → net.nvgt)

**Arquivo Original:** `cliente/includes/net.bgt` (1623 linhas)  
**Arquivo Destino:** `cliente/includes/net.nvgt`  
**Status:** 📋 Mapeamento completo - Pronto para implementação

---

## 📊 ESTATÍSTICAS

- **Total de comandos identificados:** ~150+
- **Comandos já implementados:** 6
- **Comandos pendentes:** ~144
- **Canais de rede:** 7 (0-6 + 7 para áudio)

---

## 🔄 COMANDOS JÁ IMPLEMENTADOS (net.nvgt)

| Comando | Canal | Função | Status |
|---------|-------|---------|--------|
| `connect` | - | Conexão estabelecida | ✅ |
| `loggedin` | 0 | Login aceito | ✅ |
| `x` | 0 | Posição X | ✅ |
| `y` | 0 | Posição Y | ✅ |
| `changemap` | 0 | Mudar de mapa | ✅ |
| `usarcolete` | 0 | Usar colete salva-vidas | ✅ |

---

## 🎯 COMANDOS PRIORITÁRIOS (Canal 0 - Eventos Principais)

### **Grupo 1: Gerenciamento de Jogadores** (15 comandos)
| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `pong` | - | Resposta de ping | 🔴 ALTA |
| `remplayer` | `username` | Remover jogador da lista | 🔴 ALTA |
| `terminate` | - | Encerrar sessão | 🔴 ALTA |
| `upl` | `un x y facedir map peer_id` | Atualizar posição jogador | 🔴 ALTA |
| `update_player2` | `un x y facedir map peer_id` | Atualizar jogador 2 | 🔴 ALTA |
| `pp` | `username` | Jogador pacífico | 🟡 MÉDIA |
| `playerbeep` | `username beep` | Beep de jogador | 🟡 MÉDIA |
| `on` | `username` | Jogador conectou | 🟡 MÉDIA |
| `off` | `username disconnect_type reconnect` | Jogador desconectou | 🟡 MÉDIA |
| `setstatus` | `status` | Definir status do jogador | 🟠 BAIXA |
| `gender` | `m/f` | Definir gênero | 🟠 BAIXA |
| `level` | `level` | Definir nível | 🟠 BAIXA |

### **Grupo 2: Movimento e Posicionamento** (10 comandos)
| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `s` | `un x y map step_sound` | Step/passo (som de passos) | 🔴 ALTA |
| `move` | `x y` | Mover jogador | 🔴 ALTA |
| `turn` | `un x y map` | Virar jogador | 🟡 MÉDIA |
| `jumping` | `un x y map` | Pular | 🟡 MÉDIA |
| `land` | `un x y map fallheight` | Aterrissar | 🟡 MÉDIA |
| `wall` | `un x y map sound` | Colidir com parede | 🟡 MÉDIA |
| `ataque` | - | Recuar após ataque | 🟠 BAIXA |
| `changemap2` | `mapname` | Mudar mapa (sem reset) | 🔴 ALTA |

### **Grupo 3: Objetos e Itens** (12 comandos)
| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `spawn_obj` | `id x y sound` | Spawnar objeto | 🔴 ALTA |
| `resetobjs` | - | Resetar objetos | 🔴 ALTA |
| `getobj` | `id` | Pegar objeto | 🔴 ALTA |
| `inv` | `items_data` | Carregar inventário | 🔴 ALTA |
| `setinv` | `items_data` | Definir inventário | 🔴 ALTA |
| `invsec` | `items_data` | Inventário secundário | 🔴 ALTA |
| `reset_items_selected` | - | Resetar seleção de itens | 🟡 MÉDIA |
| `select_items` | `items_list` | Selecionar itens | 🟡 MÉDIA |

### **Grupo 4: Lojas e Comércio** (9 comandos)
| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `manage_stores` | `store_data` | Gerenciar lojas | 🟡 MÉDIA |
| `open_store` | `store_id` | Abrir loja | 🟡 MÉDIA |
| `show_store` | `store_data` | Mostrar loja | 🟡 MÉDIA |
| `list_clothes` | `clothes_data` | Listar roupas | 🟡 MÉDIA |
| `show_clothes` | `clothes_data` | Mostrar roupas | 🟡 MÉDIA |
| `add_clothes_to_inv` | `clothes_list` | Adicionar roupas ao inv | 🟡 MÉDIA |
| `show_items` | `items_list` | Mostrar itens | 🟡 MÉDIA |
| `show_weapons` | `weapons_list` | Mostrar armas | 🟡 MÉDIA |
| `reset_weapons` | - | Resetar armas | 🟡 MÉDIA |

### **Grupo 5: Armas e Combate** (8 comandos)
| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `create_weapon` | `weapon_data` | Criar arma | 🔴 ALTA |
| `hit` | `attacker victim damage x y` | Acerto | 🔴 ALTA |
| `miss` | `attacker x y` | Erro | 🔴 ALTA |
| `death` | `victim killer` | Morte | 🔴 ALTA |
| `respawn` | `x y` | Respawn | 🔴 ALTA |
| `finalhit` | `sound x y voice` | Golpe final | 🟡 MÉDIA |
| `impact` | `sound x y` | Impacto | 🟡 MÉDIA |
| `inithurt` | `voice x y` | Dor inicial | 🟡 MÉDIA |

---

## 💬 COMANDOS DE MENSAGENS (Canal 0 - Todos msg*)

### **Mensagens Simples** (40+ comandos)
| Comando | Função | Exemplo |
|---------|---------|---------|
| `msg avisos <text>` | Mensagem para avisos | `msg avisos Você pegou uma espada` |
| `msg2` | Mensagem com separadores `;` | `msg2 Você está vestindo;camisa azul` |
| `msg3` | Mensagem para equipe | `msg3 Vamos atacar!` |
| `msg4` | Visões angelicais | `msg4 Você vê uma luz` |
| `msgvoz` | Mensagem de voz | `msgvoz username` |
| `msgconexoes` | Notificações de conexão | `msgconexoes Jogador conectou` |
| `msgnormal` | Mensagem normal traduzida | `msgnormal Bem-vindo` |
| `msgadmin` | Mensagem admin | `msgadmin Sistema reiniciando` |
| `msglinha` | Mensagem multilinha `\r\n` | `msglinha linha1\r\nlinha2` |
| `msglinha2` | Mensagem multilinha `:` | `msglinha2 parte1:parte2` |
| `msgsublinhado` | Mensagem com `_` | `msgsublinhado texto_com_underline` |

### **Mensagens de Gameplay** (30+ comandos)
| Comando | Função |
|---------|---------|
| `msgpegouitem` | Você pegou [item] |
| `msgvocêganhou` | Você ganhou [xp] xp |
| `msgvocêganhou2` | Você ganhou mais [xp] pelo doublexp |
| `msgpossuixp` | [player] possui [xp] xp |
| `msgvida` | [hp] de [maxhp] |
| `msgvida2` | [hp] porcento |
| `msgvocênãotem` | Você não tem isso |
| `msgvocênãotem2` | Você não tem [quantidade] [item] |
| `msglhedeu` | [player] lhe deu [quantidade] [item] |
| `msgvocêdeu` | Você deu [quantidade] [item] para [player] |
| `msgstats` | Estatísticas do jogador |
| `msgvestindo` | Você está vestindo [roupas] |
| `msgonlines` | Jogadores online |

### **Mensagens de Morte** (Canal 3 - ~20 comandos)
| Comando | Função |
|---------|---------|
| `msgmuerte` | Morte genérica |
| `msgmortanaarena` | Morte na arena |
| `msgmortonaarena` | Morto na arena |
| `msgtrampa` | Morreu em armadilha |
| `msgcayu1` | Caiu e quebrou coluna |
| `msgcayu2` | Caiu e quebrou perna |
| `msgafogada` / `msgafogado` | Morreu afogado(a) |
| `msgmorreuqueimada` / `msgmorreuqueimado` | Morreu queimado(a) |
| `msgcongelada` / `msgcongelado` | Morreu congelado(a) |
| `msgcaiunamina` | Caiu na mina de [player] |
| `msgbombarelogio` | Explodiu na bomba-relógio |
| `msgmaxbomba` | Morreu na maxbomba |
| `msgbombaatomicam` / `msgbombaatomicah` | Mutilado(a) pela bomba atômica |

### **Mensagens de Leilão/Vendas** (~10 comandos)
| Comando | Função |
|---------|---------|
| `msgnovoleilão` / `msgnovoleilão2` | Novo leilão (reais/euros) |
| `msgfezaoferta` / `msgfezaoferta2` | Fez oferta (reais/euros) |
| `msgleilãoconcluido` | Venda concluída |
| `msgleilãoterminado` / `msgleilãoterminado2` | Venda terminada |
| `msgumoumaisjogadoresdessavenda` | Venda cancelada |
| `msgleilãonãoépermitido` | Venda não permitida |
| `msgreaisFaltandoparaoleilão` | Dinheiro removido |

---

## 🎵 COMANDOS DE ÁUDIO (Canais 0, 4, 5, 7)

### **Canal 0 - Sons Gerais** (20+ comandos)
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `play` | `sound x y` | Tocar som 2D |
| `play2` | `sound x y` | Tocar som 2D (loop) |
| `play3` | `sound x y pitch` | Tocar som extended |
| `play4` | `sound pan volume pitch` | Tocar stationary extended |
| `ps` | `sound` | Tocar stationary |
| `ps2` | `sound pitch` | Tocar stationary com pitch |
| `p2d` | `sound x y` | Tocar 2D |
| `pan` | `sound pan` | Tocar com pan |
| `pst` | `sound` | Tocar ambiente |
| `rs` | `sound_id x y` | Tocar som registrado |
| `rico` | `sound x y` | Ricochete |
| `draw` | `sound x y` | Sacar arma |

### **Canal 4 - Sons de Tiro**
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `f` | `sound x y` | Disparo |
| `f2` | `un sound x y` | Disparo galil |

### **Canal 5 - Sons de Mapa** (4 comandos)
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `play_body` | `sound x y` | Som de corpo |
| `play_wall` | `sound x y` | Som de parede |
| `play_npc` | `sound x y` | Som de NPC |
| `play_step` | `sound x y` | Som de passo |

### **Canal 7 - Áudio de Voz** (3 comandos)
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `map_audio` | `x y audio_data` | Áudio no mapa |
| `private_audio` | `username audio_data` | Áudio privado |
| `team_audio` | `audio_data` | Áudio do time |

---

## 🌍 COMANDOS DE AMBIENTE E CLIMA (10 comandos)

| Comando | Parâmetros | Função | Prioridade |
|---------|-----------|---------|-----------|
| `chuvaativa` | - | Ativar chuva | 🟡 MÉDIA |
| `fimchuva` | - | Desativar chuva | 🟡 MÉDIA |
| `volumechuva` | `volume` | Volume da chuva | 🟡 MÉDIA |
| `addambiente` | `id x y range sound` | Adicionar ambiente | 🟡 MÉDIA |
| `rsonsmo` | - | Resetar sons de ambiente | 🟡 MÉDIA |
| `cm` | `id sound x y file` | Criar som de música | 🟡 MÉDIA |
| `destroymsound` | `id` | Destruir som de música | 🟡 MÉDIA |
| `um` | `id x y` | Atualizar som de música | 🟡 MÉDIA |

---

## 🎮 COMANDOS DE GAMEPLAY ESPECIAIS (20+ comandos)

### **Estados do Jogador**
| Comando | Função |
|---------|---------|
| `startfloat` / `stopfloat` | Flutuar on/off |
| `startcloak` / `stopcloak` | Invisibilidade on/off |
| `superjumpon` / `superjumpoff` | Super pulo on/off |
| `start_watch` / `stop_watch` | Vigilância on/off |
| `stopmoving` / `startmoving` | Movimento on/off |
| `staron` / `staroff` | Estrela on/off |
| `bolhadearon` / `bolhaaroff` | Bolha de ar on/off |
| `fimnovato` / `ininovato` | Novato on/off |
| `morreu` | Reset afogamento/congelamento |
| `usarcolete` / `retirarcolete` | Colete salva-vidas on/off |
| `ausente0` / `ausente1` | Ausente on/off |
| `seguro` | Não vai cair (on) |
| `aveloz` / `dveloz` | Velocidade rápida on/off |

### **Habilidades**
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `spellslist` | `spells_data` | Lista de feitiços |
| `mtester` | `data` | Teste de mana |

### **NPCs e Animais**
| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `manimais` | `animal_data` | Menu de animais |
| `mmaquina` | `machine_data` | Menu de máquina |
| `mtext` | `title\|text\|sound\|type` | Menu de texto |

---

## 📚 COMANDOS DE LIVROS E PORTAIS (10 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `showbooks` | `books_list` | Mostrar livros |
| `readbook` | `book_data` | Ler livro |
| `databook` | `book_id data` | Dados do livro |
| `dataportal` | `portal_data` | Dados do portal |
| `portal` | `portals_list` | Lista de portais |
| `use_portal` | `portal_options` | Usar portal |
| `list_news_categories` | `categories` | Categorias de notícias |

---

## 🎛️ COMANDOS DE MENUS (15 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `servermenu` | `title\|desc\|type\|items\|sounds` | Menu do servidor |
| `menutext` | `items_list` | Menu de texto |
| `menuleitura` | `items_list` | Menu de leitura 1 |
| `menuleitura2` | `items_list` | Menu de leitura 2 |
| `menuleitura3` | `items_list` | Menu de leitura 3 |
| `menuleitura4` | `items_list` | Menu de leitura 4 |
| `menuleitura5` | `items_list` | Menu de leitura 5 |
| `menuvehiculos` | - | Menu de veículos |
| `telemenu` | `destinations` | Menu de teletransporte |

---

## ⚙️ COMANDOS ADMINISTRATIVOS (10 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `djogador` | - | Permissão: Desenvolvedor |
| `dmoderador` | - | Permissão: Moderador |
| `dconstructor` | - | Permissão: Construtor |
| `enabletranslate` / `disabletranslate` | - | Tradutor on/off |
| `enablechatadm` / `disablechatadm` | - | Chat admin on/off |
| `restart` | - | Reiniciar NVDA |
| `update` | - | Atualizar cliente |
| `kill` | - | Encerrar cliente |
| `reiniciar` | - | Resetar e relogar |
| `chutad` | - | Chutado |

---

## 🔐 COMANDOS DE AUTENTICAÇÃO (5 comandos)

| Comando | Parâmetros | Função | Status |
|---------|-----------|---------|--------|
| `loggedin` | - | Login aceito | ✅ |
| `block` | `reason` | Login bloqueado | ⏳ |
| `erro:` / `Error:` | `message` | Erro de login | ⏳ |
| `updatenow` | - | Versão desatualizada | ⏳ |
| `pass_changed` | - | Senha alterada | ⏳ |

---

## 👥 COMANDOS DE TIMES E GRUPOS (Canal 6 - 15 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `set_team_members` | `members_list` | Definir membros do time |
| `add_team_member` | `username` | Adicionar membro |
| `remove_team_member` | `username` | Remover membro |
| `clear_team_members` | - | Limpar time |
| `set_married_variable` | `spouse` | Definir casado(a) |
| `set_parabatai_variable` | `parabatai` | Definir parabatai |
| `set_items_for_translate` | `items_list` | Itens para traduzir |
| `show_eagle_messages` | `messages_list` | Mensagens da águia |

---

## 🗺️ COMANDOS DE MAPA (Canal 6 - 10 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `set_map_players` | `players_data` | Definir jogadores no mapa |
| `add_player_to_map` | `un x y facedir map peer_id` | Adicionar jogador ao mapa |
| `remove_player_from_map` | `username` | Remover jogador do mapa |
| `add_line_to_map` | `map_line` | Adicionar linha ao mapa |
| `remove_line_from_map` | `map_line` | Remover linha do mapa |
| `reset_all_weapons_ammo` | - | Resetar munição |

---

## 📝 COMANDOS ESPECIAIS (10 comandos)

| Comando | Parâmetros | Função |
|---------|-----------|---------|
| `set_lang_file` | `filename` | Definir arquivo de idioma |
| `channels` | `channels_list` | Lista de canais de chat |
| `fbau` | - | Flag: bau |
| `motd3` | `message` | Mensagem do dia admin |
| `upload` | `allow` | Upload de arquivo |
| `madness_cinematic` | - | Cinemática de loucura |
| `permanent` | `from message` | Mensagem permanente |
| `pm` / `you reply:` | `from message` | Mensagem privada |
| `mensaje` | `from message` | Mensagem |
| `r` / `respuesta reply:` | `from message` | Resposta |

---

## 🎯 PLANO DE IMPLEMENTAÇÃO

### **Fase 1: Comandos Essenciais (2-3 horas)**
1. ✅ `loggedin`, `x`, `y`, `changemap` - **COMPLETO**
2. ⏳ `pong`, `terminate`, `remplayer`
3. ⏳ `upl`, `update_player2`, `s` (movimentação)
4. ⏳ `move`, `changemap2`
5. ⏳ `inv`, `setinv`, `invsec`

### **Fase 2: Audio e Gameplay (2 horas)**
6. ⏳ `play`, `p2d`, `ps`, `play2`, `play3`, `play4`
7. ⏳ `play_body`, `play_wall`, `play_npc`, `play_step`
8. ⏳ `f`, `rs`, `rico`, `draw`
9. ⏳ `spawn_obj`, `resetobjs`, `getobj`

### **Fase 3: Mensagens (1-2 horas)**
10. ⏳ `msg`, `msg2`, `msg3`, `msg4`
11. ⏳ `msgnormal`, `msglinha`, `msgadmin`
12. ⏳ Todas as mensagens específicas (msgpegouitem, msgvocêganhou, etc)

### **Fase 4: Combate e Times (1 hora)**
13. ⏳ `hit`, `miss`, `death`, `respawn`
14. ⏳ `finalhit`, `impact`, `inithurt`
15. ⏳ `set_team_members`, `add_team_member`, `remove_team_member`
16. ⏳ `create_weapon`, `reset_weapons`

### **Fase 5: Ambiente e Especiais (1 hora)**
17. ⏳ Estados (startfloat, startcloak, superjumpon, etc)
18. ⏳ Clima (chuvaativa, volumechuva, etc)
19. ⏳ Menus (servermenu, menutext, etc)
20. ⏳ Admin (djogador, dmoderador, restart, update, kill)

---

## ✅ CRITÉRIOS DE SUCESSO

- [ ] Todos os 150+ comandos portados
- [ ] Criptografia/descriptografia em todos os canais
- [ ] Processamento multi-canal (0-7)
- [ ] Tradução de mensagens funcionando
- [ ] Sons 2D/3D funcionando
- [ ] Inventário sincronizado
- [ ] Jogadores atualizados em tempo real
- [ ] Chat completo (canal principal, PMs, times)
- [ ] Compila sem erros

---

**Última atualização:** 5 de outubro de 2025  
**Próximo passo:** Implementar Fase 1 (comandos essenciais)
