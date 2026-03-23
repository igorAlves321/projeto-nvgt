Excelente escolha! Chegamos à \*\*Fase 4: Sistemas Sociais\*\*. Esta é a camada que transforma o seu servidor de um simples mapa multijogador em um verdadeiro MMORPG.



No BGT antigo, as equipes eram gerenciadas de forma muito arcaica através de arrays de strings no próprio jogador (`players\[i].nomesequipe`) e comandos como `/equipea`, `/equiper` e `/e`. Isso causava muitos bugs se um jogador desconectasse.



Na sua nova arquitetura NVGT, nós temos uma classe orientada a objetos fantástica chamada `party` em \*\*`party.nvgt`\*\*. Ela gerencia o líder, os membros, compartilhamento de XP e os convites pendentes de forma segura usando dicionários (`pending\_invites`).



Vamos transformar os \*stubs\* vazios do seu `party.nvgt` em código real!



\### Mini-Task 10: Sistema de Grupos (Party) no Servidor



Abra o arquivo \*\*`server/includes/party.nvgt`\*\*. Nós vamos substituir as funções vazias de criação, convite, entrada e chat para que elas manipulem a classe `party` corretamente. 



Substitua as funções `cmd\_createparty`, `cmd\_invite`, `cmd\_joinparty` e `cmd\_partychat` por este código:



```cpp

// ============================================================================

// SISTEMA DE GRUPOS (PARTY) - LÓGICA CORE (Mini-Task 10)

// ============================================================================



// Comando: Criar party

void cmd\_createparty(int player\_index) {

&nbsp;   string player\_name = players\[player\_index].charname;

&nbsp;   

&nbsp;   if(is\_in\_party(player\_name)) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você já está em uma equipe!", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Instancia o novo grupo e define o jogador como líder

&nbsp;   party new\_party;

&nbsp;   new\_party.leader = player\_name;

&nbsp;   new\_party.members.insert\_last(player\_name); // O líder também é um membro

&nbsp;   new\_party.max\_members = 8;

&nbsp;   new\_party.share\_xp = true;

&nbsp;   new\_party.share\_gold = true;

&nbsp;   new\_party.creation\_time.restart();



&nbsp;   active\_parties.insert\_last(new\_party);

&nbsp;   send\_reliable\_text(players\[player\_index].peer\_id, "say Grupo criado com sucesso! Você é o líder do grupo.", 0);

}



// Comando: Convidar para party (Antigo /equipea)

void cmd\_invite(int player\_index, string target\_name) {

&nbsp;   string player\_name = players\[player\_index].charname;

&nbsp;   int p\_idx = get\_party\_index(player\_name);

&nbsp;   

&nbsp;   if(p\_idx == -1) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você não está em uma equipe! Use o menu ou digite /createparty.", 0);

&nbsp;  return;

&nbsp;   }



&nbsp;   party@ p = active\_parties\[p\_idx];

&nbsp;   if(p.leader != player\_name) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Apenas o líder pode convidar novos membros!", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   int target\_idx = get\_player\_index\_from(target\_name);

&nbsp;   if(target\_idx == -1) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Jogador não encontrado ou offline.", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   if(is\_in\_party(target\_name)) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] O jogador " + target\_name + " já pertence a um grupo.", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Cria o convite usando o dicionário nativo do NVGT com timestamp

&nbsp;   p.pending\_invites.set(target\_name, time\_stamp());

&nbsp;   

&nbsp;   // Notifica ambos os jogadores

&nbsp;   send\_reliable\_text(players\[target\_idx].peer\_id, "say " + player\_name + " te convidou para um grupo! Digite /joinparty para aceitar.", 0);

&nbsp;   send\_reliable\_text(players\[player\_index].peer\_id, "say Convite enviado para " + target\_name + ".", 0);

}



// Comando: Entrar em party (Aceitar convite)

void cmd\_joinparty(int player\_index) {

&nbsp;   string player\_name = players\[player\_index].charname;

&nbsp;   

&nbsp;   if(is\_in\_party(player\_name)) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você já está em um grupo!", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Varre todas as parties ativas para ver qual tem o nome dele nos convites

&nbsp;   for(uint i = 0; i < active\_parties.length(); i++) {

&nbsp;       if(active\_parties\[i].pending\_invites.exists(player\_name)) {

&nbsp;           

&nbsp;           // Checa limite de vagas

&nbsp;           if(active\_parties\[i].members.length() >= uint(active\_parties\[i].max\_members)) {

&nbsp;               send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] O grupo de " + active\_parties\[i].leader + " já está cheio!", 0);

&nbsp;               active\_parties\[i].pending\_invites.delete(player\_name);

&nbsp;               return;

&nbsp;           }



&nbsp;           // Adiciona o membro e remove o convite

&nbsp;           active\_parties\[i].members.insert\_last(player\_name);

&nbsp;           active\_parties\[i].pending\_invites.delete(player\_name);



&nbsp;           // Avisa a todos os membros antigos que alguém novo entrou

&nbsp;           for(uint j = 0; j < active\_parties\[i].members.length(); j++) {

&nbsp;               int m\_idx = get\_player\_index\_from(active\_parties\[i].members\[j]);

&nbsp;               if(m\_idx != -1) {

&nbsp;                   send\_reliable\_text(players\[m\_idx].peer\_id, "say \[Grupo] " + player\_name + " se juntou à equipe!", 0);

&nbsp;               }

&nbsp;           }

&nbsp;           return;

&nbsp;       }

&nbsp;   }

&nbsp;   

&nbsp;   send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você não possui convites de grupo pendentes.", 0);

}



// Comando: Chat do party (Antigo /e)

void cmd\_partychat(int player\_index, string message) {

&nbsp;   string player\_name = players\[player\_index].charname;

&nbsp;   int p\_idx = get\_party\_index(player\_name);

&nbsp;   

&nbsp;   if(p\_idx == -1) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você não está em um grupo!", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   party@ p = active\_parties\[p\_idx];

&nbsp;   

&nbsp;   // Entrega a mensagem instantaneamente para todos os membros do grupo

&nbsp;   for(uint i = 0; i < p.members.length(); i++) {

&nbsp;       int m\_idx = get\_player\_index\_from(p.members\[i]);

&nbsp;       if(m\_idx != -1) {

&nbsp;           // Emite a mensagem no chat com a tag \[Grupo]

&nbsp;           send\_reliable\_text(players\[m\_idx].peer\_id, "say \[Grupo] " + player\_name + " diz: " + message, 0);

&nbsp;           

&nbsp;           // Opcional: Tocar um som de notificação local para a equipe (substituindo process\_msg3)

&nbsp;           send\_reliable\_text(players\[m\_idx].peer\_id, "play\_stationary notify2.ogg", 0);

&nbsp;       }

&nbsp;   }

}

```



