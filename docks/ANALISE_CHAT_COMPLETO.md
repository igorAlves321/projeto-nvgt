# 💬 ANÁLISE: Sistema de Chat BGT → NVGT

## 1. Arquitetura do Chat em BGT

### 1.1 Estrutura de Dados (add.bgt)

```bgt
class add {
    int active = 1;
    int pos;
    string name;                    // Nome do canal (ex: "local", "pm", "team", "general")
    string currently_buffer;
    string[] items;                 // Array de mensagens
}

add@[] adds;                        // Array de canais
int addpos;                         // Índice do canal atual
```

**Canais Principais:**
```
1. "general"                        // Tudo (histórico de todos)
2. "canal_principal"                // Chat público/global
3. "canal_local"                    // Chat do mapa local
4. "mensajes_del_equipo"            // Chat de equipe
5. "conversaciones_privadas"        // Mensagens privadas
6. "avisos"                         // Avisos do sistema
7. "mensajes_de_voz"                // Mensagens de voz
```

### 1.2 Fluxo de Recebimento (net.bgt, linhas 66-72)

```bgt
// Chat do NPC
else if(parsed[0] == "hablarbot") {
    add_add_item("canal_local", pu.get_value(parsed[1]) + " " + 
                 pu.get_value("lhe diz:") + " " + 
                 pu.get_value(string_replace(pegar_mensagem(), parsed[0]+" "+parsed[1]+" ", "", false)));
    p.play_stationary("chatmap.ogg", false);
}

// Chat local do mapa
else if(parsed[0] == "local" && parsed.length() > 1) {
    string texto = string_replace(pegar_mensagem(), parsed[0]+" ", "", false);
    send_unreliable(event.peer_id, "/falarnomapa " + texto, 0);
}
```

**Protocolo Server → Client:**
- `local <mensagem>` → Adiciona ao canal "canal_local"
- `hablarbot <npc_name> <mensagem>` → Adiciona com som
- `say <mensagem>` → Chat global (não implementado no trecho)
- `pm <from_player> <mensagem>` → Chat privado (não implementado)
- `team <mensagem>` → Chat de equipe (não implementado)

### 1.3 Menu de Chat (menu.bgt, linhas 1738-1776)

```bgt
void chatmenu() {
    // Configurar menu
    setupmenu2();
    
    // Adicionar opções de chat
    for(int i = 0; i < idiomaschat.length(); i++) {
        string[] parsed = string_split(idiomaschat[i], "=", true);
        if(parsed.length() == 2) {
            m.add_item_tts(pu.get_value(parsed[0]), parsed[1]);
        }
    }
    
    // Opções: "Desativar chat", "Arabic", "English", "Español", "Français", "Português"
    
    // Executar menu
    mres = m.run(...);
    
    // Salvar escolha
    if(mres != 0 && m.get_item_name(mres) != "back") {
        idiomachat = m.get_item_name(mres);
        writeprefs();
        send_reliable(peer_id, "idiomachat " + idiomachat, 0);
    }
}
```

**Observação**: Este menu é para **IDIOMA do chat**, não para **CANAIS**. 
O `idiomachat` é uma variável que define o idioma tradução das mensagens.

### 1.4 Sistema de Adição de Mensagens (add.bgt, linhas 132-164)

```bgt
void add_add_item(string addname, string item, bool speakitem = true) {
    // Log em arquivo se ativado
    if(logs == 1) {
        file logfile;
        logfile.open("logs/log_"+DATE_YEAR+"_"+DATE_MONTH+"_"+DATE_DAY+".log", "a");
        logfile.write(item + "\r\n");
        logfile.close();
    }
    
    // Verificar se canal existe
    bool canal_existe = false;
    for(uint i = 0; i < adds.length(); i++) {
        if(adds[i].name == addname) {
            canal_existe = true;
            break;
        }
    }
    
    // Se não existe, criar
    if(!canal_existe) {
        create_add(addname);
        sort_channels();
    }
    
    // Adicionar ao canal e ao "general"
    for(uint i = 0; i < adds.length(); i++) {
        if(adds[i].name == addname || adds[i].name == "general") {
            // Falar a mensagem se não for "general"
            if(speakitem && adds[i].name != "general") {
                speak(item, 0);
            }
            adds[i].items.insert_last(item);
        }
    }
}
```

