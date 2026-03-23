Excelente escolha. O sistema de Mapas e o Modo Construtor (Builder) são realmente a espinha dorsal de todo o ecossistema do EVM. Sem eles funcionando plenamente, itens, NPCs, portais e lojas não têm onde existir. 

Lendo os arquivos de arquitetura, notei em `server_map.txt` que a refatoração do sistema de mapas parou exatamente no fim da base estrutural: *"FASE 1/14: CONCLUÍDA - Classe map criada [...] PRÓXIMO: FASE 2 - Implementar loops de objetos coletáveis"*. Além disso, em `buildermenu.txt` e `stubs.txt`, os menus para criar essas estruturas no mapa estão apenas avisando que "ainda não foram implementados".

Aqui está o **Plano de Implementação Passo a Passo**, focado em reativar e modernizar o ecossistema de Mapas e Builder, utilizando as referências do BGT como norte:

---

### 🗺️ Plano de Ação: Reconstrução do Ecossistema de Mapas

#### **Mini-Task 1: Reviver os Menus de Construção Essenciais (Cliente - `buildermenu.nvgt`)**
*   **O que faremos:** Substituir os *stubs* de criação (como `portalsmenu()`, `stores_building_menu()`, `itemsmenu()`, `weapons_menu()`) por formulários reais utilizando a classe nativa `input_form`.
*   **Referência BGT:** No BGT, quando um admin escolhia criar um portal, abria-se um menu pedindo: X/Y atual, Mapa de destino, X/Y de destino, etc.
*   **Ação NVGT:** Vamos codificar esses menus no cliente para que coletem os dados corretamente e enviem a string estruturada (ex: `add_line::portal:x:y:dest_map...`) para o servidor usando a função `send_to_server()`.

#### **Mini-Task 2: Interceptação e Validação de Construção (Servidor - `builder.nvgt`)**
*   **O que faremos:** O cliente agora enviará comandos para criar portais, itens e lojas no mapa. O servidor precisa estar pronto para recebê-los e processá-los de forma segura.
*   **Referência BGT/Ação NVGT:** No arquivo `builder.nvgt`, o *handler* principal `req_builder_create_element` intercepta mensagens `add_line::`. Vamos adicionar os *parsers* e funções de criação que faltam (ex: `builder_create_portal()`, `builder_create_store()`), garantindo que chamem `builder_check_permission(p)` para evitar *exploits* de *hacks* que forjem pacotes.

#### **Mini-Task 3: Progressão da Fase 2 de Mapas - Loops e Físicas (Servidor - `server_map.nvgt`)**
*   **O que faremos:** Retomar a conversão a partir da Fase 2 ("Implementar loops de objetos coletáveis"). 
*   **Referência BGT:** O BGT usava grandes loops globais (`objloop()`, `portals_loop()`) para checar se algum jogador estava pisando em um objeto ou portal.
*   **Ação NVGT:** Vamos otimizar esses loops. Em vez de iterar sobre *todos* os jogadores e *todos* os itens ao mesmo tempo, vamos garantir que o `server_map.nvgt` processe apenas os itens/portais que estão no mesmo mapa em que há jogadores ativos, ativando as classes em `map_elements.nvgt`.

#### **Mini-Task 4: Integração das Lojas Físicas no Mapa (Cliente/Servidor - `store.nvgt` e `stubs.nvgt`)**
*   **O que faremos:** Os balcões de lojas (`roupas()`, `armasbertalina()`, `joalheria()`) estão atualmente como *stubs*. Precisamos fazer o jogador interagir com o balcão no mapa.
*   **Referência BGT/Ação NVGT:** Quando o jogador der Enter no balcão da loja, em vez de mostrar um aviso de não implementado, o cliente enviará o comando `/store`. O servidor buscará os itens via `cmd_store` e os devolverá no formato JSON para o menu dinâmico da loja.

---

### 🚀 Começando a Mini-Task 1: Menus do Construtor

