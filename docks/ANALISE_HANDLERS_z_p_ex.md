# 🔍 Análise Profunda: Handlers Críticos (z, p, ex)

## 1. Handler `z:` - ZONE (19,126 ocorrências)

### Definição
```bgt
class zone {
    int min_x;
    int max_x;
    int min_y;
    int max_y;
    string text;
}
```

### Formato de Parse (map.bgt linha 84)
```bgt
if(parsed[0] =="z" && parsed.length() ==6) {
    zone z1(string_to_number(parsed[1]),   // min_x
            string_to_number(parsed[2]),   // max_x
            string_to_number(parsed[3]),   // min_y
            string_to_number(parsed[4]),   // max_y
            parsed[5]);                     // text
    zones.insert_last(z1);
}
```

### Padrão do .map
```
z:min_x:max_x:min_y:max_y:text
```

### Exemplos Reais

**Exemplo 1 - Simples:**
```
z:1:50:0:50:-
```
- min_x: 1
- max_x: 50
- min_y: 0
- max_y: 50
- text: "-"

**Exemplo 2 - Com Texto Longo:**
```
z:1:1:0:0:El aire puede ser sumamente destructivo, as... (texto muito longo)
```
- min_x: 1
- max_x: 1
- min_y: 0
- max_y: 0
- text: [mensagem longa de diálogo]

**Exemplo 3 - Diálogo:**
```
z:2:2:45:45:Dice una voz grave.
```

### Propósito
- **Zone / Area**: Define áreas retangulares no mapa
- **Possível Uso**: 
  - Triggar de diálogo ao entrar em zona
  - Áreas de efeito especial
  - Pontos de interesse
  - Sistema de chat/mensagens

### Implementação NVGT

```nvgt
class zone_class {
    int min_x, max_x;
    int min_y, max_y;
    string text;
    
    zone_class(int minx, int maxx, int miny, int maxy, string txt) {
        min_x = minx;
        max_x = maxx;
        min_y = miny;
        max_y = maxy;
        text = txt;
    }
}

// Global
zone_class@[] zones;
```

---

## 2. Handler `p:` - PLATFORM (9,162 ocorrências)

### Definição
```bgt
class platform {
    string plattype;
    bool is_platform, is_staircase, is_wall;
    int min_x, max_x, min_y, max_y;
    string tiles;
}
```

### Formato de Parse (map.bgt linha 80)
```bgt
platform p1(parsed[0],              // type (pode ser "p", "sc", "w")
            string_to_number(parsed[1]),   // min_x
            string_to_number(parsed[1]),   // max_x (duplicado?)
            string_to_number(parsed[2]),   // min_y
            string_to_number(parsed[3]),   // max_y
            parsed[4]);                     // tiles
```

### Padrão do .map
```
p:type:x:y:tiles
ou
p:minx:maxx:miny:maxy:tiles
```

### Exemplo Real

**Exemplo 1:**
```
p:0:30:0:calcada
```

**Exemplo 2 (possivelmente):**
```
p:0:100:0:50:tilename
```

### Propósito
- **Platform / Elemento Físico**
- **Tipo pode ser:**
  - "p" → Platform (plataforma para pular)
  - "sc" → Staircase (escada)
  - "w" → Wall (parede)
- **tiles**: Nome do arquivo de sprite/tile

### Possível Padrão Corrigido

O código em map.bgt parece estranho (duplica min_x para maxx):
```bgt
// Original (pode estar errado):
platform p1(parsed[0], 
            string_to_number(parsed[1]),   // min_x
            string_to_number(parsed[1]),   // maxx (DUPLICADO!)
            string_to_number(parsed[2]),   // min_y
            string_to_number(parsed[3]),   // maxy
            parsed[4]);
```

Provável padrão correto:
```
p:type:minx:maxx:miny:maxy:tiles
// Exemplo:
p:p:0:100:0:50:tilename
```

---

## 3. Handler `ex:` - EXTRACT (6,345 ocorrências)

### Definição
```bgt
class extract {
    int minx, maxx, miny, maxy;
    int hmitems;              // how many items
    int attempts, initial_attempts;
    string extracting, extracted;
    string item;
    int extracttime;
    timer extracttimer;
}
```

### Formato de Parse (map.bgt linha 92)
```bgt
if(parsed[0]=="ex" && parsed.length()==11) {
    extract e(string_to_number(parsed[1]),   // min_x
              string_to_number(parsed[2]),   // max_x
              string_to_number(parsed[3]),   // min_y
              string_to_number(parsed[4]),   // max_y
              string_to_number(parsed[5]),   // how many items
              string_to_number(parsed[6]),   // attempts
              string_to_number(parsed[7]),   // extracttime
              parsed[8],                      // item name
              parsed[9],                      // sound extracting
              parsed[10]);                    // sound extracted
    extracts.insert_last(e);
}
```

### Padrão do .map
```
ex:minx:maxx:miny:maxy:items:attempts:time:item:sound1:sound2
```

### Exemplo Provável
```
ex:100:200:50:150:5:3:5000:madeira:chop:success
```
- Zona: (100-200, 50-150)
- Itens por colheita: 5
- Tentativas: 3
- Tempo de extração: 5000ms
- Item dropado: madeira
- Som extracting: chop
- Som extracted: success

