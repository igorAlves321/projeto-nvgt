# Plano de Conversão: Servidor BGT → NVGT

## 🎯 **OBJETIVO PRINCIPAL**
Converter o servidor EVM de BGT para NVGT usando funcionalidades nativas e bibliotecas internas do NVGT, garantindo compatibilidade total com o cliente NVGT já convertido.

---

## 📊 **ANÁLISE COMPLETA DO SERVIDOR BGT**

### 🗂️ **Estrutura Atual do Servidor:**
```
server/
├── server.bgt (7266 linhas) - Arquivo principal
├── includes/ - 38+ arquivos BGT
│   ├── player.bgt - Sistema de jogadores 
│   ├── map.bgt - Sistema de mapas
│   ├── item.bgt - Sistema de items/objetos
│   ├── comandos.bgt - Sistema de comandos
│   ├── comandos/ - 20+ subcomandos específicos
│   ├── moving_sound/ - Sistema de som móvel
│   ├── mine/ - Sistema de minas
│   └── [33+ outros sistemas específicos]
├── maps/ - Arquivos de mapas
├── players/ - Dados de jogadores
├── qcomandos/ - Comandos administrativos
└── [diversos arquivos de configuração e dados]
```

### 🔧 **Sistemas Principais Identificados:**

#### **1. 🌐 Sistema de Rede (CRÍTICO)**
- **Arquivo**: `server.bgt` (linhas 47, 153, 3663-3705)
- **BGT**: `network net;`, `network_event event;`
- **Funcionalidade**: 
  - Servidor TCP/UDP para múltiplos clientes
  - Criptografia de pacotes com `NETWORK_ENCRYPTION_KEY`
  - Gerenciamento de eventos de conexão/desconexão
  - Sistema `send_reliable()` e `send_packet()`
- **NVGT Equivalente**: `game_net` class (já usado no cliente)

#### **2. 👥 Sistema de Jogadores (CORE)**
- **Arquivo**: `includes/player.bgt` (378 linhas)
- **Funcionalidade**:
  - Classe `player` completa com 50+ propriedades
  - Sistema de inventário, stats, timers
  - Estados: envenenado, paralisado, doente, etc.
  - Sistema de equipes e combate
  - Timers individuais para cada jogador
- **Arrays**: `player@[] players(0);`
- **NVGT Equivalente**: Classes nativas + timer system

#### **3. 🗺️ Sistema de Mapas (CORE)**
- **Arquivo**: `includes/map.bgt` (120 linhas)
- **Funcionalidade**:
  - `get_tile_at()` para verificação de tiles
  - Carregamento de mapas de arquivos `.map`
  - Sistema de plataformas, escadas, paredes
  - Verificação de posições válidas
- **NVGT Equivalente**: file handling + string processing nativo

#### **4. 📦 Sistema de Items/Objetos (CORE)**
- **Arquivo**: `includes/item.bgt` (216 linhas)
- **Funcionalidade**:
  - Classe `obj` para items no mundo
  - Sistema de timeout para items
  - Items aleatórios (`_rand` suffix)
  - Lógica de pegar/dropar items
- **Arrays**: `obj@[] objs;`
- **NVGT Equivalente**: Classes nativas + timer system

#### **5. ⚔️ Sistemas de Combate (COMPLEXO)**
- **Arquivos**: 20+ arquivos de comandos específicos
- **Funcionalidade**:
  - Balas, bombas, minas, projéteis
  - NPCs: dragões, cachorros, zumbis, etc.
  - Sistema de armas com dano/alcance
  - Efeitos: veneno, paralisia, fogo
- **Classes**: `bullet`, `bombaremota`, `dragonsauro`, etc.
- **NVGT Equivalente**: Classes nativas + physics simulation

#### **6. 🎵 Sistema de Som (IMPORTANTE)**
- **Arquivo**: `includes/moving_sound/msound.bgt`
- **Funcionalidade**:
  - Sons posicionais 3D
  - Sons em movimento (projéteis, NPCs)
  - Propagação de som por mapas
- **NVGT Equivalente**: `sound_pool` system (já usado no cliente)

#### **7. 🏠 Sistemas de Objetos de Mundo (MÉDIO)**
- **Arquivos**: apartamento, computador, fonteagua, etc.
- **Funcionalidade**:
  - Objetos interativos no mundo
  - Sistemas específicos (banheiros, pias, etc.)
  - Mecânicas especiais por objeto
- **NVGT Equivalente**: Classes nativas + event system

---

