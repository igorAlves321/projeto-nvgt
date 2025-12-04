\# Task 4 — Sistema de Movimento do Jogador (Servidor + Rede + Sincronização)

\*\*Epic:\*\* 2 — Sistemas Core Faltantes (Movimento, NPC, Social)  

\*\*Arquivo:\*\* `/epic2/tasks/movimento\_jogador.md`  

\*\*Status:\*\* A fazer  

\*\*Dependências:\*\*  

\- Task 2 — Carregamento do Jogador  

\- Task 3 — Sistema de Rede e Handlers  

\- Estrutura de mapas (mínimo: grid navegável com colisão)  



---



\# 🎯 Objetivo

Implementar o sistema completo de movimentação do jogador, incluindo:



\- Recebimento de comandos de movimento via rede (`event\_receive`)

\- Parsing e roteamento desses comandos

\- Atualização segura da posição do jogador no servidor

\- Validação de colisão, bordas e áreas inválidas

\- Notificação aos outros jogadores no mesmo mapa

\- Sincronização constante (via `send\_unreliable()`)

\- Tick-rate configurável para movimento suave



Este sistema desbloqueia todos os outros sistemas core: combate, NPCs, coleta, triggers, mapa e interação.



---



\# 📌 Descrição Técnica



\## ✔ 1. Protocolo de Movimento (Cliente → Servidor)

O cliente envia:

MOVE:X=12;Y=8



Ou em JSON (se preferir):

{"type":"move","x":12,"y":8}



A task assume o padrão prefixado do exemplo oficial:



MOVE:X=<value>;Y=<value>



---



\## ✔ 2. Dispatcher (Task 3) deve encaminhar comandos MOVE

Exemplo:



```cpp

if (message.starts\_with("MOVE:")) {

&nbsp;   handle\_move(event, server);

}

Exemplo:

if (message.starts\_with("MOVE:")) {

&nbsp;   handle\_move(event, server);

}

&nbsp;

✔ 3. Lógica do Handler handle\_move

Funções esperadas:

1\. Parse do comando

Separar:

• 

X

• 

Y

• 

(opcional) velocidade

• 

(opcional) direção

2\. Validar posição

Checklist:

• 

jogador está carregado?

• 

mapa existe?

• 

célula é navegável?

• 

não é parede?

• 

não é zona proibida?

• 

não está fora dos limites?

3\. Aplicar movimento

Atualizar na estrutura global:

• 

globals.players\[peer\_id].x

• 

globals.players\[peer\_id].y

• 

globals.players\[peer\_id].direction

4\. Sincronizar com outros jogadores

Enviar a todos no mesmo mapa (menos o próprio):

server.send\_unreliable(peer\_id\_destino, "MOVE\_SYNC:peer=" + id + ";x=..;y=..", 0);

Código de Exemplo 

void handle\_move(network\_event@ event, network@ server) {

&nbsp;   uint peer = event.peer\_id;

&nbsp;   string msg = event.message; // Ex: "MOVE:X=12;Y=8"



&nbsp;   // Extrair X e Y

&nbsp;   int x = parseInt(msg.substr(msg.find("X=") + 2, msg.find(";") - (msg.find("X=") + 2)));

&nbsp;   int y = parseInt(msg.substr(msg.find("Y=") + 2));



&nbsp;   // Validar jogador carregado

&nbsp;   if (!player\_exists(peer)) {

&nbsp;       server.send\_reliable(peer, "ERR:PlayerNotLoaded", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Validar mapa e colisão

&nbsp;   if (!is\_walkable(globals.players\[peer].map, x, y)) {

&nbsp;       server.send\_reliable(peer, "ERR:BlockedCell", 0);

&nbsp;       return;

&nbsp;   }



&nbsp;   // Aplicar movimento

&nbsp;   globals.players\[peer].x = x;

&nbsp;   globals.players\[peer].y = y;



&nbsp;   // Sincronizar para outros jogadores

&nbsp;   broadcast\_unreliable(peer,

&nbsp;       "MOVE\_SYNC:peer=" + peer + ";X=" + x + ";Y=" + y,

&nbsp;       server);

}

Exemplo de broadcast\_unreliable

void broadcast\_unreliable(uint origin\_peer, string msg, network@ server) {

&nbsp;   for (uint i = 0; i < globals.player\_count; i++) {

&nbsp;       uint target = globals.players\_online\[i];

&nbsp;       if (target != origin\_peer) {

&nbsp;           server.send\_unreliable(target, msg, 0);

&nbsp;       }

&nbsp;   }

}

✔ 4. Estruturas de Mapa Necessárias que devem existir.

is\_walkable(map\_id, x, y)

• 

get\_map\_bounds(map\_id)

• 

globals.players\[peer].map

&nbsp;

✔ 5. Tick-rate de Movimento

// 60 ticks por segundo

const int TICK = 16; // ms



void movement\_tick() {

&nbsp;   // NPCs, gravidade, status, empurrões etc.

}

E dentro do loop principal:

last\_tick += delta;

if (last\_tick >= TICK) {

&nbsp;   movement\_tick();

&nbsp;   last\_tick = 0;

}

6\. Critérios de Aceitação

O servidor deve:

• 

Processar comandos MOVE sem travar

• 

Rejeitar movimentos inválidos

• 

Impedir colisão corretamente

• 

Atualizar posições no servidor

• 

Sincronizar com jogadores próximos via send\_unreliable

O cliente deve:

• 

Conseguir mover o personagem

• 

Receber atualizações de players próximos

• 

Não sofrer rollback incoerente

• 

Não atravessar paredes ou limites

&nbsp;

🔧 Subtasks

1\. Criar handle\_move()

parse do comando

• 

validação de célula

• 

atualização de posição

• 

sincronização

2\. Criar função utilitária broadcast\_unreliable()

3\. Criar/Adaptar mapa

• 

função is\_walkable()

• 

limites

4\. Integrar ao dispatcher

Adicionar ao roteamento da Task 3:

if (msg.starts\_with("MOVE:")) handle\_move(event, server);



5\. Adicionar tick loop

Para manter fluidez e permitir expansão futura (NPCs, gravidade etc.)

&nbsp;

📦 Resultado Esperado

Ao final da task, o jogo terá:

• 

Movimento funcional

• 

Sincronização entre múltiplos jogadores

• 

Validação de colisão

• 

Estrutura base para:

• 

combate

• 

AI de NPCs

• 

triggers do mapa

• 

habilidades

• 

pathfinding

provável que muita coisa já esteja pronta e você precise só revizar, talvez alterar, mas, vai que vai