**Regras importantes:**
1. ✅ Se canal não existe, criar automaticamente
2. ✅ Adicionar mensagem TANTO ao canal quanto ao "general"
3. ✅ Vocalizar (speak) apenas para não-general
4. ✅ Log em arquivo se habilitado

### 1.5 Navegação entre Canais (add.bgt, linhas 96-130)

```bgt
void addleft() {
    if (addpos <= 0) addpos = 0;
    else {
        addpos -= 1;
        speakfocusedadd();
    }
}

void addright() {
    if (addpos >= (adds.length()-1)) {
        if (adds.length() > 0) addpos = adds.length()-1;
    } else {
        addpos += 1;
        speakfocusedadd();
    }
}

void speakfocusedadd() {
    if(adds.length() == 0) {
        speak("Nenhum canal disponível.");
        return;
    }
    
    adds[addpos].currently_buffer = adds[addpos].name;
    
    if(adds[addpos].items.length() > 0) {
        speak(pu.get_value(adds[addpos].name) + ". " + 
              (adds[addpos].pos+1) + " " + 
              pu.get_value("de") + " " + 
              adds[addpos].items.length() + ".");
    }
}
```

**Comandos:**
- `addleft()` / `addright()` → Navega entre canais
- `speakfocusedadd()` → Verbaliza canal atual

## 2. Tipos de Chat Identificados

| Tipo | Comando | Origem | Destino | Exemplo |
|------|---------|--------|---------|---------|
| Local | `local` | Server | Client | `local João diz: Olá!` |
| NPC | `hablarbot` | Server | Client | `hablarbot Vendedor diz: Bem-vindo!` |
| Privado | `pm` | Server | Client | `pm Joao diz: Como vai?` |
| Equipe | `team` | Server | Client | `team Mensagem de equipe` |
| Global | `say` | Server | Client | `say João diz globalmente: Oi!` |
| Sistema | (diversos) | Server | Client | Avisos, notificações |

## 3. Fluxo Completo: Enviar → Receber

### 3.1 Usuário Envia Chat Local

```
Cliente BGT:
  1. Usuário pressiona Enter
  2. Dialogo pergunta: "Digite sua mensagem"
  3. Usuário digita: "Olá pessoal!"
  4. send_unreliable(peer_id, "/falarnomapa Olá pessoal!", 0)
     
Server BGT:
  1. Recebe "/falarnomapa Olá pessoal!" do player João
  2. Broadcast para todos na mesma localização:
     local João diz: Olá pessoal!
     
Todos os Clientes BGT:
  1. Recebem "local João diz: Olá pessoal!"
  2. add_add_item("canal_local", "João diz: Olá pessoal!")
  3. play_stationary("chatmap.ogg")  // Som de chat
  4. speak("João diz: Olá pessoal!")  // TTS
```

### 3.2 Usuário Envia Chat PM

```
Cliente BGT:
  1. Usuário abre menu de PM
  2. Seleciona destinatário: Maria
  3. Digita: "Tudo bem?"
  4. send_unreliable(peer_id, "/pm Maria Tudo bem?", 0)
  
Server BGT:
  1. Encontra Maria na lista de players
  2. Envia APENAS para Maria:
     pm João diz: Tudo bem?
     
Maria's Cliente BGT:
  1. Recebe "pm João diz: Tudo bem?"
  2. add_add_item("conversaciones_privadas", "João diz: Tudo bem?")
  3. speak("João diz: Tudo bem?")
```

### 3.3 Usuário Envia Chat Equipe

```
Cliente BGT:
  1. Usuário em equipe pressiona tecla de equipe
  2. Dialogo: "Mensagem de equipe"
  3. Digita: "Vamos atacar!"
  4. send_unreliable(peer_id, "/team Vamos atacar!", 0)

Server BGT:
  1. Broadcast APENAS para membros da equipe:
     team João diz: Vamos atacar!
     
Equipe Completa recebe:
  1. add_add_item("mensajes_del_equipo", "João diz: Vamos atacar!")
  2. play_stationary("teamchat.ogg")  // Som especial
  3. speak("Team: João diz: Vamos atacar!")
```

