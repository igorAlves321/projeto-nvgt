Bora! É agora que o mapa começa a ficar perigoso para os exploradores desavisados! ☠️

Atualmente, o seu Menu de Construtor já consegue criar Áreas de Morte (`deaths:x1:x2:y1:y2:time:msg`) e Areia Movediça (`am:x:y`) e gravá-las no banco de mapas. Além disso, você tem o módulo **`progressive_death.nvgt`**, que é uma arquitetura fantástica para gerenciar danos contínuos ao longo do tempo (como sufocamento e envenenamento) sem travar o servidor. O que precisamos fazer é **conectar as duas coisas**!

Vamos para a **Mini-Task 7: Zonas Dinâmicas e Perigosas (Servidor)**.

### Passo 1: Criando a Detecção Físico-Química no Mapa
Nós precisamos varrer o chão onde o jogador pisa. Se ele entrar nas coordenadas da morte, nós ativamos a `progressive_death`. Se ele conseguir sair antes de morrer, nós a desativamos e ele se salva.

Abra o seu arquivo **`server/includes/server_map.nvgt`** (onde colocamos os eventos do mapa nas tasks anteriores) e adicione esta função no final do arquivo:

```cpp
// ============================================================================
// ZONAS DE PERIGO E HAZARDS (Mini-Task 7)
// ============================================================================

void check_hazard_zones(int player_index) {
    if(player_index < 0 || player_index >= int(players.length())) return;
    
    player@ p = players[player_index];
    
    // Jogadores pacíficos, mortos ou desenvolvedores imortais não sofrem dano de zona
    if(p is null || p.health <= 0 || p.pacifico == 1 || has_role(p.charname, "dev")) return;

    int map_idx = get_map_index_from(p.map);
    if(map_idx < 0) return;
    
    map@ current_map = server_maps[map_idx];
    bool in_danger = false;

    // Varre os elementos do mapa em busca de armadilhas
    for(uint i = 0; i < current_map.mapdata.length(); i++) {
        string[] parsed = current_map.mapdata[i].split(":");
        if(parsed.length() == 0) continue;

        // --- ÁREA DE MORTE (deaths) ---
        // Formato salvo pelo builder: deaths:minx:maxx:miny:maxy:time:msg
        if(parsed == "deaths" && parsed.length() >= 5) {
            int minx = parse_int(parsed);
            int maxx = parse_int(parsed);
            int miny = parse_int(parsed);
            int maxy = parse_int(parsed);

            // Verifica se o jogador está pisando dentro do quadrante da morte
            if(p.x >= minx && p.x <= maxx && p.y >= miny && p.y <= maxy) {
                in_danger = true;
                
                // Se a morte progressiva ainda não estiver ativada nele
                if(p.progressive_death == 0) {
                    // Inicia morte progressiva por sufocamento (tipo 4), tirando 15 de vida a cada 1 segundo (1000ms)
                    start_progressive_death(player_index, 4, 15.0, 1000, "Morreu na zona tóxica");
                    send_reliable_text(p.peer_id, "say [SISTEMA] Você entrou em uma zona mortal! Saia imediatamente!", 0);
                    send_reliable_text(p.peer_id, "play_stationary hazzard_enter.ogg", 0);
                }
                break;
            }
        }

        // --- AREIA MOVEDIÇA (am) ---
        // Formato salvo pelo builder: am:x:y
        else if(parsed == "am" && parsed.length() >= 3) {
            int x = parse_int(parsed);
            int y = parse_int(parsed);

            // Areia movediça é um ponto específico
            if(p.x == x && p.y == y) {
                in_danger = true;
                if(p.progressive_death == 0) {
                    // Areia movediça machuca mais rápido (a cada 800ms)
                    start_progressive_death(player_index, 4, 25.0, 800, "Foi engolido pela areia movediça");
                    send_reliable_text(p.peer_id, "say Você pisou na areia movediça e está afundando!", 0);
                    send_reliable_text(p.peer_id, "play_stationary morrendo_areia.ogg", 0);
                }
                break;
            }
        }
    }

    // Se o jogador deu um passo para fora de todas as zonas, nós o curamos do status de dano
    if(!in_danger && p.progressive_death == 1) {
        stop_progressive_death(player_index);
        send_reliable_text(p.peer_id, "say Você conseguiu escapar da zona de perigo a tempo.", 0);
    }
}
```

### Passo 2: Plugar na movimentação do servidor
Para que isso funcione em tempo real e de forma otimizada (sem loops infinitos causando lag no servidor todo), nós vamos checar essas zonas **apenas quando o jogador anda**.

No mesmo arquivo (`server_map.nvgt`), procure a função que criamos algumas mensagens atrás chamada `process_map_step(int player_index)`. Vá até a **última linha** de dentro dessa função e adicione a chamada:

```cpp
    // Adicione no fim da função process_map_step()
    check_hazard_zones(player_index);
```

### O que acontece agora?
A mágica toda ocorre nos bastidores: o seu construtor delimita a área, o jogador não enxerga, mas ao pisar, a função `start_progressive_death` do seu servidor assume o controle, ativando um sub-timer que suga a `health` do jogador a cada segundo (1000ms). Ele começa a ouvir sons de alerta locais (`hazzard_enter.ogg`). Se ele correr para trás e a coordenada `X/Y` sair da `zona`, a função `stop_progressive_death` salva a vida dele. Tudo usando a arquitetura moderna baseada em eventos de passo!

Isso conclui a Trilogia do Modo Pacífico (Construtor, Interações e Zonas Ambientais). 
