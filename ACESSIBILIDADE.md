# ♿ GUIA DE ACESSIBILIDADE - AUDIOGAMES PARA DEFICIENTES VISUAIS

## 🎯 BOAS PRÁTICAS IMPLEMENTADAS

### ✅ **1. Detecção Automática de Leitor de Telas**
```angelscript
// globals.nvgt
bool screen_reader_is_running() {
    return screen_reader_detect() != "";
}
```

**Status:** ✅ Implementado corretamente

---

### ✅ **2. Síntese de Fala (TTS)**
```angelscript
// Usar speak() para mensagens importantes
speak("Bem-vindo ao jogo!");
speak("Você foi atingido!");
speak("Nível aumentou para " + nivel);
```

**Status:** ✅ Usando API NVGT nativa

**Recomendações:**
- ⚠️ **NÃO abuse do TTS** - use apenas para eventos importantes
- ✅ **Priorize áudio 3D** - deixe o jogador se orientar pelo som
- ✅ **Use rate control** - ajuste velocidade de fala nas preferências

---

### ✅ **3. Áudio 3D Posicional**
```angelscript
// sound_pool para áudio espacial
sound_pool p;
p.play_2d("passos.ogg", me.x, me.y, outro_x, outro_y, false);
```

**Status:** ✅ Implementado com NVGT sound_pool

**Importância para Deficientes Visuais:**
- 🎧 **Orientação espacial** - jogador sabe onde estão objetos/inimigos
- 🎧 **Navegação** - áudio indica direção do movimento
- 🎧 **Imersão** - experiência mais realista

**Configurações Recomendadas:**
```angelscript
p.max_distance = 30;     // Distância máxima de audição
p.rolloff_factor = 1.0;  // Quão rápido o som diminui com distância
p.doppler_factor = 1.0;  // Efeito Doppler (movimento)
```

---

### ✅ **4. Navegação por Teclado 100%**
```angelscript
// Tudo deve ser acessível por teclado
if(key_pressed(KEY_UP)) move_forward();
if(key_pressed(KEY_SPACE)) jump();
if(key_pressed(KEY_I)) open_inventory();
if(key_pressed(KEY_ESCAPE)) show_menu();
```

**Status:** ✅ Implementado

**Recomendações:**
- ✅ **Nunca exigir mouse** - deficientes visuais não usam mouse
- ✅ **Teclas de atalho claras** - F1=Ajuda, I=Inventário, etc.
- ✅ **Navegação consistente** - sempre as mesmas teclas
- ✅ **Feedback sonoro** - cada ação tem um som

---

### ✅ **5. Menus Acessíveis**
```angelscript
// Usar menu class nativo NVGT
menu game_menu;
game_menu.add_item("Conectar", "1");
game_menu.add_item("Criar Conta", "2");
game_menu.add_item("Opções", "3");
game_menu.intro_text = "Menu Principal";
int selection = game_menu.run();
```

**Status:** ✅ Implementado

**Vantagens:**
- ✅ Compatível com leitores de tela
- ✅ Navegação por setas
- ✅ Som de navegação automático
- ✅ Fala automática dos itens

---

### ✅ **6. Feedback Constante**
```angelscript
// Sempre informar o que está acontecendo
speak("Conectando ao servidor...");
speak("Carregando mapa...");
speak("Aguarde...");
speak("Conectado com sucesso!");
```

**Status:** ✅ Implementado em vários lugares

**Por que é importante:**
- 🔊 Deficiente visual não vê barra de progresso
- 🔊 Precisa saber se o jogo travou ou está processando
- 🔊 Precisa de confirmação de ações

---

### ✅ **7. Orientação Espacial**
```angelscript
// Sistema de coordenadas faladas
void tell_where(int x, int y) {
    if (me.x <= x) {
        godir = "direita";
        go = x - me.x;
    } else {
        godir = "esquerda";
        go = me.x - x;
    }
    if (me.y <= y) {
        godir2 = "acima";
        go2 = y - me.y;
    } else {
        godir2 = "abaixo";
        go2 = me.y - y;
    }
    speak(pu.get_value(godir) + " " + go + " " + pu.get_value("e") + " " + pu.get_value(godir2) + " " + go2);
}
```

**Status:** ✅ Implementado no client.nvgt

**Uso:**
- 📍 Informar localização de objetivos
- 📍 Informar direção de inimigos
- 📍 Ajudar na navegação

---

## 🎨 RECOMENDAÇÕES ADICIONAIS

### 🔴 **CRÍTICO: Evitar Barreiras Visuais**

#### ❌ **NÃO FAÇA:**
```angelscript
// ERRADO: Captcha visual
if(!solve_captcha()) return;

// ERRADO: Cor como única informação
if(vida < 20) set_color("red");  // Deficiente visual não vê cor!

// ERRADO: Minimapa visual
draw_minimap();  // Inútil para deficientes visuais
```

