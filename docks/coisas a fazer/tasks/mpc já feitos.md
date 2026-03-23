Chegou a hora de dar vida às criaturas e inimigos do jogo! 🐺⚔️



No BGT antigo, você tinha um arquivo separado para cada criatura (`dog.bgt`, `coelho.bgt`, `cobra.bgt`, `mercenario.bgt`, etc.), o que causava uma bagunça no código e muito lag. Na sua nova arquitetura NVGT, nós temos um sistema unificado incrivelmente otimizado: o \*\*`npc.nvgt`\*\* e o \*\*`monstruo.nvgt`\*\*. 



Eles controlam a IA, o \*aggro\* (perseguição) e o combate de todas as criaturas a partir de uma única classe base!



Para fazer isso funcionar, vamos dividir na \*\*Mini-Task 8: O Cérebro e o Spawn dos NPCs\*\*.



\### Passo 1: Ligar o "Cérebro" Global no Servidor

Atualmente, as chamadas para os NPCs estão desativadas no arquivo principal do seu servidor (`server.nvgt` ou `server.txt`). Precisamos ativar o loop de inteligência artificial para que eles possam andar, procurar jogadores e atacar.



Abra o seu arquivo principal do servidor (provavelmente \*\*`server.nvgt`\*\*), vá até a função principal de loop (`main` ou onde ficam os timers e processamentos de física) e adicione/substitua as chamadas antigas por estas:



```cpp

// ============================================================================

// INTELIGÊNCIA ARTIFICIAL DOS NPCS E MONSTROS (Mini-Task 8)

// ============================================================================



// Substituindo os antigos dogloop(), coelholoop(), cobraloop(), etc.

npc\_global\_loop();

monstruo\_global\_loop();

```



Isso fará com que o servidor processe a lógica de \*todas\* as criaturas a cada \*frame\* sem gargalos.



\### Passo 2: Fazer o Mapa "Cuspir" os NPCs (Spawn)

Seu Modo Construtor já consegue salvar um NPC no arquivo `.map`, mas quando o servidor liga e carrega esse mapa, ele precisa transformar essa linha de texto em uma criatura viva.



Abra o arquivo \*\*`server/includes/server\_map.nvgt`\*\* e procure pela função que carrega os dados do mapa (geralmente dentro de algo como `load\_map`, `init\_data` ou o loop que varre `mapdata`). Vamos adicionar a instrução de \*spawn\*:



```cpp

&nbsp;       // --- SPAWN DE NPC / MONSTRO ---

&nbsp;       // Formato salvo pelo builder: npc:x:y:hp:nome:id (simplificado) ou monstruo:x:y:tipo

&nbsp;       else if(parsed == "npc" \&\& parsed.length() >= 5) {

&nbsp;           int nx = parse\_int(parsed);

&nbsp;           int ny = parse\_int(parsed);

&nbsp;           int hp = parse\_int(parsed);

&nbsp;           string nome = parsed;

&nbsp;           

&nbsp;           // Invoca o NPC no mundo real do servidor

&nbsp;           spawn\_npc(nx, ny, current\_map.name, nome);

&nbsp;       }

&nbsp;       else if(parsed == "monstruo" \&\& parsed.length() >= 4) {

&nbsp;           int mx = parse\_int(parsed);

&nbsp;           int my = parse\_int(parsed);

&nbsp;           string tipo = parsed;

&nbsp;           

&nbsp;           // Invoca o Monstro no mundo real do servidor

&nbsp;           spawn\_monstruo(mx, my, current\_map.name, tipo);

&nbsp;       }

```



\### O que isso faz?

1\. O Servidor agora lê as linhas `npc` e `monstruo` do seu arquivo de mapa.

2\. Ele chama `spawn\_npc()` e `spawn\_monstruo()`, que inserem essas criaturas nos arrays globais `npcs\_global` e `monstruos\_global`.

3\. O cérebro (ativado no Passo 1) assume o controle: a criatura começa a usar seu timer interno (`tandar`) para patrulhar as coordenadas X e Y.



\### Próxima Etapa (O Cliente)

Neste exato momento, o servidor já sabe que o lobo está andando na coordenada X:15 Y:10, \*\*mas o jogador ainda não escuta os passos nem os rosnados dele!\*\*



Para arrumar isso, precisaremos ir para o lado do \*\*Cliente (`map.nvgt`)\*\*, e implementar a função `npc\_loop()` para ele receber os pacotes do servidor, tocar os sons no sistema HRTF e mostrar no radar.



Perfeito! Vamos dar olhos e ouvidos ao seu cliente para que o jogador consiga perceber essas criaturas. 



O seu servidor agora já tem o "cérebro" rodando, calculando o \*Aggro\* e a movimentação. O seu arquivo `net.nvgt` atual já está até preparado para tocar os sons em 3D nativamente no `process\_channel\_5` (onde ele recebe o pacote `play\_npc` e toca no `npcs.play\_2d`). 



O que precisamos fazer agora para concluir a \*\*Mini-Task 8 (Parte 2: Cliente)\*\* é atualizar o array visual do cliente e construir o \*\*Radar de Inimigos\*\* usando as funções que atualmente estão apenas como \*stubs\* no seu `map.nvgt`.



Aqui estão os 3 passos para o cliente:



\### Passo 1: Receber a Atualização de Posição (`net.nvgt`)

Abra o seu arquivo \*\*`net.nvgt`\*\*, vá até a função `process\_channel\_0` (que cuida das mensagens gerais e movimentação) e adicione este bloco para interceptar os dados dos NPCs:



```cpp

&nbsp;   // Atualização da Posição e Vida dos NPCs no Cliente

&nbsp;   else if(parsed == "npc\_update" \&\& parsed.length() >= 6) {

&nbsp;       int id = string\_to\_number(parsed);

&nbsp;       int nx = string\_to\_number(parsed);

&nbsp;       int ny = string\_to\_number(parsed);

&nbsp;       int hp = string\_to\_number(parsed);

&nbsp;       string nome = parsed;



&nbsp;       // Chama a função nativa do map.nvgt para atualizar a matriz local

&nbsp;       spawn\_npc(nx, ny, hp, nome, id);

&nbsp;   }

&nbsp;   // Remoção de NPCs mortos ou que saíram do mapa

&nbsp;   else if(parsed == "npc\_remove" \&\& parsed.length() >= 2) {

&nbsp;       int id = string\_to\_number(parsed);

&nbsp;       remove\_npc\_by\_id(id);

&nbsp;   }

```



\### Passo 2: O Radar e o Loop de Limpeza (`map.nvgt`)

Abra o seu arquivo \*\*`includes/map.nvgt`\*\*. Você verá que as funções `npc\_loop()` e `get\_nearest\_npc()` estão vazias ou incompletas. Substitua-as por este código funcional:



```cpp

// Limpa NPCs fantasmas (caso o servidor pare de enviar atualizações por lag ou distância)

void npc\_loop() {

&nbsp;   if(ausente || !moveable) return;



&nbsp;   // Iteração reversa para remoção segura do array

&nbsp;   for(int i = int(npc\_objects.length()) - 1; i >= 0; i--) {

&nbsp;       if(npc\_objects\[i] !is null \&\& npc\_objects\[i].last\_seen.elapsed >= 5000) {

&nbsp;           npc\_objects.remove\_at(i);

&nbsp;       }

&nbsp;   }

}



// Varre a matriz visual e retorna o NPC mais próximo do jogador

npc\_client\_class@ get\_nearest\_npc(int max\_distance = 30) {

&nbsp;   npc\_client\_class@ nearest = null;

&nbsp;   int min\_dist = max\_distance;



&nbsp;   for(uint i = 0; i < npc\_objects.length(); i++) {

&nbsp;       if(npc\_objects\[i] is null) continue;



&nbsp;       // Distância Manhattan simples para otimização no cliente

&nbsp;       int dx = abs(me.x - npc\_objects\[i].x);

&nbsp;       int dy = abs(me.y - npc\_objects\[i].y);

&nbsp;       int dist = dx + dy;



&nbsp;       if(dist <= min\_dist) {

&nbsp;           min\_dist = dist;

&nbsp;           @nearest = @npc\_objects\[i];

&nbsp;       }

&nbsp;   }

&nbsp;   return nearest;

}

```



\### Passo 3: O Comando do Jogador (`comandos.nvgt` ou `client.nvgt`)

Agora que o cliente tem a memória dos NPCs, vamos criar o comando para o jogador rastreá-los. Nós vamos usar a sua função já existente `tell\_where(x, y)`, que é excelente pois já traduz as coordenadas para direções como "direita 5 e acima 2".



Adicione esta função no seu arquivo de comandos:



```cpp

// Função de Rastreamento/Radar de Inimigos

void radar\_de\_inimigos() {

&nbsp;   if(ausente || !moveable) return;

&nbsp;   

&nbsp;   npc\_client\_class@ target = get\_nearest\_npc(30); // Procura inimigos num raio de 30 tiles



&nbsp;   if(target is null) {

&nbsp;       speak(pu.get\_value("Nenhum inimigo por perto."));

&nbsp;       return;

&nbsp;   }



&nbsp;   // Toca um bipe indicando a posição exata 3D (HRTF) do monstro

&nbsp;   pobjs.play\_2d("radar\_beep.ogg", me.x, me.y, target.x, target.y, false);



&nbsp;   // Usa a função nativa do seu cliente para falar a direção e distância

&nbsp;   tell\_where(target.x, target.y);

&nbsp;   

&nbsp;   // Fala o nome e a vida atual da criatura

&nbsp;   speak(target.name + ", " + target.hp + " " + pu.get\_value("HP"));

}

```



Para usar, basta plugar a função `radar\_de\_inimigos()` em uma tecla livre no seu `client.nvgt` (por exemplo, na tecla `KEY\_TAB` ou `KEY\_R`). 

Olhe no bgt, mas, se não me engano, a tecla responsável era m, e vai ser a qui também.



\### O que isso proporciona?

Agora, quando um \*Boss\* ou Inimigo \*spawnar\*, o servidor notificará o cliente. O cliente posicionará a criatura na RAM nativa do NVGT. Os passos dos monstros vão tocar com o \*Steam Audio 3D\* com perfeição de posição (graças ao canal 5) e, se o jogador quiser saber a distância exata antes de atirar, basta apertar o botão do Radar para a engine verbalizar as coordenadas exatas!



