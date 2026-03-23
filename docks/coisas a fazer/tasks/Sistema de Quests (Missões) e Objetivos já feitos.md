Passo 1: O Motor de Quests (quests.nvgt)

O seu arquivo de quests já tem as definições das classes (quest\_definition e quest\_progress). Nós precisamos preencher os stubs de aceitar, progredir e completar as missões

1

...

.

Abra o arquivo server/includes/quests.nvgt e substitua as funções cmd\_acceptquest, quest\_update\_kill e cmd\_completequest por este código completo e seguro:

// ============================================================================

// NÚCLEO DO SISTEMA DE MISSÕES / QUESTS (Mini-Task 19)

// ============================================================================



// Comando: Aceitar uma Quest (Chamado ao falar com um NPC)

void cmd\_acceptquest(int player\_index, int quest\_id) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   player\_quest\_log@ qlog = get\_player\_quest\_log(p.charname);



&nbsp;   // Verifica se a missão existe no banco de dados de quests

&nbsp;   quest\_definition@ qdef = get\_quest\_by\_id(quest\_id);

&nbsp;   if(qdef is null) return;



&nbsp;   // Valida o nível do jogador

&nbsp;   if(p.level < qdef.required\_level) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say \[Sistema] Nível " + qdef.required\_level + " necessário para esta missão.", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Verifica limite de missões ativas

&nbsp;   if(qlog.active\_quests.length() >= uint(qlog.max\_active\_quests)) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say \[Sistema] Você já atingiu o limite de missões ativas.", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Verifica se já foi completada (caso não seja repetível/diária)

&nbsp;   if(!qdef.is\_repeatable \&\& qlog.completed\_quests.find("" + quest\_id) >= 0) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say \[Sistema] Você já concluiu esta missão.", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Aceita a missão e inicializa os contadores de progresso em 0

&nbsp;   quest\_progress qp;

&nbsp;   qp.quest\_id = quest\_id;

&nbsp;   qp.status = QUEST\_STATUS\_ACTIVE;

&nbsp;   qp.accepted\_time.restart();

&nbsp;   

&nbsp;   string\[] objs = qdef.objectives.get\_keys();

&nbsp;   for(uint i = 0; i < objs.length(); i++) {

&nbsp;       qp.progress.set(objs\[i], 0.0);

&nbsp;   }

&nbsp;   

&nbsp;   qlog.active\_quests.insert\_last(qp);



&nbsp;   // Feedback audiovisual nativo para o cliente

&nbsp;   send\_reliable\_text(p.peer\_id, "play\_stationary quest\_accept.ogg", 0);

&nbsp;   send\_reliable\_text(p.peer\_id, "say \[Nova Missão] " + qdef.name + " - " + qdef.description, 0);

}



// Atualiza o progresso quando o jogador matar um monstro

