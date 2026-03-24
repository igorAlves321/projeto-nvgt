Chegou a hora de trazer o desafio real de sobrevivência para o seu MMORPG! 🍖💧



Até agora o jogador só se preocupava em fugir de monstros, mas com a \*\*Mini-Task 22: Sobrevivência e Consumíveis\*\*, a \*\*Fome\*\* e a \*\*Sede\*\* serão os maiores inimigos dele. Nós vamos configurar a classe `consumable\_effect` para restaurar esses atributos e criar o loop que drena as necessidades vitais com o passar do tempo.



E o melhor: como já temos o `inventory\_sync.nvgt` funcionando, consumir itens é 100% à prova de duplicação.



\### Passo 1: O Núcleo de Consumíveis (`consumables.nvgt`)



Abra o seu arquivo \*\*`server/includes/consumables.nvgt`\*\*. Nós vamos modernizar os \*stubs\* e criar os itens de sobrevivência básicos. Substitua o código existente por este:



```cpp

// ============================================================================

// SISTEMA DE SOBREVIVÊNCIA E CONSUMÍVEIS (Mini-Task 22)

// ============================================================================



class consumable\_effect {

&#x20;   string item\_name;

&#x20;   string effect\_type;  // "health", "food", "drink"

&#x20;   int value;           // Valor restaurado (HP ou Fome)

&#x20;   int thirst\_reduce;   // Valor restaurado de Sede

&#x20;   string sound;        // Som ao usar (ex: drink.ogg, eat.ogg)

&#x20;   string message;      // Mensagem mostrada ao jogador



&#x20;   consumable\_effect(string i, string et, int v, int tr = 0, string s = "", string m = "") {

&#x20;       item\_name = i;

&#x20;       effect\_type = et;

&#x20;       value = v;

&#x20;       thirst\_reduce = tr;

&#x20;       sound = s;

&#x20;       message = m;

&#x20;   }

}



dictionary consumables;

timer survival\_timer; // Timer global para drenar fome e sede



// 1. INICIALIZAÇÃO DOS ITENS

void init\_consumables\_system() {

&#x20;   // Bebidas (Restauram muita Sede)

&#x20;   consumables.set("agua", consumable\_effect("agua", "drink", 0, 40, "drink.ogg", "Você bebeu água fresca. Saciou 40 de Sede!"));

&#x20;   consumables.set("refrigerante", consumable\_effect("refrigerante", "drink", 5, 25, "drink.ogg", "Você bebeu um refrigerante. +5 HP e -25 Sede!"));

&#x20;   

&#x20;   // Comidas (Restauram muita Fome)

&#x20;   consumables.set("comida", consumable\_effect("comida", "food", 30, 0, "eat.ogg", "Você comeu uma refeição quente. -30 Fome!"));

&#x20;   consumables.set("maca", consumable\_effect("maca", "food", 10, 5, "eat.ogg", "Você comeu uma maçã suculenta. -10 Fome e -5 Sede."));

&#x20;   

&#x20;   // Poções (Restauram HP)

&#x20;   consumables.set("pocao\_vida", consumable\_effect("pocao\_vida", "health", 50, 0, "drink.ogg", "Você tomou uma Poção de Vida! +50 HP."));

&#x20;   

&#x20;   debug\_log("🍔 Sistema de Sobrevivência inicializado com " + consumables.get\_size() + " consumíveis.");

}



// 2. FUNÇÃO DE USAR O ITEM

bool use\_item(int player\_index, string item\_name) {

&#x20;   if(player\_index < 0 || player\_index >= int(players.length())) return false;

&#x20;   player@ p = players\[player\_index];



&#x20;   consumable\_effect@ effect;

&#x20;   if(!consumables.get(item\_name, @effect)) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Sistema] O item " + item\_name + " não pode ser consumido.", 0);

&#x20;       return false;

&#x20;   }



&#x20;   // Tenta remover o item do inventário real (Segurança Anti-dupe)

&#x20;   if(remove\_item\_with\_sync(p, item\_name, 1)) {

&#x20;       

&#x20;       // Aplica o Efeito Principal

&#x20;       if(effect.effect\_type == "health") {

&#x20;           p.hp += effect.value;

&#x20;           if(p.hp > p.max\_hp) p.hp = p.max\_hp;

&#x20;       } 

&#x20;       else if(effect.effect\_type == "food") {

&#x20;           p.fome -= effect.value;

&#x20;           if(p.fome < 0) p.fome = 0;

&#x20;       }

&#x20;       else if(effect.effect\_type == "drink") {

&#x20;           // Apenas para diferenciar categoricamente

&#x20;       }



&#x20;       // Aplica redução de Sede (Funciona em comidas e bebidas)

&#x20;       if(effect.thirst\_reduce > 0) {

&#x20;           p.nsede -= effect.thirst\_reduce;

&#x20;           if(p.nsede < 0) p.nsede = 0;

&#x20;       }



&#x20;       // Feedback de Som e Mensagem

&#x20;       if(effect.sound != "") {

&#x20;           server\_broadcast("play\_body " + effect.sound + " " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&#x20;           send\_reliable\_text(p.peer\_id, "play\_stationary " + effect.sound, 0);

&#x20;       }

&#x20;       if(effect.message != "") send\_reliable\_text(p.peer\_id, "say " + effect.message, 0);



&#x20;       // Notifica o cliente da nova Vida/Fome/Sede para atualizar a interface

&#x20;       send\_reliable\_text(p.peer\_id, "UPDATE:health|" + p.hp, 0);

&#x20;       

&#x20;       return true;

&#x20;   }



&#x20;   send\_reliable\_text(p.peer\_id, "say \[Erro] Você não tem esse item na mochila.", 0);

&#x20;   return false;

}



// 3. MOTOR DE SOBREVIVÊNCIA (Aumento de Fome/Sede com o tempo)

void survival\_loop() {

&#x20;   // A cada 60 segundos, aumenta a fome e a sede dos jogadores online

&#x20;   if(survival\_timer.elapsed >= 60000) {

&#x20;       survival\_timer.restart();

&#x20;       

&#x20;       for(uint i = 0; i < players.length(); i++) {

&#x20;           player@ p = players\[i];

&#x20;           if(p !is null \&\& p.hp > 0 \&\& !p.afk \&\& p.admin\_status == false) {

&#x20;               

&#x20;               p.fome += 2;  // Aumenta 2% de fome por minuto

&#x20;               p.nsede += 3; // Sede aumenta mais rápido (3% por minuto)



&#x20;               // Dano por inanição (Fome no limite)

&#x20;               if(p.fome >= 100) {

&#x20;                   p.fome = 100;

&#x20;                   p.hp -= 5;

&#x20;                   send\_reliable\_text(p.peer\_id, "play\_stationary pain1.ogg", 0);

&#x20;                   send\_reliable\_text(p.peer\_id, "say \[Sobrevivência] Você está morrendo de fome! Procure comida.", 0);

&#x20;               }

&#x20;               

&#x20;               // Dano por desidratação (Sede no limite)

&#x20;               if(p.nsede >= 100) {

&#x20;                   p.nsede = 100;

&#x20;                   p.hp -= 8;

&#x20;                   send\_reliable\_text(p.peer\_id, "play\_stationary cough.ogg", 0);

&#x20;                   send\_reliable\_text(p.peer\_id, "say \[Sobrevivência] Você está severamente desidratado! Procure água.", 0);

&#x20;               }



&#x20;               // Checagem de Morte por fome/sede

&#x20;               if(p.hp <= 0) {

&#x20;                   p.hp = 0;

&#x20;                   server\_broadcast("play\_body mortejogador.ogg " + p.x + " " + p.y, p.map);

&#x20;                   send\_reliable\_text(p.peer\_id, "say Você morreu pelas forças da natureza (Inanição/Desidratação).", 0);

&#x20;                   // (Aqui seu sistema de morte já fará ele respawnar no hospital sem itens)

&#x20;               }

&#x20;           }

&#x20;       }

&#x20;   }

}

```