## 🚀 **ESTRATÉGIA DE CONVERSÃO PARA NVGT**

### 📋 **FASE 1: Configuração e Base (1-2 dias)**

#### **1.1 Configuração Inicial**
```bash
# Criar estrutura base
server/
├── server.nvgt - Arquivo principal
├── includes/
│   ├── config.nvgt - Configurações
│   ├── globals.nvgt - Utilitários globais
│   ├── network.nvgt - Sistema de rede NVGT
│   └── stubs.nvgt - Implementações temporárias
```

#### **1.2 Migração do `config.bgt`**
- ✅ **JÁ CONVERTIDO**: `config.nvgt` existe e está funcional
- **Ação**: Reutilizar configuração existente

#### **1.3 Implementação de Utilitários Base**
```nvgt
// server/includes/globals.nvgt
#include "../../config.nvgt"

// Funções utilitárias usando NVGT nativo
string[] nvgt_split(string str, string delimiter) {
    return str.split(delimiter);
}

void debug_log(string message) {
    file_put_contents("log.md", "[" + datetime().format("%Y-%m-%d %H:%M:%S") + "] " + message + "\n", true);
}

// Timer wrapper para compatibilidade
class game_timer {
    timer t;
    void restart() { t.restart(); }
    uint64 elapsed() { return t.elapsed; }
    void force(uint64 time) { t.force(time); }
    void pause() { t.pause(); }
}
```

### 📋 **FASE 2: Sistema de Rede NVGT (2-3 dias)**

#### **2.1 Implementação do Sistema de Rede**
```nvgt
// server/includes/network.nvgt
#include "../../include/networking.nvgt"  // NVGT networking library

game_net server_net;
uint64[] connected_peers;
string[] peer_addresses;

bool server_init(int port) {
    // Usar NVGT network server setup
    if(!server_net.setup_server(100, port)) {  // max 100 players
        debug_log("Erro: Não foi possível inicializar servidor na porta " + port);
        return false;
    }
    debug_log("Servidor iniciado na porta " + port);
    return true;
}

void server_broadcast(string message, string target_map = "") {
    for(uint i = 0; i < connected_peers.length(); i++) {
        if(target_map == "" || players[i].map == target_map) {
            server_net.send(connected_peers[i], message, 0, true);
        }
    }
}

// Criptografia usando NVGT nativo
string encrypt_packet(string data) {
    return string_aes_encrypt(data, NETWORK_ENCRYPTION_KEY);
}

string decrypt_packet(string data) {
    return string_aes_decrypt(data, NETWORK_ENCRYPTION_KEY);
}

void network_loop() {
    network_event@ event;
    while((@event = server_net.request()) !is null) {
        handle_network_event(event);
    }
}
```

#### **2.2 Compatibilidade com Cliente NVGT**
- **Protocolo**: Manter mesmo formato de mensagens do BGT
- **Criptografia**: Usar AES nativo do NVGT (`string_aes_encrypt/decrypt`)
- **Eventos**: Adaptar `network_event` BGT para NVGT events

### 📋 **FASE 3: Sistema de Jogadores (3-4 dias)**

#### **3.1 Conversão da Classe Player**
```nvgt
// server/includes/player.nvgt
player@[] players;

class player {
    // Dados básicos
    uint64 peer_id;
    string name;
    string map;
    int x, y;
    int level, xp, life;
    
    // Estados
    bool moderador = false;
    bool envenenado = false;
    bool paralisado = false;
    bool afk = false;
    
    // Timers usando NVGT nativo
    timer tempoveneno;
    timer tlutar;
    timer tinv;
    timer idletimer;
    
    // Inventário usando NVGT arrays/dictionaries
    dictionary@ inventory;  // NVGT dictionary for dynamic inventory
    
    // Métodos usando NVGT APIs
    void save_player() {
        string player_data = serialize_player_data();
        file_put_contents("players/" + name + ".usr", player_data);
    }
    
    void load_player() {
        if(file_exists("players/" + name + ".usr")) {
            string data = file_get_contents("players/" + name + ".usr");
            deserialize_player_data(data);
        }
    }
    
    void inv_add_item(string item, int amount) {
        if(inventory.exists(item)) {
            int current = int(inventory[item]);
            inventory[item] = current + amount;
        } else {
            inventory[item] = amount;
        }
    }
    
    int inv_item_number(string item) {
        if(inventory.exists(item)) {
            return int(inventory[item]);
        }
        return 0;
    }
}
```

