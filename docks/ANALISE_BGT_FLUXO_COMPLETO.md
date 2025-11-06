# 📊 ANÁLISE DO PROJETO BGT - FLUXO COMPLETO DO JOGO

**Data:** 6 de novembro de 2025  
**Objetivo:** Usar como referência para verificar/corrigir implementação NVGT  
**Status:** ✅ Projeto BGT original estava **100% FUNCIONAL**

---

## 🎯 FLUXO PRINCIPAL (Login → Gameplay)

```
┌─────────────┐
│   MENU      │
│ (principal) │
└──────┬──────┘
       │ Usuário clica "Jogar"
       ▼
┌─────────────────────────────────────┐
│  CLIENTE - net_logar()              │
│  (cliente/includes/net.bgt)         │
│                                     │
│  1. con.setup_client(1, 100)       │
│  2. con.connect(server, port)      │
│  3. Envia: "h33j user hash ver"    │
│  4. Aguarda loggedin ✅            │
│  5. NÃO chama game() ainda ❌      │
│  6. Aguarda changemap ✅           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  SERVIDOR - handle_login()          │
│  (server/includes/net.bgt)          │
│                                     │
│  1. Valida credenciais no DB       │
│  2. Carrega dados do jogador       │
│  3. Envia: "loggedin"              │
│  4. Chama: changemap()             │
│  5. Envia: "changemap mapa x y"    │
│     + dados do mapa                │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  CLIENTE - Recebe "loggedin"        │
│  (cliente/includes/net.bgt:        │
│   netloop())                        │
│                                     │
│  ✅ Marca: connected = true        │
│  ⏳ Aguarda changemap...           │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  CLIENTE - Recebe "changemap"       │
│  (cliente/includes/net.bgt:        │
│   netloop())                        │
│                                     │
│  1. Parser mapa x y                │
│  2. load_map(mapname)              │
│  3. me.x = x; me.y = y             │
│  4. ✅ AGORA chama game()          │
│  5. game() inicia loop             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  CLIENTE - game()                   │
│  (cliente/Projeto Ig.bgt ~500 L)   │
│                                     │
│  Loop infinito enquanto connected:  │
│  1. netloop() → processa eventos    │
│  2. Trata input (setas)            │
│  3. tprincipais() → F1-F8, etc     │
│  4. atualiza gráficos/sons         │
└─────────────────────────────────────┘
```

---

## 📋 COMPONENTES CRÍTICOS PARA NVGT

### 1️⃣ **FUNÇÃO: net_logar() - Login do Jogador**

**Arquivo BGT:** `cliente/includes/net.bgt` (linhas 200-300+)

**Responsabilidades:**
- Conectar ao servidor
- Enviar credenciais (username + hash senha)
- Aguardar confirmação "loggedin"
- Aguardar "changemap" (IMPORTANTE: não chamar game() logo)
- Processar changemap

**Fluxo Correto:**
```bgt
void net_logar() {
    // 1. Conectar
    con.setup_client(1, 100);
    peer_id = con.connect(game_serveraddress, game_serverport);
    
    // 2. Enviar login
    string pwd_hash = hash_password(net_pw);
    string msg = "h33j " + net_un + " " + pwd_hash + " " + ver + " " + banned;
    send_reliable(peer_id, msg, 0);
    
    // 3. Aguardar eventos
    while(true) {
        network_event@ event = con.request();
        
        if(event.type == event_receive) {
            string msg = decrypt_packet(event.message);
            
            // Recebeu loggedin
            if(msg == "loggedin") {
                connected = true;
                speak("Logado! Aguardando mapa...");
                continue; // Aguarda changemap
            }
            
            // Recebeu changemap
            if(msg.find("changemap") != -1) {
                string[] parts = msg.split(" ");
                string mapdata = string_join(parts[1..], " ");
                
                load_map(mapdata);
                game(); // Chama game() APÓS carregar mapa
                return;
            }
        }
    }
}
```

**❌ ERRO COMUM (NVGT):**
- Chamar `game()` imediatamente após "loggedin"
- Mapa não carregado quando loop de jogo começa
- Coordenadas me.x/me.y não setadas

---

### 2️⃣ **FUNÇÃO: load_map() - Parser e Carregamento do Mapa**

**Arquivo BGT:** `cliente/includes/map.bgt` (linhas 1-300)

**Responsabilidades:**
- Parsear string de dados do mapa
- Extrair nome, dimensões (maxx, maxy)
- Carregar plataformas (p: x y tipo)
- Carregar paredes (w: x y altura tipo)
- Carregar zonas de descrição (z: x y x y descricao)
- Popular arrays globais: `map[]`, `zones[]`, `safemap`

**Formato do Mapa (BGT):**
```
map:escuela
maxx:201
maxy:1001
p:0:201:0:concrete18
w:0:0:1001:wallnone
w:201:0:1001:wallnone
teto:none
z:1:200:0:1000:-
z:1:20:0:49:Pasillo de entrada...
dv:coordenadas
```

