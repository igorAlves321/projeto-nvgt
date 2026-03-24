Passo 1: A Roleta, Caixas e Recompensas Diárias (daily\_rewards.nvgt)

Abra o arquivo server/includes/daily\_rewards.nvgt. Ele contém vários stubs (funções vazias) de comandos como cmd\_dailyreward e cmd\_luckywheel. Substitua todo o conteúdo das funções vazias por este código funcional:

// ============================================================================

// SISTEMA DE RECOMPENSAS DIÁRIAS, ROLETA E CAIXAS (Mini-Task 21 - Parte 1)

// ============================================================================



// Comando: Coletar recompensa diária (/claimdaily)

void cmd\_dailyreward(int player\_index) {

&#x20;   player@ p = players\[player\_index];

&#x20;   daily\_reward\_tracker@ dt = get\_daily\_tracker(p.charname);



&#x20;   if(dt.claimed\_today) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Sistema] Você já coletou sua recompensa de hoje! Volte amanhã.", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Incrementa a sequência (streak)

&#x20;   dt.current\_streak++;

&#x20;   dt.total\_days++;

&#x20;   dt.claimed\_today = true;

&#x20;   dt.last\_claim.restart();



&#x20;   // Recompensa baseada na sequência (Máximo de 1500 moedas por dia)

&#x20;   int gold\_reward = 150 \* dt.current\_streak;

&#x20;   if(gold\_reward > 1500) gold\_reward = 1500; 

&#x20;   

&#x20;   p.gold += gold\_reward;

&#x20;   

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary trade\_success.ogg", 0);

&#x20;   send\_reliable\_text(p.peer\_id, "say \[Diária] Você coletou " + gold\_reward + " moedas! Sua sequência é de " + dt.current\_streak + " dias consecutivos.", 0);

&#x20;   

&#x20;   // A cada 7 dias seguidos, o jogador ganha uma Caixa Misteriosa!

&#x20;   if(dt.current\_streak % 7 == 0) {

&#x20;       dt.box\_available = true;

&#x20;       send\_reliable\_text(p.peer\_id, "play\_stationary levelup.ogg", 0);

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Sistema] PARABÉNS! Você ganhou uma Caixa Misteriosa por completar 7 dias! Digite /box para abrir.", 0);

&#x20;   }

}



// Comando: Roda da Sorte (/spin)

void cmd\_luckywheel(int player\_index) {

&#x20;   player@ p = players\[player\_index];

&#x20;   daily\_reward\_tracker@ dt = get\_daily\_tracker(p.charname);



&#x20;   if(!dt.spin\_available) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Roleta] Você não tem giros disponíveis no momento. Volte amanhã!", 0);

&#x20;       return;

&#x20;   }



&#x20;   dt.spin\_available = false;

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary roleta.ogg", 0); // Você precisará ter esse som

&#x20;   

&#x20;   int prize = random(1, 100);



&#x20;   if(prize <= 50) { // 50% de chance

&#x20;       p.gold += 300;

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Roleta] A roda parou em... 300 Moedas!", 0);

&#x20;   } else if(prize <= 80) { // 30% de chance

&#x20;       ganhaxp(player\_index, 500); // Dá XP usando nosso sistema da Task 17

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Roleta] A roda parou em... 500 de Experiência!", 0);

&#x20;   } else if(prize <= 95) { // 15% de chance

&#x20;       add\_item\_with\_sync(p, "pocao\_vida", 5); 

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Roleta] Sorte! A roda parou em... 5 Poções de Vida!", 0);

&#x20;   } else { // 5% de chance

&#x20;       dt.box\_available = true;

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Roleta] JACKPOT!!! A roda parou em... CAIXA MISTERIOSA! Digite /box para abrir!", 0);

&#x20;   }

}



// Comando: Abrir Caixa Misteriosa (/box)

void cmd\_mysterybox(int player\_index) {

&#x20;   player@ p = players\[player\_index];

&#x20;   daily\_reward\_tracker@ dt = get\_daily\_tracker(p.charname);



&#x20;   if(!dt.box\_available) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Caixa] Você não possui nenhuma Caixa Misteriosa.", 0);

&#x20;       return;

&#x20;   }



&#x20;   dt.box\_available = false;

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary open\_box.ogg", 0);

&#x20;   

&#x20;   int prize = random(1, 3);

&#x20;   if(prize == 1) {

&#x20;       p.gold += 5000;

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Caixa Misteriosa] UAU! Você encontrou um Saco de Ouro contendo 5000 moedas!", 0);