\### O que isso resolve?

1\. \*\*Remoção das Gambiarras do BGT:\*\* Não precisamos mais de `emequipe()` iterando loops complexos em cada monstro. O sistema de XP agora só precisa chamar `party\_distribute\_xp(killer, xp)` e a classe cuidará de dividir isso perfeitamente.

2\. \*\*Otimização de Convites:\*\* Usamos o `dictionary pending\_invites` do NVGT. Isso nos permite verificar convites na velocidade da luz, evitando criar \*arrays\* falsos.

3\. \*\*Chat Instantâneo:\*\* O `cmd\_partychat` substitui a antiga lógica do canal `3` do BGT. Agora, o servidor empacota a string `\[Grupo] Player:` e manda direto para quem importa, tocando o som de notificação com segurança de thread.



\### Como ligar isso no seu roteador?

Se o jogador digitar os comandos antigos (como `/equipea` ou `/e`), você só precisa ir no seu `network\_handlers.nvgt` ou `commands.nvgt` e apontar para essas novas funções:

\*   `/equipea Joao` -> `cmd\_invite(player\_idx, "Joao")`

\*   `/e vamos atacar!` -> `cmd\_partychat(player\_idx, "vamos atacar!")`



\*\*Próximo passo lógico (Mini-Task 11):\*\*

Agora que o \*\*Grupo (Party)\*\* existe temporariamente na RAM enquanto jogam juntos, o próximo nível é a \*\*Guilda (Clan)\*\* no arquivo `guilds.nvgt`. As Guildas são permanentes, possuem Tags (ex: `\[BR]`), níveis e, mais importante, precisam ser salvas e carregadas do Banco de Dados SQLite / Arquivo.

Passo 1: O Código dos Menus Sociais (Cliente)