#### ✅ **FAÇA:**
```angelscript
// CERTO: Captcha sonoro
if(!solve_audio_captcha()) return;

// CERTO: Som + fala para vida baixa
if(vida < 20) {
    play_sound("heartbeat.ogg", true);  // Loop de batimento cardíaco
    speak("Vida crítica!");
}

// CERTO: Áudio 3D em vez de minimapa
// O jogador ouve onde estão os inimigos pela posição do som
```

---

### 🟡 **IMPORTANTE: Customização**

#### **Permitir Personalização:**
```angelscript
// Preferências de acessibilidade
int ouvirhits = 1;        // Ouvir sons de acertos
int ouvirpassos = 1;      // Ouvir passos de outros jogadores
int ouvirmortes = 1;      // Ouvir notificações de mortes
int beaconing = 0;        // Beacon de orientação
double volumejogo = 0;    // Volume master
int ttsrate = 0;          // Velocidade do TTS
```

**Status:** ✅ Já implementado!

**Recomendação:** Adicionar mais opções:
```angelscript
int audio3d_enabled = 1;     // Habilitar áudio 3D
int reverb_enabled = 1;      // Reverberação para ambientes
int footsteps_volume = 100;  // Volume dos passos
int combat_volume = 100;     // Volume de combate
int ambient_volume = 50;     // Volume ambiente
int music_volume = 30;       // Volume da música
```

---

### 🟢 **BOM TER: Tutoriais Interativos**

#### **Tutorial Acessível:**
```angelscript
void tutorial() {
    speak("Bem-vindo ao tutorial! Vou ensinar os controles básicos.");
    wait(2000);
    
    speak("Use as setas ou WASD para se mover. Tente andar para frente.");
    wait_for_key(KEY_UP);
    speak("Muito bem! Agora ande para trás.");
    wait_for_key(KEY_DOWN);
    
    speak("Pressione I para abrir o inventário.");
    wait_for_key(KEY_I);
    speak("Este é o seu inventário. Use setas para navegar e Enter para selecionar.");
    
    speak("Tutorial concluído! Boa sorte no jogo!");
}
```

**Status:** ⏳ Não implementado

**Benefício:** 
- Reduz curva de aprendizado
- Jogadores novatos entendem rapidamente
- Menos perguntas no suporte

---

### 🟢 **BOM TER: Beacon System**

#### **Sistema de Orientação:**
```angelscript
// Beacon para encontrar objetivos
void beacon_to(int target_x, int target_y) {
    timer beacon_timer;
    sound beacon_sound;
    beacon_sound.load("beacon.ogg");
    
    while(me.x != target_x || me.y != target_y) {
        if(beacon_timer.elapsed >= 1000) {
            // Tocar beacon na direção do objetivo
            p.play_2d("beacon.ogg", me.x, me.y, target_x, target_y, false);
            beacon_timer.restart();
        }
        wait(5);
    }
    
    speak("Objetivo alcançado!");
}
```

**Status:** ✅ Parcialmente implementado (`beaconing` nas preferências)

**Uso:**
- 🎯 Encontrar NPCs importantes
- 🎯 Navegar para lojas
- 🎯 Completar missões
- 🎯 Encontrar outros jogadores

---

## 🔊 DESIGN DE ÁUDIO PARA DEFICIENTES VISUAIS

### **Princípios Fundamentais:**

#### 1. **Camadas de Áudio**
```angelscript
// Layer 1: Ambiente (constante, baixo volume)
sound_pool ambient;
ambient.play_looped("rain.ogg", me.x, me.y, 0, 0, true);

// Layer 2: Objetos (periódico, médio volume)
sound_pool objects;
objects.play_2d("fire.ogg", me.x, me.y, fire_x, fire_y, true);

// Layer 3: Ações (momentâneo, alto volume)
sound_pool actions;
actions.play_stationary("sword_swing.ogg", false);

// Layer 4: Feedback (imediato, alto volume)
speak("Você acertou o inimigo!");
```

#### 2. **Distinção Clara de Sons**
```angelscript
// Cada tipo de entidade tem som único
// ❌ ERRADO: Todos os inimigos fazem o mesmo som
play_sound("enemy.ogg");

// ✅ CERTO: Cada inimigo tem som característico
if(enemy.type == "zombie") play_sound("zombie_groan.ogg");
if(enemy.type == "skeleton") play_sound("bones_rattle.ogg");
if(enemy.type == "dragon") play_sound("dragon_roar.ogg");
```

