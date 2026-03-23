Na Mini-Task 9, nós já tínhamos criado a inteligência da colisão no servidor (check\_npc\_collisions no bullet.nvgt), que faz a bala subtrair a vida do monstro e aplicar o sistema de Aggro

1

. No entanto, o jogador atualmente não consegue puxar o gatilho, pois a função weaponcheckloop() no cliente está completamente vazia como um stub

2

.

Vamos implementar a Mini-Task 12: Gatilho e Disparo Físico, conectando o botão Ctrl do cliente ao sistema de física de balas do servidor.

Passo 1: O Gatilho no Cliente (stubs.nvgt ou weapon.nvgt)

Nós precisamos substituir o stub vazio do weaponcheckloop por um código que detecte a tecla de tiro, verifique o pente de munição local, toque o som e avise o servidor.

Vá no código do seu cliente, procure pelo stub void weaponcheckloop()

2

&nbsp;e substitua por este código completo:

// ============================================================================

// LOOP DE TIRO E GATILHO (Cliente)

// ============================================================================

void weaponcheckloop() {

&nbsp;   // Validações básicas de movimento e seleção de arma

&nbsp;   if (ausente || !moveable || dcamera == 1) return;

&nbsp;   if (selected < 0 || selected >= int(player\_weapons.length())) return;



&nbsp;   // Se o jogador segurar o Control Esquerdo para atirar

&nbsp;   if (key\_down(KEY\_LCONTROL)) {

&nbsp;       weapon@ w = player\_weapons\[selected];

&nbsp;       

&nbsp;       // Define a velocidade do tiro dependendo se a arma está no modo rajada/automático

&nbsp;       double current\_speed = w.speed;

&nbsp;       // Se a arma suporta modo automático e estiver ativado (assumindo que 1 é o modo auto)

&nbsp;       if (w.enable\_burst == 1) { 

&nbsp;           current\_speed = w.speed\_burst;

&nbsp;       }



&nbsp;       // Verifica o tempo de recarga (cooldown do tiro) e se não está recarregando o pente

&nbsp;       if (weapontimer.elapsed >= current\_speed \&\& w.loading == 0) {



&nbsp;           // Se a arma precisa de munição e o pente está vazio

&nbsp;           if (w.require\_ammo == 1 \&\& w.ammo\_load <= 0) {

&nbsp;               p.play\_stationary(w.sound\_unload + ".ogg", false);

&nbsp;               weapontimer.restart();

&nbsp;               return;

&nbsp;           }



&nbsp;           // Desconta a munição localmente

&nbsp;           if (w.require\_ammo == 1) {

&nbsp;               w.ammo\_load -= w.ammo\_cantity\_descount;

&nbsp;           }



&nbsp;           weapontimer.restart();



&nbsp;           // Toca o som do tiro localmente para o atirador

&nbsp;           p.play\_stationary(w.sound\_shoot + ".ogg", false);



&nbsp;           // Avisa o servidor para criar a bala no mundo físico!

&nbsp;           // Envia o comando estruturado com o nome da arma e a direção que o jogador está olhando

&nbsp;           send\_reliable(peer\_id, "ACTION:shoot|" + w.name + "|" + facing, 4); // Canal 4 de ações

&nbsp;       }

&nbsp;   }

}

(Não se esqueça de garantir que weaponcheckloop(); está sendo chamado dentro do loop principal game() ou tprincipais() do seu cliente para que ele cheque a tecla a cada frame).

Passo 2: A Física da Bala no Servidor (network\_handlers.nvgt)

Agora, quando o servidor receber o pacote "ACTION:shoot|nome\_da\_arma|direção", ele precisa criar a entidade "bala" (bullet) no mapa, para que a função bulletloop() calcule o voo dela frame a frame até colidir em uma parede ou monstro

3

.

No servidor, abra o arquivo onde você processa as mensagens de ação do cliente (provavelmente network\_handlers.nvgt, dentro do handle\_combat ou handle\_action

4

) e adicione a interceptação do tiro:

// ============================================================================

// PROCESSAMENTO DE TIRO (Servidor)

// ============================================================================

void handle\_shoot(player@ p, string data) {

&nbsp;   // Desempacota os dados: nome\_da\_arma|direção

&nbsp;   string\[] parts = data.split("|");

&nbsp;   if (parts.length() < 2) return;



&nbsp;   string weapon\_name = parts;

&nbsp;   int shoot\_direction = parse\_int(parts\[5]);



&nbsp;   // Busca a arma no banco de dados do servidor para pegar o dano real

&nbsp;   int w\_index = get\_weapon\_index(weapon\_name);

&nbsp;   if (w\_index < 0) return;

&nbsp;   

&nbsp;   weapon@ w = weapons\_list\[w\_index];



&nbsp;   // Toca o som do tiro em 3D para todos os OUTROS jogadores que estiverem perto no mesmo mapa

&nbsp;   server\_broadcast("play\_body " + w.sound\_shoot + ".ogg " + p.x + " " + p.y, p.map);



&nbsp;   // Cria a bala física e a injeta no motor do jogo

&nbsp;   bullet b;

&nbsp;   b.owner = p.charname;

&nbsp;   b.somarma = w.sound\_shoot;

&nbsp;   b.mapname = p.map;

&nbsp;   b.x = p.x;

&nbsp;   b.y = p.y;

&nbsp;   b.facing = shoot\_direction;

&nbsp;   b.dano = int(w.damage);         // O dano real que vai machucar o boss/NPC

&nbsp;   b.distance = int(w.distance);   // Até onde a bala consegue viajar

&nbsp;   b.velocidade = 20;              // Velocidade de viagem no grid



&nbsp;   // Insere no array global de balas. 

&nbsp;   // O `bulletloop()` assumirá o controle a partir daqui!

&nbsp;   bullets.insert\_last(b);

}

O Círculo do Combate está completo! ⚔️

O que acabamos de fazer une todas as pontas:

1\. O jogador segura Ctrl e o Cliente desconta a bala do pente localmente e faz o barulho

5

.

2\. O Servidor recebe o pacote, escuta o estampido em 3D (para que os outros ouçam de onde veio o tiro) e invoca o objeto bullet na exata coordenada X/Y do jogador.

3\. O bulletloop() do seu servidor faz a bala voar tile por tile na direção do tiro

3

.

4\. Quando a bala bater no X/Y de um Monstro Ativo, a nossa função da Mini-Task 9 (check\_npc\_collisions) aplica o b.dano, subtrai o HP e aciona a IA do monstro para perseguir quem atirou (b.owner)

1

Como nós migramos o inventário para um sistema moderno com JSON (inventory\_sync.nvgt) na Task 5, recarregar a arma não é mais apenas uma ilusão no cliente. O cliente vai verificar se o jogador tem o item da munição e avisar o servidor. O servidor, de forma segura, vai descontar a caixa de munição do inventário real e tocar o som de recarga em 3D para todos ao redor

Aqui está a Mini-Task 13: Pentes de Munição e Recarga Automática.

Passo 1: O Motor da Arma no Cliente (weapon.nvgt)

No seu arquivo de cliente, a classe weapon precisa saber como se recarregar e como alternar o modo de tiro (Semiautomático/Automático).

Abra o arquivo weapon.nvgt (no cliente). Procure a sua class weapon { ... }

1

. Adicione a variável int current\_mode = 0; no topo das propriedades da classe e, no final dela (antes da chave de fechamento } da classe), adicione estes dois métodos:

&nbsp;   // Variável para controlar o modo de tiro (0 = Semi, 1 = Auto)

&nbsp;   int current\_mode = 0;



&nbsp;   // Método de recarga da arma