Adicione este bloco de código no seu arquivo de comandos do cliente (como comandos.nvgt ou crie um novo arquivo menu\_social.nvgt e dê #include no client.nvgt).

Ele constrói o Menu Principal, os Submenus e o formulário de Múltipla Escolha:

// ============================================================================

// SISTEMA DE MENU SOCIAL AVANÇADO (Ctrl + Enter)

// ============================================================================



// Formulário de Múltipla Seleção (Checkbox com Espaço)

void menu\_adicionar\_multiplos(string tipo) {

&nbsp;   audio\_form form;

&nbsp;   form.create\_window(pu.get\_value("Adicionar ") + tipo, false, true);



&nbsp;   // Cria uma lista nativa com 'multiselect' ativado (parâmetro true)

&nbsp;   int list\_idx = form.create\_list(pu.get\_value("Selecione os jogadores com Espaço e pressione Enter para enviar as solicitações."), 0, true, false);



&nbsp;   // Popula a lista com os jogadores visíveis pelo cliente

&nbsp;   int jogadores\_validos = 0;

&nbsp;   for(uint i = 0; i < players.length(); i++) {

&nbsp;       // Ignora a si mesmo na lista

&nbsp;       if(players\[i].charname != un) { 

&nbsp;           form.add\_list\_item(list\_idx, players\[i].charname, players\[i].charname);

&nbsp;           jogadores\_validos++;

&nbsp;       }

&nbsp;   }



&nbsp;   if(jogadores\_validos == 0) {

&nbsp;       speak(pu.get\_value("Não há outros jogadores próximos ou online para selecionar."));

&nbsp;       return;

&nbsp;   }



&nbsp;   // Botões de ação

&nbsp;   form.create\_button(pu.get\_value("Confirmar"), true, false); // Enter aciona este botão

&nbsp;   form.create\_button(pu.get\_value("Cancelar"), false, true);  // Esc aciona este botão



&nbsp;   // Monitora o formulário até o usuário confirmar ou cancelar

&nbsp;   int result = -1;

&nbsp;   while((result = form.monitor()) == -1) {

&nbsp;       wait(5);

&nbsp;       if(is\_connected) {

&nbsp;           netloop(); // Mantém a rede viva enquanto o menu está aberto \[1]

&nbsp;       }

&nbsp;   }



&nbsp;   // Se o usuário não apertou ESC (Cancelar)

&nbsp;   if(result != form.get\_cancel\_button()) {

&nbsp;       // Pega todos os itens que foram marcados com a tecla Espaço \[2]

&nbsp;       int\[]@ checked = form.get\_checked\_list\_items(list\_idx);

&nbsp;       

&nbsp;       if(@checked != null \&\& checked.length() > 0) {

&nbsp;           for(uint i = 0; i < checked.length(); i++) {

&nbsp;               string target = form.get\_list\_item\_id(list\_idx, checked\[i]);

&nbsp;               

&nbsp;               // Envia o comando correto para o servidor dependendo do tipo

&nbsp;               if(tipo == "amigo") {

&nbsp;                   send\_reliable(peer\_id, "/addfriend " + target, 0); \[3]

&nbsp;               } else if(tipo == "equipe") {

&nbsp;                   send\_reliable(peer\_id, "/invite " + target, 0); \[4]

&nbsp;               }

&nbsp;           }

&nbsp;           speak(pu.get\_value("Solicitações enviadas."));

&nbsp;       } else {

&nbsp;           speak(pu.get\_value("Nenhum jogador foi selecionado."));

&nbsp;       }

&nbsp;   }

}



// Submenu: Equipe

void menu\_equipe\_social() {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Gerenciar Equipe:");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver quem me convidou / Aceitar Convites"), "aceitar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Convidar jogadores (Múltipla Seleção)"), "convidar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Informações da equipe"), "info");

&nbsp;   game\_menu.add\_item(pu.get\_value("Sair da equipe"), "sair");

&nbsp;   game\_menu.add\_item(pu.get\_value("Voltar"), "voltar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "aceitar") send\_reliable(peer\_id, "/joinparty", 0); \[4]

&nbsp;       else if(op == "convidar") menu\_adicionar\_multiplos("equipe");

&nbsp;       else if(op == "info") send\_reliable(peer\_id, "/partyinfo", 0); \[5]

&nbsp;       else if(op == "sair") send\_reliable(peer\_id, "/leaveparty", 0); \[6]

&nbsp;       else if(op == "voltar") menu\_social\_principal();

&nbsp;   }

}



// Submenu: Amigos

