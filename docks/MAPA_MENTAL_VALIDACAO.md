# 🗺️ MAPA MENTAL - Validação NVGT baseada em BGT

## ESTRUTURA DO PROJETO NVGT

```
cliente/
├── client.nvgt (1052L)
│   ├── void main()
│   └── void game() ← LOOP PRINCIPAL
│
└── includes/
    ├── net.nvgt (500L)
    │   ├── net_logar() ← LOGIN
    │   ├── netloop() ← EVENTOS REDE
    │   └── process_channel_0()
    │
    ├── map.nvgt (300L)
    │   └── load_map() ← PARSER MAPA
    │
    ├── player.nvgt (200L)
    │   ├── class player_class
    │   └── update_player() ← POSIÇÃO
    │
    ├── comandos.nvgt (500L)
    │   └── tprincipais() ← TECLAS F1-F8
    │
    ├── globals.nvgt (707L)
    │   ├── network con
    │   ├── player_class me
    │   ├── player_class[] players
    │   ├── dictionary player_inv
    │   ├── string copiaragora
    │   └── inv_category[] inv_categories
    │
    ├── inv.nvgt (166L)
    │   ├── class inv_category
    │   ├── load_inv()
    │   ├── setinv()
    │   └── invmenu()
    │
    └── stubs.nvgt (302L)
```

---

## FLUXO CRÍTICO: LOGIN → GAME