&nbsp;   void reload() {

&nbsp;       if(this.require\_ammo == 0) return; // Armas brancas/infinitas não recarregam

&nbsp;       if(this.loading == 1) return; // Evita bugar apertando R várias vezes

&nbsp;       

&nbsp;       if(this.ammo\_load >= this.ammo\_cantity) {

&nbsp;           speak(pu.get\_value("A arma já está totalmente carregada."));

&nbsp;           return;

&nbsp;       }



&nbsp;       // Verifica no inventário local se o jogador possui o item da munição (Ex: "municao\_9mm")

&nbsp;       if(inv\_item\_number(this.ammo) <= 0) {

&nbsp;           p.play\_stationary(this.sound\_unload + ".ogg", false);

&nbsp;           speak(pu.get\_value("Sem munição: ") + pu.get\_value(this.ammo));

&nbsp;           return;

&nbsp;       }



&nbsp;       // Trava o gatilho e inicia o timer de recarga

&nbsp;       this.loading = 1;

&nbsp;       this.tspeed\_reloading.restart();

&nbsp;       

&nbsp;       // Enche o pente de balas localmente

&nbsp;       this.ammo\_load = this.ammo\_cantity; 



&nbsp;       // Toca o som na orelha do atirador

&nbsp;       p.play\_stationary(this.sound\_reload + ".ogg", false);

&nbsp;       speak(pu.get\_value("Recarregando..."));



&nbsp;       // Avisa o servidor: "Me tire uma caixa de munição e toque o som 3D para os outros!"

&nbsp;       send\_reliable(peer\_id, "ACTION:reload|" + this.name, 4); // Canal de ações

&nbsp;   }



&nbsp;   // Alternar modo de tiro (Tecla T)

&nbsp;   void change\_mode() {

&nbsp;       if(this.enable\_burst == 0) return; // Arma não possui modo automático

&nbsp;       

&nbsp;       if(this.current\_mode == 0) {

&nbsp;           this.current\_mode = 1;

&nbsp;           p.play\_stationary(this.sound\_mode1 + ".ogg", false);

&nbsp;           speak(pu.get\_value("Modo Automático"));

&nbsp;       } else {

&nbsp;           this.current\_mode = 0;

&nbsp;           p.play\_stationary(this.sound\_mode2 + ".ogg", false);

&nbsp;           speak(pu.get\_value("Modo Semiautomático"));

&nbsp;       }

&nbsp;   }

(Nota: No nosso weaponcheckloop() da task anterior, eu já adicionei o gatilho para usar this.current\_mode na verificação de velocidade de tiro, então isso deixará a Tecla T perfeitamente funcional!)

Passo 2: A Validação Segura no Servidor (network\_handlers.nvgt)

O servidor agora vai receber o comando ACTION:reload|m4a1. Precisamos interceptá-lo.

Abra o arquivo server/includes/network\_handlers.nvgt

3

. Logo abaixo da função handle\_shoot que criamos antes, adicione a função de recarga:

// ============================================================================

// PROCESSAMENTO DE RECARGA DE ARMAS (Servidor)

// ============================================================================

