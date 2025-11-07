# 📋 Plano Detalhado de Implementação de NPC para NVGT

## 🎯 Visão Geral

Implementar sistema de NPCs no cliente NVGT replicando estrutura BGT, mas adaptado para cliente (recebe dados do servidor).

---

## 📋 TASK 1: Criar Estrutura de Dados NPC

### Objetivo
Criar classe `npc_client_class` com dados mínimos para renderização.

### Scope
- Arquivo: `cliente/includes/globals.nvgt`
- Depois: `cliente/includes/classes.nvgt` (se quiser estrutura maior)

### Estrutura (Mínima)
```nvgt
class npc_client_class {
    int x, y;              // Posição
    int id;                // ID único
    int hp, max_hp;        // Vida
    string name;           // Nome
    string map;            // Mapa onde está
    timer last_seen;       // Quando foi visto pela última vez
}

npc_client_class[] npcs; // Array global de NPCs visíveis
```

### Verificação
- Compile sem erros
- Declare array `npcs` em globals.nvgt

---

## 📋 TASK 2: Criar Classe para Dados de NPC do Servidor

### Objetivo
Estrutura para receber dados completos do servidor (25+ parâmetros).

### Scope
- Arquivo: `cliente/includes/classes.nvgt`

### Estrutura
```nvgt
class npc_spawn_data_class {
    // Posição
    int x, y, x_inicial, y_inicial;
    int left_range, right_range;
    
    // Vida e Dano
    int hp, max_hp;
    double dano_recibido, dano_causado, dano_espejo;
    double degradation;
    
    // Comportamento
    int intervalo_ataque, intervalo_movimento, intervalo_som;
    int tempo_aparicion;
    int enable_respawn, enable_bomba;
    
    // Identidade
    string nome;
    int id;
    
    // Items e Som
    string items;
    string som_ataque, som_calmo, som_muerte;
    string msg_muerte;
    
    // Ranges
    int distancia_ataque;
}
```

### Verificação
- Compile sem erros
- Estrutura pronta para receber 25+ parâmetros

---

## 📋 TASK 3: Implementar Handler `npc:` em map.nvgt

### Objetivo
Parser que lê comando `npc:` e armazena dados.

### Scope
- Arquivo: `cliente/includes/map.nvgt`
- Localização: Após handler `item` ou `where`

### Código
```nvgt
else if(parsed[0] == "npc" && parsed.length() >= 18) {
    // Parsear todos os 25 parâmetros
    int x = string_to_number(parsed[1]);
    int y = string_to_number(parsed[2]);
    double vida = string_to_number(parsed[3]);
    double xp = string_to_number(parsed[4]);
    double dist_ataque = string_to_number(parsed[5]);
    double dano_recib = string_to_number(parsed[6]);
    double dano_causa = string_to_number(parsed[7]);
    double dano_espejo = string_to_number(parsed[8]);
    int tiempo_ataque = string_to_number(parsed[9]);
    int tiempo_caminar = string_to_number(parsed[10]);
    int tiempo_sonido = string_to_number(parsed[11]);
    string items = parsed[12];
    string som_ataque = parsed[13];
    string som_calmo = parsed[14];
    string som_muerte = parsed[15];
    string nombre = parsed[16];
    string msg_muerte = parsed[17];
    int tiempo_apariencia = (parsed.length() > 18) ? string_to_number(parsed[18]) : 0;
    int respawn = (parsed.length() > 19) ? string_to_number(parsed[19]) : 0;
    int bomba = (parsed.length() > 20) ? string_to_number(parsed[20]) : 0;
    
    // Criar NPC client
    npc_client_class new_npc;
    new_npc.x = x;
    new_npc.y = y;
    new_npc.hp = (int)vida;
    new_npc.max_hp = (int)vida;
    new_npc.name = nombre;
    new_npc.id = random(1000, 9999);
    new_npc.map = mapname;
    new_npc.last_seen.restart();
    
    npcs.insert_last(new_npc);
    
    debug_log("👹 NPC criado: " + nombre + " em (" + x + "," + y + ") HP:" + vida);
}
```

### Verificação
- Compile sem erros
- Teste parsing com exemplo real de .map

---

## 📋 TASK 4: Criar Função spawn_npc()

### Objetivo
Função para criar/atualizar um NPC no cliente.

### Scope
- Arquivo: `cliente/includes/map.nvgt` (ou novo arquivo `npc.nvgt`)

### Código
```nvgt
void spawn_npc(int x, int y, int hp, string nome, int id) {
    // Verificar se NPC já existe
    for(uint i = 0; i < npcs.length(); i++) {
        if(npcs[i].id == id) {
            npcs[i].x = x;
            npcs[i].y = y;
            npcs[i].hp = hp;
            npcs[i].last_seen.restart();
            return; // Atualizar existente
        }
    }
    
    // Criar novo
    npc_client_class novo;
    novo.x = x;
    novo.y = y;
    novo.hp = hp;
    novo.max_hp = hp;
    novo.name = nome;
    novo.id = id;
    novo.map = mapname;
    novo.last_seen.restart();
    
    npcs.insert_last(novo);
}

void remove_npc(int id) {
    for(uint i = 0; i < npcs.length(); i++) {
        if(npcs[i].id == id) {
            npcs.remove_at(i);
            return;
        }
    }
}

void clear_npcs() {
    npcs.resize(0);
}
```

