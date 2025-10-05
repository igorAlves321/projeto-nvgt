# 📋 PLANO DE CONVERSÃO DO CLIENTE - ORGANIZADO POR PRIORIDADE

**Data:** 5 de outubro de 2025  
**Status:** 🟢 **FASE 1: 70% COMPLETO**

---

## 🎯 ESTRATÉGIA DE CONVERSÃO

1. ✅ **Fase 1 (70% completo):** Áudio e Fala - APIs nativas
2. 🔄 **Fase 2 (Próxima):** Rede e Autenticação
3. ⏳ **Fase 3:** Interface de Usuário (Menus)
4. ⏳ **Fase 4:** Lógica de Jogo e Mundo

---

## 📁 ARQUIVOS .bgt RESTANTES (47 arquivos)

### 🟢 **PRIORIDADE ALTA - Fase 2 (Rede)**
| Arquivo BGT | Status | Ação | Substituído Por |
|-------------|---------|------|-----------------|
| `net.bgt` | ⏳ PENDENTE | Converter | `net.nvgt` (classe `network` nativa) |
| `comandos.bgt` | ⏳ PENDENTE | Converter | `comandos.nvgt` (send_reliable nativo) |
| `comandos grandes.bgt` | ⏳ PENDENTE | Converter | `comandos.nvgt` (expansão) |
| `downloader.bgt` | ⏳ PENDENTE | Deletar | Classe `http` nativa |
| `googletranslateclient.bgt` | ⏳ PENDENTE | Deletar | Classe `http` nativa |

---

### 🟡 **PRIORIDADE MÉDIA - Fase 3 (UI)**
| Arquivo BGT | Status | Ação | Substituído Por |
|-------------|---------|------|-----------------|
| `m_pro.bgt` | ⏳ PENDENTE | Deletar | `menu.nvgt` nativo |
| `menu.bgt` | ⏳ PENDENTE | Deletar | `menu.nvgt` nativo |
| `menu2.bgt` | ⏳ PENDENTE | Deletar | `menu.nvgt` nativo |
| `adminmenu.bgt` | ⏳ PENDENTE | Converter | `menu.nvgt` + lógica |
| `buildermenu.bgt` | ⏳ PENDENTE | Converter | `menu.nvgt` + lógica |
| `dialogos.bgt` | ✅ CONVERTIDO | OK | `dialogos.nvgt` |
| `editor.bgt` | ⏳ PENDENTE | Deletar | `audio_form::create_input_box()` |
| `virtualizer.bgt` | ✅ CONVERTIDO | OK | `virtualizer.nvgt` |

---

### 🟢 **PRIORIDADE ALTA - Fase 4 (Mundo)**
| Arquivo BGT | Status | Ação | Substituído Por |
|-------------|---------|------|-----------------|
| `map.bgt` | ✅ CONVERTIDO | OK | `map.nvgt` (classe `grid`) |
| `player.bgt` | ✅ CONVERTIDO | OK | `player.nvgt` |
| `zones.bgt` | ⏳ PENDENTE | Converter | `zones.nvgt` |
| `safezones.bgt` | ⏳ PENDENTE | Converter | `safezones.nvgt` |
| `platforms.bgt` | ⏳ PENDENTE | Converter | `platforms.nvgt` |
| `staircase.bgt` | ✅ CONVERTIDO | OK | `staircase.nvgt` |
| `door.bgt` | ✅ CONVERTIDO | OK | `door.nvgt` |
| `elevador.bgt` | ✅ CONVERTIDO | OK | `elevador.nvgt` |

---

### 🔵 **PRIORIDADE BAIXA - Sistemas Auxiliares**
| Arquivo BGT | Status | Ação | Substituído Por |
|-------------|---------|------|-----------------|
| `add.bgt` | ✅ CONVERTIDO | OK | `add.nvgt` |
| `ambiente.bgt` | ✅ CONVERTIDO | OK | `ambiente.nvgt` |
| `classes.bgt` | ✅ CONVERTIDO | OK | `classes.nvgt` |
| `item.nvgt` | ✅ CONVERTIDO | OK | `item.nvgt` |
| `inv.bgt` | ⏳ PENDENTE | Converter | Lógica em `player.nvgt` |
| `weapon.bgt` | ⏳ PENDENTE | Converter | Lógica em `player.nvgt` |
| `secondary_inventory.bgt` | ⏳ PENDENTE | Converter | Lógica em `player.nvgt` |
| `wine.bgt` | ✅ CONVERTIDO | OK | `wine.nvgt` |
| `updater.bgt` | ✅ CONVERTIDO | OK | `updater.nvgt` |
| `texto.bgt` | ✅ CONVERTIDO | OK | `texto.nvgt` |
| `parsed_data.bgt` | ✅ CONVERTIDO | OK | `parsed_data.nvgt` |
| `key_hold.bgt` | ✅ CONVERTIDO | OK | `key_hold.nvgt` |

---

