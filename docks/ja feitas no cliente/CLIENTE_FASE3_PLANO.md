# 🎨 CLIENTE - FASE 3: UI/MENUS - PLANO DE AÇÃO

**Data:** 5 de outubro de 2025  
**Status:** 🔄 **EM ANDAMENTO**

---

## 📊 SITUAÇÃO ATUAL

### **Arquivos BGT Existentes**
| Arquivo | Linhas | Status | Ação |
|---------|--------|--------|------|
| `menu.bgt` | 1773 | ⚠️ Parcialmente convertido | Completar conversão |
| `menu.nvgt` | 649 | ✅ 37% convertido | Completar |
| `menu2.bgt` | ? | ❌ Não iniciado | Analisar e converter |
| `adminmenu.bgt` | 240 | ❌ Não iniciado | Converter |
| `buildermenu.bgt` | ? | ❌ Não iniciado | Converter |
| `editor.bgt` | ? | ❌ Não iniciado | Converter |

### **Sistema de Menu Nativo NVGT**
```nvgt
// NVGT tem menu nativo em include/menu.nvgt
class menu {
    void create_window(string title);
    int add_item(string label, string id = "");
    int run(string intro = "", bool wait_for_release = true);
    string get_item_id(int index);
    void set_callback(string event_type, funcdef@ callback);
    void set_intro_text(string text);
}
```

---

## 🎯 ESTRATÉGIA DE CONVERSÃO

### **1. Sistema de Menu BGT → NVGT**

#### **BGT (Antigo):**
```bgt
dynamic_menu_pro m;  // Menu customizado BGT

void setupmenu() {
    m.enable_sound_flag=1;
    m.extra_keys=1;
    // ... configurações
}

m.add_item_tts(pu.get_value("Opção"), "id");
int mres = m.run("Título", true);
if(m.get_item_name(mres) == "id") { /* ação */ }
```

#### **NVGT (Novo):**
```nvgt
menu game_menu;  // Menu nativo NVGT

void menusilent() {
    game_menu = menu();
    // Configurações simplificadas
}

game_menu.add_item(pu.get_value("Opção"), "id");
int selection = game_menu.run();
if(game_menu.get_item_id(selection) == "id") { /* ação */ }
```

### **2. Músicas de Menu**

```nvgt
// Sistema de música de fundo já implementado em menu.nvgt
sound menu_music_sound;

void start_menu_music() {
    string track = "m" + random(1, 8) + ".ogg";
    menu_music_sound.load(track);
    menu_music_sound.volume = menu_volume_to_db();
    menu_music_sound.play_looped();
}

void fade_menu_music(int steps = 30) {
    // Fade out suave
}
```

### **3. Formulários de Entrada**

```nvgt
// NVGT tem input_form nativo
#include "../../include/input_forms.nvgt"

input_form form("Título");
form.add_text_field("username", "Digite usuário:", "", true);
form.add_text_field("password", "Digite senha:", "", true, true);  // true = senha oculta
dictionary@ result = form.run();
```

---

## 📋 TAREFAS DETALHADAS

### **FASE 3.1: Completar menu.nvgt** (1-2 horas)

#### **Funções já implementadas:** ✅
- ✅ `stop_menu_music()`
- ✅ `fade_menu_music()`
- ✅ `start_menu_music()`
- ✅ `ensure_menu_music_volume()`
- ✅ `prompt_login_form()`
- ✅ `menusilent()`

#### **Funções pendentes:** ⏳
- [ ] `main_menu()` - Menu principal
- [ ] `menuupdates()` - Menu de atualizações
- [ ] `reportmenu()` - Menu de relatórios
- [ ] `converter_menu()` - Conversor de moedas
- [ ] `optionsmenu()` - Menu de opções
- [ ] `config_account()` - Configurar conta
- [ ] `testspeaks()` - Teste de alto-falantes
- [ ] `celularmenu()` - Menu do celular
- [ ] `chatmenu()` - Menu de chat
- [ ] `inventarymenu()` - Menu de inventário
- [ ] ... (~30+ funções de menu do menu.bgt)

---

### **FASE 3.2: Converter adminmenu.bgt** (1 hora)

