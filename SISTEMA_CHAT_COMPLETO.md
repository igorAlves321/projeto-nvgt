# Sistema de Chat - Projeto IG (BGT → NVGT)

## 📋 Resumo do Sistema de Chat

### 1. Arquitetura Geral

O sistema de chat usa um modelo **Cliente ↔ Servidor**:
- **Cliente**: Envia comandos de texto via `/falarnomapa`, `/pm`, `/e`, `adm`, etc.
- **Servidor**: Processa e roteia mensagens para os destinatários corretos
- **Cliente**: Recebe e exibe em buffers organizados por canal

---

## 2. Tipos de Mensagens (Servidor → Cliente)

### 2.1 `msg <canal> <texto|separado|por|pipes>`
**Uso**: Mensagem em canal específico com tradução automática
- Cada parte entre `|` é traduzida separadamente
- Exemplo: `msg canal_local |alguém diz:| Olá!`

### 2.2 `msg2 <texto;separado;por;ponto_e_virgula>`
**Uso**: Avisos do sistema
- Cada parte entre `;` é traduzida separadamente
- Canal: `avisos`
- Exemplo: `msg2 Você está;no nível;5`

### 2.3 `msg3 <texto;separado;por;ponto_e_virgula>`
**Uso**: Mensagens de equipe (party/team)
- Canal: `mensajes_del_equipo`
- Exemplo: `msg3 João ;disse:; Vamos atacar!`

### 2.4 `msg4 <texto;separado;por;ponto_e_virgula>`
**Uso**: Chat administrativo (visões angelicais)
- Canal: `visiones_angelicales`
- Apenas admins/moderadores recebem
- Exemplo: `msg4 Admin ;diz:; Servidor reiniciará em 5 min`

### 2.5 `pm de/para <nome>: <mensagem>`
**Uso**: Mensagens privadas
- Canal: `conversaciones_privadas`
- Formato: `pm de João: Olá` ou `pm para Maria: Oi`

### 2.6 `fm |titulo| nome |ação| mensagem`
**Uso**: Fala local (mapa) com formatação
- Canal: `canal_local`
- Exemplo: `fm |Guerreiro| João |diz:| Olá pessoal`

### 2.7 `msgconexoes <texto>`
**Uso**: Notificações de conexão/desconexão
- Canal: `notificaciones_de_conexiones`

---

## 3. Comandos de Chat (Cliente → Servidor)

### 3.1 Chat Local: `/falarnomapa <mensagem>`
- Envia para jogadores próximos (15 tiles de distância em X)
- Verifica silêncio, AFK, spam
- Suporte a `/me` para ações

### 3.2 Chat Equipe: `/e <mensagem>` ou `/t <mensagem>`
- Envia para todos da equipe (`nomesequipe[]`)
- Verifica se tem equipe ativa

### 3.3 Chat Admin: `adm <mensagem>`
- Envia para admins, moderadores e quem tem `enable_chat_adm.usr`
- Jogadores com título "CHATTER" recebem prefixo [LOGO_CHATTER]

### 3.4 Mensagem Privada: `/pm <nome> <mensagem>`
- Envia direto para jogador específico
- Se offline, salva em `players/<nome>/pm.md`

### 3.5 Responder PM: `/reply <mensagem>` ou `/r <mensagem>`
- Responde para último PM recebido

---

## 4. Canais do Cliente (Buffers)

Os buffers são gerenciados pela classe `add` em `add.nvgt`:

**Sistema simplificado - canais só aparecem quando têm mensagens:**

| Canal | Nome | Descrição |
|-------|------|-----------|
| `tudo` | Tudo | Sempre existe - recebe cópia de todas as mensagens |
| `global` | Global | Chat global |
| `local` | Local | Fala no mapa (chat local) |
| `equipe` | Equipe | Chat de equipe/party |
| `privado` | Privado | Mensagens privadas (PM) |
| `admin` | Admin | Chat administrativo (só para admins) |
| `leilão` | Leilão | Chat de leilão |

**Comportamento:**
- Canal só aparece na navegação se tiver pelo menos 1 mensagem
- Exceção: `tudo` sempre aparece (recebe saudação ao entrar)
- Formato de anúncio: "chat global. 444 de 615" (posição atual de total)

---

## 5. Status de Implementação NVGT

### ✅ Implementado no Servidor (`server.nvgt`)
- [x] `msg2` - Avisos (sistema)
- [x] `msg4` - Chat admin com prefixo [LOGO_CHATTER]
- [x] `idiomachat` - Configuração de idioma
- [x] `/falarnomapa` - Chat local
- [x] `/e` e `/t` - Chat de equipe
- [x] `/pm` - Mensagem privada
- [x] `/reply` e `/r` - Responder PM

### ✅ Implementado no Servidor (`chat_advanced.nvgt`)
- [x] Anti-spam (5 msg/10s, 3 avisos = mute)
- [x] Filtro de palavras
- [x] Mute manual por admin
- [x] Preferências de canal
- [x] `send_global_message()`
- [x] `send_local_message()`
- [x] `send_trade_message()`
- [x] `telllocal()` - Chat local completo
- [x] `tellteam()` - Chat de equipe
- [x] `send_pm()` - Mensagem privada
- [x] `reply_pm()` - Responder PM