#### 3. **Hierarquia de Importância**
```angelscript
// Eventos mais importantes têm prioridade
enum SoundPriority {
    LOW = 0,      // Ambiente, passos distantes
    NORMAL = 1,   // Ações do jogador
    HIGH = 2,     // Combate, inimigos próximos
    CRITICAL = 3  // Vida baixa, alertas
}

// Implementar sistema de prioridade
void play_prioritized_sound(string filename, int priority) {
    if(priority >= CRITICAL) {
        // Interromper outros sons se necessário
        stop_low_priority_sounds();
    }
    play_sound(filename);
}
```

#### 4. **Feedback Tátil Auditivo**
```angelscript
// Som que simula tato
void play_surface_sound(string surface) {
    if(surface == "wood") {
        play_sound("footstep_wood.ogg");
    } else if(surface == "metal") {
        play_sound("footstep_metal.ogg");
    } else if(surface == "grass") {
        play_sound("footstep_grass.ogg");
    }
    // Jogador "sente" o chão pelos sons
}
```

---

## 📚 RECURSOS DE ACESSIBILIDADE NO CÓDIGO

### **Arquivo: `cliente/includes/globals.nvgt`**
```angelscript
// ✅ Boa implementação
bool screen_reader_is_running() {
    return screen_reader_detect() != "";
}

// ✅ Detecção automática
if(screen_reader_is_running()) {
    install_keyhook();  // Captura teclas para leitores de tela
}
```

### **Arquivo: `cliente/includes/net.nvgt`**
```angelscript
// ✅ Feedback constante
speak(pu.get_value("Conectando ao servidor..."));
speak(pu.get_value("Logado com sucesso! Entrando no jogo..."));
```

### **Arquivo: `cliente/client.nvgt`**
```angelscript
// ✅ Áudio 3D implementado
p.max_distance = 30;
p.play_2d("passos.ogg", me.x, me.y, player_x, player_y, false);
```

---

## 🎯 CHECKLIST DE ACESSIBILIDADE

### ✅ **Implementado**
- [x] Detecção automática de leitor de telas
- [x] Síntese de fala (TTS)
- [x] Áudio 3D posicional
- [x] Navegação 100% por teclado
- [x] Menus acessíveis
- [x] Feedback sonoro de ações
- [x] Orientação espacial por coordenadas
- [x] Preferências de áudio customizáveis
- [x] Suporte a múltiplos leitores de tela (NVDA, JAWS, Narrator)

### ⏳ **A Implementar**
- [ ] Tutorial interativo acessível
- [ ] Sistema de beacon aprimorado
- [ ] Descrições detalhadas de ambientes
- [ ] Mapa tátil auditivo
- [ ] Sistema de waypoints sonoros
- [ ] Alertas de perigo por áudio
- [ ] Perfis de acessibilidade pré-definidos
- [ ] Legendas para sons (para surdos que usam leitores de tela)

### ⚠️ **Atenção Especial**
- [ ] Testar com usuários reais deficientes visuais
- [ ] Verificar compatibilidade com TODOS os leitores de tela
- [ ] Garantir que NENHUMA funcionalidade requer visão
- [ ] Adicionar atalhos de teclado para tudo
- [ ] Documentar todos os controles em áudio

---

## 🏆 PADRÕES OURO DE AUDIOGAMES

### **Exemplos de Jogos Acessíveis:**
1. **A Hero's Call** - RPG com áudio 3D excepcional
2. **Swamp** - FPS com orientação sonora perfeita
3. **Manamon** - RPG acessível similar a Pokémon
4. **Alter Aeon** - MUD com ótima acessibilidade

### **O que eles fazem certo:**
- 🏆 Zero dependência de visão
- 🏆 Áudio 3D de alta qualidade
- 🏆 Controles intuitivos
- 🏆 Feedback constante e claro
- 🏆 Documentação em áudio
- 🏆 Comunidade inclusiva

---

## 💬 LINGUAGEM INCLUSIVA

### ✅ **Fazer:**
- "Jogador" (neutro)
- "Pessoa deficiente visual"
- "Usuário de leitor de telas"
- "Acessível"

### ❌ **Evitar:**
- "Cego" (a menos que a pessoa prefira)
- "Portador de deficiência"
- "Pessoa com necessidades especiais"
- "Deficiente" (sozinho, sem contexto)

---

## 🎉 CONCLUSÃO

**Seu projeto já tem uma EXCELENTE base de acessibilidade!** 

**Pontos Fortes:**
- ✅ Áudio 3D bem implementado
- ✅ Detecção de leitores de tela
- ✅ Controles por teclado
- ✅ Feedback sonoro

**Próximos Passos:**
1. Testar com usuários deficientes visuais reais
2. Adicionar tutorial interativo
3. Melhorar sistema de beacon
4. Documentar todos os controles em áudio

**Continue com o ótimo trabalho! ♿🎮🎧**

---

*Desenvolvido por: GitHub Copilot*  
*Especializado em: Acessibilidade, AudioGames, Deficiência Visual*
