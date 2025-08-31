# Relatório de Migração BGT → NVGT - Projeto IG

## 🔧 Capacidades Nativas do NVGT (IMPORTANTE)

### SQLite Plugin (nvgt_sqlite)
NVGT possui plugin nativo para SQLite que pode substituir implementações customizadas:
- **Plugin:** `#pragma plugin nvgt_sqlite`
- **Funcionalidade:** Interface completa para banco de dados SQLite
- **Vantagem:** Performance superior e funcionalidades avançadas vs. arrays customizados
- **Status:** Disponível (precisa de documentação detalhada)

### Sistema de Concorrência Nativo
NVGT oferece sistema de threading robusto com múltiplas primitivas:
- **async<T>:** Execução assíncrona com template para tipos de retorno
- **mutex:** Exclusão mútua para proteção de recursos compartilhados
- **atomic_T:** Operações atômicas (atomic_int, atomic_bool, etc.)
- **thread_event:** Sincronização entre threads (manual/auto reset)
- **Funcionalidades:** 
  - Timeouts configuráveis
  - Notificação de threads (notify_one/notify_all)
  - Memory ordering para performance
  - Proteção contra deadlocks

### Recomendação de Arquitetura
1. **Database:** Migrar para SQLite nativo para dados persistentes
2. **Threading:** Usar async<T> para operações de rede/IO
3. **Sincronização:** atomic_T para flags simples, mutex para recursos complexos
4. **Custom DB Class:** Manter apenas para compatibility layer se necessário

## Sumário