&#x20;   } else if(prize == 2) {

&#x20;       add\_item\_with\_sync(p, "espada\_lendaria", 1);

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Caixa Misteriosa] ÉPICO! Você encontrou uma Espada Lendária!", 0);

&#x20;   } else {

&#x20;       add\_item\_with\_sync(p, "diamante", 5);

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Caixa Misteriosa] BRILHANTE! Você encontrou 5 Diamantes!", 0);

&#x20;   }

}



// Verificar daily no login do jogador

void check\_daily\_on\_login(int player\_index) {

&#x20;   daily\_reward\_tracker@ dt = get\_daily\_tracker(players\[player\_index].charname);

&#x20;   

&#x20;   // Verifica se passaram 24 horas (86.400.000 ms) desde o último reset

&#x20;   if(dt.last\_reset.elapsed >= 86400000) {

&#x20;       // Se passaram mais de 48h (172.800.000 ms), ele quebrou a sequência diária!

&#x20;       if(dt.last\_reset.elapsed >= 172800000) {

&#x20;           dt.current\_streak = 0;

&#x20;           send\_reliable\_text(players\[player\_index].peer\_id, "say \[Sistema] Você perdeu um dia de jogo e sua sequência diária foi zerada.", 0);

&#x20;       }

&#x20;       

&#x20;       dt.claimed\_today = false;

&#x20;       dt.spin\_available = true; // Ganha um giro grátis na roleta por dia

&#x20;       dt.last\_reset.restart();

&#x20;       

&#x20;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[Recompensas] Um novo dia começou! Use /claimdaily para pegar seu bônus de ouro e /spin para girar a Roleta da Sorte!", 0);

&#x20;   }

}

Passo 2: O Sistema de Conquistas e Títulos (achievements.nvgt)

As conquistas darão recompensas e "títulos" que o jogador pode exibir para os outros. Abra server/includes/achievements.nvgt e substitua as funções init\_achievements\_system e update\_achievement\_progress por:

// ============================================================================

// SISTEMA DE CONQUISTAS E TÍTULOS (Mini-Task 21 - Parte 2)

// ============================================================================



void init\_achievements\_system() {

&#x20;   achievement\_database.resize(0);

&#x20;   

&#x20;   // Conquista 1: O Caçador (Matar monstros)

&#x20;   achievement\_definition ach1;

&#x20;   ach1.id = 1;

&#x20;   ach1.name = "Primeiro Sangue";

&#x20;   ach1.description = "Derrote 10 monstros no mundo.";

&#x20;   ach1.category = ACH\_COMBAT;

&#x20;   ach1.points = 15;

&#x20;   ach1.requirements.set("kills", 10.0);

&#x20;   ach1.title\_reward = "Caçador Aprendiz";

&#x20;   achievement\_database.insert\_last(ach1);

&#x20;   

&#x20;   // Conquista 2: O Magnata (Juntar moedas)

&#x20;   achievement\_definition ach2;

&#x20;   ach2.id = 2;

&#x20;   ach2.name = "Caminho para a Riqueza";

&#x20;   ach2.description = "Acumule um total de 10.000 moedas de ouro.";

&#x20;   ach2.category = ACH\_ECONOMY;

&#x20;   ach2.points = 50;

&#x20;   ach2.requirements.set("gold\_earned", 10000.0);

&#x20;   ach2.title\_reward = "O Magnata";

&#x20;   achievement\_database.insert\_last(ach2);

&#x20;   

&#x20;   debug\_log("🏆 Sistema de Conquistas Inicializado (" + achievement\_database.length() + " registradas).");

}



// Atualizar progresso de achievement e verificar desbloqueio