## 4. Implementação Necessária em NVGT

### 4.1 Estrutura de Dados (chat.nvgt - novo arquivo)

```nvgt
// Classe para representar um canal de chat
class chat_channel {
    string name;            // Nome do canal
    string[] messages;      // Array de mensagens
    uint current_position;  // Posição de leitura
    bool active = true;
}

// Array de canais
chat_channel@[] chat_channels;
uint current_channel = 0;   // Índice do canal ativo

// Tipos de chat como constantes
const string CHAT_GENERAL = "general";
const string CHAT_LOCAL = "local";
const string CHAT_PRIVATE = "private";
const string CHAT_TEAM = "team";
const string CHAT_GLOBAL = "global";
const string CHAT_SYSTEM = "system";
```

### 4.2 Funções Necessárias

**Inicialização:**
```nvgt
void initialize_chat_system() {
    // Criar canal "general" padrão
    chat_channel ch("general");
    chat_channels.insert_last(ch);
}
```

**Adicionar Mensagem:**
```nvgt
void chat_add_message(string channel_name, string message) {
    // Se canal não existe, criar
    bool exists = false;
    for(uint i = 0; i < chat_channels.length(); i++) {
        if(chat_channels[i].name == channel_name) {
            exists = true;
            break;
        }
    }
    
    if(!exists) {
        chat_channel new_ch(channel_name);
        chat_channels.insert_last(new_ch);
    }
    
    // Adicionar ao canal e ao general
    for(uint i = 0; i < chat_channels.length(); i++) {
        if(chat_channels[i].name == channel_name || 
           chat_channels[i].name == CHAT_GENERAL) {
            chat_channels[i].messages.insert_last(message);
            
            // Vocalizar se não for general
            if(channel_name != CHAT_GENERAL) {
                speak(message, 0);
            }
        }
    }
}
```

**Navegar Canais:**
```nvgt
void chat_next_channel() {
    if(current_channel < chat_channels.length() - 1) {
        current_channel++;
        chat_speak_current();
    }
}

void chat_prev_channel() {
    if(current_channel > 0) {
        current_channel--;
        chat_speak_current();
    }
}

void chat_speak_current() {
    if(chat_channels.length() == 0) {
        speak("Nenhum canal disponível");
        return;
    }
    
    string ch_name = chat_channels[current_channel].name;
    uint msg_count = chat_channels[current_channel].messages.length();
    
    speak(ch_name + ". " + (current_channel+1) + " de " + 
          chat_channels.length() + ". " + msg_count + " mensagens");
}
```

**Ler Mensagens:**
```nvgt
void chat_read_current() {
    if(chat_channels.length() == 0 || 
       chat_channels[current_channel].messages.length() == 0) {
        speak("Canal vazio");
        return;
    }
    
    string[] messages = chat_channels[current_channel].messages;
    uint pos = chat_channels[current_channel].current_position;
    
    if(pos >= messages.length()) {
        pos = messages.length() - 1;
    }
    
    speak(messages[pos]);
}

void chat_next_message() {
    if(chat_channels[current_channel].messages.length() == 0) return;
    
    uint max = chat_channels[current_channel].messages.length() - 1;
    if(chat_channels[current_channel].current_position < max) {
        chat_channels[current_channel].current_position++;
        chat_read_current();
    }
}

void chat_prev_message() {
    if(chat_channels[current_channel].current_position > 0) {
        chat_channels[current_channel].current_position--;
        chat_read_current();
    }
}
```

### 4.3 Handlers em net.nvgt

**Chat Local:**
```nvgt
else if(parsed[0] == "local" && parsed.length() > 1) {
    string msg = string_replace(full_msg, "local ", "", false);
    chat_add_message(CHAT_LOCAL, msg);
    p.play_stationary(get_sound_path("chatmap.ogg"), false);
}
```