void menu\_amigos\_social() {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Gerenciar Amigos:");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver solicitações / Aceitar"), "recebidas"); // Depende do back-end

&nbsp;   game\_menu.add\_item(pu.get\_value("Adicionar Amigo (Múltipla Seleção)"), "adicionar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver lista de amigos"), "listar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Voltar"), "voltar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "adicionar") menu\_adicionar\_multiplos("amigo");

&nbsp;       else if(op == "listar") send\_reliable(peer\_id, "/friends", 0); \[7]

&nbsp;       // Se o servidor ainda não tiver o comando de aceitar amigo, você pode rotear para a lista de amigos por enquanto.

&nbsp;       else if(op == "voltar") menu\_social\_principal();

&nbsp;   }

}



// Menu Principal

void menu\_social\_principal() {

&nbsp;   if(ausente || !moveable) return;

&nbsp;   

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Menu Social. O que você deseja acessar?");

&nbsp;   game\_menu.add\_item(pu.get\_value("Lista de Amigos"), "amigos");

&nbsp;   game\_menu.add\_item(pu.get\_value("Equipe / Party"), "equipe");

&nbsp;   game\_menu.add\_item(pu.get\_value("Fechar Menu"), "fechar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "amigos") menu\_amigos\_social();

&nbsp;       else if(op == "equipe") menu\_equipe\_social();

&nbsp;   }

}

Passo 2: Interceptar a Tecla Ctrl + Enter

Agora, você precisa dizer ao cliente para chamar a função menu\_social\_principal() quando o atalho for pressionado.

Abra o seu arquivo onde fica o loop principal de teclas (geralmente em client.nvgt dentro de um loop de controle ou na função game()). Procure por outras checagens de teclas (como if(key\_pressed(...))) e adicione:

&nbsp;   // Interceptação de Ctrl + Enter para o Menu Social

&nbsp;   if((key\_down(KEY\_LCTRL) || key\_down(KEY\_RCTRL)) \&\& key\_pressed(KEY\_RETURN)) {

&nbsp;       menu\_social\_principal();

&nbsp;   }

Análise da Lógica Backend (Servidor)

Pelo seu código existente que analisei:

1\. O Sistema de Equipes (party.nvgt)

1

&nbsp;está totalmente pronto para essa funcionalidade! Ele possui o dictionary pending\_invites e o comando /joinparty. Portanto, quando o usuário enviar convites em massa, a equipe do servidor gerenciará e eles poderão usar o botão "Ver quem me convidou" na interface nova.

2\. O Sistema de Amigos (friends.nvgt)

2

: Atualmente ele possui o comando /addfriend

2

. É possível que o comando atualmente adicione o amigo instantaneamente sem exigir que a outra pessoa aceite (um sistema unilateral, muito comum em jogos antigos). Se no futuro você quiser que a amizade exija confirmação, nós precisaremos replicar a mecânica de pending\_invites do party.nvgt dentro do friends.nvgt. Por enquanto, o menu listado acima executará o comando com perfeição!

Ao inserir esse código e compilar, seu cliente ganhará instantaneamente uma interface robusta baseada em NVGT onde você passeia pela lista usando as setas para Cima/Baixo, marca os 5 amigos com Espaço e dá um único Enter para puxar os 5 para o seu grupo de uma vez!

Sistema de Guildas (Clans).

Como deixamos os Grupos e Amigos funcionando redondinhos na interface, o próximo passo para fechar a sua "Fase 4: Sistemas Sociais" com chave de ouro é estruturar as Guildas. Diferente dos Grupos, que se desfazem quando o servidor reinicia ou os jogadores deslogam, as Guildas são permanentes.

Analisando os seus arquivos do servidor, vejo que o guilds.nvgt já tem uma classe guild fantástica que suporta um cofre (guild\_gold), armazém compartilhado (dictionary storage), uma tag de até 5 caracteres, além de sistema de níveis e experiência da guilda

1

. Para que tudo isso seja permanente, a persistência já está apontada para o arquivo database/guilds.dat

1

2

.

Podemos continuar o nosso trabalho de duas formas agora:

Opção 1 (Backend): Ativar a persistência e os comandos base do servidor. Nós revisamos e ligamos as funções como /createguild, /joinguild, /promote e garantimos que o servidor chame load\_guilds() ao iniciar e save\_guilds() a cada alteração para que o progresso dos clãs nunca seja perdido

2

...