Para começarmos a colocar a mão na massa **agora**, vamos focar na **Mini-Task 1**.
Caso seja preciso, olhe o fluxo bgt, para ter referencias, e um norte a seguir, claro que adaptando ao nosso contexto.

Eles usarão a API moderna do NVGT (`input_form`) para capturar as informações passo a passo da tela do construtor e já farão o envio empacotado para o servidor.
Códigos exemplos:
// Menu para criar Portais pelo Construtor
void portalsmenu() {
    input_form form(pu.get_value("Criar Portal Mágico"));
    form.description = pu.get_value("Preencha os dados para criar um portal no mapa atual.");
    
    // Coordenadas de origem (onde o portal vai ficar)
    form.add_number_field("x", pu.get_value("Coordenada X do portal"), 0, true);
    form.add_number_field("y", pu.get_value("Coordenada Y do portal"), 0, true);
    
    // Dados de destino
    form.add_text_field("dest_map", pu.get_value("Nome do mapa de destino"), "", true);
    form.add_number_field("dest_x", pu.get_value("Coordenada X de destino"), 0, true);
    form.add_number_field("dest_y", pu.get_value("Coordenada Y de destino"), 0, true);

    dictionary@ result = form.run();
    
    if(!form.user_canceled) {
        double x, y, dest_x, dest_y;
        string dest_map;
        
        result.get("x", x);
        result.get("y", y);
        result.get("dest_x", dest_x);
        result.get("dest_y", dest_y);
        result.get("dest_map", dest_map);

        if(dest_map != "") {
            // Formata a string: portal:x:y:dest_map:dest_x:dest_y
            string data = "portal:" + int(x) + ":" + int(y) + ":" + dest_map + ":" + int(dest_x) + ":" + int(dest_y);
            send_to_server("add_line::" + data, 13, true);
            speak(pu.get_value("Comando de criação de portal enviado ao servidor."));
        }
    }
}

// Menu para criar Zonas de Lojas pelo Construtor
void stores_building_menu() {
    input_form form(pu.get_value("Criar Loja / Estabelecimento"));
    form.description = pu.get_value("Defina a área de balcão e o tipo da loja.");
    
    // Definindo a área do balcão da loja
    form.add_number_field("x1", pu.get_value("Início da coordenada X"), 0, true);
    form.add_number_field("x2", pu.get_value("Fim da coordenada X"), 0, true);
    form.add_number_field("y1", pu.get_value("Início da coordenada Y"), 0, true);
    form.add_number_field("y2", pu.get_value("Fim da coordenada Y"), 0, true);
    
    // Identificador da Loja (ex: armas, roupas, farmacia, lanchonete)
    form.add_text_field("store_type", pu.get_value("Tipo de Loja (ex: armas, roupas, farmacia, lanchonete)"), "", true);

    dictionary@ result = form.run();
    
    if(!form.user_canceled) {
        double x1, x2, y1, y2;
        string store_type;
        
        result.get("x1", x1);
        result.get("x2", x2);
        result.get("y1", y1);
        result.get("y2", y2);
        result.get("store_type", store_type);

        if(store_type != "") {
            // Formata a string: store:x1:x2:y1:y2:tipo_da_loja
            string data = "store:" + int(x1) + ":" + int(x2) + ":" + int(y1) + ":" + int(y2) + ":" + store_type;
            send_to_server("add_line::" + data, 13, true);
            speak(pu.get_value("Comando de criação de loja enviado ao servidor."));
        }
    }
}
O que este código faz?
1. O uso do input_form: Em vez dos antigos menus estáticos do BGT, o NVGT utiliza input_form.add_number_field e add_text_field, criando uma janela perfeitamente acessível aos leitores de tela onde você digita todas as informações e dá um único Enter.
2. Validação: Ele verifica se o usuário não cancelou a operação com o ESC (if(!form.user_canceled)).
3. Empacotamento da String: Ele constrói a string no formato exato que o Builder Mode precisa (add_line::portal:...) e a envia pelo canal 13 via rede segura (send_to_server)
3
.
O Próximo Passo (Mini-Task 2)
Agora que o cliente já sabe como perguntar os dados ao admin e enviar o comando, o servidor vai receber strings como:
• add_line::portal:10:5:cidade:20:20
• add_line::store:5:10:5:10:armas
O servidor vai lançar um erro dizendo que não reconhece o tipo portal e store, pois precisamos implementar os handlers no arquivo builder.nvgt do servidor.
// --- PORTAL MÁGICO (portal) ---
// Formato recebido: portal:x:y:dest_map:dest_x:dest_y
bool builder_create_portal(player@ p, map@ current_map, string[] parsed) {
    if(parsed.length() < 6) {
        builder_send_error(p, "Portal requer: portal:x:y:mapa_destino:dest_x:dest_y");
        return false;
    }

    int x = parse_int(parsed[3]);
    int y = parse_int(parsed[4]);
    string dest_map = parsed[5];
    int dest_x = parse_int(parsed[6]);
    int dest_y = parse_int(parsed[7]);

    // Validação de segurança [8]
    if(!builder_validate_coords(x, y) || !builder_validate_coords(dest_x, dest_y)) {
        builder_send_error(p, "Coordenadas do portal inválidas. Estão fora dos limites do mapa.");
        return false;
    }

    // Opcional: Validar se o mapa de destino é um nome seguro [9]
    if(!builder_is_valid_map_name(dest_map)) {
         builder_send_error(p, "O nome do mapa de destino contém caracteres inválidos.");
         return false;
    }

    // Reconstrói a linha para injetar no array do mapa
    string line = "portal:" + x + ":" + y + ":" + dest_map + ":" + dest_x + ":" + dest_y;

    // Injeta na memória atual do mapa [10]
    current_map.mapdata.insert_last(line);
    builder_send_success(p, "Portal mágico para " + dest_map + " criado com sucesso!");
    return true;
}