### Verificação
- Compile sem erros
- Teste criar/remover NPCs

---

## 📋 TASK 5: Criar npc_loop() - Detecção de NPCs

### Objetivo
Loop que detecta NPCs próximos e atualiza estado.

### Scope
- Arquivo: `cliente/includes/map.nvgt`

### Código
```nvgt
void npc_loop() {
    for(uint i = 0; i < npcs.length(); i++) {
        // Verificar se NPC está próximo (20 tiles)
        if(npcs[i].x >= me.x - 20 && npcs[i].x <= me.x + 20 &&
           npcs[i].y >= me.y - 20 && npcs[i].y <= me.y + 20) {
            
            // NPC próximo - reproduzir som se necessário
            if(npcs[i].last_seen.elapsed > 2000) {
                // Reproduzir som nervioso (calmo)
                npcs[i].last_seen.restart();
                debug_log("🎵 Som de NPC: " + npcs[i].name);
            }
        }
        
        // Remover NPCs muito antigos (mais de 1 minuto sem atualização)
        if(npcs[i].last_seen.elapsed > 60000) {
            npcs.remove_at(i);
            i--;
        }
    }
}
```

### Verificação
- Compile sem erros
- Teste loop com NPCs criados

---

## 📋 TASK 6: Integrar npc_loop() no Game Loop

### Objetivo
Chamar `npc_loop()` no main game loop para manter NPCs atualizados.

### Scope
- Arquivo: `cliente/includes/comandos.nvgt`
- Localização: Após `safeloop()` e `travel_point_loop()`

### Código
```nvgt
// Adicionar após travel_point_loop():
npc_loop(); // Detectar e processar NPCs

// No final do game loop principal
```

### Verificação
- Compile sem erros
- NPCs devem ser atualizados a cada frame

---

## 📋 TASK 7: Implementar Detecção de Ataque de NPC

### Objetivo
Processar mensagens do servidor indicando que NPC atacou.

### Scope
- Arquivo: `cliente/includes/net.nvgt` (processar mensagens)

### Pseudo-Código
```
Quando receber mensagem "npc_attack:id:dano" do servidor:
├─ Encontrar NPC com id
├─ Exibir mensagem de dano
├─ Tocar som de dano
└─ Reduzir HP do player
```

### Verificação
- Compilação não afeta por agora
- Deixar TODO para depois

---

## 📋 TASK 8: Criar Função para Exibir NPCs no HUD

### Objetivo
Mostrar lista de NPCs próximos no HUD (opcional para fase 1).

### Scope
- Arquivo: `cliente/includes/hud.nvgt` (se existir)

### Função Sugerida
```nvgt
void display_npcs_nearby() {
    speak("Inimigos próximos:");
    for(uint i = 0; i < npcs.length(); i++) {
        int dist = abs(npcs[i].x - me.x) + abs(npcs[i].y - me.y);
        speak(npcs[i].name + " a " + dist + " tiles");
    }
}
```

### Verificação
- Compilação não requerida para fase 1
- Deixar para depois

---

## 📋 TASK 9: Testar Compilação

### Objetivo
Compilar cliente com todas as mudanças de NPC.

### Scope
- Rodar compilador
- 0 erros esperados
- Warnings OK

### Checklist
- [ ] map.nvgt compila
- [ ] classes.nvgt compila
- [ ] globals.nvgt compila
- [ ] comandos.nvgt compila
- [ ] client.nvgt compila
- [ ] client.zip gerado

---

## 📋 TASK 10: Testar em Mapas Reais

### Objetivo
Validar que NPCs aparecem em mapas com comando `npc:`.

### Scope
- Carregar mapa com NPCs
- Verificar que dados são parseados
- Ver debug logs de NPC criado

### Teste
```
□ Mapa carrega sem erro
□ NPCs aparecem no debug log
□ spawn_npc() é chamado
□ npc_loop() executa sem erro
□ debug_log mostra mensagens de NPC
```

---

## 🎯 Ordem de Execução Recomendada

```
1. TASK 1 - Estrutura de Dados (5 min)
   ↓
2. TASK 2 - Classe Spawn Data (5 min)
   ↓
3. TASK 3 - Handler NPC em map.nvgt (10 min)
   ↓
4. TASK 4 - Função spawn_npc() (5 min)
   ↓
5. TASK 5 - npc_loop() (10 min)
   ↓
6. TASK 6 - Integrar no Game Loop (5 min)
   ↓
7. TASK 9 - Testar Compilação (5 min)
   ↓
8. TASK 10 - Testar em Mapas (10 min)
   ↓
9. TASK 7 - Detecção de Ataque (TODO depois)
   ↓
10. TASK 8 - Exibir no HUD (TODO depois)
```

**Tempo Total Fase 1**: ~55 minutos

---

## 📊 Métricas de Sucesso

- ✅ Handler `npc:` parser todos os 25 parâmetros
- ✅ 0 erros de compilação
- ✅ NPCs aparecem em debug log
- ✅ 432 ocorrências de `npc:` parseadas corretamente
- ✅ npc_loop() executa sem travamento

---

## 🚀 Próxima Fase (Depois de Sucesso)

1. Sistema de ataque de NPC (servidor envia dano)
2. Exibição de HP em HUD
3. Som de movimento de NPC
4. Integração com sistema de combate

---

**Status**: 🟢 PLANO COMPLETO

Pronto para começar TASK 1!