### ✅ Implementado no Cliente (`net.nvgt`)
- [x] `process_msg()` - Canal específico
- [x] `process_msg2()` - Avisos
- [x] `process_msg3()` - Equipe
- [x] `process_msg4()` - Admin com [LOGO_CHATTER]
- [x] `process_msg_translated()` - Genérico
- [x] `process_fm()` - Chat local (fala mapa)
- [x] `process_pm()` - Mensagem privada
- [x] `process_msgconexoes()` - Conexões

### ✅ Implementado no Cliente (`add.nvgt` e `client.nvgt`)
- [x] Sistema de buffers
- [x] `add_add_item()` - Adicionar mensagem
- [x] Navegação (up/down/left/right)
- [x] Todos os canais BGT criados:
  - `tudo`, `canal_principal`, `canal_local`
  - `mensajes_del_equipo`, `conversaciones_privadas`
  - `visiones_angelicales`, `avisos`
  - `notificaciones_de_conexiones`, `avisos_de_morte`
  - `mensagens_de_voz`

---

## 6. O que Falta Implementar

### 6.1 Servidor - Comandos de Chat
```nvgt
// Em server.nvgt ou net_handlers.nvgt
- /falarnomapa → telllocal()
- /e ou /t → chat equipe
- /pm → mensagem privada
- /reply ou /r → responder PM
```

### 6.2 Servidor - Funções Auxiliares
```nvgt
// telllocal() - Chat local
void telllocal(int index, string message) {
    // Enviar para jogadores em range 15 no mesmo mapa
    // Formato: fm |titulo| nome |diz:| mensagem
}
```

### 6.3 Cliente - Criação de Canais
```nvgt
// Criar todos os canais na inicialização
create_add("tudo");
create_add("canal_principal");
create_add("canal_local");
create_add("mensajes_del_equipo");
create_add("conversaciones_privadas");
create_add("visiones_angelicales");
create_add("avisos");
create_add("notificaciones_de_conexiones");
create_add("avisos_de_morte");
create_add("mensagens_de_voz");
```

### 6.4 Cliente - Handler `fm` (Fala Mapa)
```nvgt
// process_fm() - Fala local formatada
// Formato: fm |titulo| nome |ação| mensagem
```

### 6.5 Cliente - Handler `pm`
```nvgt
// process_pm() - Mensagem privada
// Formato: pm de/para nome: mensagem
```

---

## 7. Fluxo de Mensagem Completo

### Exemplo: Chat Local
```
[CLIENTE] Jogador digita: /falarnomapa Olá pessoal!
    ↓
[SERVIDOR] Recebe comando, chama telllocal(index, "Olá pessoal!")
    ↓
[SERVIDOR] Loop: para cada jogador em range 15:
    send_reliable(peer_id, "fm |título| nome |diz:| Olá pessoal!", 0)
    ↓
[CLIENTE] process_packets() recebe "fm |título| nome |diz:| Olá pessoal!"
    ↓
[CLIENTE] process_fm() adiciona ao canal "canal_local"
    ↓
[CLIENTE] speak() fala a mensagem
```

### Exemplo: Chat Equipe
```
[CLIENTE] Jogador digita: /e Vamos atacar!
    ↓
[SERVIDOR] Loop: para cada membro da equipe:
    send_reliable(peer_id, "msg3 nome ;disse:; Vamos atacar!", 0)
    ↓
[CLIENTE] process_msg3() adiciona ao canal "mensajes_del_equipo"
```

### Exemplo: Chat Admin
```
[CLIENTE] Jogador digita: adm Atenção todos!
    ↓
[SERVIDOR] Verifica se jogador é CHATTER → adiciona [LOGO_CHATTER]
    ↓
[SERVIDOR] Loop: para cada admin/mod:
    send_reliable(peer_id, "msg4 [LOGO_CHATTER] nome; ;diz:; Atenção todos!", 0)
    ↓
[CLIENTE] process_msg4() detecta [LOGO_CHATTER], toca som especial
    ↓
[CLIENTE] Adiciona "Chatter: nome diz: Atenção todos!" ao canal "visiones_angelicales"
```

---

## 8. Arquivos Relevantes

### Servidor
- `server/server.nvgt` - Handler principal
- `server/includes/chat_advanced.nvgt` - Sistema de chat avançado
- `server/includes/voids.nvgt` - Funções auxiliares (eadm)

### Cliente
- `cliente/includes/net.nvgt` - Processamento de pacotes
- `cliente/includes/add.nvgt` - Buffers de chat
- `cliente/client.nvgt` - Loop principal

### Referência BGT
- `server/includes/net.bgt` - Handlers originais
- `server/server.bgt` - telllocal() original
- `cliente/includes/add.bgt` - Sistema de buffers original