// --- LOJA / ESTABELECIMENTO COMERCIAL (store) ---
// Formato recebido: store:x1:x2:y1:y2:store_type
bool builder_create_store(player@ p, map@ current_map, string[] parsed) {
    if(parsed.length() < 6) {
        builder_send_error(p, "Loja requer: store:x1:x2:y1:y2:tipo_loja");
        return false;
    }

    int x1 = parse_int(parsed[3]);
    int x2 = parse_int(parsed[4]);
    int y1 = parse_int(parsed[5]);
    int y2 = parse_int(parsed[6]);
    string store_type = parsed[7];

    // Validação de segurança [8]
    if(!builder_validate_coords(x1, y1) || !builder_validate_coords(x2, y2)) {
        builder_send_error(p, "Coordenadas da loja inválidas. Estão fora dos limites.");
        return false;
    }

    // Reconstrói a linha
    string line = "store:" + x1 + ":" + x2 + ":" + y1 + ":" + y2 + ":" + store_type;

    current_map.mapdata.insert_last(line);
    builder_send_success(p, "Área de loja (" + store_type + ") demarcada com sucesso!");
    return true;
}
2. Conectando no Roteador Principal
Agora, procure no mesmo arquivo a função req_builder_create_element(player@ p, string element_data)
3
. Dentro dela, existe uma cadeia de checagens (if(element_type == "p"), else if(element_type == "pwall"), etc.).
Adicione nossas duas novas funções dentro dessa estrutura de roteamento:
    // (dentro de req_builder_create_element, junto aos outros 'else if')
    else if(element_type == "portal") {
        builder_create_portal(p, current_map, parsed);
    }
    else if(element_type == "store") {
        builder_create_store(p, current_map, parsed);
    }