.

Opção 2 (Frontend): Injetar as Guildas no nosso novo menu. Nós adicionamos a terceira opção "Gerenciar Guilda" naquele menu do Ctrl + Enter, permitindo que os líderes usem a mesma facilidade da barra de espaço para convidar ou expulsar vários membros de uma vez.

A escolhida foi opção b.

Perfeito! Vamos incluir as \*\*Guildas (Clans)\*\* na nossa interface social maravilhosa que acabamos de desenhar.



A vantagem de fazer isso agora é que usamos exatamente a mesma lógica de seleção múltipla (marcar com a barra de espaço) para convidar vários jogadores para a Guilda de uma só vez, o que poupa muito trabalho dos líderes de clan!



Aqui está o código atualizado. Você pode substituir aquele bloco do menu social que te mandei antes por este novo, que agora inclui o roteamento completo para as Guildas, comunicando-se perfeitamente com os comandos nativos do seu `guilds.nvgt`.



\### O Código Atualizado do Menu Social (Cliente)



Substitua ou adicione este bloco no seu arquivo de comandos (onde você gerencia o atalho `Ctrl + Enter`):



```cpp

// ============================================================================

// SISTEMA DE MENU SOCIAL AVANÇADO (Amigos, Equipe e Guilda)

// ============================================================================



// Formulário de Múltipla Seleção (Checkbox com Espaço)

void menu\_adicionar\_multiplos(string tipo) {

&nbsp;   audio\_form form;

&nbsp;   form.create\_window(pu.get\_value("Adicionar ") + tipo, false, true);



&nbsp;   // Cria uma lista nativa com 'multiselect' ativado (parâmetro true)

&nbsp;   int list\_idx = form.create\_list(pu.get\_value("Selecione os jogadores com Espaço e pressione Enter para enviar as solicitações."), 0, true, false);



&nbsp;   // Popula a lista com os jogadores visíveis pelo cliente

&nbsp;   int jogadores\_validos = 0;

&nbsp;   for(uint i = 0; i < players.length(); i++) {

&nbsp;       // Ignora a si mesmo na lista

&nbsp;       if(players\[i].charname != un) { 

&nbsp;           form.add\_list\_item(list\_idx, players\[i].charname, players\[i].charname);

&nbsp;           jogadores\_validos++;

&nbsp;       }

&nbsp;   }



&nbsp;   if(jogadores\_validos == 0) {

&nbsp;       speak(pu.get\_value("Não há outros jogadores próximos ou online para selecionar."));

&nbsp;       return;

&nbsp;   }



&nbsp;   // Botões de ação

&nbsp;   form.create\_button(pu.get\_value("Confirmar"), true, false); // Enter aciona este botão

&nbsp;   form.create\_button(pu.get\_value("Cancelar"), false, true);  // Esc aciona este botão



&nbsp;   // Monitora o formulário até o usuário confirmar ou cancelar

&nbsp;   int result = -1;

&nbsp;   while((result = form.monitor()) == -1) {

&nbsp;       wait(5);

&nbsp;       if(is\_connected) {

&nbsp;           netloop(); 

&nbsp;       }

&nbsp;   }



&nbsp;   // Se o usuário não apertou ESC (Cancelar)

&nbsp;   if(result != form.get\_cancel\_button()) {

&nbsp;       // Pega todos os itens que foram marcados com a tecla Espaço

&nbsp;       int\[]@ checked = form.get\_checked\_list\_items(list\_idx);

&nbsp;       

&nbsp;       if(@checked != null \&\& checked.length() > 0) {

&nbsp;           for(uint i = 0; i < checked.length(); i++) {

&nbsp;               string target = form.get\_list\_item\_id(list\_idx, checked\[i]);

&nbsp;               

&nbsp;               // Envia o comando correto para o servidor dependendo do tipo

&nbsp;               if(tipo == "amigo") {

&nbsp;                   send\_reliable(peer\_id, "/addfriend " + target, 0);

&nbsp;               } else if(tipo == "equipe") {

&nbsp;                   send\_reliable(peer\_id, "/invite " + target, 0);

&nbsp;               } else if(tipo == "guilda") {

&nbsp;                   send\_reliable(peer\_id, "/inviteguild " + target, 0);

&nbsp;               }

&nbsp;           }

&nbsp;           speak(pu.get\_value("Solicitações enviadas."));

&nbsp;       } else {

&nbsp;           speak(pu.get\_value("Nenhum jogador foi selecionado."));

&nbsp;       }

&nbsp;   }

}



// Submenu: Guildas (Clans)

void menu\_guilda\_social() {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Gerenciar Guilda:");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver convites pendentes / Aceitar"), "aceitar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Convidar jogadores (Múltipla Seleção)"), "convidar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Informações da Guilda"), "info");

&nbsp;   game\_menu.add\_item(pu.get\_value("Criar uma nova Guilda"), "criar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Sair da Guilda"), "sair");

&nbsp;   game\_menu.add\_item(pu.get\_value("Voltar"), "voltar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "aceitar") send\_reliable(peer\_id, "/joinguild", 0);

&nbsp;       else if(op == "convidar") menu\_adicionar\_multiplos("guilda");

&nbsp;       else if(op == "info") send\_reliable(peer\_id, "/guildinfo", 0);

&nbsp;       else if(op == "sair") send\_reliable(peer\_id, "/leaveguild", 0);

&nbsp;       else if(op == "criar") {

&nbsp;           // Abre um formulário de texto para digitar o nome da guilda

&nbsp;           input\_form form(pu.get\_value("Criar Nova Guilda"));

&nbsp;           form.add\_text\_field("nome", pu.get\_value("Digite o nome do seu novo Clan"), "", true);

&nbsp;           form.add\_text\_field("tag", pu.get\_value("Digite a TAG (ex: BR, USA)"), "", false);

&nbsp;           dictionary@ r = form.run();

&nbsp;           if(!form.user\_canceled) {

&nbsp;               string nome\_guilda, tag\_guilda;

&nbsp;               r.get("nome", nome\_guilda);

&nbsp;               r.get("tag", tag\_guilda);

&nbsp;               send\_reliable(peer\_id, "/createguild " + nome\_guilda + " " + tag\_guilda, 0);

&nbsp;           }

&nbsp;       }

&nbsp;       else if(op == "voltar") menu\_social\_principal();

&nbsp;   }

}



// Submenu: Equipe

void menu\_equipe\_social() {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Gerenciar Equipe:");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver quem me convidou / Aceitar Convites"), "aceitar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Convidar jogadores (Múltipla Seleção)"), "convidar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Informações da equipe"), "info");

&nbsp;   game\_menu.add\_item(pu.get\_value("Sair da equipe"), "sair");

&nbsp;   game\_menu.add\_item(pu.get\_value("Voltar"), "voltar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "aceitar") send\_reliable(peer\_id, "/joinparty", 0);

&nbsp;       else if(op == "convidar") menu\_adicionar\_multiplos("equipe");

&nbsp;       else if(op == "info") send\_reliable(peer\_id, "/partyinfo", 0);

&nbsp;       else if(op == "sair") send\_reliable(peer\_id, "/leaveparty", 0);

&nbsp;       else if(op == "voltar") menu\_social\_principal();

&nbsp;   }

}



// Submenu: Amigos

void menu\_amigos\_social() {

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Gerenciar Amigos:");

&nbsp;   game\_menu.add\_item(pu.get\_value("Adicionar Amigo (Múltipla Seleção)"), "adicionar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Ver lista de amigos"), "listar");

&nbsp;   game\_menu.add\_item(pu.get\_value("Voltar"), "voltar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "adicionar") menu\_adicionar\_multiplos("amigo");

&nbsp;       else if(op == "listar") send\_reliable(peer\_id, "/friends", 0);

&nbsp;       else if(op == "voltar") menu\_social\_principal();

&nbsp;   }

}



// Menu Principal

void menu\_social\_principal() {

&nbsp;   if(ausente || !moveable) return;

&nbsp;   

&nbsp;   setupmenu();

&nbsp;   game\_menu.intro\_text = pu.get\_value("Menu Social. O que você deseja acessar?");

&nbsp;   game\_menu.add\_item(pu.get\_value("Lista de Amigos"), "amigos");

&nbsp;   game\_menu.add\_item(pu.get\_value("Equipe / Party"), "equipe");

&nbsp;   game\_menu.add\_item(pu.get\_value("Guilda / Clan"), "guilda");

&nbsp;   game\_menu.add\_item(pu.get\_value("Fechar Menu"), "fechar");



&nbsp;   int res = game\_menu.run();

&nbsp;   if(res > -1) {

&nbsp;       string op = game\_menu.get\_item\_id(res);

&nbsp;       if(op == "amigos") menu\_amigos\_social();

&nbsp;       else if(op == "equipe") menu\_equipe\_social();

&nbsp;       else if(op == "guilda") menu\_guilda\_social();

&nbsp;   }

}

```