1. [Resumo Executivo do Projeto](#1-resumo-executivo-do-projeto)
2. [Inventário do Código](#2-inventário-do-código)
3. [Contratos e Fronteiras (Cliente/Servidor)](#3-contratos-e-fronteiras-clienteservidor)
4. [Matriz de Migração BGT → NVGT](#4-matriz-de-migração-bgt--nvgt)
5. [Lacunas e Adaptações Necessárias](#5-lacunas-e-adaptações-necessárias)
6. [Plano de Ação Detalhado e Ordem Lógica de Conversão](#6-plano-de-ação-detalhado-e-ordem-lógica-de-conversão)
7. [Checklist de Conformidade com a Documentação NVGT](#7-checklist-de-conformidade-com-a-documentação-nvgt)
8. [Estratégia de Testes e Paridade de Comportamento](#8-estratégia-de-testes-e-paridade-de-comportamento)
9. [Riscos, Mitigações e Plano de Rollback](#9-riscos-mitigações-e-plano-de-rollback)
10. [Próximas Ações Concretas](#10-próximas-ações-concretas)

---

## 1. Resumo Executivo do Projeto

### Finalidade do jogo/sistema
O Projeto IG é um audio game multiplayer em mundo aberto que simula um ambiente virtual interativo onde jogadores podem:
- Explorar mapas com sistema de áudio espacial 3D
- Interagir com outros jogadores em tempo real
- Usar sistema de inventário e comércio
- Combater com diferentes armas
- Construir e personalizar ambientes
- Participar de eventos e missões

### Plataformas-alvo
- **Principal**: Windows (95% do código atual)
- **Potencial**: Linux/macOS com NVGT (expansão futura)

### Principais features implementadas

**Áudio/TTS:**
- Sistema de áudio 3D espacial com BASS library
- Text-to-speech integrado
- Beacons de posicionamento para jogadores
- Efeitos sonoros contextuais (chuva, passos, combate)
- Sistema de vozes/mensagens gravadas

**Entrada:**
- Input de teclado com sistema key_hold customizado
- Controles de movimento omnidirecional
- Sistema de comandos por chat
- Atalhos de teclado para ações rápidas

**Rede:**
- Arquitetura cliente/servidor TCP confiável
- Protocolo de mensagens em texto estruturado
- Sistema de heartbeat e reconexão
- Suporte para múltiplos idiomas (PT, ES, EN, FR, TR)

**Filesystem:**
- Sistema de persistência com arquivos criptografados
- Gestão de mapas, inventários e configurações
- Sistema de packs para distribução de conteúdo
- Logs e backups automáticos

**Timers:**
- Sistema de cooldowns para ações
- Eventos temporais (chuva, spawns, leilões)
- Beacons de posição periódicos
- Sistema de turnos em combate

**UI/CLI:**
- Menus navegáveis por teclado
- Sistema de diálogos interativos
- Chat multicanal com moderação
- Editor de mapas integrado

### Pontos sensíveis
- **Latência de áudio**: Sistema 3D requer <50ms para imersão
- **Sincronização de rede**: Estados compartilhados críticos para gameplay
- **GameEngine.dll**: Dependência externa sem código-fonte
- **BASS.dll**: Dependência de áudio comercial
- **Performance**: 100+ jogadores simultâneos com áudio espacial
- **Criptografia**: Proteção de assets e dados de usuário

---

## 2. Inventário do Código

### Árvore de diretórios

```
C:\git\bgt\projetoIg\
├── cliente\                          # 🖥️ CLIENTE
│   ├── Projeto Ig.bgt               # Main entry point (150 linhas)
│   ├── includes\                    # Core modules
│   │   ├── net.bgt                  # Network client (800+ linhas) ⭐
│   │   ├── player.bgt               # Player management (600+ linhas) ⭐
│   │   ├── map.bgt                  # Map rendering (500+ linhas) ⭐
│   │   ├── bass.bgt                 # Audio system (400+ linhas) ⭐
│   │   ├── GameEngine.bgt           # External DLL interface (200 linhas) ⚠️
│   │   ├── menu.bgt                 # UI system (300 linhas)
│   │   ├── commands.bgt             # Command processing (400 linhas)
│   │   ├── inv.bgt                  # Inventory (250 linhas)
│   │   └── [42+ outros módulos]
│   ├── lang\                        # Internationalization
│   └── audios\                      # Audio assets
├── servidor\                        # 🖥️ SERVIDOR  
│   ├── server.bgt                   # Main server (200 linhas)
│   ├── includes\
│   │   ├── net.bgt                  # Network server (1000+ linhas) ⭐
│   │   ├── player.bgt               # Player state mgmt (700+ linhas) ⭐
│   │   ├── map.bgt                  # Map server logic (400+ linhas) ⭐
│   │   ├── login.bgt                # Authentication (300 linhas) ⭐
│   │   ├── weapons.bgt              # Combat system (250 linhas)
│   │   └── [35+ outros módulos]
│   ├── maps\                        # Map files (500+ arquivos .map)
│   ├── commands\                    # Admin commands (100+ arquivos .txt)
│   └── items\                       # Item definitions
└── config-test.bgt                  # 🔄 COMUM - Configurações globais
```

### Tamanho aproximado por componente

| Componente | Cliente (linhas) | Servidor (linhas) | Criticidade |
|------------|------------------|-------------------|-------------|
| Sistema de Rede | 800 | 1000 | 🔴 Crítico |
| Gerenciamento de Jogadores | 600 | 700 | 🔴 Crítico |
| Sistema de Mapas | 500 | 400 | 🔴 Crítico |
| Sistema de Áudio | 400 | 50 | 🔴 Crítico |
| GameEngine Integration | 200 | 0 | ⚠️ Dependência externa |
| Autenticação/Login | 100 | 300 | 🟡 Importante |
| Interface/Menus | 300 | 0 | 🟡 Importante |
| Sistema de Comandos | 400 | 200 | 🟡 Importante |
| Inventário | 250 | 100 | 🟢 Normal |
| **Total Estimado** | **~8000** | **~6000** | **14000 linhas** |

### Grafo de dependências principais

**Cliente:**
```
Projeto Ig.bgt
├── net.bgt ← player.bgt, map.bgt, commands.bgt
├── bass.bgt ← src.bgt, src2.bgt, voices.bgt
├── GameEngine.bgt ← map.bgt, player.bgt
├── player.bgt ← inv.bgt, weapon.bgt
└── menu.bgt ← dialogs.bgt, simple_menu.bgt
```

**Servidor:**
```
server.bgt
├── net.bgt ← player.bgt, map.bgt, login.bgt
├── player.bgt ← weapons.bgt, inv.bgt, marriages.bgt
├── login.bgt ← db.bgt, tempban.bgt
└── map.bgt ← zones.bgt, portals.bgt, vehicles.bgt
```

### Mapa de camadas

**CLIENTE:**
- **Apresentação**: menu.bgt, dialogs.bgt, voices.bgt
- **Aplicação**: commands.bgt, player.bgt, inv.bgt  
- **Domínio**: map.bgt, weapon.bgt, vehicles.bgt
- **Infraestrutura**: net.bgt, bass.bgt, GameEngine.bgt
- **Dados**: db.bgt, parsed_data.bgt

**SERVIDOR:**
- **API**: commands/ (admin commands)
- **Aplicação**: login.bgt, player.bgt, arena.bgt
- **Domínio**: map.bgt, weapons.bgt, marriages.bgt
- **Infraestrutura**: net.bgt, db.bgt
- **Dados**: *.db, *.usr, maps/

---

## 3. Contratos e Fronteiras (Cliente/Servidor)

### Identificação dos componentes

**Cliente** (`cliente/`): Interface de usuário, renderização de áudio 3D, input handling
**Servidor** (`servidor/`): Lógica de negócio, persistência, authoritative state

### Protocolo de comunicação

**Tipo**: TCP confiável
**Porto**: Configurável via `config-test.bgt` (padrão: indeterminado)
**Serialização**: Texto estruturado com separadores

### Handshake e autenticação
```bgt
// Login sequence
CLIENT → SERVER: "login {username} {password} {client_version}"
SERVER → CLIENT: "login_ok {player_id} {x} {y} {map_name}"
SERVER → CLIENT: "login_error {error_code} {message}"
```

### Esquema de mensagens principais

| Comando | Direção | Frequência | Formato | Exemplo |
|---------|---------|-------------|---------|---------|
| `move` | C→S | Alto (movimento) | `"move {x} {y}"` | `"move 10 15"` |
| `player_moved` | S→C | Alto (broadcast) | `"player_moved {id} {x} {y}"` | `"player_moved 123 10 15"` |
| `chat` | C→S | Médio | `"chat {message}"` | `"chat hello world"` |
| `chat_message` | S→C | Médio | `"chat_message {id} {message}"` | `"chat_message 123 hello"` |
| `beacon` | S→C | Periódico | `"beacon {id} {x} {y}"` | `"beacon 123 10 15"` |
| `disconnect` | Ambos | Baixo | `"disconnect {reason}"` | `"disconnect timeout"` |
| `map_change` | S→C | Baixo | `"map_change {map_name}"` | `"map_change bosque"` |
| `item_pickup` | C→S | Baixo | `"item_pickup {item_id}"` | `"item_pickup sword_001"` |

### Dependências específicas do ambiente

**Cliente:**
- Windows: `bass.dll`, `GameEngine.dll`, `nvdaControllerClient32.dll`
- Permissões: Network access, audio device access, file write access

**Servidor:**
- Windows: File system access para maps/, database files
- Permissões: Network binding, file read/write, potencialmente service installation
- Portas: TCP listening port (configurável)

---

## 4. Matriz de Migração BGT → NVGT

| Capacidade | API/Uso Atual BGT | Equivalente NVGT | Notas de Compatibilidade | Risco | Complexidade |
|------------|-------------------|------------------|--------------------------|--------|--------------|
| **Áudio 3D** | `sound_pool_3d`, `play_3d()`, `update_sound_position()` | `sound` object (NVGT), spatial audio built-in | NVGT usa BASS internamente, compatibilidade esperada | Médio | 4 |
| **Network/Sockets** | `network`, `network_event`, `send_reliable()` | TCP stream sockets, websockets client (NVGT docs) | Mudança de API, refatoração necessária | Alto | 5 |
| **Áudio Base** | `bass2` library, `BASS_Init()`, `BASS_StreamCreateURL()` | `sound` object, `mixer` class | NVGT abstrai BASS, simplifica API | Baixo | 3 |
| **TTS** | `speak()` | `screen_reader_speak()`, `speech.nvgt` include | API similar, funcionalidade mantida | Baixo | 2 |
| **Timers** | `timer`, `wait()` | `timer`, `wait()` | Compatibilidade direta esperada | Baixo | 1 |
| **Entrada/Teclado** | `key_down()`, `key_pressed()` | Equivalentes esperados (não documentados) | API similar esperada | Médio | 3 |
| **Filesystem** | `file`, `directory_exists()`, `pack_file` | File operations disponíveis, `#pragma embed` | API de arquivos mantida | Baixo | 2 |
| **Database** | Classe customizada `db` | Manter implementação customizada | Não é funcionalidade nativa do BGT/NVGT | Baixo | 1 |
| **String Processing** | `string_split()`, `string_replace()` | Funções equivalentes esperadas | Core language features | Baixo | 1 |
| **Criptografia** | `string_encrypt()`, `string_decrypt()` | **⚠️ LACUNA IDENTIFICADA** | Pode precisar de biblioteca externa | Alto | 4 |
| **Threading** | Limitado no BGT | **Investigar disponibilidade NVGT** | Melhorias possíveis | Médio | 3 |
| **GameEngine.dll** | `library engine`, funções específicas | **⚠️ BLOQUEIO CRÍTICO** | DLL externa sem código-fonte | Muito Alto | 5 |
| **Random/Math** | `random()`, operadores aritméticos | Equivalentes diretos esperados | Core language | Baixo | 1 |

---

## 5. Lacunas e Adaptações Necessárias

### 5.1 Database - Usar SQLite Nativo (ALTA PRIORIDADE)
**Oportunidade**: NVGT possui plugin SQLite nativo que é superior ao sistema atual
**Recomendação**: Migrar `db.nvgt` customizado para SQLite nativo

**Benefícios**:
- Performance superior para grandes datasets
- Queries SQL complexas vs. loops em arrays
- Transações ACID para consistência de dados
- Backup/restore nativo
- Índices para busca rápida

**Migração sugerida**:
```angelscript
#pragma plugin nvgt_sqlite

class DatabaseManager {
    database@ db;
    
    bool init(string filename) {
        @db = database();
        return db.open(filename);
    }
    
    // Migrar métodos get/set para SQL
    string get(string key) {
        database_result@ result = db.execute("SELECT value FROM config WHERE key = ?", {key});
        return result.rows.length() > 0 ? result.rows[0][0] : "";
    }
    
    void set(string key, string value) {
        db.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", {key, value});
    }
}
```

### 5.2 Threading - Usar Concorrência Nativa (ALTA PRIORIDADE)
**Oportunidade**: NVGT oferece sistema de threading robusto
**Recomendação**: Implementar async operations para rede/IO

**Implementação sugerida**:
```angelscript
// Para operações de rede assíncronas
async<bool> network_operation(string data) {
    // Operação em background thread
    return tcp_socket.send(data);
}

// Para proteção de recursos compartilhados
mutex player_list_mutex;
atomic_int connection_count;

class NetworkManager {
    async<network_event@>@ pending_request;
    
    void send_async(string data) {
        @pending_request = async<network_event@>(tcp_send_operation, data);
    }
    
    network_event@ check_response() {
        if (pending_request.complete) {
            return pending_request.value;
        }
        return null;
    }
}
```

### 5.3 GameEngine.dll - Bloqueio Crítico
**Problema**: Dependência de DLL externa sem código-fonte disponível
**Funcionalidades em risco**:
- `spawn_platform2D()`, `spawn_platform3D()`
- `start_recording_audio()`, `stop_recording_audio()`
- `import_map()`, `export_map()`

**Adaptação proposta**:
```angelscript
// Adapter interface
class GameEngineAdapter {
    bool spawn_platform2D(int x, int y, string type) {
        // Implementation using NVGT native features
        // or disable functionality temporarily
        return false; // Graceful degradation
    }
    
    void start_recording_audio() {
        // Investigate NVGT audio recording capabilities
        // or use external process
    }
}
```

### 5.4 Sistema de Criptografia
**Problema**: `string_encrypt()` / `string_decrypt()` não documentados no NVGT
**Adaptação necessária**:
```angelscript
// Crypto adapter using external library
#pragma include "crypto_adapter.nvgt"

class CryptoAdapter {
    string encrypt(string data, string key) {
        // Implement using available crypto library
        // Consider: OpenSSL, libsodium bindings
        return encrypted_data;
    }
}
```

### 5.5 Network API Redesign
**Problema**: BGT `network` class vs NVGT TCP sockets
**Refatoração necessária**:

**BGT atual**:
```bgt
network net;
network_event event;
event = net.request();
if(event.type == event_receive) {
    string message = event.message;
}
```

**NVGT proposto**:
```angelscript
// New network wrapper
class NetworkManager {
    tcp_socket socket;
    string[] message_queue;
    
    void connect(string host, int port) {
        socket.connect(host, port);
    }
    
    NetworkEvent get_event() {
        // Implement event-based wrapper
        // around socket operations
    }
}
```

### 5.4 Áudio 3D Spatial
**Restrições NVGT a investigar**:
- Máximo de sources simultâneas
- Latência do sistema
- Compatibilidade com HRTF
- Performance com 100+ jogadores

### 5.5 Threading e Async Operations
**Lacuna**: Modelo de concorrência não documentado no NVGT
**Investigação necessária**:
- Suporte a operações não-bloqueantes
- Thread pool para I/O
- Async networking

---

## 6. Plano de Ação Detalhado e Ordem Lógica de Conversão

### Priorização Atualizada com Capacidades Nativas NVGT

**MUDANÇA ESTRATÉGICA**: Aproveitar SQLite e threading nativos do NVGT para arquitetura superior

### Roadmap Sequencial

#### **FASE 0: Preparação (Semanas 1-2)**
**Arquivos afetados**: Nenhum código-fonte alterado
- [ ] Setup ambiente NVGT development
- [ ] Análise profunda da documentação NVGT
- [ ] Proof of concept: Hello World NVGT
- [ ] **NOVO**: Teste SQLite plugin e threading nativo
- **Critério de pronto**: Ambiente funcional e POCs validados
- **Teste mínimo**: Compilação, execução básica, SQLite + async

#### **FASE 1: Fundamentos Modernizados (Semanas 3-4)** ✅ CONCLUÍDA
**Arquivos convertidos**: 
- `projeto nvgt/servidor/includes/db.nvgt` (BGT compatibility)
- `projeto nvgt/config-test.nvgt` (Global constants)
- `projeto nvgt/servidor/includes/readable_time.nvgt` (Time utilities)
- `projeto nvgt/servidor/includes/net.nvgt` (Basic TCP wrapper)

**Status**: Implementação customizada funcionando, mas...
**PRÓXIMA ITERAÇÃO**: Avaliar migração para SQLite nativo
- [ ] **Decisão técnica**: Manter db.nvgt customizado ou migrar para SQLite?
- [ ] **Análise**: Performance e complexidade de dados atuais
- [ ] **POC**: Converter parte do sistema para SQLite nativo

#### **FASE 2: Modernização Database (NOVA - Semanas 5-6)**  
**Decisão pendente**: Aproveitar SQLite nativo vs. manter compatibilidade
**Arquivos afetados**:
- `projeto nvgt/servidor/includes/database_manager.nvgt` (NOVO)
- `projeto nvgt/servidor/includes/db.nvgt` (Adapter layer se necessário)

**Implementação sugerida**:
- [ ] Criar DatabaseManager com SQLite nativo
- [ ] Migrar dados de config para SQLite
- [ ] Performance testing vs. implementação atual
- [ ] Manter backward compatibility se necessário
- **Critério de pronto**: Performance igual ou superior + dados migrados

#### **FASE 3: Threading e Concorrência (NOVA - Semanas 7-8)**
**Objetivo**: Modernizar para async operations nativas
**Arquivos afetados**:
- `projeto nvgt/servidor/includes/net.nvgt` (Upgrade para async)
- `projeto nvgt/servidor/includes/async_manager.nvgt` (NOVO)

**Implementação**:
- [ ] Converter operações de rede para async<T>
- [ ] Implementar mutex para recursos compartilhados
- [ ] atomic_int para contadores (conexões, players online)
- [ ] thread_event para sincronização
- **Critério de pronto**: Operações não-blocking + thread safety

#### **FASE 4: Networking Servidor (Semanas 9-11)**  
**Arquivos afetados**:
- `projeto nvgt/servidor/server.nvgt` (Main server loop)
- Upgrade de `net.nvgt` com async operations

**Dependências**: Threading modernizado (Fase 3)
- [ ] Implementar async NetworkManager 
- [ ] Event-driven wrapper sobre TCP sockets
- [ ] Parser de protocolo com threading
- [ ] Sistema de heartbeat assíncrono
- [ ] Pool de connections thread-safe
- **Critério de pronto**: Cliente BGT consegue conectar ao servidor NVGT
- **Teste mínimo**: Login e chat básico funcionando com concorrência
**Arquivos afetados**:
- `servidor/includes/login.bgt` ⭐
- `servidor/includes/player.bgt` ⭐
- `servidor/includes/tempban.bgt`

**Dependências**: Fase 2 (network)
- [ ] Sistema de login/logout
- [ ] Gerenciamento de estado de jogadores
- [ ] Persistência de dados de usuário
- [ ] Sistema de bans temporários
- **Critério de pronto**: Múltiplos clientes BGT logando simultaneamente
- **Teste mínimo**: Login concurrent de 10 usuários

#### **FASE 4: Mapas e Posicionamento Servidor (Semanas 10-11)**
**Arquivos afetados**:
- `servidor/includes/map.bgt` ⭐
- `servidor/includes/zones.bgt`
- `servidor/includes/portals.bgt`

**Dependências**: Fase 3 (player state)
- [ ] Carregamento de mapas (.map files)
- [ ] Sistema de coordenadas e movimento
- [ ] Validação de posições
- [ ] Broadcast de movimentos
- **Critério de pronto**: Jogadores se veem e se movem no mapa
- **Teste mínimo**: Movimento multiplayer sincronizado

#### **FASE 5: Combat e Items Servidor (Semanas 12-13)**
**Arquivos afetados**:
- `servidor/includes/weapons.bgt`
- `servidor/includes/item.bgt`
- `servidor/includes/crafting.bgt`

**Dependências**: Fase 4 (mapas)
- [ ] Sistema de armas e combate
- [ ] Inventário servidor-side  
- [ ] Drops e pickups
- [ ] Sistema de crafting
- **Critério de pronto**: Combate funcional entre jogadores
- **Teste mínimo**: PvP básico com diferentes armas

#### **FASE 6: Cliente - Fundamentos (Semanas 14-15)**
**Arquivos afetados**:
- `cliente/includes/db.bgt` (reutilizar)
- `cliente/Projeto Ig.bgt` (main entry)

**Dependências**: Servidor estável (Fases 1-5)
- [ ] Port dos utilitários para cliente
- [ ] Main loop básico NVGT
- [ ] Configurações cliente
- **Critério de pronto**: Cliente NVGT conecta no servidor NVGT
- **Teste mínimo**: Handshake successful

#### **FASE 7: Cliente - Networking (Semanas 16-17)**
**Arquivos afetados**:
- `cliente/includes/net.bgt` ⭐ CRÍTICO

**Dependências**: Fase 6
- [ ] NetworkManager cliente NVGT
- [ ] Event processing loop
- [ ] Command sender
- **Critério de pronto**: Chat bidirecional funcionando
- **Teste mínimo**: Conversação entre 2 clientes NVGT

#### **FASE 8: Cliente - Áudio Básico (Semanas 18-19)**
**Arquivos afetados**:
- `cliente/includes/bass.bgt` → Substituir por NVGT sound
- `cliente/includes/voices.bgt`

**Dependências**: Fase 7
- [ ] Sistema de áudio 2D NVGT
- [ ] TTS integration
- [ ] UI sounds (beeps, notifications)
- **Critério de pronto**: Feedback auditivo básico funcionando  
- **Teste mínimo**: Mensagens faladas via TTS

#### **FASE 9: Cliente - Áudio 3D (Semanas 20-22)**
**Arquivos afetados**:
- `cliente/includes/src.bgt` ⭐ CRÍTICO
- `cliente/includes/src2.bgt`
- `cliente/includes/player.bgt`

**Dependências**: Fase 8
- [ ] Sound pool 3D em NVGT
- [ ] Beacons de jogadores
- [ ] Environmental audio
- [ ] Performance optimization
- **Critério de pronto**: Áudio espacial comparável ao BGT
- **Teste mínimo**: Localização precisa de 5+ jogadores por áudio

#### **FASE 10: Cliente - Interface (Semanas 23-24)**
**Arquivos afetados**:
- `cliente/includes/menu.bgt`
- `cliente/includes/dialogs.bgt`
- `cliente/includes/commands.bgt`

**Dependências**: Fase 9
- [ ] Sistema de menus
- [ ] Input handling
- [ ] Command processor
- **Critério de pronto**: Interface navegável completamente
- **Teste mínimo**: Navegação completa dos menus

#### **FASE 11: GameEngine.dll Workarounds (Semanas 25-26)**
**Arquivos afetados**:
- `cliente/includes/GameEngine.bgt` ⚠️
- Módulos dependentes

**Dependências**: Fase 10  
- [ ] Implementar adapters para funcionalidades críticas
- [ ] Graceful degradation para funcionalidades não-disponíveis
- [ ] Alternative implementations onde possível
- **Critério de pronto**: Jogo funcional sem GameEngine.dll
- **Teste mínimo**: Gameplay completo sem crashes

#### **FASE 12: Empacotamento/Distribuição (Semanas 27-28)**
**Arquivos afetados**:
- Build scripts
- Asset packaging

**Dependências**: Fase 11
- [ ] NVGT build optimization
- [ ] Asset packing com NVGT
- [ ] Installer/updater
- **Critério de pronto**: Distribuição funcional
- **Teste mínimo**: Install e execução em máquina limpa

### Nós críticos do grafo (blockers)

1. **`servidor/includes/net.bgt`** - Bloqueia todo networking
2. **`cliente/includes/src.bgt`** - Bloqueia áudio 3D  
3. **`GameEngine.bgt`** - Bloqueia funcionalidades avançadas
4. **`bass.bgt`** - Bloqueia todo áudio cliente

---

## 7. Checklist de Conformidade com a Documentação NVGT

### Funcionalidades por Seção da Documentação NVGT

**⚠️ NOTA**: Documentação NVGT limitada encontrada. Referencias precisam ser validadas.

#### Áudio (nvgt.gg/docs/audio - presumido)
- [ ] Usar `sound` object para reprodução básica
- [ ] Implementar `mixer` class para mixing múltiplas fontes
- [ ] Verificar compatibilidade HRTF para áudio 3D
- [ ] Validar latência <50ms para audio games
- [ ] Testar com 100+ sources simultâneas

#### Networking (nvgt.gg/docs/network - presumido)  
- [ ] Usar TCP sockets para reliable messaging
- [ ] Implementar WebSocket client se necessário para web features
- [ ] HTTP object para atualizações/telemetria
- [ ] Validar throughput para 100+ jogadores simultâneos

#### Threading/Async (nvgt.gg/docs/async - presumido)
- [ ] Investigar model de concorrência NVGT
- [ ] Non-blocking I/O para network operations
- [ ] Thread safety para shared state

#### File I/O (nvgt.gg/docs/files - presumido)
- [ ] Usar APIs padrão de file operations  
- [ ] `#pragma embed` para asset embedding
- [ ] Validar performance com arquivos grandes (mapas)

### Itens de Segurança/Estabilidade

#### Tratamento de Erros
- [ ] Try/catch para todas operações de rede
- [ ] Validação de input do usuário
- [ ] Graceful degradation para falhas de áudio
- [ ] Logging structured de erros

#### Limites e Buffers
- [ ] Network message size limits (avoid buffer overflow)
- [ ] Audio buffer underrun protection
- [ ] Memory usage limits para sound pools
- [ ] Connection timeout management

#### Thread Safety
- [ ] Validar se NVGT sound operations são thread-safe
- [ ] Synchronization para shared game state
- [ ] Lock-free data structures onde possível

### Performance Critical Path

#### Áudio
- [ ] Latência máxima 50ms para spatial audio
- [ ] CPU usage <30% para audio processing
- [ ] Memory footprint <500MB para sound pools

#### Network
- [ ] Round-trip time <100ms para game actions
- [ ] Packet loss recovery mechanisms
- [ ] Bandwidth optimization (compression)

#### Geral
- [ ] Startup time <10s
- [ ] Memory leaks prevention
- [ ] CPU usage monitoring

### APIs Deprecadas a Evitar

**⚠️ LACUNA**: Sem documentação específica sobre APIs deprecadas no NVGT
**Ação necessária**: 
- Consultar NVGT changelog
- Community forums/Discord
- GitHub issues para deprecated features

---

## 8. Estratégia de Testes e Paridade de Comportamento

### 8.1 Testes de Fumaça por Capacidade

#### **Teste 1: Áudio 3D Spatial**
```angelscript
// smoke_test_audio3d.nvgt
void test_audio_3d() {
    sound beacon = sound();
    beacon.load("beacon.wav");
    
    // Test: Jogador a 10m de distância
    beacon.play_3d(100, 0, 0); // x=100, y=0, z=0
    listener.set_position(0, 0, 0);
    
    // Expected: Som audível da direita, volume ~50%
    assert(beacon.playing);
    assert(beacon.volume > 0.3 && beacon.volume < 0.7);
}
```

#### **Teste 2: Network Event Processing**  
```angelscript
// smoke_test_network.nvgt
void test_network_events() {
    NetworkManager net = NetworkManager();
    net.connect("127.0.0.1", 8080);
    
    net.send("chat hello world");
    wait(100);
    
    NetworkEvent event = net.get_event();
    // Expected: Receive echo from test server
    assert(event.type == EVENT_RECEIVE);
    assert(event.message.find("hello world") != -1);
}
```

#### **Teste 3: Timer Precision**
```angelscript
// smoke_test_timers.nvgt  
void test_timer_precision() {
    timer t;
    wait(1000); // 1 second
    
    // Expected: 1000ms ±50ms tolerance
    int elapsed = t.elapsed;
    assert(elapsed >= 950 && elapsed <= 1050);
}
```

#### **Teste 4: File I/O and Encryption**
```angelscript
// smoke_test_fileio.nvgt
void test_encrypted_files() {
    string test_data = "sensitive_player_data";
    string key = "encryption_key_123";
    
    // Test encryption/decryption cycle
    string encrypted = crypto_encrypt(test_data, key);
    string decrypted = crypto_decrypt(encrypted, key);
    
    assert(decrypted == test_data);
    assert(encrypted != test_data);
}
```

#### **Teste 5: TTS Functionality**
```angelscript
// smoke_test_tts.nvgt
void test_text_to_speech() {
    // Test basic speech output
    bool spoken = screen_reader_speak("Hello World", true);
    assert(spoken == true);
    
    // Test speech interruption
    screen_reader_speak("First message", false);
    bool interrupted = screen_reader_speak("Second message", true);
    assert(interrupted == true);
}
```

### 8.2 Testes de Contrato Cliente↔Servidor

#### **Teste de Contrato 1: Login Sequence**
```angelscript
// contract_test_login.nvgt
void test_login_contract() {
    // GIVEN: Clean server state
    ServerInstance server = start_test_server();
    ClientInstance client = ClientInstance();
    
    // WHEN: Client sends login
    client.send("login testuser testpass 2.1");
    
    // THEN: Server responds with success
    string response = client.receive(5000); // 5s timeout
    assert(response.starts_with("login_ok"));
    
    // AND: Player appears in server player list
    assert(server.get_player_count() == 1);
    assert(server.get_player("testuser") != null);
}
```

#### **Teste de Contrato 2: Movement Broadcast**
```angelscript
// contract_test_movement.nvgt
void test_movement_broadcast() {
    // GIVEN: 2 clients connected
    ClientInstance client1 = connect_test_client("player1");
    ClientInstance client2 = connect_test_client("player2");
    
    // WHEN: Player1 moves
    client1.send("move 10 15");
    
    // THEN: Player2 receives movement notification
    string notification = client2.receive(1000);
    assert(notification == "player_moved player1 10 15");
    
    // AND: Player1 receives confirmation
    string confirmation = client1.receive(1000);
    assert(confirmation.find("move_ok") != -1);
}
```

#### **Teste de Contrato 3: Chat Message Routing**
```angelscript
// contract_test_chat.nvgt  
void test_chat_routing() {
    // GIVEN: Multiple clients in same map
    ClientInstance[] clients = connect_multiple_clients(5);
    
    // WHEN: One client sends chat
    clients[0].send("chat Hello everyone!");
    
    // THEN: All other clients receive the message
    for(int i = 1; i < 5; i++) {
        string message = clients[i].receive(1000);
        assert(message.find("Hello everyone!") != -1);
        assert(message.find(clients[0].username) != -1);
    }
}
```

### 8.3 Oráculos de Paridade BGT vs NVGT

#### **Oracle 1: Audio Position Accuracy**
```bash
# Test script: audio_position_oracle.sh
#!/bin/bash

# Run both versions with same input
./bgt_client --test-mode --input="move_sequence.txt" --output="bgt_audio.log"
./nvgt_client --test-mode --input="move_sequence.txt" --output="nvgt_audio.log"

# Compare audio event timings
python3 compare_audio_logs.py bgt_audio.log nvgt_audio.log
# Expected: <5% difference in timing, same sequence of events
```

#### **Oracle 2: Network Message Ordering**  
```python
# compare_network_logs.py
def compare_message_ordering(bgt_log, nvgt_log):
    bgt_messages = parse_network_log(bgt_log)
    nvgt_messages = parse_network_log(nvgt_log)
    
    # Compare message sequence
    for i, (bgt_msg, nvgt_msg) in enumerate(zip(bgt_messages, nvgt_messages)):
        assert bgt_msg.type == nvgt_msg.type, f"Message {i} type mismatch"
        assert bgt_msg.timestamp_diff < 100, f"Message {i} timing diff >100ms"
```

#### **Oracle 3: Game State Consistency**
```angelscript
// state_consistency_oracle.nvgt
class GameStateCapture {
    dictionary player_positions;
    dictionary inventory_states;
    dictionary map_objects;
    
    void capture_state() {
        // Capture complete game state at specific moments
        // Compare BGT vs NVGT state snapshots
    }
    
    bool compare_with_reference(GameStateCapture reference) {
        // Verify state consistency between implementations
        return positions_match && inventories_match && objects_match;
    }
}
```

### 8.4 Métricas de Aceitação

#### **Performance Metrics**
- **Audio Latency**: <50ms para spatial audio response
- **Network Latency**: <100ms round-trip time para ações críticas
- **Memory Usage**: <1GB total application memory
- **CPU Usage**: <50% em hardware médio (i5, 8GB RAM)
- **Startup Time**: <10s da execução até login screen

#### **Stability Metrics**  
- **Uptime**: >99% server availability em 24h continuous operation
- **Error Rate**: <1% network packet loss em condições normais
- **Memory Leaks**: 0 detectados em 2h continuous play session
- **Crash Rate**: <1 crash por 10h de gameplay

#### **Functional Metrics**
- **Feature Parity**: 100% core features funcionando (movement, chat, combat, audio 3D)
- **Audio Quality**: Indistinguível do BGT original em blind tests
- **Network Compatibility**: 100% protocolo messages compatíveis
- **Data Migration**: 100% dados existentes (players, maps) migrados sem corrupção

---

## 9. Riscos, Mitigações e Plano de Rollback

### 9.1 Riscos Técnicos por Área

#### **🔴 ALTO RISCO - GameEngine.dll Dependency**
**Impacto**: Funcionalidades críticas podem ser perdidas
**Probabilidade**: 90% - DLL externa sem código-fonte
**Mitigação**:
- Começar pela Fase 11 (workarounds) mais cedo no timeline
- Implementar graceful degradation para cada função da DLL
- Considerar reverse engineering (se legal) ou substitute implementation
- Contactar desenvolvedores originais se disponível

**Ponto de controle**: Fase 11 - Avaliar viabilidade de workarounds
**Rollback**: Manter cliente BGT para funcionalidades que dependem da DLL

#### **🟡 MÉDIO RISCO - NVGT Audio 3D Performance**  
**Impacto**: Performance degradada, experiência prejudicada
**Probabilidade**: 40% - NVGT é novo, pode ter limitações de performance
**Mitigação**:
- Benchmark early na Fase 8 (Audio Básico)
- Implementar audio pooling e streaming optimizations  
- Fallback para áudio 2D se spatial performance for inadequada
- Considerar direct BASS integration se NVGT wrapper for limitado

**Ponto de controle**: Fase 9 - Performance test com 50+ concurrent sounds
**Rollback**: Hybrid approach - NVGT core + direct BASS para áudio

#### **🟡 MÉDIO RISCO - Network API Incompatibility**
**Impacto**: Refatoração massiva necessária  
**Probabilidade**: 50% - BGT network events vs NVGT TCP sockets
**Mitigação**:
- Implementar abstraction layer (NetworkManager) early
- Maintain BGT-compatible event interface internamente
- Gradual migration por modules em vez de big bang

**Ponto de controle**: Fase 2 - Networking proof of concept
**Rollback**: Manter servidor BGT se NVGT networking for insuficiente

#### **🟢 BAIXO RISCO - String/File Operations**  
**Impacto**: Bugs menores, easy fixes
**Probabilidade**: 20% - Core functionality similar entre BGT/NVGT  
**Mitigação**: Extensive unit testing, validation scripts

### 9.2 Pontos de Controle e Go/No-Go Decisions

#### **Checkpoint 1 - Fim da Fase 2 (Networking Servidor)**
**Critérios Go**:
- [ ] Cliente BGT conecta a servidor NVGT
- [ ] Performance acceptável (<100ms latency)
- [ ] Stability >2h continuous operation

**No-Go Action**: Avaliar hybrid architecture (BGT client + NVGT server components)

#### **Checkpoint 2 - Fim da Fase 5 (Servidor Completo)**  
**Critérios Go**:
- [ ] Full gameplay functioning com cliente BGT
- [ ] 10+ concurrent players stable  
- [ ] Data migration successful

**No-Go Action**: Focar só em servidor migration, manter cliente BGT

#### **Checkpoint 3 - Fim da Fase 9 (Cliente Áudio 3D)**
**Critérios Go**:
- [ ] Audio quality indistinguível do BGT
- [ ] Performance metrics met
- [ ] Player acceptance em beta tests

**No-Go Action**: Cliente híbrido (NVGT + direct BASS integration)

#### **Checkpoint 4 - Fim da Fase 11 (GameEngine Workarounds)**
**Critérios Go**:
- [ ] Core gameplay preservado sem GameEngine.dll
- [ ] Acceptable feature degradation level
- [ ] No critical crashes

**No-Go Action**: Manter cliente BGT para advanced features

### 9.3 Estratégias de Isolamento de Mudanças

#### **Branch Strategy**
```
main (BGT stable)
├── feature/nvgt-server (Fases 1-5)  
├── feature/nvgt-client (Fases 6-10)
├── feature/gameengine-adapter (Fase 11)
└── integration/nvgt-full (merge point)
```

#### **Feature Flags**  
```angelscript
// config.nvgt
const bool ENABLE_NVGT_AUDIO = true;
const bool ENABLE_NVGT_NETWORK = true;
const bool ENABLE_GAMEENGINE_ADAPTER = false;

// Runtime switching
if(ENABLE_NVGT_AUDIO) {
    audio_system = NVGTAudioSystem();
} else {
    audio_system = BGTAudioSystem(); // fallback
}
```

#### **Adapter Pattern para Rollback**
```angelscript
interface IAudioSystem {
    void play_3d(string file, float x, float y);
    void set_listener(float x, float y);
}

class BGTAudioAdapter : IAudioSystem {
    // Wraps existing BGT code
}

class NVGTAudioAdapter : IAudioSystem {  
    // New NVGT implementation
}

// Easy switching
IAudioSystem@ audio = enable_nvgt ? NVGTAudioAdapter() : BGTAudioAdapter();
```

### 9.4 Plano de Rollback Detalhado

#### **Rollback Level 1: Feature-specific (Baixo impacto)**
**Trigger**: Performance issue em uma funcionalidade específica
**Action**: 
- Disable feature flag
- Fallback para BGT implementation
- Continue development de outras áreas
**Recovery time**: <1 dia

#### **Rollback Level 2: Component-specific (Médio impacto)**  
**Trigger**: Major issue em servidor OU cliente
**Action**:
- Branch rollback para last stable version
- Manter progresso do componente não-afetado  
- Reavaliar architecture decision
**Recovery time**: 1-3 dias

#### **Rollback Level 3: Project-wide (Alto impacto)**
**Trigger**: NVGT inadequado para game requirements
**Action**:
- Full rollback para BGT  
- Preserve lessons learned e adapters desenvolvidos
- Consider alternative solutions (otras engines, BGT improvements)
**Recovery time**: 1 semana

#### **Rollback Safety Mechanisms**
```bash
# Automated backup before major changes
./backup-project.sh "pre-phase-N-migration"

# Database migration rollback scripts  
./rollback-db.sh "phase-N-checkpoint"

# Asset versioning
git tag "bgt-stable-baseline"
git tag "phase-N-checkpoint"
```

---

## 10. Próximas Ações Concretas

### **Ação 1: Setup Ambiente NVGT Development**
**Objetivo**: Estabelecer environment funcional para development
**Insumos**: 
- NVGT SDK/installer
- Documentação oficial
- Exemplos de código
**Saída esperada**: 
- NVGT compile e run funcionando
- Hello World executável  
- Basic project structure

**Executação**:
```bash
# Download NVGT
wget https://nvgt.gg/releases/latest/nvgt-windows.zip
unzip nvgt-windows.zip

# Test compilation
nvgt.exe --compile hello_world.angelscript
./hello_world.exe

# Verify output: "Hello World!"
```

### **Ação 2: Análise Profunda da API NVGT**
**Objetivo**: Catalogar exact APIs disponíveis em NVGT vs BGT requirements
**Insumos**:
- NVGT documentation complete scan
- NVGT source code analysis (se disponível)  
- Community forums/Discord research
**Saída esperada**:
- API mapping spreadsheet completo
- Feature gap analysis detalhado
- Priority areas for POC development

**Executação**:
```bash
# Download and analyze all documentation
wget -r --no-parent https://nvgt.gg/docs/
grep -r "class\|function\|method" nvgt-docs/ > nvgt_api_catalog.txt

# Create comparison matrix
python3 create_api_matrix.py bgt_usage_analysis.csv nvgt_api_catalog.txt
```

### **Ação 3: Implementar NetworkManager POC**
**Objetivo**: Provar que NVGT TCP sockets podem substituir BGT network class
**Insumos**:
- BGT network.bgt analysis
- NVGT socket documentation
- Protocol message samples
**Saída esperada**:
- NetworkManager class funcional
- Basic client-server communication
- Event-driven message processing

**Executação**:
```angelscript  
// networkmanager_poc.nvgt
class NetworkManager {
    tcp_socket socket;
    string[] message_queue;
    bool connected = false;
    
    bool connect(string host, int port) {
        return socket.connect(host, port);
    }
    
    void send(string message) {
        socket.write(message + "\n");
    }
    
    string receive() {
        return socket.read_line();
    }
}

// Test with simple echo server
void test_networking() {
    NetworkManager net;
    if(net.connect("127.0.0.1", 8080)) {
        net.send("hello server");
        string response = net.receive();
        assert(response == "hello server");
        print("POC SUCCESS: Basic networking works");
    }
}
```

### **Ação 4: Audio 3D Performance Benchmark**
**Objetivo**: Validar que NVGT audio performance atende requirements do jogo  
**Insumos**:
- NVGT sound class documentation
- BGT audio performance baseline  
- Test audio files (beacon.wav, step.wav, etc.)
**Saída esperada**:
- Benchmark results comparison
- Maximum concurrent sounds supported
- Latency measurements
- Memory usage analysis

**Executação**:
```angelscript
// audio_benchmark.nvgt
void benchmark_audio_3d() {
    timer t;
    sound[] beacon_pool(100); // Test 100 concurrent sounds
    
    // Load sounds
    t.restart();
    for(int i = 0; i < 100; i++) {
        beacon_pool[i].load("beacon.wav");
    }
    int load_time = t.elapsed;
    
    // Play all simultaneously at different positions
    t.restart();
    for(int i = 0; i < 100; i++) {
        beacon_pool[i].play_3d(i * 10, 0, 0); // Spread across X axis
    }
    int play_time = t.elapsed;
    
    // Report results
    print("Load 100 sounds: " + load_time + "ms");
    print("Play 100 sounds 3D: " + play_time + "ms");
    print("Memory usage: " + get_memory_usage() + "MB");
    
    // Performance criteria
    assert(load_time < 5000); // <5s load time
    assert(play_time < 100);   // <100ms play time
}
```

### **Ação 5: Database Migration Script**
**Objetivo**: Garantir que dados existentes (players, maps, items) podem ser migrados
**Insumos**:
- Current .db, .usr, .map files
- BGT db class implementation
- NVGT file I/O capabilities
**Saída esperada**:
- Migration scripts funcionais  
- Data integrity validation
- Rollback capability

**Executação**:
```bash
#!/bin/bash
# migrate_data.sh

echo "=== BGT to NVGT Data Migration ==="

# Backup original data  
cp -r servidor/*.db servidor/*.usr backup/
cp -r servidor/maps/ backup/

# Convert databases
python3 convert_databases.py servidor/items.db servidor/nvgt_items.db
python3 convert_databases.py servidor/weapons.db servidor/nvgt_weapons.db

# Validate migration
./nvgt_server --validate-data --config=test_config.nvgt
if [ $? -eq 0 ]; then
    echo "✓ Data migration successful"
else
    echo "✗ Data migration failed - restoring backup"
    cp -r backup/* servidor/
fi
```

### **Ação 6: Protocol Compatibility Validator**
**Objetivo**: Assegurar que mensagens de rede mantêm compatibilidade durante transição
**Insumos**:
- BGT network protocol documentation (servidor/includes/net.bgt)
- Message samples from logs
- NVGT NetworkManager implementation
**Saída esperada**:
- Protocol validation suite
- Message format compatibility tests
- Backward compatibility assurance

**Executação**:
```python
# protocol_validator.py
import json
import socket

class ProtocolValidator:
    def __init__(self):
        self.bgt_messages = self.load_bgt_samples()
        self.nvgt_server = self.connect_nvgt_server()
    
    def validate_login_sequence(self):
        # Send BGT-format login to NVGT server
        login_msg = "login testuser testpass 2.1"
        response = self.send_and_receive(login_msg)
        
        # Verify response format matches BGT expectations
        assert response.startswith("login_ok"), f"Unexpected response: {response}"
        
    def validate_chat_routing(self):
        # Test chat message format compatibility
        chat_msg = "chat Hello World"  
        self.send_and_receive(chat_msg)
        # Expect: "chat_message testuser Hello World"
        
    def validate_movement_sync(self):
        # Test movement protocol
        move_msg = "move 10 15"
        self.send_and_receive(move_msg)
        # Expect: "move_ok" + broadcast to other clients
        
if __name__ == "__main__":
    validator = ProtocolValidator()
    validator.run_all_tests()
    print("✓ Protocol compatibility validated")
```

### **Ação 7: GameEngine.dll Analysis e Replacement Strategy**  
**Objetivo**: Definir como substituir ou contornar a dependência da GameEngine.dll
**Insumos**:
- GameEngine.bgt function usage analysis
- DLL exported functions list (via dependency walker)
- Alternative implementation research
**Saída esperada**:
- Function-by-function replacement plan
- Adapter interface design
- Graceful degradation strategy

**Executação**:
```bash
# analyze_gameengine.sh
echo "=== GameEngine.dll Dependency Analysis ==="

# Extract function usage from BGT code
grep -r "engine\." cliente/ > gameengine_usage.txt

# Analyze DLL exports (if available)
dumpbin /exports GameEngine.dll > gameengine_exports.txt

# Create replacement matrix
python3 analyze_gameengine_deps.py gameengine_usage.txt gameengine_exports.txt
```

```angelscript
// gameengine_adapter.nvgt - Proof of concept
interface IGameEngine {
    bool spawn_platform2D(int x, int y, string type);
    void start_recording_audio();
    bool import_map(string filename);
}

class GameEngineAdapter : IGameEngine {
    bool spawn_platform2D(int x, int y, string type) {
        // NVGT alternative implementation or graceful degradation
        print("Platform spawn disabled - GameEngine.dll unavailable");
        return false; // Graceful failure
    }
    
    void start_recording_audio() {
        // Research NVGT audio recording capabilities
        print("Audio recording not available in NVGT version");
    }
    
    bool import_map(string filename) {
        // Implement using NVGT file operations
        file f;
        if(f.open(filename, "r")) {
            // Custom map parser implementation
            return parse_map_file(f);
        }
        return false;
    }
}
```

---

## Arquivos para Modificar - Lista Ordenada por Prioridade

### **FASE 1-2: SERVIDOR (Crítico - Começar aqui)**

#### Servidor - Ordem de modificação:
1. **`servidor/includes/db.bgt`** (COMUM) - Sistema de banco de dados customizado
2. **`config-test.bgt`** (COMUM) - Configurações globais
3. **`servidor/includes/net.bgt`** (SERVIDOR) - ⭐ Sistema de rede servidor  
4. **`servidor/server.bgt`** (SERVIDOR) - Main server entry point
5. **`servidor/includes/login.bgt`** (SERVIDOR) - Sistema de autenticação
6. **`servidor/includes/player.bgt`** (SERVIDOR) - Gerenciamento de estado dos jogadores
7. **`servidor/includes/map.bgt`** (SERVIDOR) - Sistema de mapas servidor
8. **`servidor/includes/weapons.bgt`** (SERVIDOR) - Sistema de combate
9. **`servidor/includes/item.bgt`** (SERVIDOR) - Sistema de itens

### **FASE 3: CLIENTE (Após servidor estável)**

#### Cliente - Ordem de modificação:
10. **`cliente/Projeto Ig.bgt`** (CLIENTE) - Main client entry point
11. **`cliente/includes/net.bgt`** (CLIENTE) - ⭐ Sistema de rede cliente
12. **`cliente/includes/player.bgt`** (CLIENTE) - Gerenciamento de jogador local
13. **`cliente/includes/bass.bgt`** (CLIENTE) - Sistema de áudio básico → **substituir por NVGT sound**
14. **`cliente/includes/src.bgt`** (CLIENTE) - ⭐ Sistema de áudio 3D espacial  
15. **`cliente/includes/src2.bgt`** (CLIENTE) - Sistema de áudio 3D estendido
16. **`cliente/includes/map.bgt`** (CLIENTE) - Renderização de mapas cliente
17. **`cliente/includes/menu.bgt`** (CLIENTE) - Sistema de interface/menus
18. **`cliente/includes/commands.bgt`** (CLIENTE) - Processamento de comandos
19. **`cliente/includes/voices.bgt`** (CLIENTE) - Sistema TTS/vozes

### **FASE 4: DEPENDÊNCIAS CRÍTICAS (Alto risco)**

#### Dependências problemáticas:
20. **`cliente/includes/GameEngine.bgt`** (CLIENTE) - ⚠️ **DLL externa** - Criar adapters
21. **`cliente/includes/basscontroller.bgt`** (CLIENTE) - Controller para BASS → **migrar para NVGT**

### **FASE 5: MÓDULOS AUXILIARES**

#### Módulos de suporte (podem ser migrados em paralelo):
22. **`cliente/includes/inv.bgt`** (CLIENTE) - Sistema de inventário
23. **`cliente/includes/weapon.bgt`** (CLIENTE) - Sistema de armas cliente
24. **`cliente/includes/dialogs.bgt`** (CLIENTE) - Sistema de diálogos  
25. **`cliente/includes/tiendas.bgt`** (CLIENTE) - Sistema de lojas
26. **`cliente/includes/vehicles.bgt`** (COMUM) - Sistema de veículos
27. **`servidor/includes/marriages.bgt`** (SERVIDOR) - Sistema de casamentos
28. **`servidor/includes/arena.bgt`** (SERVIDOR) - Sistema de arena/combate

### **Resumo da Ordem de Migração:**

**🎯 Começar pelo SERVIDOR** porque:
- Menos dependências externas (sem GameEngine.dll, sem BASS)
- Pode ser testado com cliente BGT existente  
- Desbloqueio crítico para testar networking NVGT
- Menor complexidade de áudio (foco na lógica de negócio)

**Sequência recomendada:**
1. **Servidor completo** (arquivos 1-9) - 4-6 semanas
2. **Cliente básico** (arquivos 10-12) - 2-3 semanas  
3. **Cliente áudio** (arquivos 13-16) - 3-4 semanas
4. **Cliente interface** (arquivos 17-19) - 2-3 semanas
5. **Dependências críticas** (arquivos 20-21) - 2-4 semanas
6. **Módulos auxiliares** (arquivos 22-28) - 3-4 semanas

**Total estimado: 16-24 semanas (4-6 meses)**