### ⚫ **DELETAR - Funcionalidades Obsoletas**
| Arquivo BGT | Ação | Razão |
|-------------|------|--------|
| `GameEngine.bgt` | 🗑️ DELETAR | Lógica movida para client.nvgt |
| `devices.bgt` | 🗑️ DELETAR | NVGT gerencia dispositivos automaticamente |
| `db.bgt` | 🗑️ DELETAR | SQLite nativo do NVGT |
| `book.bgt` | 🗑️ DELETAR | Funcionalidade removida |
| `dialogs.bgt` | 🗑️ DELETAR | Duplicado de dialogos.bgt |
| `disableds.bgt` | 🗑️ DELETAR | Funcionalidade removida |
| `mlists.bgt` | 🗑️ DELETAR | Funcionalidade removida |
| `speed_stop.bgt` | 🗑️ DELETAR | Funcionalidade removida |
| `tiendas.bgt` | 🗑️ DELETAR | Lógica movida para comandos.nvgt |
| `vehicles.bgt` | 🗑️ DELETAR | Lógica movida para player.nvgt |
| `weather info.bgt` | 🗑️ DELETAR | Lógica movida para clima.nvgt |

---

## 🚀 PRÓXIMAS AÇÕES IMEDIATAS

### **FASE 2: Rede e Autenticação (4-6 horas)**

#### **Passo 1: Deletar arquivos obsoletos de rede (30min)**
```powershell
# Arquivos HTTP que serão substituídos por classe http nativa
Remove-Item downloader.bgt, googletranslateclient.bgt, "weather info.bgt"

# Arquivos obsoletos gerais
Remove-Item GameEngine.bgt, devices.bgt, db.bgt, book.bgt, dialogs.bgt
Remove-Item disableds.bgt, mlists.bgt, speed_stop.bgt, tiendas.bgt, vehicles.bgt
```

#### **Passo 2: Converter net.bgt → net.nvgt (2 horas)**
- [ ] Ler `net.bgt` completo
- [ ] Identificar funções de send/receive
- [ ] Reescrever usando `network` nativa
- [ ] Implementar `send_reliable()`, `send_unreliable()`
- [ ] Implementar loop de eventos `network::request()`

#### **Passo 3: Converter comandos.bgt → comandos.nvgt (2 horas)**
- [ ] Ler `comandos.bgt` completo
- [ ] Identificar comandos do servidor
- [ ] Reescrever processamento de mensagens
- [ ] Integrar com `net.nvgt`

#### **Passo 4: Integrar autenticação (1 hora)**
- [ ] Implementar `send_login_attempt()`
- [ ] Implementar `handle_network_events()`
- [ ] Usar `string_aes_encrypt()` para senha
- [ ] Processar resposta "loggedin"

---

### **FASE 3: Interface de Usuário (3-4 horas)**

#### **Passo 1: Deletar wrappers de menu antigos (10min)**
```powershell
Remove-Item m_pro.bgt, menu.bgt, menu2.bgt, editor.bgt
```

#### **Passo 2: Converter menus específicos (2 horas)**
- [ ] `adminmenu.bgt` → usar `menu.nvgt` nativo
- [ ] `buildermenu.bgt` → usar `menu.nvgt` nativo
- [ ] Implementar com `menu::add_item()` e `menu::run()`

#### **Passo 3: Atualizar client.nvgt para usar menus nativos (1 hora)**
- [ ] Substituir `m.run()` por `menu::run()`
- [ ] Substituir `v.input()` por `input_box()`
- [ ] Testar navegação de menus

---

### **FASE 4: Lógica de Jogo (4-5 horas)**

#### **Passo 1: Converter sistemas de mundo (2 horas)**
- [ ] `zones.bgt` → `zones.nvgt`
- [ ] `safezones.bgt` → `safezones.nvgt`
- [ ] `platforms.bgt` → `platforms.nvgt`

#### **Passo 2: Converter inventário e armas (2 horas)**
- [ ] `inv.bgt` → integrar em `player.nvgt`
- [ ] `weapon.bgt` → integrar em `player.nvgt`
- [ ] `secondary_inventory.bgt` → integrar em `player.nvgt`

#### **Passo 3: Integrar com servidor (1 hora)**
- [ ] Processar mensagens `changemap`, `update_player`
- [ ] Sincronizar estado do mundo
- [ ] Testar comunicação cliente-servidor

---

## 📊 PROGRESSO GERAL

| Fase | Arquivos | Convertidos | Progresso |
|------|----------|-------------|-----------|
| **Fase 1: Áudio** | 7 | 7 | ✅ 100% |
| **Fase 2: Rede** | 5 | 0 | ⏳ 0% |
| **Fase 3: UI** | 8 | 2 | ⏳ 25% |
| **Fase 4: Mundo** | 11 | 6 | 🔄 55% |
| **Auxiliares** | 12 | 10 | ✅ 83% |
| **Deletar** | 11 | 0 | ⏳ 0% |
| **TOTAL** | **54** | **25** | **🔄 46%** |

---

## ✅ CRITÉRIOS DE CONCLUSÃO

### **Fase 2 Completa Quando:**
- [ ] `net.nvgt` compilando sem erros
- [ ] Cliente conecta ao servidor
- [ ] Login funcionando
- [ ] Mensagens enviadas/recebidas

### **Fase 3 Completa Quando:**
- [ ] Todos menus usando `menu.nvgt` nativo
- [ ] Input usando `input_box()` nativo
- [ ] Navegação funcional

### **Fase 4 Completa Quando:**
- [ ] Jogador se move no mapa
- [ ] Sincronização com servidor funciona
- [ ] Inventário funcional
- [ ] Armas funcionais

### **Projeto Completo Quando:**
- [ ] Cliente e servidor se comunicam
- [ ] Gameplay básico funcional
- [ ] Zero erros de compilação
- [ ] Zero dependências BGT

---

**Última atualização:** 5 de outubro de 2025  
**Próxima ação:** Iniciar Fase 2 - Converter net.bgt
