# 🔍 Análise de Implementação de NPC - BGT para NVGT

## Arquivo Fonte: `server/includes/bots/npc.bgt`

---

## 📊 Estrutura da Classe NPC (BGT)

### Propriedades Principais

```nvgt
class npc {
    // Posição
    int x, y, x_inicial, y_inicial;
    int left_range, right_range;
    
    // Identidade
    int id, my_index, mapindex, p_index;
    string map, nombrenpc;
    
    // Vida e Dano
    double vidainicial, vida;
    double danoquerecibira, danoquedara, danodelespejo;
    double degradation; // Desgaste de armas
    
    // Experiência
    double xp;
    
    // Distâncias
    double distanciaataques;
    
    // Sons
    string[] items, pasos, impactos, sonidosataque, sonidosnervioso;
    string sonidoataque, sonidonervioso, sonidomuerte;
    
    // Items e Drops
    string itemsadar;
    string asesino, msgmuerte;
    
    // Timers
    int tiempoparaatacar, tiempoparacaminar, tiempodelossonidos, tiempoaparicion;
    int enablerespawn, enablebombs;
    timer ttiempoparaatacar, ttiempoparacaminar, ttiempodelossonidos, ttiempoaparicion;
    
    // Combate
    string impactosbala;
}
```

### Parâmetros do Construtor (24 parâmetros!)

```
npc(
    int xx, int yy,                           // Posição (x, y)
    double vida2,                              // HP inicial
    double xpquedara,                          // XP ao derrotar
    double distanciaataque,                    // Distância de ataque
    double ddanoquerecibira,                   // Dano que recebe
    double ddanoquedara,                       // Dano que causa
    double ddanodelespejo,                     // Dano de reflexo
    int tttiempoparaatacar,                    // Intervalo ataque (ms)
    int tttiempoparacaminar,                   // Intervalo movimento (ms)
    int tttiempodelossonidos,                  // Intervalo som (ms)
    string itemsquedara,                       // Items ao morrer (csv)
    string sonidoalatacar,                     // Som ataque (csv)
    string sonidocalmado,                      // Som calmo (csv)
    string sonidoalmorir,                      // Som morte
    string nombredelbot,                       // Nome do NPC
    string mensajealmorir,                     // Mensagem ao morrer
    int tttiempoaparicion,                     // Delay aparição
    int enablerespawn2,                        // Respa automático?
    int enablebombs2,                          // Pode usar bomba?
    string map,                                // Mapa
    string pasosnpc2,                          // Sons de passos (csv)
    int l_r,                                   // Left range
    int r_r,                                   // Right range
    string balas,                              // Impactos de bala (csv)
    double degradation2                        // Taxa degradação arma
)
```

---

## 🎬 Métodos Implementados

### 1. `void die()` - Morte do NPC
```
- Reproduz som de morte
- Encontra assassino
- Envia mensagem de morte
- Distribui items para jogador
- Incrementa contador de kills
- Verifica títulos (10 kills = Caçador)
- Ganha XP
- Armazena dados em npc_data para respawn
```

### 2. `void move()` - Movimento
```
- Se jogador à direita: move para esquerda (x -= 2)
- Se jogador à esquerda: move para direita (x += 2)
- Respeita left_range e right_range
- Reproduz som de passos
- Verifica minas no chão
```

### 3. `void attack()` - Ataque
```
- Sistema de degradação de armas (1/300 chance)
- Reproduz som de ataque (aleatório)
- Calcula dano com proteção de roupa
- Reduz HP do jogador
- Marca "última vez que foi atingido" (lasthit)
```

### 4. `bool exists_player_in_my_map()`
```
- Verifica se há jogador no mapa
```

### 5. `int select_player_to_attack()`
```
- Seleciona jogador aleatório para atacar
```

---

## 📦 Classe Complementar: npc_data

Usada para armazenar dados de NPC que morreram (para respawn).

```nvgt
class npc_data {
    // Mesmas propriedades da classe npc
    // Usado para persistência de dados após morte
    timer respawn; // Timer para respawn automático
}
```

---

## 📋 Formato de NPC nos Arquivos .map

