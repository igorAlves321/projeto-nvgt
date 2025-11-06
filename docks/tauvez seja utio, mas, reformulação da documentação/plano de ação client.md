Plano de Ação: Conversão do Cliente de BGT para NVGT
Este plano detalha o passo a passo para converter o cliente de BGT para NVGT, aproveitando as APIs, bibliotecas e funções internas da linguagem NVGT. A lógica e a estruturação dos arquivos BGT servirão como base, enquanto o NVGT será a linguagem e o framework de implementação principal. Muitos exemplos de código pode ser encontrados em include dentro de docks, A quilo que já tiver implementado, veja se ta correto e já feito

 Fase 1: Substituição das APIs de Baixo Nível (Áudio, Fala e Entrada)
Objetivo: Eliminar dependências de wrappers BGT e migrar completamente para as classes nativas do NVGT, promovendo uma base de código mais limpa e eficiente.
Arquivos BGT a Serem Substituídos/Alterados nesta Fase:
• 
Áudio: bass.bgt, basscontroller.bgt, sp.bgt, ambiente.bgt, src.bgt, src2.bgt.
• 
Fala/Acessibilidade: usl.bgt.
• 
Utilitários de Áudio: ultrarec.bgt, voices.bgt.
1. Subsistema de Áudio (Core e Gerenciamento de Sons)
Ação Necessária
Detalhes e Correção Crítica do NVGT
Substituir Wrappers BASS
Remova todos os wrappers manuais (bass.bgt, basscontroller.bgt). A funcionalidade de áudio é agora encapsulada na classe sound e em includes de alto nível, embora o NVGT use BASS internamente no momento.
Gerenciamento de Sound Pool
Substitua sp.bgt pela classe sound_pool nativa do NVGT (disponível via sound_pool.nvgt). Esta classe replica a gestão de sons 1D, 2D e 3D, mantendo a lógica de reutilização de slots de som.
Carregamento de Sons (Terminologia)
Altere todas as chamadas sound::stream() para sound::load(). No NVGT, stream() é apenas um alias para load(), e load() gerencia o streaming e pré-carregamento de forma mais eficiente.
Definição de Pacotes Padrão
Se o BGT usava set_sound_storage(), migre para a propriedade global @sound_default_pack. Atribua a ela uma referência para um objeto pack aberto para definir de onde os sons devem ser carregados por padrão.
2. Subsistema de Fala e Acessibilidade
Ação Necessária
Detalhes e Correção Crítica do NVGT
Substituir USL
Remova usl.bgt e utilize o include speech.nvgt. O NVGT usa a função speak() de alto nível.
Prioridade de Saída de Voz
A função speak() do NVGT verifica automaticamente se um leitor de tela está disponível (screen_reader_has_speech()) e, se ativado, prioriza o uso de screen_reader_speak() para acessibilidade nativa, antes de recorrer à voz TTS interna (tts_voice).
Ajuste de Volume TTS
Atenção: Se estiver interagindo diretamente com a classe tts_voice (Texto para Fala), o NVGT inverte a escala de volume do BGT: 0 é silencioso e 100 é o máximo.
Exemplo de Código da Fase 1:
#include "bgt_compat.nvgt"
#include "speech.nvgt"
#include "sound_pool.nvgt"

#pragma embed game_assets.pack

sound_pool g_sound_pool;
pack@ g_assets_pack = null;
bool g_game_running = true;

void game_init() {
    pack temp_pack;
    if (temp_pack.open("game_assets.pack", PACK_OPEN_MODE_READ)) {
        @g_assets_pack = temp_pack;
        @sound_default_pack = g_assets_pack;
        speak("Pacote de ativos carregado e definido como padrão.", false);
    } else {
        speak("Aviso: Falha ao carregar pacote de ativos.", false);
    }
    
    // Configuração da voz TTS (NVGT usa escala 0-100 para volume)
    tts.set_volume(80);
    speak("Sistemas de NVGT inicializados.", true); 
}

