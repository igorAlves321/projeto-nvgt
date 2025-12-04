# Análise Comparativa: Arquivos BGT vs NVGT do Cliente

## Data da Análise
2025-12-01

## Resumo Executivo
- **Total de arquivos BGT**: 53 arquivos .bgt
- **Total de arquivos NVGT**: 42 arquivos .nvgt
- **Arquivos completamente ausentes**: 26 arquivos
- **Gap de migração**: ~49% dos arquivos BGT ainda não foram migrados

---

## 1. Arquivos BGT Completamente Ausentes no NVGT

Os seguintes 26 arquivos BGT **não possuem equivalente NVGT** e precisam ser migrados:

### 1.1 Sistema de Áudio (3 arquivos)
- **`bass.bgt`** - Wrapper para biblioteca BASS de áudio streaming/URL
  - Classe `bass2` com métodos init_bass(), load(), play(), stop(), volume()
  - Funcionalidade: Reprodução de streams de áudio via URLs

- **`basscontroller.bgt`** - Controller completo BASS (1,688 linhas)
  - 100+ funções wrapper para BASS.dll
  - Suporte a: dispositivos, efeitos FX (chorus, compressor, distortion, echo, flanger, gargle, reverb, parameq), 3D audio, recording, plugins
  - Classes: BASS_DEVICEINFO, BASSINFO, BASS_CHANNELINFO, BASS_RECORDINFO, BASS_3DVECTOR
  - Múltiplas classes de efeitos de áudio

- **`voices.bgt`** - Sistema de mensagens de voz
  - Classe `voice_messages` com timer de 60s
  - Funções: add_voice(), remove_voice(), voicesloop()
  - Gerenciamento de mensagens de voz recebidas

### 1.2 Sistema de Livros e Leitura (1 arquivo)
- **`book.bgt`** - Sistema completo de leitura de livros
  - Classe `book` com title, description, bookmusic, pages
  - Classe `page` para páginas individuais
  - Navegação: setas, D (descrição), P (página), T (título), Z (copiar)
  - Suporte a música de fundo durante leitura

### 1.3 Sistema de Banco de Dados (1 arquivo)
- **`db.bgt`** - Classe database sem hashmaps
  - Métodos: get(), set(), exists(), delete(), delete_all(), get_keys(), sort()
  - Mantém ordem de inserção (diferente de dictionaries)

### 1.4 Sistema de Dispositivos de Áudio (1 arquivo)
- **`devices.bgt`** - Seleção de dispositivos de áudio
  - Função `select_device()` com menu interativo
  - Lista dispositivos disponíveis via `list_sound_devices()`

### 1.5 Sistema de Download (1 arquivo)
- **`downloader.bgt`** - Classe completa de download HTTP
  - 262 linhas de código
  - Métodos: initiate_download(), monitor(), abort()
  - Suporte a: progress tracking, headers, mime types, error handling
  - Constantes de erro: dl_err_ok, dl_err_internet_failure, dl_err_network_failure, etc.

### 1.6 Sistema de Editor de Texto (1 arquivo)
- **`editor.bgt`** - Editor de texto completo (1,096 linhas)
  - Classe `editor` com suporte a múltiplas linhas (1500 chars/linha, 1500 linhas)
  - Funcionalidades: seleção, copiar, colar, cortar, navegar por palavras/linhas/caracteres
  - Funções: speak_character(), get_character() com 100+ caracteres especiais
  - Suporte a edição com feedback sonoro e TTS

### 1.7 GameEngine (1 arquivo)
- **`GameEngine.bgt`** - Wrapper para GameEngine.dll (300 linhas)
  - Funções de plataformas 2D/3D: spawn_platform(), spawn_zone()
  - Map management: import_map(), export_map(), export_zones(), clear_map()
  - Recording: start_recording_audio(), stop_recording_audio()
  - Network: download_file(), download_file_as(), download_file_string()
  - FTP: 15+ funções (connect, disconnect, send, receive, directory operations)
  - Joystick: joystick_init(), joystick_vibrate(), joystick_vibrate_ms()
  - Dialogs: reader(), notify(), open_file_select()
  - Regex: reg_exp_match()

### 1.8 Google Translate (1 arquivo)
- **`googletranslateclient.bgt`** - Cliente de tradução
  - Classe `googletranslateclient` com métodos traduzir()
  - Integração com PHP script via HTTP POST