```
┌─────────────────────────────────────────────────────────────────┐
│                        INÍCIO                                   │
│                    main_menu()                                  │
│            [Menu Principal com opções]                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Usuário clica "Logar"
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   net_logar()                                   │
│        (includes/net.nvgt - FUNÇÃO CRÍTICA #1)                 │
│                                                                 │
│  ETAPAS:                                                        │
│  1. con.setup_client(1, 100)           ✓ Setup network        │
│  2. peer_id = con.connect(ip, port)    ✓ Connect              │
│  3. send_reliable(peer_id, msg, 0)     ✓ Enviar login        │
│  4. event = con.request()              ← Aguarda evento       │
│     └─ if(msg == "loggedin")           ✓ Login OK            │
│     └─ if(msg.find("changemap") != -1) ✓ Mapa recebido      │
│                                                                 │
│  ❌ NÃO FAZER:                                                  │
│     Chamar game() antes do changemap!                          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Recebeu "loggedin"
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   changemap processing                          │
│        (includes/net.nvgt - ETAPA CRÍTICA #2)                  │
│                                                                 │
│  PARSING:                                                       │
│  msg = "changemap map:escuela maxx:201 maxy:1001 ..."         │
│  ├─ Extract: mapname = "escuela"                              │
│  ├─ Extract: spawn_x = parse(parts[2])                        │
│  └─ Extract: spawn_y = parse(parts[3])                        │
│                                                                 │
│  AÇÕES:                                                         │
│  1. load_map(msg)          ✓ Carrega dados                    │
│  2. me.x = spawn_x         ✓ Posiciona jogador                │
│  3. me.y = spawn_y         ✓ em coordenadas                   │
│  4. mapname = map_name     ✓ Define nome globalmente          │
│  5. game()                 ✓ AGORA SIM entra no loop          │
└────────────────────────┬────────────────────────────────────────┘
                         │ Mapa carregado
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    load_map()                                   │
│        (includes/map.nvgt - PARSER CRÍTICO #3)                 │
│                                                                 │
│  INPUT:                                                         │
│  string full_map_data = "map:escuela\r\nmaxx:201\r\n..."      │
│                                                                 │
│  PARSE:                                                         │
│  string[] lines = full_map_data.split("\r\n")                 │
│  foreach line:                                                  │
│    if(line.find("map:") != -1)     → mapname = ...            │
│    if(line.find("maxx:") != -1)    → dimensions.x = ...       │
│    if(line.find("maxy:") != -1)    → dimensions.y = ...       │
│    if(line.find("z:") != -1)       → zones.push({x,y,desc})  │
│    if(line.find("p:") != -1)       → platforms.push(...)      │
│    if(line.find("w:") != -1)       → walls.push(...)          │
│                                                                 │
│  OUTPUT:                                                        │
│  ✓ map[] array populado                                        │
│  ✓ zones[] array populado                                      │
│  ✓ mapname definido                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │ Mapa pronto
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      game()                                     │
│   (client.nvgt - LOOP PRINCIPAL CRÍTICO #4)                    │
│                                                                 │
│  LOOP:                                                          │
│  while(connected == true) {                                    │
│                                                                 │
│    ┌─────── netloop() ────────┐  CRÍTICO #5                  │
│    │ 1. con.request()         │  Processa eventos             │
│    │ 2. decrypt_packet()      │  de rede a cada frame         │
│    │ 3. Parse commands        │  (upl, pong, s, etc)          │
│    │ 4. Call handlers         │                               │
│    └──────────────────────────┘                               │
│                                                                 │
│    ┌─────── Input Handler ────────┐  CRÍTICO #6               │
│    │ if(KEY_UP)    move(0, -1)     │  Trata setas              │
│    │ if(KEY_DOWN)  move(0, 1)      │  Envia ao servidor        │
│    │ if(KEY_LEFT)  move(-1, 0)     │                           │
│    │ if(KEY_RIGHT) move(1, 0)      │                           │
│    └────────────────────────────────┘                          │
│                                                                 │
│    ┌─────── tprincipais() ────────┐  CRÍTICO #7               │
│    │ if(F1) → menu_ações()        │  Teclas especiais          │
│    │ if(F2) → menu_personagem()   │  F1-F8: menus             │
│    │ if(I)  → invmenu()           │  I: inventário             │
│    │ if(B)  → speak(location)     │  B: localização            │
│    │ if(C)  → speak(coords)       │  C: coordenadas            │
│    │ if(S)  → send("status")      │  S: status                │
│    └────────────────────────────────┘                          │
│                                                                 │
│    wait(50)  ← Timeout para não travar CPU                   │
│  }                                                              │
│                                                                 │
│  SAÍDA:                                                         │
│  Retorna quando connected = false (desconexão)                │
└────────────────────────┬────────────────────────────────────────┘
                         │ Desconectado
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Retorna ao Menu                               │
│              (game() retorna para main_menu())                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## FLUXO NETLOOP: PROCESSAMENTO DE EVENTOS

```
netloop()
│
├─ con.request() → network_event
│  │
│  └─ if(event.type == event_none) return
│
├─ if(event.type == event_disconnect)
│  │
│  └─ connected = false
│     └─ reset()
│        └─ volta ao menu
│
└─ if(event.type == event_receive)
   │
   ├─ string msg = decrypt_packet(event.message)
   │
   ├─ Parse msg and dispatch:
   │
   │  ┌─ if(msg == "pong")
   │  │  └─ pingtimer.restart()
   │
   │  ├─ if(msg.find("upl") != -1)
   │  │  └─ update_player(parts[1], parts[2], parts[3])
   │  │     └─ Outro player se moveu!
   │  │        └─ Toca som 3D de passos
   │
   │  ├─ if(msg.find("s ") != -1)
   │  │  └─ steps.play_2d(som, me.x, me.y, x, y, false)
   │  │     └─ Som 3D de movimento
   │
   │  ├─ if(msg.find("local ") != -1)
   │  │  └─ add_chat_message(parsed[1])
   │  │     └─ Chat local do mapa
   │
   │  └─ if(msg.find("hablarbot") != -1)
   │     └─ add_npc_message(parsed[1], texto)
   │        └─ Fala de NPC
   │
   └─ return
