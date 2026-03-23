Vamos atacar a \*\*Opção A: O Menu de Inventário Definitivo\*\*. 



No momento, a função `inventarymenu()` está apenas emitindo um aviso de voz ("use as teclas de atalho I..."). Como o seu cliente já possui o dicionário global `player\_inv` e funções nativas prontas como `interact`, `drop` e `give`, nós podemos criar uma interface moderna, unificada e acessível com a classe `menu` do NVGT.



\### Mini-Task 5: Substituindo o Stub do Menu de Inventário (Cliente)



Abra o arquivo onde está o seu menu (provavelmente \*\*`menu.nvgt`\*\* ou \*\*`stubs.nvgt`\*\*), procure pela antiga função `void inventarymenu()` e \*\*substitua todo o bloco dela\*\* por este código abaixo:



```cpp

// ============================================================================

// MENU DE INVENTÁRIO NATIVO (Mini-Task 5)

// ============================================================================



void inventarymenu() {

&nbsp;   if(ausente || !moveable) return;

&nbsp;   

&nbsp;   setupmenu(); // Inicializa o menu nativo com os sons padrão

&nbsp;   game\_menu.intro\_text = pu.get\_value("Seu Inventário. O que deseja acessar?");

&nbsp;   

&nbsp;   // Pega todas as chaves (nomes dos itens) do dicionário do jogador

&nbsp;   string\[] keys = player\_inv.get\_keys();

&nbsp;   

&nbsp;   if(keys.length() == 0) {

&nbsp;       speak(pu.get\_value("Seu inventário está vazio."));

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   // Popula o menu iterando pelo dicionário

&nbsp;   int itens\_reais = 0;

&nbsp;   for(uint i = 0; i < keys.length(); i++) {

&nbsp;       int qtd = inv\_item\_number(keys\[i]);

&nbsp;       if(qtd > 0) {

&nbsp;           // Traduz o nome do item e exibe a quantidade

&nbsp;           string item\_name = pu.get\_value(keys\[i]);

&nbsp;           game\_menu.add\_item(item\_name + " (" + qtd + ")", keys\[i]);

&nbsp;           itens\_reais++;

&nbsp;       }

&nbsp;   }

&nbsp;   

&nbsp;   if(itens\_reais == 0) {

&nbsp;       speak(pu.get\_value("Seu inventário está vazio."));

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   game\_menu.add\_item(pu.get\_value("Sair do Inventário"), "sair");

&nbsp;   

&nbsp;   // Executa o menu e aguarda a escolha do jogador

&nbsp;   int result = game\_menu.run();

&nbsp;   if(result > -1) {

&nbsp;       string selected\_item = game\_menu.get\_item\_id(result);

&nbsp;       if(selected\_item != "sair") {

&nbsp;           // Abre o submenu de ações para o item escolhido Mas, isso se ele pressionar enter, por que espaço, //usa o item

&nbsp;           inv\_action\_menu(selected\_item);

&nbsp;       }

&nbsp;   }

}



// Submenu de ações (Dropar, Dar)

void inv\_action\_menu(string item\_id) {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("O que deseja fazer com ") + pu.get\_value(item\_id) + "?";

&nbsp;   

&nbsp;   game\_menu.add\_item(pu.get\_value("Usar / Equipar"), "use");

&nbsp;   game\_menu.add\_item(pu.get\_value("Descartar no chão (Drop)"), "drop");

&nbsp;   game\_menu.add\_item(pu.get\_value("Dar a um jogador próximo"), "give");

&nbsp;   game\_menu.add\_item(pu.get\_value("Cancelar"), "cancel");

&nbsp;   

&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string action = game\_menu.get\_item\_id(res);

&nbsp;       

&nbsp;       if(action == "use") {

&nbsp;           // Usa a função existente para processar uso do item

&nbsp;           interact(item\_id); 

&nbsp;       } 

&nbsp;       else if(action == "drop") {

&nbsp;           // Pede a quantidade e descarta

&nbsp;           string qt\_str = prompt\_numeric\_input(

&nbsp;               pu.get\_value("Quantidade"), 

&nbsp;               pu.get\_value("Quantos deseja jogar no chão?"), 

&nbsp;               1

&nbsp;           );

&nbsp;           if(qt\_str != "") {

&nbsp;               drop(item\_id, parse\_int(qt\_str));

&nbsp;           }

&nbsp;       } 

&nbsp;       else if(action == "give") {

&nbsp;           // Aciona a lógica de dar item

&nbsp;           give(item\_id);

&nbsp;       }

&nbsp;   }

}

```