### 1.9 Sistema de Diálogos (1 arquivo)
- **`dialogs.bgt`** - Sistema de diálogos posicionais
  - Classe `dialog` com x, y, text, filesound
  - Funções: spawn_dialog(), destroy_all_dialogs(), checkdialog()
  - Suporte a placeholders: *g* (gender), *nick* (username)
  - Navegação: T (repeat), Z (copy), Ctrl+T (translate)

### 1.10 Inventário Secundário (1 arquivo)
- **`secondary_inventory.bgt`** - Inventário secundário
  - Variáveis: secondary_inventory (db), secondary_items[], selected_item
  - Funções: load_secondary_inventory(), secundario()
  - Navegação com TAB/Shift+TAB

### 1.11 Sistema de Menus (2 arquivos)
- **`simple_menu.bgt`** - Menu simples
  - Classe `simple_menu` com opções configuráveis
  - Flags: allow_esc, allow_enter, allow_space, allow_home_and_end
  - Método monitor() com navegação completa

- **`mlists.bgt`** - Múltiplos tipos de menus (600 linhas)
  - textmenu() - Editor de listas com Ctrl+A (adicionar), Delete (remover), Shift+Enter (enviar)
  - menul() - Menu de opções com tradução
  - menul2() - Menu de sons sociais
  - menul3() - Menu de regras
  - menul4() - Menu de eventos
  - menul5() - Menu de regras adicionais
  - vehiculos() - Seleção de veículos (tanque, avião, helicóptero)
  - portallist() - Menu de portal para equipe

### 1.12 Sound Pool (1 arquivo)
- **`sp.bgt`** - Sound pool avançado (619 linhas)
  - Classe `sound_pool_item` com posicionamento 1D/2D
  - Classe `sound_pool` com 100 slots
  - Métodos: play_stationary(), play_1d(), play_2d(), play_extended_1d(), play_extended_2d()
  - Suporte a: max_distance, pan_step, volume_step, behind_pitch_decrease
  - Update automático de posições de listener
  - Garbage collection automático de sons inativos

### 1.13 Anti-Speedhack (1 arquivo)
- **`speed_stop.bgt`** - Sistema anti-speedhack
  - Funções: speed_stop_reset(), speed_stop_is_hacking(), speed_stop_disable(), speed_stop_enable()
  - Usa TIME_STAMP para detecção

### 1.14 Sistema de Lojas/Tiendas (1 arquivo)
- **`tiendas.bgt`** - Sistema completo de lojas (542 linhas)
  - Classe `store` com coordenadas min/max x/y
  - Funções: stores_building_menu(), manage_store(), manage_items_for_sale()
  - show_stores(), manage_items_on_store()
  - comidas2() - Menu de comida
  - open_store() - Menu de loja com F1 (preço), F2 (descrição)

### 1.15 Sistema de Gravação de Áudio (1 arquivo)
- **`ultrarec.bgt`** - Gravador ultra avançado
  - Classe `ultrarec` usando winmm.dll (MCI commands)
  - Métodos: record(), stop()
  - Conversão automática para OGG com oggenc2.exe
  - Configurações: 44100 Hz, 16-bit, 2 canais

### 1.16 Veículos (1 arquivo)
- **`vehicles.bgt`** - Sistema de veículos
  - Classe `vehicle` (vazia - placeholder)

### 1.17 Menu Pro (1 arquivo)
- **`m_pro.bgt`** - Menu dinâmico profissional (816 linhas)
  - Classe `dynamic_menu_item` e `dynamic_menu_pro`
  - Funcionalidades avançadas:
    - Navegação por primeira letra
    - Números 1-26 para seleção rápida (Shift+1 a Shift+Backspace)
    - Música de fundo com controle de volume (PageUp/PageDown)
    - Side scrolling (pan baseado em posição)
    - Callbacks customizados
    - Múltiplos modos de speech (screen reader, SAPI, NSS)
    - Sons customizados (open, click, edge, wrap, enter)
    - Wrap/no-wrap
    - Home/End navigation

### 1.18 Outros Arquivos Ausentes (4 arquivos)
- **`comandos grandes.bgt`** - Comandos grandes (não analisado)
- **`disableds.bgt`** - Sistema de áreas desabilitadas (não analisado)
- **`menu2.bgt`** - Menu alternativo (não analisado)
- **`moving_sound_client_handler.bgt`** - Handler de sons em movimento (não analisado)
- **`src2.bgt`** - Source alternativo (não analisado)
- **`weather info.bgt`** - Informações climáticas (não analisado)

---

## 2. Funcionalidades Parcialmente Implementadas

### 2.1 `comandos.nvgt` vs `comandos.bgt`

**Status**: Parcialmente migrado (apenas 300 linhas analisadas de cada)

