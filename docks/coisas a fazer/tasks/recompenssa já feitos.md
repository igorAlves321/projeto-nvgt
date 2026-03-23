Vamos para a Mini-Task 16: Sistema de Caçadores de Recompensas.

Passo 1: A Lógica Central (bounty.nvgt)

Abra o arquivo server/includes/bounty.nvgt. Você tem os esqueletos das funções lá

3

. Substitua todo o conteúdo pelo código abaixo, que fará o processamento financeiro e os anúncios globais:

// ============================================================================

// SISTEMA DE RECOMPENSAS (BOUNTY) - Mini-Task 16

// ============================================================================



// Valor mínimo para colocar a cabeça de alguém a prêmio

const int BOUNTY\_MIN\_VALUE = 100;



// Coloca uma recompensa na cabeça de um jogador

bool set\_bounty(int target\_index, int setter\_index, int value) {

&nbsp;   if(target\_index < 0 || target\_index >= int(players.length())) return false;

&nbsp;   if(setter\_index < 0 || setter\_index >= int(players.length())) return false;



&nbsp;   player@ target = players\[target\_index];

&nbsp;   player@ setter = players\[setter\_index];



&nbsp;   // Validações

&nbsp;   if(value < BOUNTY\_MIN\_VALUE) {

&nbsp;       send\_reliable\_text(setter.peer\_id, "say \[SISTEMA] O valor minimo da recompensa e " + BOUNTY\_MIN\_VALUE + " moedas.", 0);

&nbsp;       return false;

&nbsp;   }

&nbsp;   if(setter.gold < value) {

&nbsp;       send\_reliable\_text(setter.peer\_id, "say \[SISTEMA] Voce nao tem ouro suficiente no inventario.", 0);

&nbsp;       return false;

&nbsp;   }

&nbsp;   if(target.charname == setter.charname) {

&nbsp;       send\_reliable\_text(setter.peer\_id, "say \[SISTEMA] Voce nao pode colocar uma recompensa na propria cabeca!", 0);

&nbsp;       return false;

&nbsp;   }



&nbsp;   // Desconta o ouro do mandante

&nbsp;   setter.gold -= value;



&nbsp;   // Aplica a recompensa no alvo (soma se já houver uma recompensa ativa)

&nbsp;   target.bounty\_on\_head = 1;

&nbsp;   target.bounty\_value += value; 

&nbsp;   target.bounty\_owner = setter.charname;

&nbsp;   target.bounty\_active = 1;



&nbsp;   // Anúncio global

&nbsp;   server\_broadcast("say \[CAÇADA] " + setter.charname + " colocou uma recompensa de " + value + " moedas pela cabeca de " + target.charname + "!", "");

&nbsp;   server\_broadcast("play\_stationary alarm.ogg", ""); // Opcional: Tocar um som global

&nbsp;   

&nbsp;   return true;

}



// Processa o pagamento quando um jogador procurado é morto

void process\_bounty\_kill(int killer\_index, int victim\_index) {

&nbsp;   if(killer\_index < 0 || killer\_index >= int(players.length())) return;

&nbsp;   if(victim\_index < 0 || victim\_index >= int(players.length())) return;



&nbsp;   player@ killer = players\[killer\_index];

&nbsp;   player@ victim = players\[victim\_index];



&nbsp;   // Verifica se a vítima tinha a cabeça a prêmio

&nbsp;   if(victim.bounty\_on\_head == 1 \&\& victim.bounty\_active == 1) {

&nbsp;       int reward = victim.bounty\_value;



&nbsp;       // Transfere o ouro para o assassino/caçador

&nbsp;       killer.gold += reward;



&nbsp;       // Remove o status de procurado da vítima

&nbsp;       victim.bounty\_on\_head = 0;

&nbsp;       victim.bounty\_value = 0;

&nbsp;       victim.bounty\_owner = "";

&nbsp;       victim.bounty\_active = 0;

&nbsp;       victim.bounty\_online\_time = 0;



&nbsp;       // Anúncio global da vitória

&nbsp;       server\_broadcast("say \[CAÇADA CONCLUIDA] " + killer.charname + " eliminou o procurado " + victim.charname + " e recebeu a recompensa de " + reward + " moedas!", "");

&nbsp;       send\_reliable\_text(killer.peer\_id, "play\_stationary trade\_success.ogg", 0);

&nbsp;   }

}



// Remove a recompensa (pode ser usado por admins)

bool remove\_bounty(int target\_index) {

&nbsp;   if(target\_index < 0 || target\_index >= int(players.length())) return false;

&nbsp;   player@ target = players\[target\_index];

&nbsp;   

&nbsp;   target.bounty\_on\_head = 0;

&nbsp;   target.bounty\_value = 0;

&nbsp;   target.bounty\_owner = "";

&nbsp;   target.bounty\_active = 0;

&nbsp;   return true;

}