void play_effect() {
    // sound_pool gerencia a reprodução de efeitos sonoros
    int slot = g_sound_pool.play_stationary("passo.wav", false, false); 
    
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
        
        // Loop principal e obrigatório de espera para evitar consumo excessivo de CPU e processar eventos
        wait(5);
        
        // Atualiza a sound_pool (essencial para gerenciamento de som)
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
                tts.speak("Leitor de tela não detectado, usando voz interna.", true);
            }
        }
    }
    
    speak("Fechando aplicação.", true);
    destroy_window();
}

Fase 2: Rede, Conexão e Autenticação
Objetivo: Estabelecer a comunicação cliente-servidor usando a API nativa network do NVGT e implementar a lógica de autenticação segura.
Arquivos BGT a Serem Substituídos/Alterados nesta Fase:
• 
net.bgt (lógica de netloop e recebimento de eventos).
• 
comandos.bgt (funções send_reliable, send_unreliable, enviar, receber, login).
• 
googletranslateclient.bgt, downloader.bgt, weather info.bgt (qualquer lógica de HTTP deve ser migrada para a classe http do NVGT).
1. Inicialização do Subsistema de Rede
• 
Instanciar e Configurar: Crie um objeto network e chame obrigatoriamente network::setup_client(max_channels, max_peers) para inicializar o objeto como cliente, definindo o número máximo de canais e peers.
• 
Conectar: Chame network::connect(hostname, port). Armazene o ID do peer retornado (que deve ser 1 se a conexão for bem-sucedida).
• 
Segurança (Opcional, mas Recomendada): Se necessário, defina a propriedade packet_compression = true no objeto network se for interagir com um servidor que usa o compressor de pacotes embutido do Enet (comum em migrações BGT).
2. Lógica de Autenticação e Transmissão
• 
Criptografar Dados: Antes de enviar credenciais (h33j, xt55), utilize string_aes_encrypt() para criptografar a senha (e idealmente todo o pacote de credenciais) para garantir segurança.
• 
Enviar Login/Criação de Conta: Envie o comando de autenticação (juntamente com os dados criptografados) para o servidor (peer ID 1) usando network::send_reliable() ou network::send(1, message, channel, true) para garantir que o pacote chegue.
3. Loop de Eventos de Rede
• 
Monitoramento Contínuo: No game loop principal (após wait(5)), adicione uma rotina para chamar repetidamente network::request(timeout) para buscar eventos.
• 
Processar Recebimento: Se um evento do tipo event_receive for detectado, processe o conteúdo em network_event::message.
• 
Marco de Sucesso: Implemente a lógica para verificar e processar o network_event::message que contém a resposta "loggedin".
Exemplo de Código da Fase 2:
#include "speech.nvgt"
#include "sound_pool.nvgt"

#pragma embed game_assets.pack

// Variaveis e Objetos Nativos
sound_pool g_sound_pool;
pack@ g_assets_pack = null;
network g_net; 
bool g_game_running = true;

const string SERVER_ADDRESS = "127.0.0.1";
const uint16 SERVER_PORT = 7000;
const string ENCRYPTION_KEY = "ChaveSecretaNVGT123456"; 
const uint64 SERVER_PEER_ID = 1;

// =================================================================
// INICIALIZAÇÃO E REDE (Fase 1 & 2)
// =================================================================

bool setup_network() {
    // 1. Configuração do Cliente de Rede (Nativo NVGT)
    if (!g_net.setup_client(2, 2)) {
        speak("Erro: Falha ao configurar o cliente de rede.", true);
        return false;
    }

    // 2. Conectar (Nativo NVGT)
    if (g_net.connect(SERVER_ADDRESS, SERVER_PORT) != SERVER_PEER_ID) {
        speak("Erro: Falha ao conectar ao servidor de jogo.", true);
        return false;
    }

    speak("Conectado ao servidor: " + SERVER_ADDRESS, false);
    return true;
}

void send_login_attempt(string username, string password) {
    // Uso nativo de criptografia
    string encrypted_pass = string_aes_encrypt(password, ENCRYPTION_KEY);
    if (encrypted_pass.empty()) return;
    
    string login_message = "h33j:" + username + ":" + encrypted_pass;

    // Envio confiável (reliable = true) para o servidor
    g_net.send(SERVER_PEER_ID, login_message, 0, true);
    speak("Tentativa de login enviada. Aguardando autenticação...", false);
}

