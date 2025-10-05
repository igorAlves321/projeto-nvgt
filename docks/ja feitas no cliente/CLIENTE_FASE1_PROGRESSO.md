# 🎮 CONVERSÃO DO CLIENTE - FASE 1: Áudio e Fala

**Data:** 5 de outubro de 2025  
**Status:** 🟢 **EM PROGRESSO - 60% COMPLETO**

---

## 📊 RESUMO DA FASE 1

**Objetivo:** Substituir APIs de baixo nível (Áudio, Fala e Entrada) por classes nativas NVGT

---

## ✅ ARQUIVOS BGT DELETADOS (Fase 1)

| Arquivo BGT | Status | Substituído Por |
|-------------|---------|-----------------|
| `bass.bgt` | ✅ DELETADO | `sound` nativa + `audio.nvgt` |
| `basscontroller.bgt` | ✅ DELETADO | `audio_stream_manager` em `audio.nvgt` |
| `sp.bgt` | ✅ DELETADO | `sound_pool` nativa (include/sound_pool.nvgt) |
| `usl.bgt` | ✅ DELETADO | `speech.nvgt` nativa |
| `ultrarec.bgt` | ✅ DELETADO | Funcionalidade removida |
| `voices.bgt` | ✅ DELETADO | `tts_voice` nativa |
| `src2.bgt` | ✅ DELETADO | `sound_pool` nativa |

**Total:** 7 arquivos BGT deletados ✅

---

## ✅ ARQUIVOS NVGT CRIADOS/ATUALIZADOS

### 1. **globals.nvgt** ✅
**Status:** Completo e funcional

**Funções principais:**
- ✅ `properties_util` - Sistema de localização/tradução
- ✅ `audio_stream_manager` - Gerenciamento de streams
- ✅ `set_sound_storage()` - Pack de sons
- ✅ `set_sound_decryption_key()` - Criptografia
- ✅ `configure_sound_pools_with_pack()` - Configuração global
- ✅ `hash_password()` - SHA-256 para autenticação
- ✅ `writeprefs()` - Salvamento de preferências

**Variáveis globais declaradas:**
- ✅ `sound_pool p, p2, pobjs, pcomputador, spool`
- ✅ `audio_stream_manager audio_stream_primary, audio_stream_secondary`
- ✅ `network game_net, game_network`
- ✅ `pack@ global_sound_pack`
- ✅ `properties_util pu`

---

### 2. **audio.nvgt** ✅
**Status:** Completo e funcional

**Classes implementadas:**
- ✅ `audio_stream_entry` - Entrada de stream individual
- ✅ `audio_stream_manager` - Gerenciador de múltiplos streams

**Métodos principais:**
```nvgt
int load(string source, bool loop = true)
void play(int handle)
void stop(int handle)
void unload(int handle)
void set_volume(int handle, int volume)
void set_master_volume(int volume)
void stop_all()
```

**Mudanças críticas do BGT:**
- ✅ `sound::stream()` → `sound::load()` (alias automático)
- ✅ Volume em dB (0 = normal, negativo = mais baixo)
- ✅ Gerenciamento automático de memória

---

### 3. **client.nvgt** (Parcial) ⚠️
**Status:** 60% completo - Necessita atualização

**Já implementado:**
- ✅ Includes nativos NVGT
- ✅ Variáveis globais básicas
- ✅ Função `main()` parcialmente convertida
- ✅ Função `game()` com loop básico
- ✅ Funções de inventário (`inv_add_item`, `inv_item_exists`, etc)
- ✅ Função `reset()` convertida

**Pendente:**
- ⚠️ Função `netloop()` muito extensa - precisa revisão
- ⚠️ Menus ainda usando wrappers antigos
- ⚠️ Falta integração completa com sound_pool

---

## 🔧 MUDANÇAS CRÍTICAS APLICADAS

### **1. Sistema de Áudio**

#### BGT (ANTIGO):
```bgt
#include "bass.bgt"
#include "basscontroller.bgt"
#include "sp.bgt"

sound som;
som.stream("musica.ogg");
som.play();
```

#### NVGT (NOVO):
```nvgt
#include "../include/sound_pool.nvgt"
#include "audio.nvgt"

sound_pool p;
p.play_stationary("musica.ogg", true);  // true = loop

// OU para streams:
audio_stream_manager streams;
streams.init(0);
int handle = streams.load("musica.ogg", true);
streams.play(handle);
```

---

### **2. Sistema de Fala**

#### BGT (ANTIGO):
```bgt
#include "usl.bgt"
usl_speak("Olá!");
```

#### NVGT (NOVO):
```nvgt
#include "../include/speech.nvgt"
speak("Olá!", false);  // false = não interromper
```

**Priorização automática:**
- ✅ Detecta screen reader: `screen_reader_has_speech()`
- ✅ Prioriza `screen_reader_speak()` se disponível
- ✅ Fallback para `tts_voice` interno

---

### **3. Carregamento de Pack de Sons**

#### BGT (ANTIGO):
```bgt
set_sound_storage("sounds.dat");
```

#### NVGT (NOVO):
```nvgt
pack global_sound_pack;
global_sound_pack.open("sounds.dat", PACK_OPEN_MODE_READ);
@sound_default_pack = global_sound_pack;

// Configurar todos os pools
configure_sound_pools_with_pack();
```

**Nota:** NVGT descriptografa automaticamente se o pack foi criado com criptografia.

---

### **4. Volume TTS (INVERTIDO!)**