Passo 2: Os Comandos dos Jogadores (commands.nvgt)

Agora precisamos permitir que os jogadores digitem /bounty Joao 500 para acionar a função que acabamos de criar.

Abra o arquivo server/includes/commands.nvgt. Localize a seção referente ao Sistema de Recompensas (por volta do comentário "SISTEMA DE RECOMPENSAS (BOUNTY)"

4

) e atualize os comandos:

// Comando /bounty - Colocar recompensa na cabeça de um jogador

bool cmd\_bounty(player@ player, string\[] args) {

&nbsp;   if(args.length() < 2) {

&nbsp;       player.send\_message("say Uso: /bounty <jogador> <valor>");

&nbsp;       player.send\_message("say Valor minimo: 100 moedas");

&nbsp;       return false;

&nbsp;   }

&nbsp;   

&nbsp;   string target\_name = args;

&nbsp;   int value = parse\_int(args\[5]);

&nbsp;   

&nbsp;   int setter\_idx = get\_player\_index\_from(player.charname);

&nbsp;   int target\_idx = get\_player\_index\_from(target\_name);

&nbsp;   

&nbsp;   if(target\_idx == -1) {

&nbsp;       player.send\_message("say \[ERRO] Jogador '" + target\_name + "' nao esta online.");

&nbsp;       return false;

&nbsp;   }

&nbsp;   

&nbsp;   return set\_bounty(target\_idx, setter\_idx, value);

}



// Comando /checkbounty - Ver recompensa na cabeça de um jogador

bool cmd\_checkbounty(player@ player, string\[] args) {

&nbsp;   if(args.length() < 1) {

&nbsp;       player.send\_message("say Uso: /checkbounty <jogador>");

&nbsp;       return false;

&nbsp;   }

&nbsp;   

&nbsp;   int target\_idx = get\_player\_index\_from(args);

&nbsp;   if(target\_idx == -1) {

&nbsp;       player.send\_message("say \[ERRO] Jogador nao encontrado.");

&nbsp;       return false;

&nbsp;   }

&nbsp;   

&nbsp;   player@ target = players\[target\_idx];

&nbsp;   if(target.bounty\_on\_head == 1) {

&nbsp;       player.send\_message("say \[BOUNTY] " + target.charname + " esta sendo procurado por " + target.bounty\_value + " moedas! (Mandante: " + target.bounty\_owner + ")");

&nbsp;   } else {

&nbsp;       player.send\_message("say \[BOUNTY] Nao ha nenhuma recompensa pela cabeca de " + target.charname + ".");

&nbsp;   }

&nbsp;   return true;

}

Passo 3: Plugar a Recompensa no Combate (combat.nvgt)

A última coisa que falta é fazer com que o servidor verifique se o jogador que acabou de morrer tinha uma recompensa, pagando o atirador

5

6

.

Vá no arquivo onde a morte do jogador PvP é processada. Pode ser no combat.nvgt (dentro de execute\_attack ou end\_combat onde o HP do defensor chega a 0) ou no loop de projéteis (bullet.nvgt).

Basta adicionar a chamada da nossa função logo após confirmar que o jogador morreu pelas mãos de outro jogador:

&nbsp;   // Onde a morte do jogador é confirmada (exemplo):

&nbsp;   if (defender.hp <= 0) {

&nbsp;       // ... (código de morte existente, dropar loot, etc)

&nbsp;       

&nbsp;       // DISPARA O PAGAMENTO DA RECOMPENSA (Caso exista)

&nbsp;       int killer\_idx = get\_player\_index\_from(attacker.charname);

&nbsp;       int victim\_idx = get\_player\_index\_from(defender.charname);

&nbsp;       

&nbsp;       process\_bounty\_kill(killer\_idx, victim\_idx); // <--- Adicione esta linha!

&nbsp;   }

O que acontece agora na gameplay?

1\. O jogador A fica bravo porque o jogador B roubou seus monstros.

2\. O jogador A digita /bounty JogadorB 5000. O servidor retira 5.000 moedas do inventário dele e dá um grito no chat global avisando a todos os jogadores

3

.

3\. Todos os assassinos do servidor vão começar a caçar o Jogador B. Eles podem usar /checkbounty JogadorB para ver se o prêmio ainda está de pé

7

.

4\. Se o Jogador C matar o Jogador B no mapa, a função process\_bounty\_kill detecta a morte, envia as 5.000 moedas silenciosamente para o inventário do Jogador C, e anuncia no chat global que a caçada foi concluída

5