void update\_achievement\_progress(string player\_name, string req\_type, int value) {

&#x20;   achievement\_progress@ ap = get\_player\_achievements(player\_name);

&#x20;   int p\_idx = get\_player\_index\_from(player\_name);

&#x20;   

&#x20;   for(uint i = 0; i < achievement\_database.length(); i++) {

&#x20;       int ach\_id = achievement\_database\[i].id;

&#x20;       

&#x20;       // Pula se já possui essa conquista desbloqueada

&#x20;       if(ap.unlocked\_achievements.find("" + ach\_id) >= 0) continue;

&#x20;       

&#x20;       double target\_val = 0;

&#x20;       // Se a conquista atual possuir o tipo de requerimento que estamos atualizando (ex: "kills")

&#x20;       if(achievement\_database\[i].requirements.get(req\_type, target\_val)) {

&#x20;           

&#x20;           double current\_val = 0;

&#x20;           string prog\_key = ach\_id + "\_" + req\_type;

&#x20;           ap.progress.get(prog\_key, current\_val);

&#x20;           

&#x20;           current\_val += value; // Adiciona o progresso

&#x20;           ap.progress.set(prog\_key, current\_val);

&#x20;           

&#x20;           // Verifica se atingiu a meta para desbloquear

&#x20;           if(current\_val >= target\_val) {

&#x20;               ap.unlocked\_achievements.insert\_last("" + ach\_id);

&#x20;               ap.total\_points += achievement\_database\[i].points;

&#x20;               

&#x20;               if(achievement\_database\[i].title\_reward != "") {

&#x20;                   ap.unlocked\_titles.insert\_last(achievement\_database\[i].title\_reward);

&#x20;               }

&#x20;               

&#x20;               // Dispara aviso audiovisual para o jogador

&#x20;               if(p\_idx > -1) {

&#x20;                   send\_reliable\_text(players\[p\_idx].peer\_id, "play\_stationary achievement.ogg", 0);

&#x20;                   send\_reliable\_text(players\[p\_idx].peer\_id, "say \[CONQUISTA DESBLOQUEADA] " + achievement\_database\[i].name + " (" + achievement\_database\[i].points + " Pontos)!", 0);

&#x20;                   if(achievement\_database\[i].title\_reward != "") {

&#x20;                       send\_reliable\_text(players\[p\_idx].peer\_id, "say \[TÍTULO] Você ganhou o título: '" + achievement\_database\[i].title\_reward + "'. Use /settitle para exibir no seu nome!", 0);

&#x20;                   }

&#x20;               }

&#x20;           }

&#x20;       }

&#x20;   }

}

Passo 3: Plugar tudo no Motor do Servidor! 🔧

Agora que as funções existem, só precisamos chamar elas nos momentos certos.

A) Para rodar o Login Diário: Abra seu arquivo auth.nvgt. Logo após a linha onde a sessão do jogador é criada com sucesso (spawn\_player\_session(...) no login), adicione:

&#x20;   int p\_idx = get\_player\_index\_from(username);

&#x20;   if(p\_idx > -1) {

&#x20;       check\_daily\_on\_login(p\_idx);

&#x20;   }

B) Para progredir a Conquista de "Kills": Lembra do nosso npc\_global\_loop na Task 14 (em npc.nvgt ou monstruo.nvgt), no exato momento onde o monstro morre e dropa os itens? Adicione lá:

&#x20;   if(m.golpeado != "") {

&#x20;       update\_achievement\_progress(m.golpeado, "kills", 1);

&#x20;   }

C) Para progredir a Conquista de "Dinheiro": Em systems\_advanced.nvgt (na função ganhaxp que criamos na task passada), logo abaixo de players\[player\_index].gold += gold\_amount, adicione:

&#x20;   if(gold\_amount > 0) {

&#x20;       update\_achievement\_progress(players\[player\_index].charname, "gold\_earned", gold\_amount);

&#x20;   }

O que o jogador sente agora? 😍

1\. Todo dia que ele fizer login, ele ouvirá: "Um novo dia começou! Use /claimdaily e /spin!"

2\. A cada 7 dias seguidos entrando no servidor, ele ganha uma caixa que pode vir armas lendárias ou muito ouro (/box).

3\. Quando ele matar o 10º Goblin dele, uma música triunfal toca (achievement.ogg), e todo o servidor vai começar a ver o nome dele no chat e no F5 como "Caçador Aprendiz Joãozinho".