### Propósito
- **Extract Zone**: Área onde jogador extrai/colhe recursos
- **Exemplo de Uso**: Minerar ouro, cortar madeira, colher plantas
- **Mecânica**: 
  - Jogador entra na zona
  - Começa a coletar (som extracting)
  - Após `attempts` tentativas → sucesso (som extracted)
  - Dropa `items` quantidade do `item` especificado

---

## 📊 Comparação dos 3 Handlers

| Aspecto | z: | p: | ex: |
|---------|----|----|-----|
| **Ocorrências** | 19,126 | 9,162 | 6,345 |
| **Parâmetros** | 5 | 5-6 | 10 |
| **Tipo** | Zona/Trigger | Elemento Físico | Zona de Extração |
| **Uso Principal** | Diálogo/Texto | Plataformas | Colheita/Mineração |
| **Classe BGT** | zone | platform | extract |
| **Tipo de Array** | zones[] | platforms[] | extracts[] |

---

## 🎯 Implementação em NVGT

### TASK 1: Criar Classes

**classes.nvgt**
```nvgt
class zone_class {
    int min_x, max_x, min_y, max_y;
    string text;
    
    zone_class(int minx, int maxx, int miny, int maxy, string txt) {
        min_x = minx;
        max_x = maxx;
        min_y = miny;
        max_y = maxy;
        text = txt;
    }
}

class platform_class {
    string plattype;
    bool is_platform, is_staircase, is_wall;
    int min_x, max_x, min_y, max_y;
    string tiles;
    
    platform_class(string type, int minx, int maxx, int miny, int maxy, string tile) {
        plattype = type;
        is_platform = (type == "p");
        is_staircase = (type == "sc");
        is_wall = (type == "w");
        min_x = minx;
        max_x = maxx;
        min_y = miny;
        max_y = maxy;
        tiles = tile;
    }
}

class extract_class {
    int min_x, max_x, min_y, max_y;
    int hmitems, attempts, initial_attempts;
    string item, extracting, extracted;
    int extracttime;
    timer extracttimer;
    
    extract_class(int minx, int maxx, int miny, int maxy, int items, 
                  int atts, int time, string itm, string snd_ext, string snd_extracted) {
        min_x = minx;
        max_x = maxx;
        min_y = miny;
        max_y = maxy;
        hmitems = items;
        attempts = atts;
        initial_attempts = atts;
        extracttime = time;
        item = itm;
        extracting = snd_ext;
        extracted = snd_extracted;
        extracttimer = timer();
    }
}
```

### TASK 2: Adicionar Globals

**globals.nvgt**
```nvgt
zone_class@[] zones;
platform_class@[] platforms;
extract_class@[] extracts;
```

### TASK 3: Handlers em map.nvgt

```nvgt
// ====== HANDLER: z (Zone) ======
else if(parsed[0] == "z" && parsed.length() >= 6) {
    int min_x = int(parsed[1]);
    int max_x = int(parsed[2]);
    int min_y = int(parsed[3]);
    int max_y = int(parsed[4]);
    string text = parsed[5];
    
    // Se houver mais parâmetros, concatenar como texto
    if(parsed.length() > 6) {
        for(int i = 6; i < parsed.length(); i++) {
            text += ":" + parsed[i];
        }
    }
    
    zone_class zone = new zone_class(min_x, max_x, min_y, max_y, text);
    zones.insert_at(zones.length(), zone);
}
// ====== HANDLER: p (Platform) ======
else if(parsed[0] == "p" && parsed.length() >= 5) {
    string plattype = parsed[1];
    int min_x = int(parsed[2]);
    int max_x = int(parsed[3]);  // ou duplica parsed[2]?
    int min_y = int(parsed[4]);
    int max_y = int(parsed[5]);
    string tiles = (parsed.length() > 6) ? parsed[6] : "";
    
    platform_class plat = new platform_class(plattype, min_x, max_x, min_y, max_y, tiles);
    platforms.insert_at(platforms.length(), plat);
}
// ====== HANDLER: ex (Extract) ======
else if(parsed[0] == "ex" && parsed.length() >= 11) {
    int min_x = int(parsed[1]);
    int max_x = int(parsed[2]);
    int min_y = int(parsed[3]);
    int max_y = int(parsed[4]);
    int items = int(parsed[5]);
    int attempts = int(parsed[6]);
    int time = int(parsed[7]);
    string item = parsed[8];
    string snd_ext = parsed[9];
    string snd_extracted = parsed[10];
    
    extract_class extr = new extract_class(min_x, max_x, min_y, max_y, 
                                           items, attempts, time, 
                                           item, snd_ext, snd_extracted);
    extracts.insert_at(extracts.length(), extr);
}
```

---

## 📝 Próximos Passos

1. **Adicionar classes** ao `classes.nvgt`
2. **Adicionar globals** ao `globals.nvgt`
3. **Adicionar handlers** ao `map.nvgt`
4. **Compilar** e verificar erros
5. **Testar** com .map reais
6. **Commit** com mensagens descritivas

---

## ⚠️ Questões Pendentes

1. **Padrão p: correto?**
   - Esperado: `p:type:minx:maxx:miny:maxy:tiles`
   - Precisa validação com exemplos reais

2. **Texto z: com múltiplos parâmetros?**
   - Se `parsed.length() > 6`, concatenar?
   - Ou usar apenas `parsed[5]`?

3. **Verificação de limites?**
   - Validar se min < max?
   - Tratar valores inválidos?

---