**Parse Esperado:**
```
map[0] = {name: "escuela", maxx: 201, maxy: 1001, ...}
zones[0] = {x1: 1, y1: 200, x2: 0, y2: 1000, desc: "-"}
```

**❌ ERRO COMUM (NVGT):**
- Não parsear corretamente as linhas com "\r\n"
- me.x/me.y não estão corretos
- Mapa.size() vazio quando game() começa

---

### 3️⃣ **FUNÇÃO: game() - Loop Principal do Jogo**

**Arquivo BGT:** `cliente/Projeto Ig.bgt` (linhas ~1300-1500)

**Responsabilidades:**
- Loop infinito enquanto `connected == true`
- Chamar `netloop()` para processar eventos de rede
- Processar input do jogador (setas, teclas)
- Chamar `tprincipais()` para verificar F1-F8, I, B, C, S
- Atualizar visão/áudio do mundo

**Estrutura do Loop:**
```bgt
void game() {
    speak(pu.get_value("Entrou no jogo! Use as setas para se mover."));
    
    while(connected) {
        // Processar rede
        netloop();
        
        // Setas: movimento
        if(key_pressed(KEY_UP) && me.y > 0) {
            me.y--;
            send_reliable(peer_id, "move 0 -1", 0);
        }
        if(key_pressed(KEY_DOWN)) {
            me.y++;
            send_reliable(peer_id, "move 0 1", 0);
        }
        // ... etc LEFT, RIGHT
        
        // Teclas principais (F1-F8, I, B, etc)
        tprincipais();
        
        // Timeout (évita 100% CPU)
        wait(50);
    }
}
```

**❌ ERRO COMUM (NVGT):**
- `netloop()` não chamado → eventos não processados
- `tprincipais()` não chamado → F1-F8 não funcionam
- Me.x/me.y não sincronizados com servidor

---

### 4️⃣ **FUNÇÃO: netloop() - Processamento de Rede**

**Arquivo BGT:** `cliente/includes/net.bgt` (linhas 1-100)

**Responsabilidades:**
- Processar eventos da rede em cada iteração
- Descriptografar mensagens
- Parsear comandos (upl, pong, hablarbot, etc)
- Chamar handlers específicos

**Comandos Processados:**
```
upl <peer_id> <x> <y>      → update_player(peer_id, x, y)
pong                        → Resposta ao ping do servidor
s <peer_id> <som> <x> <y>  → Tocar som 3D de movimento
local <texto>               → Chat do mapa
hablarbot <npc> <texto>     → Fala de NPC
listplayers <data>          → Menu de jogadores (F5)
married                     → Status de casamento
```

**Exemplo:**
```bgt
void netloop() {
    network_event@ event = con.request();
    if(event.type != event_receive) return;
    
    string[] parts = decrypt_packet(event.message).split(" ");
    
    if(parts[0] == "upl") {
        // outro jogador se moveu
        update_player(parse_int(parts[1]), 
                      parse_int(parts[2]), 
                      parse_int(parts[3]));
    }
    else if(parts[0] == "s") {
        // Som 3D
        steps.play_2d(parts[2], me.x, me.y, 
                      parse_int(parts[3]), 
                      parse_int(parts[4]), false);
    }
}
```

**❌ ERRO COMUM (NVGT):**
- Não descriptografar (usar string_decrypt)
- Parser quebrado
- Sem tratamento de timeouts

---

### 5️⃣ **FUNÇÃO: tprincipais() - Teclas Principais**

**Arquivo BGT:** `cliente/includes/comandos.bgt` (linhas ~100-400)

**Responsabilidades:**
- Verificar teclas F1-F8 (menus especiais)
- Verificar I (inventário)
- Verificar B (localização)
- Verificar C (coordenadas)
- Verificar S (status)
- Verificar outras teclas de ação

**Exemplo:**
```bgt
void tprincipais() {
    if(key_pressed(KEY_F5)) {
        // Menu de jogadores
        send_reliable(peer_id, "listplayers", 0);
    }
    else if(key_pressed(KEY_I)) {
        // Inventário
        invmenu();
    }
    else if(key_pressed(KEY_B)) {
        // Localização
        speak(pu.get_value(zone_atual.desc));
    }
    else if(key_pressed(KEY_C)) {
        // Coordenadas
        speak("Você está em: " + me.x + ", " + me.y);
    }
    else if(key_pressed(KEY_S)) {
        // Status
        send_reliable(peer_id, "status", 0);
    }
}
```

**❌ ERRO COMUM (NVGT):**
- `tprincipais()` não chamado em game()
- Teclas não respondem
- Menus não abrem

---

### 6️⃣ **VARIÁVEIS GLOBAIS CRÍTICAS**

**Arquivo BGT:** `cliente/Projeto Ig.bgt` (linhas ~50-150)