#### **3.2 Sistema de Persistência NVGT**
```nvgt
// Serialização usando NVGT file APIs
string serialize_player_data() {
    string data = "";
    data += "name=" + name + "\n";
    data += "level=" + level + "\n";
    data += "xp=" + xp + "\n";
    data += "life=" + life + "\n";
    data += "map=" + map + "\n";
    data += "x=" + x + "\n";
    data += "y=" + y + "\n";
    
    // Serializar inventário
    string[] keys = inventory.get_keys();
    for(uint i = 0; i < keys.length(); i++) {
        data += "inv_" + keys[i] + "=" + inventory[keys[i]] + "\n";
    }
    
    return data;
}

void deserialize_player_data(string data) {
    string[] lines = data.split("\n");
    for(uint i = 0; i < lines.length(); i++) {
        if(lines[i].find("=") >= 0) {
            string[] parts = lines[i].split("=");
            string key = parts[0];
            string value = parts[1];
            
            if(key == "name") name = value;
            else if(key == "level") level = parse_int(value);
            else if(key == "xp") xp = parse_int(value);
            else if(key == "life") life = parse_int(value);
            else if(key == "map") map = value;
            else if(key == "x") x = parse_int(value);
            else if(key == "y") y = parse_int(value);
            else if(key.substr(0, 4) == "inv_") {
                string item = key.substr(4);
                inventory[item] = parse_int(value);
            }
        }
    }
}
```

### 📋 **FASE 4: Sistema de Mapas (2 dias)**

#### **4.1 Conversão do Sistema de Mapas**
```nvgt
// server/includes/map.nvgt
string get_tile_at(int x, int y, string mapname) {
    if(!file_exists("maps/" + mapname + ".map")) {
        return "";
    }
    
    string map_data = file_get_contents("maps/" + mapname + ".map");
    string[] lines = map_data.split("\n");
    
    for(uint i = 0; i < lines.length(); i++) {
        string[] parts = lines[i].split(":");
        if(parts[0] == "platform") {
            int minx = parse_int(parts[1]);
            int maxx = parse_int(parts[2]);
            int miny = parse_int(parts[3]);
            int maxy = parse_int(parts[3]);
            
            if(x >= minx && x <= maxx && y >= miny && y <= maxy) {
                return parts[4];
            }
        }
        // Processar outros tipos: wall, staircase, etc.
    }
    
    return "";
}

bool is_valid_position(int x, int y, string mapname) {
    string tile = get_tile_at(x, y, mapname);
    return tile != "";
}

void load_map_objects(string mapname) {
    // Carregar objetos específicos do mapa
    string map_data = file_get_contents("maps/" + mapname + ".map");
    string[] lines = map_data.split("\n");
    
    for(uint i = 0; i < lines.length(); i++) {
        string[] parts = lines[i].split(":");
        if(parts[0] == "spawn_item") {
            // Spawn items using NVGT
            spawn_item(parse_int(parts[1]), parse_int(parts[2]), parts[3]);
        }
    }
}
```

### 📋 **FASE 5: Sistema de Items/Objetos (2 dias)**

#### **5.1 Conversão do Sistema de Items**
```nvgt
// server/includes/item.nvgt
obj@[] world_objects;

class obj {
    string item_name;
    int amount;
    string map;
    int x, y;
    string owner;
    timer timeout_timer;
    bool marked_for_deletion = false;
    
    obj(int ox, int oy, string what, int qty, string m, string who = "") {
        x = ox;
        y = oy;
        item_name = what;
        amount = qty;
        map = m;
        owner = who;
        timeout_timer.restart();
    }
    
    void pickup_by_player(int player_index) {
        if(item_name == "coins") {
            players[player_index].inv_add_item("coins", amount);
            server_broadcast("play getcoins.ogg " + x + " " + y + " " + map, map);
        } else {
            players[player_index].inv_add_item(item_name, amount);
            server_broadcast("play getitem.ogg " + x + " " + y + " " + map, map);
        }
        
        marked_for_deletion = true;
    }
    
    void update() {
        // Auto cleanup after timeout
        if(timeout_timer.elapsed > 300000) {  // 5 minutes
            marked_for_deletion = true;
        }
    }
}

void spawn_item(int x, int y, string item, int amount = 1, string map = "", string owner = "") {
    world_objects.insert_last(obj(x, y, item, amount, map, owner));
}

void items_loop() {
    // Cleanup deleted items
    for(int i = int(world_objects.length()) - 1; i >= 0; i--) {
        world_objects[i].update();
        if(world_objects[i].marked_for_deletion) {
            world_objects.remove_at(i);
        }
    }
}
```