Analisando exemplo: `npc:100:0:3000000:400000:2:0:5000:0:800:500:3000:mgerems.700000,cuerpo_de_rata.1:morcegobater:morcegonervioso,morcegoanda:none:Una rata:¡*nick* ;Mat! a una rata!;:180000:0:0:nada:1:1000:default:0.1`

Parâmetros em ordem:
```
0  = npc (comando)
1  = x = 100
2  = y = 0
3  = vida inicial = 3000000
4  = xp = 400000
5  = distancia ataque = 2
6  = dano recebido = 0
7  = dano causado = 5000
8  = dano reflexo = 0
9  = intervalo ataque = 800
10 = intervalo movimento = 500
11 = intervalo som = 3000
12 = items = mgerems.700000,cuerpo_de_rata.1
13 = som ataque = morcegobater
14 = som calmo = morcegonervioso,morcegoanda
15 = som morte = none
16 = nome = Una rata
17 = mensagem = ¡*nick* ;Mat! a una rata!;
18 = tempo aparição = 180000
19 = respawn? = 0
20 = bomba? = 0
21 = tipo drops = nada
22 = stance? = 1
23 = respawn time? = 1000
24 = dificuldade? = default
25 = degradation = 0.1
```

---

## 🎯 O Que é Necessário para NVGT

### ✅ Já Existe
- Sistema de combate (dano, proteção, HP)
- Sistema de items
- Sistema de sons
- Sistema de zonas/mapas
- Timer class

### ⚠️ Precisa Ser Criado
1. **Classe `npc_class`** - Estrutura de dados
2. **Classe `npc_data_class`** - Para respawn
3. **Função `spawn_npc()`** - Criar NPC
4. **Função `npc_loop()`** - Loop principal (movimento, ataque, morte)
5. **Handler `npc:` em map.nvgt** - Parser de comando
6. **Integração no game loop** - Chamar npc_loop()

### ⚠️ SIMPLIFICAÇÕES PARA NVGT
(Cliente não é servidor, não controla tudo)

- **Movimento**: Cliente pode apenas exibir movimento (servidor controla)
- **Ataque**: Cliente recebe dano do servidor
- **Respawn**: Servidor gerencia, cliente recebe update
- **Drops**: Servidor envia, cliente exibe items

---

## 📐 Estratégia de Implementação (Cliente NVGT)

### Fase 1: Estrutura de Dados
```nvgt
class npc_client_class {
    int x, y, id;
    string name;
    double life, max_life;
    // Apenas o mínimo para renderização cliente
}
```

### Fase 2: Parser
```nvgt
Handler npc: em map.nvgt
├─ Parsear todos os 25 parâmetros
├─ Enviar para servidor
└─ Receber confirmação
```

### Fase 3: Loop
```nvgt
npc_loop() {
    ├─ Detectar NPCs visíveis
    ├─ Atualizar posição (recebida do servidor)
    ├─ Reproduzir sons (se próximo)
    └─ Exibir em HUD
}
```

### Fase 4: Integração
```nvgt
No game loop (comandos.nvgt):
├─ Chamar npc_loop()
├─ Processar dano recebido
└─ Atualizar HUD com NPCs
```

---

## 🚨 IMPORTANTE: Cliente vs Servidor

**NPC no BGT é SERVIDOR-SIDE!**

No NVGT (cliente), precisamos:
1. Receber dados de NPC do servidor
2. Exibir posição, nome, vida
3. Processar ataques que vêm do servidor
4. Enviar ações do jogador

**Não vamos implementar:**
- Lógica completa de combate (servidor cuida)
- AI de movimento (servidor cuida)
- Respawn (servidor cuida)

**Vamos implementar:**
- Parser do comando `npc:` para receber dados do servidor
- Exibição visual de NPCs
- Loop de renderização

---

## 📝 Plano de Tarefas

1. **Análise Completa** - Entender BGT 100%
2. **Criar Classe npc_client_class** - Estrutura minimal
3. **Implementar Handler npc:** - Parser em map.nvgt
4. **Criar npc_loop()** - Detectar e exibir
5. **Integrar no game loop** - Chamar npc_loop()
6. **Testar compilação** - 0 erros
7. **Testar em mapas reais** - Ver NPCs aparecerem

---

**Status**: 🟡 ANÁLISE COMPLETA

Pronto para começar implementação!