O que acontece agora?
Com isso, a Mini-Task 1 e 2 estão prontas. O Admin vai no jogo, aperta para criar um Portal Mágico, preenche o formulário. O cliente envia add_line::portal:50:0:cidade:10:0. O servidor intercepta, valida as permissões do Admin
3
, verifica se as coordenadas não quebram o mapa
4
, injeta a linha direto na matriz do servidor (current_map.mapdata) e notifica o admin
5
.
Próximo Passo (Mini-Task 3): Agora que o arquivo .map está gravando as linhas portal e store, o jogador comum precisa conseguir interagir com elas! No momento, o mapa lê os dados, mas ainda precisamos implementar a lógica física (se o jogador pisar em x:50 y:0, ele deve ser teletransportado).
No BGT antigo, o servidor rodava um loop global a cada 50 milissegundos verificando a posição de todos os jogadores contra todos os portais e zonas do mapa, o que causava muito lag.
No NVGT, faremos isso de forma moderna e otimizada, baseada em Eventos: o servidor só vai checar as físicas do mapa no momento exato em que o jogador der um passo ou apertar Enter (interagir).
Abra o seu arquivo server/includes/server_map.nvgt e adicione as seguintes funções no final do arquivo:
// ============================================================================
// FÍSICA E EVENTOS DO MAPA (Mini-Task 3)
// ============================================================================

// Processa eventos de "pisar" (Ex: Portais, armadilhas). 
// DEVE SER CHAMADO: Sempre que o jogador se mover (handle_move).
void process_map_step(int player_index) {
    if(player_index < 0 || player_index >= int(players.length())) return;
    
    player@ p = players[player_index];
    if(p is null) return;

    int map_idx = get_map_index_from(p.map);
    if(map_idx < 0) return;
    
    map@ current_map = server_maps[map_idx];

    // Varre os elementos do mapa atual
    for(uint i = 0; i < current_map.mapdata.length(); i++) {
        string[] parsed = current_map.mapdata[i].split(":");
        if(parsed.length() == 0) continue;

        // Verifica se é um Portal Mágico e se o jogador pisou na coordenada exata
        if(parsed == "portal" && parsed.length() >= 6) {
            int px = parse_int(parsed[1]);
            int py = parse_int(parsed[2]);

            if(p.x == px && p.y == py) {
                string dest_map = parsed[3];
                int dest_x = parse_int(parsed[4]);
                int dest_y = parse_int(parsed[5]);

                // Dispara som de teletransporte para quem está perto
                broadcast_to_map(p.map, "play_stationary teleport.ogg " + p.x + " " + p.y);
                
                // Teleporta o jogador usando a função nativa do ecossistema
                move_player_to_map(player_index, dest_map, dest_x, dest_y);
                
                // Notifica o jogador
                send_reliable_text(p.peer_id, "say Você atravessou um portal mágico!", 0);
                return; // Para o loop após o teleporte para evitar bugs
            }
        }
    }
}