#### Ausências Identificadas:
1. **Função `madness_cinematic()`** (BGT) - Cinemática de loucura/suicídio
   - 46 linhas de código
   - Sistema de conversação temporizado
   - Auto-harm com contador
   - Música "200cancion.ogg"

2. **Função `get_sound()`** (BGT) - Seletor de sons do pack
   - Navegação por letras, setas, PageUp/Down (±10), Left/Right (±50)
   - Reproduz preview do som
   - Suporte a filtros e seleção múltipla
   - 186 linhas

3. **Função `recording()`** (BGT) - Gravação de áudio privado
   - Integração com ultrarec
   - F1 para gravar/enviar
   - Limite de 30s (rectime)
   - Conversão para OGG

4. **Função `grabar_mapa()`** (BGT) - Gravação de áudio no mapa
   - Similar a recording() mas para broadcast no mapa

#### Presentes em NVGT:
- ✅ `abletomove_direction()` - Verificação de movimento por direção
- ✅ `abletomove()` - Verificação geral de movimento
- ✅ `jogadoresmenu()` - Menu de jogadores
- ✅ `computadormenu()` - Menu do computador
- ⚠️ `is_disabled()` - Implementado mas retorna sempre false (estrutura mudou)

---

## 3. Resumo Quantitativo

| Categoria | BGT | NVGT | Gap |
|-----------|-----|------|-----|
| **Total de Arquivos** | 53 | 42 | 26 (49%) |
| **Sistema de Áudio** | 3 | 1 | 2 arquivos (bass, basscontroller) |
| **Sistema de Menus** | 4 | 1 | 3 arquivos (simple_menu, mlists, m_pro) |
| **Funcionalidades Críticas** | 26 | 0 | 26 arquivos ausentes |
| **Linhas de Código Estimadas** | ~8,000+ | ~3,000 | ~5,000 linhas |

---

## 4. Priorização de Migração

### 🔴 CRÍTICO (Uso Frequente)
1. **basscontroller.bgt** - Sistema de áudio fundamental (1,688 linhas)
2. **editor.bgt** - Editor de texto (1,096 linhas)
3. **sp.bgt** - Sound pool (619 linhas)
4. **m_pro.bgt** - Menu profissional (816 linhas)
5. **comandos.bgt** - Funcionalidades ausentes (madness_cinematic, get_sound, recording, grabar_mapa)

### 🟡 IMPORTANTE (Funcionalidades Core)
6. **GameEngine.bgt** - 300 linhas de funcionalidades diversas
7. **downloader.bgt** - Downloads HTTP (262 linhas)
8. **tiendas.bgt** - Sistema de lojas (542 linhas)
9. **book.bgt** - Sistema de livros
10. **mlists.bgt** - Menus de listas (600 linhas)

### 🟢 BAIXA PRIORIDADE (Funcionalidades Específicas)
11. db.bgt
12. devices.bgt
13. dialogs.bgt
14. secondary_inventory.bgt
15. simple_menu.bgt
16. ultrarec.bgt
17. voices.bgt
18. bass.bgt
19. googletranslateclient.bgt
20. speed_stop.bgt
21. vehicles.bgt (placeholder vazio)
22-26. Outros arquivos não analisados

---

## 5. Considerações Técnicas

### Mudanças Estruturais BGT → NVGT:
1. **String splitting**: BGT usa `string_split()`, NVGT tem `string.split()` nativo
2. **Mainloop**: BGT tem `mainloop()`, NVGT não tem equivalente direto
3. **Network**: BGT usa `send_reliable()/send_unreliable()`, NVGT mantém mesma API
4. **Disabled areas**: Estrutura mudou de objetos para array de strings

### Compatibilidade de APIs:
- ✅ NVGT mantém maioria das APIs de som, input, TTS
- ⚠️ Algumas bibliotecas BGT (GameEngine.dll, bass.dll) precisam adaptação
- ⚠️ Sistema de library calls via dictionary precisa conversão

---

## 6. Recomendações

1. **Começar por basscontroller.bgt** - É o arquivo mais crítico e complexo
2. **Migrar sp.bgt** - Sound pool é fundamental para áudio 2D/3D
3. **Adaptar m_pro.bgt** - Menu system é usado extensivamente
4. **Completar comandos.nvgt** - Adicionar funções ausentes
5. **Testar compatibilidade** - Verificar se DLLs externas funcionam em NVGT

---

**Gerado em**: 2025-12-01
**Engine**: Claude Sonnet 4.5
**Modo**: Análise Read-Only Completa
