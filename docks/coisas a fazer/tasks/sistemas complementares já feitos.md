Para dar vida à \*\*Imobiliária\*\* e aos \*\*Eventos\*\*, vamos modernizar os \*stubs\* que você já possui e conectá-los usando os recursos nativos do NVGT (como dicionários e timers). Faremos isso em duas etapas lógicas.



\### Mini-Task 17: Sistema de Imobiliária (Casas, Baús e Fechaduras)



O seu código antigo dependia de strings longas para salvar o baú (`apartamentoinv`) e de um sistema engessado de computador. Nós vamos unificar tudo isso em uma classe orientada a objetos moderna, onde o jogador compra um mapa privado, tranca a porta e usa o dicionário para guardar itens.



Abra o arquivo \*\*`server/includes/apartamento.nvgt`\*\* e substitua o conteúdo por este código:



```cpp

// ============================================================================

// SISTEMA DE IMOBILIÁRIA E CASAS (Mini-Task 17)

// ============================================================================



class player\_house {

&nbsp;   string owner;           // Dono da casa

&nbsp;   string map\_name;        // Mapa instanciado para a casa (ex: "casa\_joao")

&nbsp;   bool is\_locked;         // Porta trancada/Alarme ativado

&nbsp;   dictionary chest;       // Baú da casa: item\_name -> quantidade

&nbsp;   

&nbsp;   player\_house(string p\_owner, string p\_map) {

&nbsp;       owner = p\_owner;

&nbsp;       map\_name = p\_map;

&nbsp;       is\_locked = true;   // Vem trancada por padrão

&nbsp;   }

}



player\_house@\[] active\_houses;



// Comando: Comprar Casa (Executado no balcão da imobiliária)

void cmd\_comprarcasa(int player\_index) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   if(p is null) return;

&nbsp;   

&nbsp;   int preco\_casa = 15000; // 15 mil moedas

&nbsp;   

&nbsp;   // Verifica se já possui casa

&nbsp;   for(uint i = 0; i < active\_houses.length(); i++) {

&nbsp;       if(active\_houses\[i].owner == p.charname) {

&nbsp;           send\_reliable\_text(p.peer\_id, "say \[SISTEMA] Você já possui uma propriedade!", 0);

&nbsp;           return;

&nbsp;       }

&nbsp;   }

&nbsp;   

&nbsp;   if(p.gold < preco\_casa) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say \[SISTEMA] Você precisa de " + preco\_casa + " moedas para comprar uma casa.", 0);

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   // Desconta o dinheiro e cria a casa

&nbsp;   p.gold -= preco\_casa;

&nbsp;   string novo\_mapa = "casa\_" + p.charname;

&nbsp;   

&nbsp;   player\_house nova\_casa(p.charname, novo\_mapa);

&nbsp;   active\_houses.insert\_last(nova\_casa);

&nbsp;   

&nbsp;   // Concede o título de construtor temporário para ele colocar móveis (banheiro, pia) no próprio mapa

&nbsp;   add\_role(p.charname, "builder", "system", "Dono de casa");

&nbsp;   

&nbsp;   send\_reliable\_text(p.peer\_id, "play\_stationary trade\_success.ogg", 0);

&nbsp;   send\_reliable\_text(p.peer\_id, "say Parabéns! Você comprou uma casa. O mapa '" + novo\_mapa + "' é seu. Use /trancar para gerenciar a porta e /bau para guardar itens.", 0);

}



// Comando: Trancar/Destrancar a porta (Substitui o antigo sistema de Computador)

void cmd\_toggle\_lock(int player\_index) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   for(uint i = 0; i < active\_houses.length(); i++) {

&nbsp;       if(active\_houses\[i].owner == p.charname) {

&nbsp;           active\_houses\[i].is\_locked = !active\_houses\[i].is\_locked;

&nbsp;           string status = active\_houses\[i].is\_locked ? "trancada com alarme" : "destrancada";

&nbsp;           send\_reliable\_text(p.peer\_id, "say \[CASA] Sua casa agora está " + status + ".", 0);

&nbsp;           return;

&nbsp;       }

&nbsp;   }

}



// Comando: Guardar item no Baú

void cmd\_guardar\_bau(int player\_index, string item\_name, int qty) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   if(p.map != "casa\_" + p.charname) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say \[ERRO] Você precisa estar dentro da sua casa para usar o baú.", 0);

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   // Remove do inventário com segurança (Anti-dupe)

&nbsp;   if(remove\_item\_with\_sync(p, item\_name, qty)) {

&nbsp;       for(uint i = 0; i < active\_houses.length(); i++) {

&nbsp;           if(active\_houses\[i].owner == p.charname) {

&nbsp;               double current\_qty = 0;

&nbsp;               active\_houses\[i].chest.get(item\_name, current\_qty);

&nbsp;               active\_houses\[i].chest.set(item\_name, current\_qty + qty);

&nbsp;               send\_reliable\_text(p.peer\_id, "say \[BAÚ] Você guardou " + qty + "x " + item\_name + ".", 0);

&nbsp;               return;

&nbsp;           }

&nbsp;       }

&nbsp;   }

}



// Comando: Retirar item do Baú

void cmd\_retirar\_bau(int player\_index, string item\_name, int qty) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   if(p.map != "casa\_" + p.charname) return;

&nbsp;   

&nbsp;   for(uint i = 0; i < active\_houses.length(); i++) {

&nbsp;       if(active\_houses\[i].owner == p.charname) {

&nbsp;           double current\_qty = 0;

&nbsp;           if(active\_houses\[i].chest.get(item\_name, current\_qty) \&\& current\_qty >= qty) {

&nbsp;               active\_houses\[i].chest.set(item\_name, current\_qty - qty);

&nbsp;               add\_item\_with\_sync(p, item\_name, qty); // Adiciona de volta ao jogador

&nbsp;               send\_reliable\_text(p.peer\_id, "say \[BAÚ] Você retirou " + qty + "x " + item\_name + ".", 0);

&nbsp;           } else {

&nbsp;               send\_reliable\_text(p.peer\_id, "say \[ERRO] Quantidade insuficiente no baú.", 0);

&nbsp;           }

&nbsp;           return;

&nbsp;       }

&nbsp;   }

}

```