void handle\_reload(player@ p, string data) {

&nbsp;   // data contém o nome da arma

&nbsp;   string weapon\_name = data;



&nbsp;   // Busca as propriedades da arma no banco do servidor

&nbsp;   int w\_index = get\_weapon\_index(weapon\_name);

&nbsp;   if (w\_index < 0) return;

&nbsp;   

&nbsp;   weapon@ w = weapons\_list\[w\_index];



&nbsp;   if (w.require\_ammo == 1) {

&nbsp;       // Usa a função moderna de sincronização JSON para remover a caixa de munição!

&nbsp;       if (remove\_item\_with\_sync(p, w.ammo, 1)) {

&nbsp;           // Sucesso! Toca o som de recarga em 3D para todos os outros jogadores próximos

&nbsp;           server\_broadcast("play\_body " + w.sound\_reload + ".ogg " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&nbsp;       } else {

&nbsp;           // Tentativa de Hack ou Lag extremo: Jogador pediu pra recarregar mas não tem a munição no banco

&nbsp;           send\_reliable\_text(p.peer\_id, "say \[SISTEMA] Falha ao recarregar: Faltam itens de munição em sua mochila (" + w.ammo + ").", 0);

&nbsp;       }

&nbsp;   } else {

&nbsp;       // Se a arma não requer munição, apenas toca o som para imersão

&nbsp;       server\_broadcast("play\_body " + w.sound\_reload + ".ogg " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&nbsp;   }

}

Passo 3: Plugar no Roteador (Servidor)

No mesmo arquivo (network\_handlers.nvgt), lá no seu Dispatcher (Roteador de pacotes principal), adicione o else if para redirecionar o tráfego:

&nbsp;   // (Dentro da sua função que intercepta os canais ou a string ACTION:)

&nbsp;   else if(parsed == "ACTION:reload" \&\& parsed.length() >= 2) {

&nbsp;       handle\_reload(p, parsed\[4]);

&nbsp;   }

O que ganhamos com isso?

Proteção total contra a famosa "munição infinita"! Antigamente, era fácil usar o Cheat Engine no BGT para travar o valor da munição. Agora, a cada "R" apertado, a arquitetura do remove\_item\_with\_sync obriga o servidor a auditar o banco de dados do jogador. Se não tiver munição verdadeira no SQLite, a arma dele não atira!

O combate de jogadores (PvE) está pronto!

Na Task 9, nós fizemos a bala do jogador bater no monstro e gravar o nome do atirador na variável golpeado da criatura. Agora vamos dar vida ao Cérebro do monstro para que ele use essa informação, persiga o jogador pelo mapa e ataque!

Vamos para a Mini-Task 14: Inteligência Artificial de Combate (Aggro e Perseguição).

Passo Único: O Loop de Perseguição e Ataque (Servidor)

Abra o arquivo server/includes/npc.nvgt (ou monstruo.nvgt, dependendo de onde está a sua função principal de loop das criaturas). Procure pela função npc\_global\_loop() e adicione a lógica de "Aggro" dentro do laço de repetição.

Substitua ou atualize a função para ficar assim:

// ============================================================================

// CÉREBRO DOS NPCS E MONSTROS (Perseguição e Combate) - Mini-Task 14

// ============================================================================



void npc\_global\_loop() {

&nbsp;   for(uint i = 0; i < npcs\_global.length(); i++) {

&nbsp;       // Pega a referência do NPC atual

&nbsp;       npc@ m = npcs\_global\[i];



&nbsp;       // Ignora NPCs mortos

&nbsp;       if(m.vida <= 0 || m.morreu) continue;



&nbsp;       // O monstro tem um alvo? (Alguém atirou nele na Task 9)

&nbsp;       if(m.golpeado != "") {

&nbsp;           int p\_idx = get\_player\_index\_from(m.golpeado);

&nbsp;           

&nbsp;           // Se o jogador ainda estiver online

&nbsp;           if(p\_idx > -1) {

&nbsp;               player@ p = players\[p\_idx];

&nbsp;               

&nbsp;               // Se o jogador estiver no mesmo mapa

&nbsp;               if(p.map == m.map \&\& p.health > 0) {

&nbsp;                   

&nbsp;                   // Calcula a distância entre o monstro e o jogador (Distância Manhattan)

&nbsp;                   int dist\_x = abs(p.x - m.x);

&nbsp;                   int dist\_y = abs(p.y - m.y);

&nbsp;                   int distancia\_total = dist\_x + dist\_y;



&nbsp;                   // 1. PERSEGUIÇÃO: Se estiver longe (mais de 2 tiles), anda na direção do jogador

&nbsp;                   if(distancia\_total > 2 \&\& m.tandar.elapsed >= 600) {

&nbsp;                       m.tandar.restart();

&nbsp;                       

&nbsp;                       if(m.x < p.x) m.x++;

&nbsp;                       else if(m.x > p.x) m.x--;



&nbsp;                       if(m.y < p.y) m.y++;

&nbsp;                       else if(m.y > p.y) m.y--;



&nbsp;                       // Toca o som de passo do monstro em 3D para os jogadores ouvirem ele se aproximando!

&nbsp;                       server\_broadcast("play\_npc step1.ogg " + m.x + " " + m.y, m.map);

&nbsp;                   }

&nbsp;                   

&nbsp;                   // 2. ATAQUE: Se estiver muito perto (2 tiles ou menos), ataca!

&nbsp;                   else if(distancia\_total <= 2 \&\& m.tatirar.elapsed >= 1500) {

&nbsp;                       m.tatirar.restart();

&nbsp;                       

&nbsp;                       // Toca o som do monstro atacando/mordendo em 3D

&nbsp;                       server\_broadcast("play\_npc mordida.ogg " + m.x + " " + m.y, m.map);



&nbsp;                       // Arranca a vida do jogador (Ex: 15 de dano)

&nbsp;                       p.health -= 15;

&nbsp;                       

&nbsp;                       // Toca som de dor no cliente do jogador

&nbsp;                       send\_reliable\_text(p.peer\_id, "play\_stationary pain1.ogg", 0);

&nbsp;                       send\_reliable\_text(p.peer\_id, "say \[Combate] O " + m.nome + " te atacou! Sua vida: " + p.health, 0);



&nbsp;                       // Se o jogador morrer para o monstro

&nbsp;                       if(p.health <= 0) {

&nbsp;                           send\_reliable\_text(p.peer\_id, "say Você foi morto por " + m.nome + "!", 0);

&nbsp;                           server\_broadcast("play\_body mortejogador.ogg " + p.x + " " + p.y, p.map);

&nbsp;                           

&nbsp;                           // O monstro perde o alvo e volta a patrulhar pacificamente

&nbsp;                           m.golpeado = ""; 

&nbsp;                           

&nbsp;                           // Aqui entraria a sua lógica de teletransportar o player morto pro hospital/spawn

&nbsp;                       }

&nbsp;                   }

&nbsp;               } else {

&nbsp;                   // O jogador fugiu para outro mapa, o monstro perde o interesse

&nbsp;                   m.golpeado = "";

&nbsp;               }

&nbsp;           } else {

&nbsp;               // Jogador deslogou, o monstro perde o alvo

&nbsp;               m.golpeado = "";

&nbsp;           }

&nbsp;       }

&nbsp;       else {

&nbsp;           // Lógica de Patrulha Passiva (quando não está atacando ninguém)

&nbsp;           if(m.tandar.elapsed >= 2000) {

&nbsp;               m.tandar.restart();

&nbsp;               // Aqui o monstro dá passos aleatórios no mapa se você quiser

&nbsp;           }

&nbsp;       }

&nbsp;   }

}

Como a Mágica Acontece Agora?

O ciclo do seu MMORPG está 100% respirando sozinho:

1\. Você acha o Monstro usando o Radar de Inimigos (Ctrl + Enter ou Tab que criamos antes).

2\. Você segura Ctrl para atirar. A sua bala tira HP do monstro e diz: "Fui eu quem atirou, pegue-me se for capaz!" (m.golpeado = player\_name).

3\. Imediatamente, esse código acima desperta! A cada 600ms o servidor recalcula o X/Y do jogador e aproxima o monstro, emitindo os temidos passos pesados (step1.ogg) pelo mapa! O Steam Audio (HRTF) faz o jogador ouvir o bicho chegando perto no fone de ouvido.

4\. Se o monstro encostar, ele morde (Tira 15 de HP).

5\. Se a arma for melhor e você matar ele antes, a função de Loot entra em ação e espalha as moedas no chão para você pegar com Enter.

É a jogabilidade completa de sobrevivência implementada em NVGT nativo!

Uma obcervação, pra achar mpcs no radar, é a letra m, como definimos, se não tiver nada por perto, ele só vai falar, nada por perto