### 📋 **FASE 6: Sistema de Comandos (3-4 dias)**

#### **6.1 Sistema de Comandos Base**
```nvgt
// server/includes/commands.nvgt
void process_player_command(int player_index, string command) {
    string[] parts = command.split(" ");
    string cmd = parts[0].lower();
    
    if(cmd == "move") {
        handle_move_command(player_index, parts);
    } else if(cmd == "attack") {
        handle_attack_command(player_index, parts);
    } else if(cmd == "say") {
        handle_chat_command(player_index, parts);
    } else if(cmd == "drop") {
        handle_drop_command(player_index, parts);
    } else if(cmd == "get") {
        handle_pickup_command(player_index, parts);
    }
    // Adicionar mais comandos conforme necessário
}

void handle_move_command(int player_index, string[] parts) {
    if(parts.length() < 3) return;
    
    int new_x = parse_int(parts[1]);
    int new_y = parse_int(parts[2]);
    
    if(is_valid_position(new_x, new_y, players[player_index].map)) {
        players[player_index].x = new_x;
        players[player_index].y = new_y;
        
        // Broadcast movement to other players
        server_broadcast("playermove " + players[player_index].name + " " + new_x + " " + new_y, 
                        players[player_index].map);
    }
}
```

### 📋 **FASE 7: Sistema de Som NVGT (2 dias)**

#### **7.1 Adaptação do Sistema de Som**
```nvgt
// server/includes/sound.nvgt
void play_positional_sound(string sound_file, int x, int y, string map, string exclude_player = "") {
    string message = "play " + sound_file + " " + x + " " + y + " " + map;
    
    for(uint i = 0; i < players.length(); i++) {
        if(players[i].map == map && players[i].name != exclude_player) {
            server_net.send(players[i].peer_id, message, 0, true);
        }
    }
}

void play_sound_to_player(int player_index, string sound_file) {
    server_net.send(players[player_index].peer_id, "ps " + sound_file, 0, true);
}

void broadcast_sound(string sound_file, string target_map = "") {
    for(uint i = 0; i < players.length(); i++) {
        if(target_map == "" || players[i].map == target_map) {
            play_sound_to_player(i, sound_file);
        }
    }
}
```

### 📋 **FASE 8: Loop Principal e Integração (2 dias)**

#### **8.1 Loop Principal NVGT**
```nvgt
// server/server.nvgt
#include "../config.nvgt"
#include "includes/globals.nvgt"
#include "includes/network.nvgt"
#include "includes/player.nvgt"
#include "includes/map.nvgt"
#include "includes/item.nvgt"
#include "includes/commands.nvgt"
#include "includes/sound.nvgt"

void main() {
    debug_log("Iniciando servidor EVM-NVGT...");
    
    // Inicializar sistema de rede
    if(!server_init(port)) {
        debug_log("ERRO: Falha ao inicializar servidor");
        exit();
    }
    
    // Carregar configurações e dados
    load_server_data();
    
    // Loop principal
    while(true) {
        wait(5);  // NVGT wait
        
        if(key_pressed(KEY_ESCAPE)) {
            save_all_players();
            debug_log("Servidor finalizado");
            exit();
        }
        
        game_loop();
    }
}

void game_loop() {
    network_loop();        // Processar eventos de rede
    players_loop();        // Atualizar jogadores
    items_loop();          // Atualizar items no mundo
    npcs_loop();           // Atualizar NPCs (se implementado)
    combat_loop();         // Processar combate
    timers_loop();         // Processar timers globais
}
```

---

## 📚 **BIBLIOTECAS NVGT NATIVAS A UTILIZAR**

### 🌐 **Networking**
```nvgt
#include "networking.nvgt"  // Para game_net, network_event
```
- `game_net` class para servidor/cliente
- `network_event` para eventos de rede  
- AES encryption nativo: `string_aes_encrypt/decrypt`

### 📁 **File System**
```nvgt
// Funções nativas NVGT (built-in)
file_exists()
file_get_contents()
file_put_contents()
directory_exists()
directory_create()
```

### 🕐 **Timers**
```nvgt
// Timer nativo NVGT
timer class {
    .restart()
    .elapsed
    .force()
    .pause()
}
```

### 🔤 **Strings**
```nvgt
// Métodos nativos string NVGT
string.split()
string.find()
string.substr()
string.replace()
string.lower()
string.upper()
```