\*\*O que fizemos aqui?\*\*

Em vez do jogador precisar acessar um objeto "computador" complexo, ele simplesmente usa o comando `/trancar` de qualquer lugar, e a casa bloqueia acessos. Como ele recebe o cargo de `builder` dinamicamente ao comprar a casa, ele pode usar o seu menu existente de Construtor (F9) para `colocar\_banheiro`, `colocar\_pia`, e montar as paredes livremente dentro do mapa dele!



\*(Não se esqueça de adicionar uma checagem no seu arquivo de portas/teleportes (`door.nvgt` ou `portals.nvgt`) para impedir que jogadores entrem no `dest\_map` se ele for uma propriedade cujo `is\_locked` seja `true` e o jogador não for o `owner`).\*



---



\### Mini-Task 18: Eventos de Servidor (Arena PvP e Caça ao Tesouro)



Você já possui o \*skeleton\* da classe `game\_event` em \*\*`events.nvgt`\*\*. Para que eles ocorram sozinhos (agendamento automático, teleporte de jogadores e distribuição de prêmios), precisamos implementar o "motor" que roda no `events\_loop()`.



Abra \*\*`server/includes/events.nvgt`\*\*, procure a função `events\_loop()` que está vazia e substitua por este controlador de estados:



```cpp

// ============================================================================

// MOTOR DE EVENTOS AUTOMÁTICOS (Mini-Task 18)

// ============================================================================



void events\_loop() {

&nbsp;   for (uint i = 0; i < scheduled\_events.length(); i++) {

&nbsp;       game\_event@ e = scheduled\_events\[i];



&nbsp;       // 1. EVENTO AGENDADO -> INICIA REGISTRO

&nbsp;       if (e.state == EVENT\_SCHEDULED) {

&nbsp;           // Supondo que você use um timer para agendar, aqui ativamos o registro

&nbsp;           e.state = EVENT\_REGISTERING;

&nbsp;           server\_broadcast("say \[EVENTO GLOBAL] O evento '" + e.name + "' vai começar em 5 minutos! Digite /registerevent " + e.id + " para participar.", "");

&nbsp;           server\_broadcast("play\_stationary alarm.ogg", "");

&nbsp;           e.event\_timer.restart(); // Inicia contagem de registro

&nbsp;       }

&nbsp;       

&nbsp;       // 2. REGISTRO -> INICIA EVENTO E PUXA JOGADORES

&nbsp;       else if (e.state == EVENT\_REGISTERING \&\& e.event\_timer.elapsed >= (e.registration\_duration\_minutes \* 60000)) {

&nbsp;           if (e.participants.length() < uint(e.min\_participants)) {

&nbsp;               server\_broadcast("say \[EVENTO GLOBAL] O evento '" + e.name + "' foi cancelado por falta de participantes.", "");

&nbsp;               e.state = EVENT\_CANCELLED;

&nbsp;           } else {

&nbsp;               e.state = EVENT\_ACTIVE;

&nbsp;               server\_broadcast("say \[EVENTO GLOBAL] O evento '" + e.name + "' começou! Boa sorte aos participantes!", "");

&nbsp;               

&nbsp;               // Puxa todos os inscritos para a Arena/Mapa do Evento

&nbsp;               for (uint p = 0; p < e.participants.length(); p++) {

&nbsp;                   int p\_idx = get\_player\_index\_from(e.participants\[p].player\_name);

&nbsp;                   if (p\_idx > -1) {

&nbsp;                       // Cobra a taxa de entrada e teleporta

&nbsp;                       players\[p\_idx].gold -= e.entry\_fee\_gold;

&nbsp;                       move\_player\_to\_map(p\_idx, "arena\_evento", 10, 10);

&nbsp;                       send\_reliable\_text(players\[p\_idx].peer\_id, "play\_stationary teleport.ogg", 0);

&nbsp;                       send\_reliable\_text(players\[p\_idx].peer\_id, "say Você foi teleportado para o evento!", 0);

&nbsp;                   }

&nbsp;               }

&nbsp;               e.event\_timer.restart(); // Inicia contagem de duração do evento

&nbsp;           }

&nbsp;       }

&nbsp;       

&nbsp;       // 3. EVENTO ATIVO -> FINALIZA E PAGA AS RECOMPENSAS

&nbsp;       else if (e.state == EVENT\_ACTIVE \&\& e.event\_timer.elapsed >= (e.duration\_minutes \* 60000)) {

&nbsp;           e.state = EVENT\_COMPLETED;

&nbsp;           server\_broadcast("say \[EVENTO GLOBAL] O evento '" + e.name + "' foi concluído!", "");

&nbsp;           

&nbsp;           // Lógica de premiação (Ex: Dá Ouro e XP para todos que ainda estão vivos no mapa da arena)

&nbsp;           for (uint p = 0; p < e.participants.length(); p++) {

&nbsp;               int p\_idx = get\_player\_index\_from(e.participants\[p].player\_name);

&nbsp;               

&nbsp;               if (p\_idx > -1 \&\& players\[p\_idx].map == "arena\_evento" \&\& players\[p\_idx].health > 0) {

&nbsp;                   players\[p\_idx].gold += e.participation\_gold;

&nbsp;                   players\[p\_idx].xp += e.participation\_xp;

&nbsp;                   

&nbsp;                   send\_reliable\_text(players\[p\_idx].peer\_id, "say \[RECOMPENSA] Você sobreviveu e ganhou " + e.participation\_gold + " moedas e " + e.participation\_xp + " XP!", 0);

&nbsp;                   send\_reliable\_text(players\[p\_idx].peer\_id, "play\_stationary trade\_success.ogg", 0);

&nbsp;                   

&nbsp;                   // Teleporta o jogador de volta à zona segura

&nbsp;                   move\_player\_to\_map(p\_idx, "zona\_de\_seguranca", 5, 5);

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

```



\*\*Como conectar tudo:\*\*

1\. No seu `server.nvgt` (na função principal do loop do servidor `main` ou `tprincipais`), certifique-se de estar chamando `events\_loop();` a cada ciclo.

2\. O servidor agora consegue iniciar e fechar arenas sozinho, administrar o ouro, pagar quem sobrou e até usar a função nativa `move\_player\_to\_map` (que converte o antigo `changemap`) para trazer os guerreiros de volta à zona de segurança após o combate!



Avise-me quando tiver compilado essas funções! Se estiver tudo funcionando, o "Cardápio" final que nos resta seria explorar o \*\*Combate PvE Avançado (Dungeons/Missões)\*\*, ou habilitar a parte de \*\*Sobrevivência (Fome/Sede)\*\*! O que achou dessas arquiteturas?