```bgt
// Rede
network con;
uint peer_id;
bool connected = false;
string net_un = "", net_pw = "";
string username = "";
double gversion = 1.0;

// Jogador
class player_class {
    string charname;
    int x, y;
    string map;
    int mapindex;
    int HP, MP, level, experience;
    string gender;
    dictionary clothing;
    // ... mais
};
player_class me;
player_class[] players;  // Outros jogadores

// Inventário
dictionary player_inv;   // Dicionário: item → quantidade
string[] inv_items_selected;

// Mapa
string mapname;
class map_class {
    string name;
    int maxx, maxy;
    string teto;
    // ... plataformas, paredes
};
map_class[] map;
class zone_class {
    int x1, y1, x2, y2;
    string desc;
};
zone_class[] zones;
```

**❌ ERRO COMUM (NVGT):**
- `player_inv` não é dictionary
- `me.x`, `me.y` não sincronizados
- `mapname` vazio ou incorreto

---

### 7️⃣ **ESTRUTURA DE CLASSES - player_class**

**Arquivo BGT:** `cliente/includes/player.bgt`

```bgt
class player_class {
    string charname;          // Nome do personagem
    int x, y;                 // Posição no mapa
    string map;               // Nome do mapa
    int mapindex;             // Índice do mapa
    
    // Stats
    int level;
    int experience;
    int HP, MP;
    
    // Dados
    string gender;            // "m" ou "f"
    dictionary clothing;      // Roupas equip
    string nickname;
    bool pacifico;
    
    // Funções
    int distance_to(int x2, int y2) {
        return abs(x - x2) + abs(y - y2);  // Manhattan distance
    }
};

// Instância global
player_class me;

// Outros jogadores
player_class[] players;
```

---

## 🔐 CRIPTOGRAFIA E COMUNICAÇÃO

**Arquivo BGT:** `cliente/includes/net.bgt`

**Método:**
- Chave de criptografia: `PREFS_ENCRYPTION_KEY`
- Algoritmo: AES-256 (nativo BGT/NVGT)
- Formato: `encrypt(message, key)` / `decrypt(message, key)`

**Exemplo:**
```bgt
// Enviar
string pwd_hash = hash_password(net_pw);
string msg = "h33j " + net_un + " " + pwd_hash + " " + ver;
string encrypted = encrypt_packet(msg);
send_reliable(peer_id, encrypted, 0);

// Receber
network_event@ event = con.request();
string decrypted = decrypt_packet(event.message);
string[] parts = decrypted.split(" ");
```

**❌ ERRO COMUM (NVGT):**
- Não criptografar/descriptografar
- Chave incorreta
- Formato de mensagem diferente

---

## 🧪 TESTE RECOMENDADO (Baseado em BGT Funcional)

### Teste 1: Conexão Básica
```
✅ Cliente conecta ao servidor
✅ Recebe evento event_connect
✅ peer_id é atribuído
```

### Teste 2: Login
```
✅ Cliente envia credenciais
✅ Servidor valida
✅ Cliente recebe "loggedin"
✅ Cliente NÃO entra em game() ainda
```

### Teste 3: Changemap
```
✅ Servidor envia "changemap escuela 1 0"
✅ Cliente parseia corretamente
✅ load_map() executa sem erros
✅ me.x = 1, me.y = 0
✅ mapname = "escuela"
```

### Teste 4: Game Loop
```
✅ game() inicia
✅ netloop() processa eventos
✅ Setas funcionam (movimento)
✅ Coords aparecem quando pressa C
```

### Teste 5: Multiplayer
```
✅ Dois clientes conectados
✅ Um se move
✅ Outro recebe "upl" e vê movimento
✅ Sons 3D tocam
```

---

## 📍 CHECKLIST: BGT vs NVGT

| Componente | BGT ✅ | NVGT ❓ | Arquivo NVGT |
|------------|--------|---------|--------------|
| net_logar() | ✅ | ❓ | includes/net.nvgt |
| load_map() | ✅ | ❓ | includes/map.nvgt |
| game() | ✅ | ❓ | client.nvgt |
| netloop() | ✅ | ❓ | includes/net.nvgt |
| tprincipais() | ✅ | ❓ | includes/comandos.nvgt |
| player_class | ✅ | ❓ | includes/player.nvgt |
| Criptografia | ✅ | ❓ | globals.nvgt |
| Menu Principal | ✅ | ❓ | includes/menu.nvgt |

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ **Compilação** - FEITA (projeto compila sem erros)
2. ⏳ **Verificar net_logar()** - Fluxo correto?
3. ⏳ **Verificar load_map()** - Parser correto?
4. ⏳ **Verificar game()** - Loop ativo?
5. ⏳ **Teste end-to-end** - Login → Jogo funciona?

---

**Status:** 📊 Análise completa baseada em BGT funcional  
**Última atualização:** 6 de novembro de 2025