void handle_network_events() {
    // Polling de rede no loop principal
    network_event@ event = g_net.request(0); 
    while (@event != null) {
        if (event.type == event_receive) {
            string message = event.message;
            if (message.starts_with("loggedin")) {
                speak("Autenticação SUCESSO!", true);
            } else if (message.starts_with("loginfailed")) {
                speak("Falha no Login.", true);
            }
        }
        @event = g_net.request(0); 
    }
}

void game_init() {
    // 1. Configuração de Pacote de Sons (Nativo: Propriedade Global)
    pack temp_pack;
    if (temp_pack.open("game_assets.pack", PACK_OPEN_MODE_READ)) {
        @g_assets_pack = temp_pack;
        // Configuração nativa: Atribuindo o handle do pacote à propriedade global
        @sound_default_pack = g_assets_pack;
        speak("Pacote de ativos carregado. Sistema de áudio pronto.", false);
    } 
    
    // 2. Configuração de Fala (TTS)
    tts.set_volume(80);
    
    // 3. Inicialização de Rede
    if (!setup_network()) g_game_running = false;
}

void main() {
    // Uso Nativo: show_window (antigo show_game_window)
    show_window("Cliente NVGT NATIVO - Fase 2"); 
    
    game_init();
    
    speak("Pressione L para tentar logar e ESC para sair.", false);

    while (g_game_running) {
        
        // Loop principal: Espera obrigatória de 5ms
        wait(5);
        
        g_sound_pool.update(0, 0, 0, 0, 1000); 
        handle_network_events();

        // Input de Simulação de Login
        if (key_pressed(KEY_L)) {
            send_login_attempt("native_player", "native_pass");
        }

        if (key_pressed(KEY_ESCAPE)) {
            g_game_running = false;
        }
        
        // Exemplo de uso nativo de funções matemáticas para pan (substitui 'absolute', 'cosine', etc.)
        // float volume_level = abs(cos(ticks() * 0.001)); 
    }
    
    speak("Fechando aplicação.", true);
    destroy_window();
}