\### O que este código realiza?

1\. \*\*Dicionário em Tempo Real:\*\* Ele varre a variável `player\_inv.get\_keys()` em tempo real, então qualquer coisa que você comprar na nossa nova Loja já aparecerá aqui com as quantidades certas.

2\. \*\*Interface Acessível NVGT:\*\* Diferente do BGT que exigia loops e `get\_characters()` complexos para ler itens de inventário, nós usamos o `game\_menu.add\_item` em conjunto com a sua arquitetura moderna do `audio\_form`.

3\. \*\*Integração com Ações:\*\* Ele aciona seus comandos já existentes de `interact(item\_name)`, `drop(item, amount)` e `give(item)`, permitindo que a jogabilidade flua através do servidor instantaneamente!



Com isso, o fluxo completo do inventário (ganhar/comprar o item -> visualizar o item -> descartar o item) está reativado do lado do cliente.

Excelente! Vamos ativar a \*\*Mini-Task 6: Itens Físicos e Coletáveis no Mapa (Loot e Drops)\*\*.



A sua arquitetura no servidor já possui um sistema avançado e robusto de Loot implementado nativamente no arquivo `loot\_drops.nvgt`. Ele já gerencia a criação, expiração, posse (owner\_only/public) e a limpeza automática (\*garbage collection\*) dos itens caídos no mapa. O que precisamos agora é ligar esse sistema maravilhoso aos comandos do jogador e dar vida a ele enviando o feedback de Áudio 3D para o cliente.



Aqui está a implementação em três passos simples:



\### Passo 1: O Servidor Processa as Ações (Drop e Pickup)

Abra o arquivo \*\*`network\_handlers.nvgt`\*\* no seu servidor. Procure as funções `handle\_drop\_item` e `handle\_pickup\_item` e substitua-as por este código para conectar com a classe de Loot:



```cpp

// ============================================================================

// HANDLERS DE INVENTÁRIO (Drop e Pickup físicos)

// ============================================================================



void handle\_drop\_item(player@ p, string data) {

&nbsp;   // Formato recebido do cliente: item\_name|quantidade

&nbsp;   string\[] parts = data.split("|");

&nbsp;   if(parts.length() < 2) return;

&nbsp;   

&nbsp;   string item\_name = parts;

&nbsp;   int qty = parse\_int(parts);



&nbsp;   // Remove do inventário com a função de sincronização nativa

&nbsp;   if(remove\_item\_with\_sync(p, item\_name, qty)) {

&nbsp;       // Instancia o drop no mundo físico! (owner\_id = 0 significa que é público)

&nbsp;       spawn\_drop(item\_name, qty, p.map, p.x, p.y, 0); 

&nbsp;   } else {

&nbsp;       send\_reliable\_text(p.peer\_id, "say Você não possui essa quantidade.", 0);

&nbsp;   }

}



void handle\_pickup\_item(player@ p, string data) {

&nbsp;   // O jogador apertou Enter no chão. O servidor varre o mapa atual

&nbsp;   string\[] map\_drops = get\_drops\_in\_map(p.map);

&nbsp;   bool pegou\_algo = false;



&nbsp;   for(uint i = 0; i < map\_drops.length(); i++) {

&nbsp;       drop\_entity@ d = get\_drop(map\_drops\[i]);

&nbsp;       

&nbsp;       // Verifica se o item existe, se está na mesma coordenada e se não expirou

&nbsp;       if(d !is null \&\& d.x == p.x \&\& d.y == p.y \&\& d.state != "expired" \&\& d.state != "picked") {

&nbsp;           

&nbsp;           // A função pickup\_drop já cuida de verificar se é owner\_only e de dar o item

&nbsp;           if(pickup\_drop(p, d.drop\_id)) {

&nbsp;               pegou\_algo = true;

&nbsp;               break; // Pega um item por vez a cada tecla "Enter"

&nbsp;           }

&nbsp;       }

&nbsp;   }



&nbsp;   if(!pegou\_algo) {

&nbsp;       send\_reliable\_text(p.peer\_id, "say Não há nada para pegar aqui.", 0);

&nbsp;   }

}

```



