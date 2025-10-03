# Sistema de Zonas Desabilitadas ✅

## 📋 Visão Geral

O sistema de **Zonas Desabilitadas** permite criar áreas seguras no mapa onde certas ações são restritas, como PvP, uso de itens ou comandos.

---

## 🎯 Funcionalidades Implementadas

### ✅ Classe `game_disabled_zone`
- Definição de áreas retangulares por coordenadas (minx, maxx, miny, maxy)
- Suporte para múltiplos mapas
- Três tipos de restrições configuráveis:
  - `disable_pvp` - Desabilita combate jogador vs jogador
  - `disable_items` - Desabilita uso de itens
  - `disable_commands` - Desabilita comandos
- Mensagem customizável por zona

### ✅ Integração com Sistema de Combate
- Balas não causam dano em zonas com PvP desabilitado (`bullet.nvgt:245`)
- Atacantes em zonas seguras não podem atacar (`bullet.nvgt:254`)
- Verificação automática durante combate

### ✅ Zonas Padrão Inicializadas
1. **Escola** - Zona segura (0-50, 0-50)
2. **Hospital** - Zona segura (0-30, 0-30)
3. **Delegacia** - Zona segura (0-25, 0-25)

---

## 🎮 Comandos Administrativos

### Para Administradores (is_admin)

#### `/listzones`
Lista todas as zonas desabilitadas configuradas no servidor.
```
Uso: /listzones
Saída: Exibe lista com índice, mapa, coordenadas e restrições
```

#### `/checkzone`
Verifica se a posição atual está em uma zona desabilitada.
```
Uso: /checkzone
Saída: Informa se está em zona e suas configurações
```

---

### Para Super Administradores (is_super_admin)

#### `/addzone <minx> <maxx> <miny> <maxy> <mapa> [mensagem]`
Adiciona nova zona desabilitada.
```
Uso: /addzone 0 100 0 100 cidade "Zona Segura - Prefeitura"
Padrão: PvP desabilitado, itens e comandos habilitados
```

#### `/removezone <índice>`
Remove zona desabilitada por índice.
```
Uso: /removezone 3
Nota: Use /listzones para ver os índices
```

#### `/togglezonepvp <índice>`
Alterna estado de PvP em uma zona específica.
```
Uso: /togglezonepvp 2
Resultado: Habilita/desabilita PvP na zona
```

#### `/savezones`
Salva configurações de zonas em arquivo `disabled_zones.cfg`.
```
Uso: /savezones
Formato: map|minx|maxx|miny|maxy|pvp|items|commands|message
```

#### `/loadzones`
Carrega zonas do arquivo `disabled_zones.cfg`.
```
Uso: /loadzones
Nota: Substitui todas as zonas atuais pelas do arquivo
```

---

## 📂 Estrutura de Arquivos

### Implementação Principal
- **`systems_advanced.nvgt`** - Classe e lógica de zonas (linhas 356-414)
- **`admin_commands.nvgt`** - Comandos de gestão (linhas 243-444)
- **`bullet.nvgt`** - Integração com combate (linhas 244-259)

### Arquivo de Configuração
**`disabled_zones.cfg`** (formato):
```
// Zonas Desabilitadas - Configuração
// Formato: map|minx|maxx|miny|maxy|pvp|items|commands|message

escola|0|50|0|50|1|0|0|Zona Segura - Escola
hospital|0|30|0|30|1|0|0|Zona Segura - Hospital
delegacia|0|25|0|25|1|0|0|Zona Segura - Delegacia
```

---

## 🔧 API de Funções

### `init_disabled_zones()`
Inicializa zonas padrão ao iniciar servidor.
```cpp
// Chamado em: server.nvgt linha 580
init_disabled_zones();
```

### `is_in_disabled_zone(int player_index) -> bool`
Verifica se jogador está em qualquer zona desabilitada.
```cpp
if(is_in_disabled_zone(player_index)) {
    // Jogador está em zona segura
}
```

### `game_disabled_zone.is_inside(int x, int y, string map) -> bool`
Verifica se coordenada específica está dentro da zona.
```cpp
if(zona.is_inside(100, 200, "cidade")) {
    // Posição está dentro da zona
}
```

---

## 🎯 Casos de Uso

### 1. Criar Zona Segura em Spawn
```
/addzone 0 100 0 100 spawn "Spawn Protegido"
/togglezonepvp 0  // Desabilitar PvP se necessário
/savezones
```

### 2. Zona de Evento sem Combate
```
/addzone 200 300 200 300 evento "Arena de Eventos"
/togglezonepvp 1  // Alternar PvP conforme evento
```

### 3. Backup e Restauração
```
// Salvar configuração atual
/savezones

// Restaurar após reset
/loadzones
```

---

## ⚙️ Configuração Personalizada

### Modificar Zona Existente
1. Use `/listzones` para ver índice
2. Use `/togglezonepvp <índice>` para alternar PvP
3. Use `/savezones` para persistir

### Adicionar Nova Restrição
Para adicionar novas restrições, modifique a classe `game_disabled_zone`:
```cpp
class game_disabled_zone {
    // Adicionar nova propriedade
    bool disable_teleport;

    // Atualizar constructor
    game_disabled_zone(...) {
        disable_teleport = false;
    }
}
```

---

## 🔍 Verificação de Funcionamento

### Testar PvP Bloqueado
1. Entre em zona com `/checkzone`
2. Tente atacar outro jogador
3. Bala não deve causar dano

### Testar Persistência
1. Configure zonas com `/addzone`
2. Salve com `/savezones`
3. Reinicie servidor
4. Carregue com `/loadzones`

---

## 📊 Status de Implementação

| Funcionalidade | Status | Arquivo | Linha |
|----------------|--------|---------|-------|
| Classe de zona | ✅ | systems_advanced.nvgt | 359-381 |
| Verificação de posição | ✅ | systems_advanced.nvgt | 407-414 |
| Integração PvP | ✅ | bullet.nvgt | 244-259 |
| Comandos admin | ✅ | admin_commands.nvgt | 243-444 |
| Persistência em arquivo | ✅ | admin_commands.nvgt | 359-444 |
| Inicialização automática | ✅ | server.nvgt | 580 |

---

## ✨ Exemplo Completo de Uso

```bash
# Admin configura nova zona segura
/addzone 0 150 0 150 cidadecentral "Centro da Cidade - Zona Segura"

# Verifica se foi criada
/listzones

# Testa a zona
/checkzone  # (dentro da área)
# Saída: "Você está na zona [3] - Centro da Cidade - Zona Segura | PvP:OFF"

# Salva para persistir
/savezones
# Saída: "4 zonas salvas em disabled_zones.cfg"
```

---

## 🚀 Melhorias Futuras Sugeridas

1. **Notificações de Entrada/Saída**
   - Avisar jogador ao entrar/sair de zona

2. **Zonas com Tempo Limitado**
   - Zonas que expiram após X minutos

3. **Zonas Circulares**
   - Além de retangulares, permitir círculos

4. **Restrições de Itens Específicos**
   - Desabilitar apenas certos itens (armas)

5. **UI de Configuração**
   - Interface gráfica para gestão de zonas

---

## 📝 Notas Técnicas

- Zonas são verificadas em tempo real durante combate
- Não há overhead significativo (verificação O(n) onde n = número de zonas)
- Suporte para zonas sobrepostas (primeira zona encontrada é aplicada)
- Sistema thread-safe para acesso concorrente

**Status:** ✅ Totalmente implementado e funcional
**Última atualização:** 2025-10-03