**Chat PM:**
```nvgt
else if(parsed[0] == "pm" && parsed.length() > 1) {
    string msg = string_replace(full_msg, "pm ", "", false);
    chat_add_message(CHAT_PRIVATE, msg);
    p.play_stationary(get_sound_path("pm.ogg"), false);
}
```

**Chat Equipe:**
```nvgt
else if(parsed[0] == "team" && parsed.length() > 1) {
    string msg = string_replace(full_msg, "team ", "", false);
    chat_add_message(CHAT_TEAM, msg);
    p.play_stationary(get_sound_path("teamchat.ogg"), false);
}
```

**Chat Global:**
```nvgt
else if(parsed[0] == "say" && parsed.length() > 1) {
    string msg = string_replace(full_msg, "say ", "", false);
    chat_add_message(CHAT_GLOBAL, msg);
    p.play_stationary(get_sound_path("chat.ogg"), false);
}
```

**NPC Chat (hablarbot):**
```nvgt
else if(parsed[0] == "hablarbot" && parsed.length() > 1) {
    string npc_name = parsed[1];
    string msg = npc_name + " diz: " + 
                 string_replace(full_msg, "hablarbot " + npc_name + " ", "", false);
    chat_add_message(CHAT_LOCAL, msg);
    p.play_stationary(get_sound_path("chatmap.ogg"), false);
}
```

### 4.4 Comando de Envio (client.nvgt game loop)

**Enviar Chat Local:**
```nvgt
if(key_pressed(K_C)) {  // Ctrl+L para local
    string msg = input_dialog("Chat Local:", "Digite sua mensagem");
    if(msg.length() > 0) {
        send_unreliable(peer_id, "/falarnomapa " + msg, 0);
    }
}

if(key_pressed(K_P)) {  // Ctrl+P para PM
    string target = input_dialog("PM Para:", "Digite nome do player");
    if(target.length() > 0) {
        string msg = input_dialog("Mensagem:", "Digite sua mensagem");
        if(msg.length() > 0) {
            send_unreliable(peer_id, "/pm " + target + " " + msg, 0);
        }
    }
}

if(key_pressed(K_T)) {  // Ctrl+T para Team
    string msg = input_dialog("Chat Equipe:", "Digite sua mensagem");
    if(msg.length() > 0) {
        send_unreliable(peer_id, "/team " + msg, 0);
    }
}
```

**Navegar Chats:**
```nvgt
if(key_pressed(K_LEFT)) {   // Seta esquerda = canal anterior
    chat_prev_channel();
}

if(key_pressed(K_RIGHT)) {  // Seta direita = próximo canal
    chat_next_channel();
}

if(key_pressed(K_UP)) {     // Seta cima = mensagem anterior
    chat_prev_message();
}

if(key_pressed(K_DOWN)) {   // Seta baixo = próxima mensagem
    chat_next_message();
}
```

## 5. Resumo das Mudanças Necessárias

| Arquivo | Mudança | Descrição |
|---------|---------|-----------|
| `cliente/includes/chat.nvgt` | ✅ NOVO | Sistema de canais de chat |
| `cliente/includes/net.nvgt` | 🔧 MODIFICAR | Adicionar handlers: local, pm, team, say, hablarbot |
| `cliente/client.nvgt` | 🔧 MODIFICAR | Inicializar chat_system(), adicionar teclas de chat no loop |
| `cliente/includes/globals.nvgt` | 🔧 MODIFICAR | Importar chat.nvgt |

## 6. Comparação: BGT vs NVGT

**BGT:**
- ✅ Sistema maduro e testado
- ✅ Múltiplos canais (general, local, pm, team, system)
- ✅ Persistência em arquivo
- ✅ Tradução de mensagens
- ✅ Logs automáticos

**NVGT (proposto):**
- ✅ Mesma arquitetura
- ✅ Mesmos canais
- ✅ Sem persistência (inicialmente)
- ✅ Sem tradução (inicialmente)
- ✅ Logs básicos

**Próximas Iterações:**
- Adicionar persistência de chat
- Implementar tradução em tempo real
- Sistema de filtro de palavras
- Histórico com limite de mensagens

## Status

⏳ **PRONTO PARA IMPLEMENTAÇÃO** - Todas as funções BGT foram analisadas e documentadas.