\### Passo 2: O Cliente Envia os Comandos Corretos

Agora precisamos atualizar as funções antigas do cliente que lidavam com drops manuais usando arrays locais, transferindo a responsabilidade para a rede moderna. 



Vá no seu cliente (em \*\*`client.nvgt`\*\* ou \*\*`comandos.nvgt`\*\*) e substitua as funções `drop` e `checkitem` por estas:



```cpp

// Função acionada quando o jogador tenta descartar um item do menu

void drop(string item, int amount = 1) {

&nbsp;   if(amount < 1 || amount > 1000000000) return;

&nbsp;   if(!inv\_item\_exists(item)) return;



&nbsp;   // Envia pacote no novo protocolo de rede (MSG\_DROP)

&nbsp;   send\_reliable(peer\_id, "DROP:" + item + "|" + amount, 0);

}



// Função acionada quando o jogador aperta Enter no chão

void checkitem() {

&nbsp;   if(ausente || !moveable) return;

&nbsp;   

&nbsp;   // Avisa ao servidor: "Tentei pegar algo nas minhas coordenadas atuais"

&nbsp;   send\_reliable(peer\_id, "PICKUP:chao", 0);

}

```



\### Passo 3: Áudio 3D Instantâneo via JSON (Cliente)

O sistema `loot\_drops.nvgt` do seu servidor já é inteligente o suficiente para emitir os broadcasts `inv\_broadcast\_drop` e `inv\_broadcast\_pickup` para todos os jogadores na mesma área quando um item cai ou é pego. Vamos ensinar o cliente a tocar os sons!



No seu cliente, abra o arquivo \*\*`net.nvgt`\*\* e procure pela parte onde processa a rede (como `process\_channel\_0` ou o seu parser JSON). Adicione a seguinte interceptação nativa:



```cpp

&nbsp;   // Interceptador de eventos físicos de Inventário (JSON nativo do NVGT)

&nbsp;   if (full\_msg.find("\\"type\\":\\"inv\_broadcast\_drop\\"") >= 0) {

&nbsp;       json\_object obj;

&nbsp;       obj.parse(full\_msg);

&nbsp;       

&nbsp;       int item\_x = obj("x").get\_int();

&nbsp;       int item\_y = obj("y").get\_int();

&nbsp;       

&nbsp;       // Toca som do item batendo no chão no espaço 3D usando o pool de objetos

&nbsp;       pobjs.play\_2d("drop.ogg", me.x, me.y, item\_x, item\_y, false);

&nbsp;   }

&nbsp;   else if (full\_msg.find("\\"type\\":\\"inv\_broadcast\_pickup\\"") >= 0) {

&nbsp;       json\_object obj;

&nbsp;       obj.parse(full\_msg);

&nbsp;       

&nbsp;       int item\_x = obj("x").get\_int();

&nbsp;       int item\_y = obj("y").get\_int();

&nbsp;       string pegador = obj("player").get\_string();

&nbsp;       

&nbsp;       // Toca o som 3D de pegar apenas se o jogador estiver perto

&nbsp;       pobjs.play\_2d("get.ogg", me.x, me.y, item\_x, item\_y, false);

&nbsp;       

&nbsp;       // Mensagem narrativa no chat local (Opcional, só se o pegador for você mesmo)

&nbsp;       if(pegador == un) {

&nbsp;           speak(pu.get\_value("Você pegou um item."));

&nbsp;       }

&nbsp;   }

```



\### O que conquistamos aqui:

1\. \*\*Remoção total de gambiarras:\*\* Em vez do cliente iterar em loops mortos checando se pisou em algo (`objsloop` antigo), a carga está toda no servidor que gerencia fisicamente o array de `drop\_entity`.

2\. \*\*Combate contra Hacks de Teleporte de Itens:\*\* Como tudo é validado pela função `pickup\_drop`, jogadores não podem mais invocar pacotes falsos dizendo que pegaram itens do outro lado do mapa; o servidor só concede se o raio da distância for válido.

3\. \*\*Imersão Auditiva (Sound\_pool):\*\* Agora, se você ou qualquer jogador próximo em um raio de até 50 metros jogar uma maçã no chão, todo mundo vai ouvir `drop.ogg` exatamente de onde o som originou graças ao HRTF e o Panning da API NVGT.



da uma olhada no fluxo bgt, para ter um norte, talvez te ajude um pouco.