Fase 3: Interface do Usuário (Menus e Interação)
Objetivo: Reconstruir toda a interface do cliente (Menus, formulários de entrada e diálogos) utilizando os componentes nativos do NVGT para garantir melhor performance, acessibilidade e manutenibilidade.
Arquivos BGT a Serem Substituídos/Alterados nesta Fase:
• 
Sistema de Menus: m_pro.bgt, menu.bgt, menu2.bgt, simple_menu.bgt.
• 
Menus Específicos: adminmenu.bgt, buildermenu.bgt, celularmenu (em menu.bgt), etc.
• 
Entrada de Texto: editor.bgt, virtualizer.bgt.
• 
Diálogos: dialogos.bgt.
1. Sistema de Menus (Navegação Principal)
A abordagem é substituir a migração complexa de classes antigas (como dynamic_menu_pro e menu.bgt) pelo sistema de menus moderno do NVGT.
• 
Substituição Core: Utilize a classe menu (disponível via #include "menu.nvgt"). Esta classe é a interface de menu moderna do NVGT.
• 
Fundação UI: A classe menu é construída sobre o controle de lista (ct_list) da classe audio_form (disponível via #include "form.nvgt").
• 
Configuração de Menu: Ao invés de lógica manual, utilize as propriedades nativas da classe menu para configurar o comportamento, incluindo sons de navegação (click_sound, select_sound), som de borda (edge_sound) e o comportamento de wrapping (enrolamento).
2. Controles de Entrada de Texto e Formulários
Substitua classes customizadas de edição de texto (editor.bgt, virtualizer.bgt) pelas funções de criação de controles do audio_form e includes de alto nível.
• 
Entrada de Campo Único (Login/Senha): Use audio_form::create_input_box(). Este método permite configurar a legenda, o texto padrão, e, crucialmente, definir uma máscara de senha (password_mask).
• 
Formulários de Dados (Múltiplos Campos): Para coletar informações estruturadas (ex: configurações do personagem, detalhes de conta), utilize o include #include "input_forms.nvgt". Esta biblioteca simplifica a criação e validação de formulários complexos usando classes como input_form e text_field.
• 
Diálogos Rápidos: Para funções simples de pop-up (como alert, question ou input_box), use o include #include "virtual_dialogs.nvgt", que oferece wrappers de alto nível (ex: virtual_alert, virtual_input_box).
• 
Captura de Jogo na UI: Se for necessário um campo de texto que capture todas as teclas para mapeamento de controles (permitindo que os controles do jogo funcionem dentro da UI), use audio_form::create_keyboard_area().
 

Fase 4: Lógica de Jogo e Sincronização de Mundo
Objetivo: Implementar a lógica principal do jogo (interpretação de dados do servidor) e portar as estruturas de dados de Mapa e Entidades, garantindo que todas as ações de feedback (áudio, inventário) usem as APIs nativas do NVGT.
Arquivos BGT a Serem Substituídos/Alterados nesta Fase:
• 
Estrutura de Mundo: map.bgt, player.bgt, zones.bgt, safezones.bgt, platforms.bgt, staircase.bgt, door.bgt, elevador.bgt.
• 
Lógica do Jogador: inv.bgt, weapon.bgt, secondary_inventory.bgt.
• 
Tratamento de Comandos: comandos.bgt, comandos grandes.bgt.
1. Carregamento de Mapa e Entidades (Estruturas de Dados e Áudio Posicional)
• 
Estrutura de Mapas (map.bgt): Em vez de reescrever manualmente wrappers de arrays 2D, utilize a classe grid. O grid é a matriz 2D nativa do NVGT, ideal para representar tabuleiros de jogo ou mapas baseados em blocos, permitindo indexação simplificada (e.g., mapa[x, y]). Classes como player.bgt e zones.bgt devem se referir ou ser armazenadas dentro dessa estrutura grid.
• 
Processamento de Mensagens do Servidor (Netloop): O tratamento de eventos de rede (network::request()) no game loop deve ser expandido para processar mensagens específicas do servidor, como changemap, add_player_to_map e update_player.
• 
Áudio de Entidades (Posicional): Ao receber dados de entidades do servidor (como de add_player_to_map), substitua todas as chamadas audio.play_sound_2d() e similares pelas funções da classe sound_pool:
• 
Use sound_pool::play_2d() ou sound_pool::play_3d() para sons de entidades fixas.
• 
Sempre chame sound_pool::update_listener_3d() no game loop para sincronizar a posição do ouvinte (seu jogador) com os novos dados de coordenadas.
2. Portabilidade da Lógica do Jogador (Controlador e Inventário)
• 
Lógica de Movimento e Posição (player.bgt): A estrutura da classe do jogador deve herdar a classe abstrata basic_character_controller. Isso elimina a necessidade de portar a lógica de física e colisão de BGT.
• 
No seu game loop, chame o método update(delta_time) do seu controlador de personagem.
• 
Ao receber comandos de movimento do servidor ou entrada do usuário (Fase 1), defina os sinais de entrada do controlador (e.g., controller.move_forward = true).
• 
Inventário, Armas e Timers (inv.bgt, weapon.bgt):
• 
Migre as classes de dados puras (inventário, itens) usando a sintaxe AngelScript nativa.
• 
Para timers (ex: recarga de arma, cooldowns), utilize a classe timer nativa do NVGT, que agora faz parte do core do engine, em vez de implementar sua própria lógica de temporização baseada em ticks.
• 
Comandos e Saída (comandos.bgt): Todas as ações resultantes (ex: notificar o usuário que a arma recarregou) devem usar:
• 
Saída de Fala: speak() (do speech.nvgt) ou screen_reader_speak() para feedback imediato.
• 
Atualização de UI/Menus: Interaja com as classes menu ou audio_form (Fase 3) para exibir o estado do inventário ou menus de armas.