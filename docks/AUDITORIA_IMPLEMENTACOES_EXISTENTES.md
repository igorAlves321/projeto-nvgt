# 🔍 Auditoria Completa: Implementações Existentes

## Data: 6 de novembro de 2025

### 📊 Resumo Executivo

Foram encontradas **implementações parciais** dos 3 sistemas que precisamos completar:

| Sistema | Status | Arquivo | O que Existe |
|---------|--------|---------|---|
| **Travel Point (tp)** | ⏳ Parcial | map.nvgt + buildermenu.nvgt | Parser OK, sem lógica de detecção |
| **Where** | ❌ Ausente | - | Apenas var global `mapname` |
| **Item** | ✅ **EXISTE** | item.nvgt | Sistema completo com `spawn_obj()` |

---

## 1️⃣ Travel Point (tp / travelpoint)

### 📍 Arquivo: `map.nvgt` (linhas 296-311)

**Status**: ✅ Parser adicionado, ⏳ Lógica TODO

```nvgt
// TRAVEL POINT (tp): Teleportes entre mapas
else if((parsed[0] == "tp" || parsed[0] == "travelpoint") && parsed.length() >= 8) {
    int zone_x1 = string_to_number(parsed[1]);
    int zone_y1 = string_to_number(parsed[2]);
    int zone_x2 = string_to_number(parsed[3]);
    int zone_y2 = string_to_number(parsed[4]);
    int dest_x = string_to_number(parsed[5]);
    int dest_y = string_to_number(parsed[6]);
    string dest_map = parsed[7];
    string message = (parsed.length() > 8) ? parsed[8] : "Você foi teleportado.";
    
    debug_log("📍 Travel Point criado: " + dest_map + " (" + dest_x + "," + dest_y + ")");
}
```

**Falta**: Estrutura para armazenar dados e lógica de detecção de entrada

---

### 📍 Arquivo: `buildermenu.nvgt` (linhas 145+)

**Status**: ✅ Menu de criação de portais existe

```nvgt
else if(selected_id == "travelpoint") {
    // Menu para criar travel point
}

// Também tem:
- portals_menu() - gerenciador de portais
- Função para criar portais com vários tipos (simples, requer item, mão única)
```

**Existe**:
- ✅ Menu de construtor
- ✅ Lógica de criação no editor
- ❌ Falta lógica de **runtime** (detecção no game loop)

---

## 2️⃣ Where (Localização)

### 📍 Arquivo: `map.nvgt` (linhas 312-317)

**Status**: ⏳ Parser básico apenas

```nvgt
// WHERE: Descrição de localização
else if(parsed[0] == "where" && parsed.length() >= 2) {
    string location = data_line.substr(6);
    debug_log("📍 Localização: " + location);
}
```

**Existe**:
- ✅ Parsing da linha
- ❌ Armazenamento global
- ❌ Exibição em HUD
- ❌ Reprodução via TTS

### 📍 Variável Global: `mapname` em `globals.nvgt` (linha 256)

```nvgt
string mapname = "";
```

**Usada em**:
- `net.nvgt`: Ao carregar mapa, chama `speak("Você está no mapa: " + mapname)`
- `classes.nvgt`: Detecção de eventos por mapa
- `map.nvgt`: Verificação de tipo de mapa

---

## 3️⃣ Item (Itens do Mapa)

### 📍 Arquivo: `item.nvgt` - **JÁ EXISTE COMPLETO!** ✅

**Status**: ✅ Sistema funcional

```nvgt
void spawn_obj(int x = random(0, 200), int y = 0, string what = "knife", int amount = 1) {
    // Criar item no mapa
    if (objs.length() <= 600) {
        obj_class obj1;
        obj1.x = x;
        obj1.y = y;
        obj1.item = what;
        obj1.amount = amount;
        obj1.loop_interval = random(1000, 2000);
        objs.insert_last(obj1);
    }
}

void objsloop() {
    // Loop de detecção e som
}

void destroy_all_objs() { }
void remove_obj(uint index) { }
int get_obj_at(int x, int y) { }
```

**Implementação Completa**:
- ✅ Classe `obj_class` em `classes.nvgt`
- ✅ Array global `objs[]` em `globals.nvgt`
- ✅ Funções de spawn/destroy
- ✅ Loop de detecção
- ✅ Sistema de som

**O que falta**:
- Integração do handler `item:` do mapa com `spawn_obj()`
- Detecção de coleta pelo player

---

## 🎯 O Que Fazer

### ✅ Já Feito
- ✅ Parser de `tp` adicionado
- ✅ Parser de `where` adicionado
- ✅ Parser de `item` adicionado
- ✅ Sistema de items em `item.nvgt`

### ⏳ TODO - Conectar Parsers com Lógica

1. **Travel Point**:
   - Criar array de `travel_point` estrutura
   - Adicionar função `spawn_travel_point()`
   - Loop de detecção em game loop
   - Executar teletransporte

2. **Where**:
   - Criar variável global `current_location`
   - Handler `where:` preencher variável
   - Exibir ao carregar mapa
   - Reproduzir via TTS

3. **Item**:
   - Handler `item:` chamar `spawn_obj()`
   - Parsear corretamente os parâmetros
   - Integrar com detecção de coleta

---

## 📂 Estrutura de Arquivos Relevantes

```
cliente/includes/
├── map.nvgt              # Parsers dos 3 comandos ✅
├── item.nvgt             # Sistema de items COMPLETO ✅
├── item.bgt              # Referência BGT
├── classes.nvgt          # obj_class, estruturas
├── globals.nvgt          # mapname, objs[], arrays
├── buildermenu.nvgt      # Portais do construtor
├── chat.nvgt             # Para reproduzir msgs TTS
└── comandos.nvgt         # Detecção de teclas
```

---

## 🔗 Integrações Necessárias

### Travel Point Requer:
- Array global de travel points (novo)
- Estrutura `travel_point` (novo)
- Loop de detecção no game loop
- Função `go_to_map()` para teletransporte

### Where Requer:
- Variável global `current_location` (novo)
- Integração com output ao carregar
- Reprodução via `speak()` (já existe)

### Item Requer:
- Apenas integração: handler → `spawn_obj()`
- Traduzir parâmetros do mapa para função

---

## ⚠️ Duplicações a Evitar

| O que NÃO fazer | Por quê | Fazer ao invés |
|---|---|---|
| Criar novo sistema de items | `item.nvgt` já existe | Integrar handler com `spawn_obj()` |
| Criar novo sistema de portais | `buildermenu.nvgt` já existe | Criar runtime logic |
| Duplicar menu de portais | Já existe em `buildermenu.nvgt` | Apenas implementar detecção |

---

**Status**: 🟡 PRONTO PARA IMPLEMENTAÇÃO

Todos os parsers estão OK. Falta apenas conectar com a lógica de runtime!