// Processa eventos de "interação" (Ex: Balcões de Loja, NPCs estáticos).
// DEVE SER CHAMADO: Quando o jogador apertar ENTER (handle_interact).
void process_map_interaction(int player_index) {
    if(player_index < 0 || player_index >= int(players.length())) return;
    
    player@ p = players[player_index];
    if(p is null) return;

    int map_idx = get_map_index_from(p.map);
    if(map_idx < 0) return;
    
    map@ current_map = server_maps[map_idx];
    bool interaction_found = false;

    // Varre os elementos em busca de lojas
    for(uint i = 0; i < current_map.mapdata.length(); i++) {
        string[] parsed = current_map.mapdata[i].split(":");
        if(parsed.length() == 0) continue;

        // Verifica se é uma Zona de Loja
        if(parsed == "store" && parsed.length() >= 6) {
            int x1 = parse_int(parsed[1]);
            int x2 = parse_int(parsed[2]);
            int y1 = parse_int(parsed[3]);
            int y2 = parse_int(parsed[4]);
            string store_type = parsed[5]; // ex: armas, roupas, farmacia

            // Verifica se o jogador está de frente para o balcão (dentro da área X/Y demarcada)
            if(p.x >= x1 && p.x <= x2 && p.y >= y1 && p.y <= y2) {
                // Envia pacote para o cliente abrir o menu correspondente
                send_reliable_text(p.peer_id, "store_open " + store_type, 0);
                interaction_found = true;
                return;
            }
        }
    }

    if(!interaction_found) {
        send_reliable_text(p.peer_id, "say Não há nada para interagir aqui.", 0);
    }
}
Onde plugar isso no servidor?
1. O Evento de Pisar: Vá no seu arquivo onde processa o movimento do jogador (pode ser no network_handlers.nvgt dentro da função handle_move ou onde o pacote de movimento é recebido) e adicione:
2. Isso garante que sempre que o jogador der um passo (move), o servidor veja se ele pisou num portal.
3. O Evento de Interagir: No mesmo arquivo (ou no comando que capta a tecla Enter do jogador para checar as coisas do chão), adicione:
O que conquistamos agora?
As mecânicas estão conectadas! O Builder cria o portal no mapa. A classe Map do servidor salva. Quando o jogador normal pisa nas coordenadas (Ex: x:10, y:5), o servidor instantaneamente detecta e dá o teleporte (move_player_to_map).
E para as lojas, quando o jogador aperta Enter na coordenada do balcão, o servidor manda o comando store_open tipo_da_loja (ex: store_open armas) para o cliente.
Próximo passo (Mini-Task 4): Como o servidor agora envia a ordem para o cliente abrir a loja, o cliente vai interceptar isso. Nós precisamos ir lá nos stubs do cliente (stubs.nvgt), deletar o aviso de "ainda não implementado" e escrever a interface da Loja em NVGT (para mostrar os preços, ouro atual e itens usando os menus).Como o servidor agora envia o comando store_open tipo_da_loja (ex: store_open armas), nós precisamos fazer duas coisas no cliente: interceptar esse pacote na rede e exibir o menu moderno da loja para o jogador escolher o item e a quantidade.
Passo 1: Substituir os Stubs pela Loja Universal (stubs.nvgt)
Abra o arquivo includes/stubs.nvgt no código do seu cliente. Apague aquelas funções antigas (roupas(), armasbertalina(), farmacia(), etc.) que só diziam "ainda não implementada" e substitua por este bloco completo:
// ============================================================================
// SISTEMA UNIFICADO DE LOJAS (Substituindo os Stubs Antigos)
// ============================================================================