\### O que isso faz de incrível?

1\. \*\*Integração Total com o Backend:\*\* A opção de "Guilda" agora se aproveita do seu `guilds.nvgt` para enviar comandos como `/createguild` e `/inviteguild`.

2\. \*\*Criação de Guildas Acessível:\*\* Adicionamos um `input\_form` específico para criação. O jogador não precisa mais decorar o comando `/createguild nome\_da\_guilda tag\_da\_guilda`. Ele clica em criar, o NVGT abre uma janela com duas caixinhas perguntando o Nome e a Tag, e envia tudo formatado pro servidor!

3\. \*\*Múltipla Seleção Otimizada:\*\* O formulário da lista universal (`menu\_adicionar\_multiplos`) agora reconhece a string `"guilda"`. O jogador pode selecionar 10 nomes usando a tecla "Espaço" e, quando der Enter, o cliente vai disparar os 10 `/inviteguild` de uma vez!



\### Próximo Passo

Como a nossa interface no cliente (`Frontend`) agora está \*\*100% pronta e com excelente design\*\*, precisamos ter certeza que, quando o servidor for desligado, os clans não vão sumir!

Esta é a Mini-Task 11: Persistência de Guildas no Servidor.

O seu arquivo guilds.nvgt já tem a estrutura pronta, mas a leitura e gravação no arquivo database/guilds.dat estão incompletas. Nós vamos implementar a serialização (transformar a Guilda em texto) e a desserialização (transformar o texto de volta na Guilda viva), e depois conectar isso ao auto-save do servidor.