```

---

## CHECKLIST DE FUNÇÕES CRÍTICAS

```
TIER 1 - ABSOLUTAMENTE CRÍTICO (Login não funciona sem)
════════════════════════════════════════════════════════════
[ ] net_logar()
    └─ Conecta ao servidor
    └─ Envia credenciais
    └─ Aguarda "loggedin"
    └─ Aguarda "changemap"
    └─ Chama load_map()
    └─ Posiciona me.x, me.y
    └─ Chama game()

[ ] load_map()
    └─ Parseia "\r\n" corretamente
    └─ Extrai mapname
    └─ Popula arrays globais
    └─ me está posicionado correto

[ ] game()
    └─ Loop principal ativo
    └─ Chama netloop()
    └─ Processa setas
    └─ Chama tprincipais()

TIER 2 - MUITO IMPORTANTE (Gameplay quebra sem)
════════════════════════════════════════════════════════════
[ ] netloop()
    └─ Descriptografa mensagens
    └─ Processa "upl" (outros players)
    └─ Processa "s" (som 3D)
    └─ Não trava em erro

[ ] tprincipais()
    └─ F1-F8 funcionam
    └─ I abre inventário
    └─ B fala localização
    └─ C fala coordenadas
    └─ S pede status

[ ] update_player()
    └─ Atualiza posição x,y
    └─ Encontra player correto
    └─ Toca som de movimento

TIER 3 - IMPORTANTE (Menor impacto)
════════════════════════════════════════════════════════════
[ ] Menu principal
[ ] Inventário (invmenu)
[ ] Criptografia (encrypt/decrypt)
[ ] Classes (player_class, inv_category)
[ ] Variáveis globais (all defined)
```

---

## COMPARAÇÃO BGT vs NVGT

```
ASPECTO              BGT              NVGT         STATUS
════════════════════════════════════════════════════════════
Network API          network class    g_net global  ✓ Similar
Encryption           Nativa BGT       Nativa NVGT   ✓ Similar
Player array         array<player>    array<player> ✓ Similar
Map parsing          string.split()   split()       ✓ Similar
Event processing     event.request()  event        ✓ Similar
Sound 3D             sound_pool       sound_pool    ✓ Similar
Menu system          bgt_menu         input_form    ~ Diferente

KEY DIFFERENCE:
NVGT usa referencias (@) para arrays/classes
NVGT não tem db class nativa (usar dictionary)
NVGT tem dictionary type (melhor que assoc. array BGT)
```

---

## PRÓXIMAS AÇÕES (ORDEM)

```
1. TESTES BÁSICOS
   ├─ [ ] Iniciar cliente
   ├─ [ ] Menu aparece
   ├─ [ ] Clique em "Logar"
   └─ [ ] Ver logs

2. TESTES DE CONEXÃO
   ├─ [ ] Conecta ao servidor
   ├─ [ ] event_connect recebido
   └─ [ ] Credenciais enviadas

3. TESTES DE LOGIN
   ├─ [ ] Recebe "loggedin"
   ├─ [ ] Aguarda changemap
   └─ [ ] Recebe changemap

4. TESTES DE MAPA
   ├─ [ ] load_map() executa
   ├─ [ ] me.x, me.y setados
   └─ [ ] mapname correto

5. TESTES DE GAMEPLAY
   ├─ [ ] game() inicia loop
   ├─ [ ] Setas funcionam
   ├─ [ ] I abre inventário
   └─ [ ] Teclas F1-F8 respondem

6. TESTES DE MULTIPLAYER
   ├─ [ ] 2 clientes conectados
   ├─ [ ] Um se move
   ├─ [ ] Outro vê movimento
   └─ [ ] Som 3D toca

7. TESTES DE ESTABILIDADE
   ├─ [ ] Desconexão limpa
   ├─ [ ] Reconexão funciona
   └─ [ ] Sem crashes
```

---

**Mapa Mental - Guia de Validação**  
**Conversão BGT → NVGT**  
**6 de novembro de 2025**