#### **Funções identificadas:**
```nvgt
void adminmenu() {
    // Menu administrativo com opções:
    // - xpespecial, pvp, minas, aviso
    // - ban, mensagens do dia (5 idiomas)
    // - dar créditos, stryx, itens
    // - regalos, sounds, silenciar
    // - audio, langs
}
```

**Conversão:**
```nvgt
void adminmenu() {
    game_menu = menu();
    game_menu.add_item(pu.get_value("ativar/desativar xp especial."), "xpespecial");
    game_menu.add_item(pu.get_value("ativar ou desativar combate."), "pvp");
    // ... adicionar todos os itens
    
    int selection = game_menu.run(pu.get_value("menu do administrador. escolha com cuidado a opção que desejar."));
    string selected_id = game_menu.get_item_id(selection);
    
    if(selected_id == "xpespecial") {
        game_net.send(net_peer_id, encrypt_packet("/xps"), 1, false);
    }
    // ... processar todas as opções
}
```

---

### **FASE 3.3: Converter buildermenu.bgt** (1 hora)

**Análise pendente** - Precisa ler arquivo

---

### **FASE 3.4: Converter menu2.bgt e editor.bgt** (1 hora)

**Análise pendente** - Precisa ler arquivos

---

## 🔄 MUDANÇAS CRÍTICAS BGT → NVGT

### **1. Inicialização de Menu**

```nvgt
// BGT
dynamic_menu_pro m;
void setupmenu() { m.enable_sound_flag=1; /* ... */ }
setupmenu();

// NVGT
menu game_menu;
void menusilent() { game_menu = menu(); }
menusilent();
```

### **2. Adicionar Itens**

```nvgt
// BGT
m.add_item_tts(pu.get_value("Texto"), "id");

// NVGT
game_menu.add_item(pu.get_value("Texto"), "id");
```

### **3. Executar Menu**

```nvgt
// BGT
int mres = m.run(pu.get_value("Título"), true);
if(m.get_item_name(mres) == "id") { /* ação */ }

// NVGT
int selection = game_menu.run(pu.get_value("Título"));
if(game_menu.get_item_id(selection) == "id") { /* ação */ }
```

### **4. Enviar Comandos para Servidor**

```nvgt
// BGT
send_unreliable(event.peer_id, "/comando", 1);
send_reliable(peer_id, "/comando", 0);

// NVGT
game_net.send(net_peer_id, encrypt_packet("/comando"), 1, false);  // unreliable
game_net.send(net_peer_id, encrypt_packet("/comando"), 0, true);   // reliable
```

### **5. Input de Usuário**

```nvgt
// BGT
virtualizer v;
string input = v.input(pu.get_value("Pergunta:"));

// NVGT
audio_form form;
form.create_window("Título", false, true);
form.add_text_field(pu.get_value("Pergunta:"));
string input = form.run_field(0);
```

---

## 🎯 OBJETIVOS DA FASE 3

### **Critérios de Sucesso:**
- [ ] Deletar `menu.bgt`, `menu2.bgt`, `editor.bgt` (obsoletos)
- [ ] Completar `menu.nvgt` com todas as funções
- [ ] Converter `adminmenu.bgt` → `adminmenu.nvgt`
- [ ] Converter `buildermenu.bgt` → `buildermenu.nvgt`
- [ ] Todos os menus usando `menu` nativo do NVGT
- [ ] Música de fundo funcionando
- [ ] Formulários de entrada funcionando
- [ ] Integração com rede (envio de comandos criptografados)

---

## 📈 PROGRESSO ESTIMADO

```
Total de funções de menu: ~50
Já convertidas: ~10 (20%)
Pendentes: ~40 (80%)

Tempo estimado: 3-4 horas
```

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

1. **Ler menu.bgt completo** - Identificar todas as funções
2. **Ler buildermenu.bgt** - Analisar estrutura
3. **Ler menu2.bgt e editor.bgt** - Avaliar necessidade
4. **Implementar funções faltantes em menu.nvgt**
5. **Criar adminmenu.nvgt e buildermenu.nvgt**
6. **Testar menus básicos**
7. **Deletar arquivos BGT obsoletos**

---

**Última atualização:** 5 de outubro de 2025  
**Status:** 🔄 Plano criado - Iniciando implementação