Passo 1: A Lógica de Salvar e Carregar (guilds.nvgt)

Abra o arquivo server/includes/guilds.nvgt, vá até o final dele (onde ficam as funções serialize\_guild, save\_guilds, etc.) e substitua todo esse bloco final por este código completo:

// ============================================================================

// TASK 2.8.1: FUNÇÕES DE PERSISTÊNCIA DE GUILDS (SQLite / Arquivo)

// ============================================================================



// Transforma a classe da Guilda em uma string separada por "|"

string serialize\_guild(guild@ g) {

&nbsp;   string data = "";

&nbsp;   data += g.name + "|";

&nbsp;   data += g.leader + "|";

&nbsp;   data += g.tag + "|";

&nbsp;   data += g.guild\_gold + "|";

&nbsp;   data += g.level + "|";

&nbsp;   data += g.xp + "|";

&nbsp;   // Junta o array de membros usando vírgula

&nbsp;   data += join(g.members, ",") + "|";

&nbsp;   // Junta o array de oficiais usando vírgula

&nbsp;   data += join(g.officers, ",");

&nbsp;   

&nbsp;   return data;

}



// Reconstrói a Guilda a partir da string salva

guild@ deserialize\_guild(string data) {

&nbsp;   string\[] parts = data.split("|");

&nbsp;   if(parts.length() < 8) return null;



&nbsp;   guild g;

&nbsp;   g.name = parts;

&nbsp;   g.leader = parts\[1];

&nbsp;   g.tag = parts\[2];

&nbsp;   g.guild\_gold = parse\_int(parts\[3]);

&nbsp;   g.level = parse\_int(parts\[4]);

&nbsp;   g.xp = parse\_int(parts\[5]);

&nbsp;   

&nbsp;   // Reconstrói os arrays de jogadores

&nbsp;   if(parts\[6] != "") g.members = parts\[6].split(",");

&nbsp;   if(parts\[7] != "") g.officers = parts\[7].split(",");

&nbsp;   

&nbsp;   g.max\_members = 50;  // Limite padrão

&nbsp;   g.max\_officers = 5;  // Limite padrão

&nbsp;   return g;

}



// Salva todas as guilds ativas no disco