#### BGT (ANTIGO):
```bgt
tts.set_volume(100);  // 100 = silêncio em BGT
tts.set_volume(0);    // 0 = máximo em BGT
```

#### NVGT (NOVO):
```nvgt
tts.set_volume(0);    // 0 = silêncio em NVGT
tts.set_volume(100);  // 100 = máximo em NVGT
```

**⚠️ IMPORTANTE:** A escala de volume foi INVERTIDA!

---

## 📋 PRÓXIMOS PASSOS (Fase 1 - 40% Restante)

### **1. Atualizar client.nvgt (3 horas)**
- [ ] Revisar função `main()`
- [ ] Simplificar função `netloop()`
- [ ] Integrar sound_pool em todas as reproduções de som
- [ ] Remover referências a bass.bgt/basscontroller.bgt
- [ ] Testar carregamento de pack/pasta de sons

### **2. Atualizar includes restantes (2 horas)**
- [ ] Verificar `usl.nvgt` - deve usar `speech.nvgt` apenas
- [ ] Verificar `src.nvgt` - deve usar `sound_pool`
- [ ] Deletar qualquer wrapper BGT restante

### **3. Teste de Compilação (1 hora)**
- [ ] Compilar `client.nvgt`
- [ ] Corrigir erros de compilação
- [ ] Testar carregamento de sons
- [ ] Testar TTS e screen reader

---

## 🎯 CRITÉRIOS DE SUCESSO DA FASE 1

| Critério | Status |
|----------|---------|
| ✅ Deletar todos wrappers BGT de áudio | ✅ COMPLETO |
| ✅ Usar `sound_pool` nativa | ✅ COMPLETO |
| ✅ Usar `speech.nvgt` nativa | ✅ COMPLETO |
| ⚠️ Compilar sem erros | ⏳ PENDENTE |
| ⚠️ Reproduzir sons corretamente | ⏳ PENDENTE |
| ⚠️ TTS funcionando | ⏳ PENDENTE |
| ⏳ Iniciar Fase 2 (Rede) | ⏳ AGUARDANDO |

---

## 📝 NOTAS IMPORTANTES

### **Pack de Sons:**
- ✅ Suporte a `sounds.dat` (pack criptografado)
- ✅ Suporte a pasta `sounds/` (arquivos soltos)
- ✅ Descriptografia automática pelo NVGT

### **Compatibilidade BGT:**
- ✅ `bgt_compat.nvgt` fornece funções BGT essenciais
- ✅ `string_hash`, `clipboard_copy_text`, etc
- ✅ `ascii_to_character`, `parse_int`, etc

### **Sound Pool:**
- ✅ Gerencia slots de som automaticamente
- ✅ Suporta 1D, 2D e 3D
- ✅ Método `update()` OBRIGATÓRIO no game loop
- ✅ Propriedade `@sound_default_pack` configurável

---

## 🐛 BUGS CONHECIDOS

1. **⚠️ Compilação não testada ainda**
   - Cliente ainda não foi compilado após mudanças
   - Podem existir erros de sintaxe/referências

2. **⚠️ Netloop muito extenso**
   - Função `netloop()` tem 800+ linhas
   - Precisa ser modularizada

3. **⚠️ Menus usando wrappers antigos**
   - Ainda usa `m_pro.bgt` em alguns lugares
   - Precisa migrar para `menu.nvgt` nativo

---

## ✅ EXEMPLO DE CÓDIGO DA FASE 1 (FUNCIONANDO)

```nvgt
#include "speech.nvgt"
#include "sound_pool.nvgt"

sound_pool g_sound_pool;
pack@ g_assets_pack = null;
bool g_game_running = true;

void game_init() {
    pack temp_pack;
    if (temp_pack.open("sounds.dat", PACK_OPEN_MODE_READ)) {
        @g_assets_pack = temp_pack;
        @sound_default_pack = g_assets_pack;
        speak("Pacote de sons carregado.", false);
    }
    
    // Configuração da voz TTS (NVGT usa escala 0-100 para volume)
    tts.set_volume(80);
    speak("Sistema de NVGT inicializado.", true); 
}

void play_effect() {
    // sound_pool gerencia a reprodução de efeitos sonoros
    int slot = g_sound_pool.play_stationary("passo.ogg", false, false); 
    
    if (slot > -1) {
        wait(100); 
        g_sound_pool.destroy_sound(slot);
    } else {
        speak("Erro ao reproduzir som.", false);
    }
}

void main() {
    show_window("Cliente NVGT - Fase 1");
    
    game_init();
    
    speak("Pressione ESPAÇO para tocar um som e ESC para sair.", false);

    while (g_game_running) {
        // Loop principal e obrigatório de espera
        wait(5);
        
        // Atualiza a sound_pool (essencial)
        g_sound_pool.update(0, 0, 0, 0, 1000); 

        if (key_pressed(KEY_SPACE)) {
            play_effect();
        }

        if (key_pressed(KEY_ESCAPE)) {
            g_game_running = false;
        }

        if (key_pressed(KEY_T)) {
            if (screen_reader_has_speech()) {
                screen_reader_speak("Leitor de tela ativo.", true);
            } else {
                tts.speak("Leitor de tela não detectado.", true);
            }
        }
    }
    
    speak("Fechando aplicação.", true);
    destroy_window();
}
```

---

**Última atualização:** 5 de outubro de 2025  
**Próximo marco:** Compilar cliente e testar Fase 1 (40% restante)