// Função universal que recebe o tipo de loja e monta o menu dinamicamente
void open_generic_store(string store_type) {
    if(ausente || !moveable) return;
    
    setupmenu(); // Prepara o menu nativo do NVGT
    string store_name = store_type;

    // Popula os itens baseado no tipo de loja que o servidor informou
    if(store_type == "armas") {
        store_name = pu.get_value("Armería Bertalina / Caça");
        game_menu.add_item(pu.get_value("Espada de Ferro (150 moedas)"), "espada_ferro");
        game_menu.add_item(pu.get_value("Arco de Caça (200 moedas)"), "arco_caca");
        game_menu.add_item(pu.get_value("Munição Padrão (10 moedas)"), "municao");
    } 
    else if(store_type == "roupas") {
        store_name = pu.get_value("Loja de Roupas");
        game_menu.add_item(pu.get_value("Camisa de Couro (50 moedas)"), "camisa_couro");
        game_menu.add_item(pu.get_value("Botas Resistentes (75 moedas)"), "botas");
    } 
    else if(store_type == "farmacia") {
        store_name = pu.get_value("Farmácia");
        game_menu.add_item(pu.get_value("Poção de Vida (20 moedas)"), "pocao_vida");
        game_menu.add_item(pu.get_value("Bandagem (15 moedas)"), "bandagem");
    } 
    else if(store_type == "lanchonete") {
        store_name = pu.get_value("Lanchonete e Bar");
        game_menu.add_item(pu.get_value("Hambúrguer (10 moedas)"), "hamburguer");
        game_menu.add_item(pu.get_value("Refrigerante (5 moedas)"), "refrigerante");
        game_menu.add_item(pu.get_value("Cerveja (8 moedas)"), "cerveja");
    }
    else if(store_type == "eletronicos") {
        store_name = pu.get_value("Loja de Eletrônicos");
        game_menu.add_item(pu.get_value("Rádio (100 moedas)"), "radio");
    } 
    else {
        store_name = pu.get_value("Loja Mista");
        game_menu.add_item(pu.get_value("Item Genérico (10 moedas)"), "item_generico");
    }

    game_menu.intro_text = pu.get_value("Bem-vindo à ") + store_name + ". " + pu.get_value("O que você gostaria de comprar?");
    game_menu.add_item(pu.get_value("Sair da Loja"), "sair");

    // Roda o menu para o jogador
    int result = game_menu.run();

    if(result > -1) {
        string selected = game_menu.get_item_id(result);
        if(selected != "sair") {
            // Usa o helper moderno do menu.nvgt para pedir a quantidade
            string qt_str = prompt_numeric_input(
                pu.get_value("Quantidade"), 
                pu.get_value("Quantos itens você deseja comprar?"), 
                1
            );

            if(qt_str != "") {
                int qtd = parse_int(qt_str);
                if(qtd > 0) {
                    // Envia a ordem de compra para o servidor: Ex: /buy pocao_vida 5
                    send_reliable(peer_id, "/buy " + selected + " " + qtd, 0);
                    speak(pu.get_value("Solicitação de compra enviada."));
                }
            }
        }
    }
}

// Mantendo compatibilidade com as chamadas antigas se o jogador der Enter nelas
void roupas() { open_generic_store("roupas"); }
void armasbertalina() { open_generic_store("armas"); }
void pesca() { open_generic_store("pesca"); }
void farmacia() { open_generic_store("farmacia"); }
void comprareletronicos() { open_generic_store("eletronicos"); }
void joalheria() { open_generic_store("joias"); }
void lanchonete() { open_generic_store("lanchonete"); }
Passo 2: Fazer o cliente obedecer à ordem do servidor (net.nvgt)
Agora precisamos ensinar ao cliente o que fazer quando o servidor disser que ele está na frente de um balcão.
Abra o arquivo de rede do seu cliente (provavelmente net.nvgt onde os pacotes chegam e são separados por parsed). Procure o local onde você processa comandos simples do servidor e adicione a interceptação:
    // Interceptação do comando para abrir a loja (passo 2 da Task)
    else if(parsed == "store_open" && parsed.length() >= 2) {
        string store_type = parsed[1];
        open_generic_store(store_type);
    }
Como isso funciona na prática agora?
1. O Admin vai lá no Modo Construtor, cria uma zona do tipo "loja" chamada farmacia.
2. Um jogador comum anda pelo mapa e dá de cara com essa zona. Ele aperta Enter.
3. A nossa Física de Mapa (Task 3) no servidor roda, percebe que ele interagiu com uma loja e envia para ele: store_open farmacia.
4. O cliente dele recebe o pacote, lê o passo 2 acima e executa a função que acabamos de criar open_generic_store("farmacia").
5. A interface acessível e moderna abre dizendo "Bem-vindo à Farmácia", ele escolhe "Poção de vida", digita "5" na caixinha de texto e dá Enter.
6. O cliente envia silenciosamente a mensagem /buy pocao_vida 5 para o servidor
1
.
(Nota: Mais para frente, podemos fazer esse menu nem ter as opções escritas "na mão", e sim pedir para o servidor listar os itens do banco de dados
2
, mas isso já destrava 100% a jogabilidade com o que você tem no banco hoje!)
Me confirme quando tiver injetado essas duas partes. Nossa espinha dorsal do modo pacífico (Construir Mapa -> Andar no Mapa -> Interagir com estruturas) está finalmente convertida e viva no 
Manda bala nessas, e logo menos já continuamos