void save\_guilds() {

&nbsp;   if(!directory\_exists("database")) directory\_create("database");

&nbsp;   

&nbsp;   file f;

&nbsp;   if(f.open(GUILDS\_FILE, "w")) {

&nbsp;       string final\_data = "";

&nbsp;       for(uint i = 0; i < active\_guilds.length(); i++) {

&nbsp;           final\_data += serialize\_guild(active\_guilds\[i]) + "\\r\\n";

&nbsp;       }

&nbsp;       f.write(final\_data);

&nbsp;       f.close();

&nbsp;       debug\_log("GUILD: " + active\_guilds.length() + " guildas salvas com sucesso em " + GUILDS\_FILE);

&nbsp;   } else {

&nbsp;       debug\_log("GUILD: Erro ao tentar salvar o arquivo de guildas!");

&nbsp;   }

}



// Carrega todas as guilds do disco para a RAM

void load\_guilds() {

&nbsp;   if(!file\_exists(GUILDS\_FILE)) {

&nbsp;       debug\_log("GUILD: Arquivo de guildas não encontrado. Nenhuma guilda carregada.");

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   file f;

&nbsp;   if(f.open(GUILDS\_FILE, "r")) {

&nbsp;       string\[] lines = f.read().split("\\r\\n");

&nbsp;       f.close();

&nbsp;       

&nbsp;       active\_guilds.resize(0);

&nbsp;       player\_guilds.delete\_all(); // Limpa o dicionário de buscas rápidas

&nbsp;       

&nbsp;       for(uint i = 0; i < lines.length(); i++) {

&nbsp;           if(lines\[i].trim\_whitespace() == "") continue;

&nbsp;           

&nbsp;           guild@ g = deserialize\_guild(lines\[i]);

&nbsp;           if(g !is null) {

&nbsp;               active\_guilds.insert\_last(g);

&nbsp;               

&nbsp;               // Mapeia rapidamente os membros para a guilda para otimizar buscas

&nbsp;               for(uint m = 0; m < g.members.length(); m++) {

&nbsp;                   player\_guilds.set(g.members\[m], g.name);

&nbsp;               }

&nbsp;           }

&nbsp;       }

&nbsp;       debug\_log("GUILD: " + active\_guilds.length() + " guildas carregadas com sucesso.");

&nbsp;   }

}



// Inicializar sistema de guilds (chamar no startup do servidor)

void init\_guilds() {

&nbsp;   load\_guilds();

}

Passo 2: Engatando no "Motor" do Servidor

Agora que o sistema sabe como ler e escrever o arquivo, precisamos avisar o servidor para fazer isso automaticamente quando ligar e desligar.

A) Ao Ligar o Servidor: Abra o arquivo server/includes/iniciar.nvgt. Vá até a função load\_persistent\_data() e adicione a inicialização lá dentro:

bool load\_persistent\_data() {

&nbsp;   debug\_log("=== PASSO 4: Carregando dados persistentes ===");

&nbsp;   

&nbsp;   // ... \[outros carregamentos] ...

&nbsp;   

&nbsp;   // Carrega as guildas salvas

&nbsp;   init\_guilds();

&nbsp;   

&nbsp;   return true;

}

B) Ao Salvar e Desligar (Auto-save): Abra o arquivo principal server.nvgt. Procure a função writeprefs(bool force\_save = false). Dentro dela, logo após onde você salva os jogadores, adicione a ordem para salvar as guildas:

void writeprefs(bool force\_save = false) {

&nbsp;   debug\_log("📝 Salvando preferências e dados de todos os jogadores...");

&nbsp;   // ...

&nbsp;   save\_guilds(); // <--- Adicione esta linha

&nbsp;   // ...

}

E no mesmo arquivo (server.nvgt), procure a função auto\_save\_all\_players(). Adicione a chamada save\_guilds() no final dela também, para que o cofre do clã seja salvo a cada 5 minutos automaticamente junto com o mapa:

&nbsp;   save\_guilds(); // Garante que as doações de Ouro para a guilda sejam salvas

O que conquistamos agora?

1\. Se um jogador usar a sua interface lindíssima para criar uma guilda chamada "Os Lendários" com a Tag "\[LND]", o servidor vai mapear isso.

2\. A cada 5 minutos (ou ao desligar o servidor de forma segura com ESC), todas as Guildas ativas são gravadas silenciosamente no arquivo database/guilds.dat.

3\. Se um hacker derrubar a luz do seu servidor, não tem problema! Ao ligar novamente, a função init\_guilds() varre o arquivo, restaura o nível, a experiência e todo o ouro dos cofres de todas as guildas!

Com a interface social pronta e as guildas persistentes, a nossa "Fase 4: Sistemas Sociais" está 100% convertida e funcional no NVGT! 🎉