### 📊 **Data Structures**
```nvgt
// Arrays dinâmicos nativos
array<type>
// Dicionários nativos  
dictionary
```

### 🎵 **Audio**
```nvgt
#include "sound_pool.nvgt"
```
- `sound_pool` para gerenciamento de áudio
- Sons posicionais integrados

### 🔢 **Math & Utilities**
```nvgt
// Funções nativas
parse_int()
parse_float()
random()
datetime()
```

---

## 🎯 **ROADMAP DETALHADO DE IMPLEMENTAÇÃO**

### **Semana 1: Base e Rede**
- **Dia 1-2**: Fase 1 (Configuração Base)
- **Dia 3-5**: Fase 2 (Sistema de Rede NVGT)
- **Dia 6-7**: Testes básicos de conectividade

### **Semana 2: Core Systems**
- **Dia 1-4**: Fase 3 (Sistema de Jogadores)
- **Dia 5-6**: Fase 4 (Sistema de Mapas)
- **Dia 7**: Testes de sistemas integrados

### **Semana 3: Gameplay**
- **Dia 1-2**: Fase 5 (Sistema de Items)
- **Dia 3-6**: Fase 6 (Sistema de Comandos)
- **Dia 7**: Testes de gameplay básico

### **Semana 4: Finalização**
- **Dia 1-2**: Fase 7 (Sistema de Som)
- **Dia 3-4**: Fase 8 (Loop Principal)
- **Dia 5-7**: Testes completos e otimização

---

## 🔧 **VANTAGENS DO NVGT SOBRE BGT**

### **🚀 Performance**
- **Compilação**: NVGT compila para código nativo mais eficiente
- **Memory Management**: Melhor gerenciamento de memória
- **Threading**: Suporte nativo a threads se necessário

### **🛡️ Segurança**
- **Encryption**: AES nativo integrado
- **Type Safety**: Melhor verificação de tipos
- **Error Handling**: Sistema de exceções mais robusto

### **📚 APIs Modernas**
- **Networking**: APIs de rede mais modernas e eficientes  
- **File I/O**: Sistema de arquivos mais rápido
- **Audio**: Sistema de áudio 3D integrado

### **🔄 Compatibilidade**
- **Cross-platform**: NVGT é mais portável
- **Future-proof**: NVGT está em desenvolvimento ativo
- **Community**: Comunidade crescente

---

## ⚠️ **DESAFIOS E CONSIDERAÇÕES**

### **🔍 Compatibilidade de Protocolo**
- **Desafio**: Manter protocolo compatível com cliente NVGT
- **Solução**: Usar mesmo formato de mensagens e criptografia

### **⏱️ Performance com Muitos Jogadores**
- **Desafio**: 100+ jogadores simultâneos
- **Solução**: Otimizar loops usando NVGT efficient structures

### **🎮 Complexidade dos NPCs**
- **Desafio**: 20+ tipos de NPCs com IA
- **Solução**: Implementar gradualmente, sistema modular

### **💾 Migração de Dados**
- **Desafio**: Converter dados existentes de jogadores BGT
- **Solução**: Script de migração automática

---

## 🎊 **RESULTADO ESPERADO**

### **📈 Melhorias**
- **Performance**: 30-50% mais rápido que BGT
- **Estabilidade**: Menos crashes, melhor error handling
- **Escalabilidade**: Suporte a mais jogadores simultâneos
- **Manutenibilidade**: Código mais limpo e modular

### **✅ Compatibilidade Total**
- **Cliente NVGT**: 100% compatível 
- **Dados Existentes**: Migração automática
- **Comandos**: Todos os comandos administrativos mantidos
- **Gameplay**: Experiência idêntica ao BGT

### **🚀 Benefícios Futuros**
- **Expansibilidade**: Fácil adicionar novas funcionalidades
- **Cross-platform**: Potencial para Linux/Mac
- **Performance**: Base sólida para crescimento

---

## 📝 **PRÓXIMOS PASSOS IMEDIATOS**

1. **✅ Aprovação do Plano**: Revisar e aprovar este roadmap
2. **🔧 Setup Ambiente**: Configurar ambiente de desenvolvimento NVGT
3. **📋 Fase 1**: Iniciar conversão com configuração base
4. **🧪 Testes Contínuos**: Testar cada fase com cliente NVGT
5. **📊 Monitoramento**: Acompanhar progresso vs. cronograma

**Este plano garante uma conversão sistemática, eficiente e totalmente compatível do servidor EVM para NVGT, aproveitando ao máximo as funcionalidades nativas e modernas da plataforma.**