void quest\_update\_kill(string player\_name, string monster\_name) {

&nbsp;   player\_quest\_log@ qlog = get\_player\_quest\_log(player\_name);

&nbsp;   int p\_idx = get\_player\_index\_from(player\_name);

&nbsp;   

&nbsp;   for(uint i = 0; i < qlog.active\_quests.length(); i++) {

&nbsp;       if(qlog.active\_quests\[i].status != QUEST\_STATUS\_ACTIVE) continue;



&nbsp;       quest\_definition@ qdef = get\_quest\_by\_id(qlog.active\_quests\[i].quest\_id);

&nbsp;       if(qdef.type != QUEST\_KILL) continue; // Só processa missões de caça



&nbsp;       // Verifica se este monstro faz parte do objetivo da missão

&nbsp;       double current\_qty = 0;

&nbsp;       if(qlog.active\_quests\[i].progress.get(monster\_name, current\_qty)) {

&nbsp;           double target\_qty = 0;

&nbsp;           qdef.objectives.get(monster\_name, target\_qty);



&nbsp;           // Se ainda não atingiu a meta, soma 1

&nbsp;           if(current\_qty < target\_qty) {

&nbsp;               qlog.active\_quests\[i].progress.set(monster\_name, current\_qty + 1.0);

&nbsp;               

&nbsp;               if(p\_idx > -1) {

&nbsp;                   if(current\_qty + 1.0 >= target\_qty) {

&nbsp;                       send\_reliable\_text(players\[p\_idx].peer\_id, "play\_stationary quest\_objective.ogg", 0);

&nbsp;                       send\_reliable\_text(players\[p\_idx].peer\_id, "say \[Objetivo Concluído] Eliminar " + monster\_name + ".", 0);

&nbsp;                   } else {

&nbsp;                       // Opcional: Feedback de progresso (Ex: 3/10)

&nbsp;                       send\_reliable\_text(players\[p\_idx].peer\_id, "say Progresso: " + (current\_qty + 1) + "/" + target\_qty + " " + monster\_name + "s.", 0);

&nbsp;                   }

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;   }

}



// Comando: Completar a missão e receber recompensas

void cmd\_completequest(int player\_index, int quest\_id) {

&nbsp;   player@ p = players\[player\_index];

&nbsp;   player\_quest\_log@ qlog = get\_player\_quest\_log(p.charname);



&nbsp;   for(uint i = 0; i < qlog.active\_quests.length(); i++) {

&nbsp;       if(qlog.active\_quests\[i].quest\_id == quest\_id) {

&nbsp;           quest\_definition@ qdef = get\_quest\_by\_id(quest\_id);



&nbsp;           // 1. Auditoria de Segurança: Verifica se TODOS os objetivos foram cumpridos

&nbsp;           string\[] objs = qdef.objectives.get\_keys();

&nbsp;           for(uint j = 0; j < objs.length(); j++) {

&nbsp;               double current = 0, target = 0;

&nbsp;               qlog.active\_quests\[i].progress.get(objs\[j], current);

&nbsp;               qdef.objectives.get(objs\[j], target);

&nbsp;               

&nbsp;               if(current < target) {

&nbsp;                   send\_reliable\_text(p.peer\_id, "say \[Sistema] Você ainda não completou todos os objetivos desta missão.", 0);

&nbsp;                   return;

&nbsp;               }

&nbsp;           }



&nbsp;           // 2. Pagamento das Recompensas (Reaproveitando o sistema sync seguro)

&nbsp;           string\[] rews = qdef.rewards.get\_keys();

&nbsp;           for(uint j = 0; j < rews.length(); j++) {

&nbsp;               double amt = 0;

&nbsp;               qdef.rewards.get(rews\[j], amt);

&nbsp;               

&nbsp;               if(rews\[j] == "gold") {

&nbsp;                   p.gold += int(amt);

&nbsp;                   send\_reliable\_text(p.peer\_id, "say Você recebeu " + amt + " moedas de ouro.", 0);

&nbsp;               } else if(rews\[j] == "xp") {

&nbsp;                   ganhaxp(player\_index, int(amt)); // Usa o sistema global de XP

&nbsp;               } else {

&nbsp;                   add\_item\_with\_sync(p, rews\[j], int(amt)); // Injeta o item diretamente no bolso via JSON

&nbsp;                   send\_reliable\_text(p.peer\_id, "say Você recebeu: " + rews\[j] + " (" + amt + "x).", 0);

&nbsp;               }

&nbsp;           }



&nbsp;           // 3. Finaliza a missão

&nbsp;           qlog.active\_quests.remove\_at(i);

&nbsp;           qlog.completed\_quests.insert\_last("" + quest\_id);



&nbsp;           send\_reliable\_text(p.peer\_id, "play\_stationary quest\_complete.ogg", 0);

&nbsp;           send\_reliable\_text(p.peer\_id, "say \[Missão Concluída] " + qdef.name + "!", 0);

&nbsp;           return;

&nbsp;       }

&nbsp;   }

}

Passo 2: O Gancho no Combate (Servidor)

A inteligência das Quests está pronta, mas o servidor precisa avisar o sistema de missões sempre que um monstro for abatido. Nós já fizemos a inteligência artificial dos NPCs na Task 14, então plugar isso é muito fácil.

Abra o arquivo onde fica a lógica de morte dos NPCs (server/includes/npc.nvgt ou monstruo.nvgt, dentro daquele npc\_global\_loop que fizemos

4

5

).

Logo após a linha onde a vida do monstro chega a 0 e ele morre, adicione esta única chamada:

&nbsp;   // (Dentro de npc\_global\_loop ou monstruo\_global\_loop)

&nbsp;   if(m.vida <= 0 \&\& !m.morreu) {

&nbsp;       

&nbsp;       // ... (seu código de tocar som de morte, dropar o loot, etc) ...



&nbsp;       // Notifica o sistema de missões que o jogador abateu essa criatura!

&nbsp;       if(m.golpeado != "") {

&nbsp;           quest\_update\_kill(m.golpeado, m.tipo); // m.tipo é o nome do monstro, ex: "lobo"

&nbsp;       }

&nbsp;       

&nbsp;       m.morreu = true;

&nbsp;   }

Por que essa estrutura é tão poderosa e escalável?

1\. É orientada a eventos: Em vez de ter comandos rodando o tempo todo verificando se a missão acabou, ela só trabalha quando a criatura morre. Zero peso no processador do servidor.

2\. Reaproveitamento Extremo: O comando cmd\_completequest usa a classe add\_item\_with\_sync (da época que você criou o inventário JSON). Isso significa que as recompensas de quests ficam atreladas ao peso, sincronizam fisicamente com o NVDA no cliente em tempo real, e são gravadas com perfeição.