\### Passo 2: Conectando os "Fios" (Servidor)



Agora precisamos garantir que tudo isso rode.



\*\*A) Ao Iniciar o Servidor:\*\*

Abra o seu arquivo \*\*`iniciar.nvgt`\*\*, procure a função que carrega os itens ou módulos avançados e adicione a inicialização:

```cpp

&#x20;   init\_consumables\_system(); // Registra maçãs, água, poções...

&#x20;   survival\_timer.restart();  // Inicia o relógio do metabolismo

```



\*\*B) No Loop Principal (`server.nvgt`):\*\*

Na sua função principal de repetição (o loop central `main` ou `tprincipais`), adicione o motor de sobrevivência junto dos outros sistemas:

```cpp

&#x20;   survival\_loop(); // O motor que esvazia a barriga dos jogadores

```



\*\*C) No Roteador de Rede (`network\_handlers.nvgt`):\*\*

Se o jogador tentar usar um item da mochila dele, ele mandará um pacote. Na Task 3 de rede que já configuramos, você adicionou o prefixo `USE:` para consumíveis. Procure a função `handle\_use\_item` (ou a função equivalente de pacote `INV:use`) e chame nosso código:

```cpp

void handle\_use\_item(player@ p, string data) {

&#x20;   // Formato: item\_name -> Exemplo: USE:agua

&#x20;   int p\_index = get\_player\_index\_from(p.charname);

&#x20;   use\_item(p\_index, data); 

}

```



\### E o que vai acontecer agora?

Se o jogador for "ficar pescando" ou construindo uma casa e esquecer da vida, ele vai começar a ouvir o próprio personagem tossir (`cough.ogg`) de Sede ou gemer de dor de Fome. Para não morrer, ele terá que abrir a interface de Inventário e usar a Maçã que ele coletou de uma árvore ou comprou na Lanchonete, que agora esvaziará o status de Fome e consumirá o item perfeitamente da \*database\*!



Com o metabolismo funcionando, faltam oficialmente \*\*APENAS DUAS TASKS\*\* para o seu MMORPG ter todas as \*features\* do GDD original ativadas:



