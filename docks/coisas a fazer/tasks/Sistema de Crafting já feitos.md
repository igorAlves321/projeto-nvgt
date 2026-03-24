Chegamos à reta final! 🔨🔥 



O \*\*Sistema de Crafting (Forja e Criação)\*\* é uma das mecânicas que mais engaja os jogadores. Fazer com que eles precisem cortar árvores e minerar minérios para fazer a própria espada movimenta toda a economia do jogo e valoriza o mapa.



Como nós temos o `inventory\_sync.nvgt` ativo, forjar itens será 100% seguro. O servidor vai auditar se o jogador realmente tem a madeira e o ferro, vai removê-los com segurança e devolver a Espada pronta!



Vamos para a \*\*Mini-Task 23: Sistema de Crafting\*\*.



\### Passo 1: O Núcleo do Crafting (`crafting.nvgt`)



Abra o arquivo \*\*`server/includes/crafting.nvgt`\*\*. Você tem um esboço (\*stub\*) dessa classe lá. Substitua todo o conteúdo pelo código abaixo. Ele cria as receitas, faz a checagem dupla dos itens e toca o som da forja.



```cpp

// ============================================================================

// SISTEMA DE CRAFTING E FORJA (Mini-Task 23)

// ============================================================================



// Definição de uma receita de craft

class craft\_recipe {

&#x20;   string result\_item;

&#x20;   int result\_qty;

&#x20;   dictionary ingredients; // item\_name -> quantidade

&#x20;   string craft\_sound;



&#x20;   craft\_recipe(string res, int qty, string sound = "anvil.ogg") {

&#x20;       result\_item = res;

&#x20;       result\_qty = qty;

&#x20;       craft\_sound = sound;

&#x20;   }



&#x20;   void add\_ingredient(string name, int qty) {

&#x20;       ingredients.set(name, double(qty));

&#x20;   }

}



// O Gerenciador global de receitas

class crafting {

&#x20;   dictionary recipes; // result\_item -> craft\_recipe@



&#x20;   void register\_recipe(craft\_recipe@ r) {

&#x20;       recipes.set(r.result\_item, @r);

&#x20;   }



&#x20;   craft\_recipe@ get\_recipe(string result\_item) {

&#x20;       craft\_recipe@ r;

&#x20;       if(recipes.get(result\_item, @r)) return r;

&#x20;       return null;

&#x20;   }

}



// Instância global do sistema

crafting crafting\_system;



// INICIALIZAÇÃO DAS RECEITAS 

void init\_crafting\_system() {

&#x20;   // Receita 1: Espada Básica (2x Ferro, 1x Madeira)

&#x20;   craft\_recipe espada("espada\_basica", 1, "anvil.ogg");

&#x20;   espada.add\_ingredient("ferro", 2);

&#x20;   espada.add\_ingredient("madeira", 1);

&#x20;   crafting\_system.register\_recipe(espada);



&#x20;   // Receita 2: Fita Explosiva (Task anterior que você tinha no BGT)

&#x20;   craft\_recipe fita("fita\_explosiva", 1, "craft\_bomb.ogg");

&#x20;   fita.add\_ingredient("polvora", 2);

&#x20;   fita.add\_ingredient("fita\_adesiva", 1);

&#x20;   crafting\_system.register\_recipe(fita);



&#x20;   // Receita 3: Atadura (Curativo)

&#x20;   craft\_recipe atadura("atadura", 2, "craft\_cloth.ogg");

&#x20;   atadura.add\_ingredient("tecido", 2);

&#x20;   atadura.add\_ingredient("alcool", 1);

&#x20;   crafting\_system.register\_recipe(atadura);



&#x20;   debug\_log("🔨 Sistema de Crafting inicializado com " + crafting\_system.recipes.get\_size() + " receitas.");

}



// FUNÇÃO DE FORJAR

bool cmd\_craft(int player\_index, string result\_item) {

&#x20;   if(player\_index < 0 || player\_index >= int(players.length())) return false;

&#x20;   player@ p = players\[player\_index];



&#x20;   // 1. VERIFICAÇÃO DE ZONA (Bancada de Trabalho)

&#x20;   string loc = get\_zone\_at(p.x, p.y, p.map);

&#x20;   if(loc != "Bancada de Trabalho" \&\& loc != "Bigorna") {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Crafting] Você precisa estar próximo a uma Bancada de Trabalho ou Bigorna para forjar.", 0);

&#x20;       return false;

&#x20;   }



&#x20;   // 2. BUSCA A RECEITA

&#x20;   craft\_recipe@ recipe = crafting\_system.get\_recipe(result\_item);

&#x20;   if(recipe is null) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Crafting] Você não sabe como forjar esse item (" + result\_item + ").", 0);

&#x20;       return false;

&#x20;   }



&#x20;   // 3. AUDITORIA: Verifica se o jogador tem TODOS os ingredientes ANTES de remover

&#x20;   string\[] ing\_names = recipe.ingredients.get\_keys();

&#x20;   for(uint i = 0; i < ing\_names.length(); i++) {

&#x20;       double req\_qty\_d = 0;

&#x20;       recipe.ingredients.get(ing\_names\[i], req\_qty\_d);

&#x20;       int req\_qty = int(req\_qty\_d);



&#x20;       double current\_qty\_d = 0;

&#x20;       p.inv.get(ing\_names\[i], current\_qty\_d);



&#x20;       if(int(current\_qty\_d) < req\_qty) {

&#x20;           send\_reliable\_text(p.peer\_id, "say \[Crafting] Faltam materiais. Você precisa de " + req\_qty + "x " + ing\_names\[i] + ".", 0);

&#x20;           send\_reliable\_text(p.peer\_id, "play\_stationary erro.ogg", 0);

&#x20;           return false;

&#x20;       }

&#x20;   }



&#x20;   // 4. EXECUTA A FORJA: Remove os ingredientes usando JSON Sync Seguro

&#x20;   for(uint i = 0; i < ing\_names.length(); i++) {

&#x20;       double req\_qty\_d = 0;

&#x20;       recipe.ingredients.get(ing\_names\[i], req\_qty\_d);

&#x20;       remove\_item\_with\_sync(p, ing\_names\[i], int(req\_qty\_d));

&#x20;   }



&#x20;   // Dá o item final ao jogador

&#x20;   add\_item\_with\_sync(p, recipe.result\_item, recipe.result\_qty);



&#x20;   // 5. FEEDBACK AUDIOVISUAL E CONQUISTAS

&#x20;   server\_broadcast("play\_body " + recipe.craft\_sound + " " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary " + recipe.craft\_sound, 0);

&#x20;   send\_reliable\_text(p.peer\_id, "say \[Crafting] Sucesso! Você forjou " + recipe.result\_qty + "x " + recipe.result\_item + "!", 0);



&#x20;   // Se o sistema de conquistas da Task 21 estiver ativado, avança!

&#x20;   // update\_achievement\_progress(p.charname, "items\_crafted", recipe.result\_qty);



&#x20;   return true;

}

```



\### Passo 2: Ligando no Servidor



\*\*A) Ao Ligar o Servidor:\*\*

Abra o seu \*\*`server/includes/iniciar.nvgt`\*\*, encontre a função de carregar dados e inicie o sistema de receitas:

```cpp

&#x20;   init\_crafting\_system(); // Registra Espada de Ferro e outros crafts

```



\*\*B) Criando o Comando de Chat para os Jogadores:\*\*

Abra o \*\*`server/includes/commands.nvgt`\*\* (ou onde ficam seus comandos de chat como `/onde`, `/equipe`, etc) e adicione o comando que invoca a nossa nova função:



```cpp

// Comando /craft ou /forjar

bool cmd\_forjar(player@ player, string\[] args) {

&#x20;   if(args.length() < 1) {

&#x20;       player.send\_message("say Uso: /forjar <nome\_do\_item>");

&#x20;       player.send\_message("say Exemplo: /forjar espada\_basica");

&#x20;       return false;

&#x20;   }

&#x20;   

&#x20;   int p\_index = get\_player\_index\_from(player.charname);

&#x20;   cmd\_craft(p\_index, args);

&#x20;   return true;

}

```



\### O que o jogador sente agora? 🛠️

1\. O jogador entra numa floresta e coleta Madeira, depois entra na mina e coleta Ferro (podemos ligar isso no seu `extract.nvgt`).

2\. Ele anda até um local do seu mapa marcado com a zona `"Bancada de Trabalho"`. Se ele tentar forjar no meio da rua, o servidor avisa que ele precisa da bancada!

3\. Ao chegar lá, ele digita `/forjar espada\_basica`.

4\. Ouve-se uma batida forte de bigorna (`anvil.ogg`) em som 3D! Os itens somem da bolsa dele graças ao sistema anti-dupe, e uma bela `espada\_basica` aparece lá.



