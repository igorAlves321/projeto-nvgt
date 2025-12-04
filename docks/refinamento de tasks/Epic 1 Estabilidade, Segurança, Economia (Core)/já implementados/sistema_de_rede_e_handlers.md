\# Task 3 — Sistema de Rede e Handlers (NVGT / ENet)

\*\*Epic:\*\* 1 — Estabilidade, Segurança, Economia (Core)  

\*\*Arquivo:\*\* `/epic1/tasks/sistema\_de\_rede\_e\_handlers.md`  

\*\*Status:\*\* A fazer  

\*\*Dependências:\*\*  

\- Task 1 — Inicialização do Servidor  

\- Task 2 — Carregamento do Jogador  

\- NVGT: `network`, `network\_event`, `send\_reliable`, `send\_unreliable`, `request()`



---



\# 🎯 Objetivo

Implementar do zero o subsistema de rede do servidor usando a API \*\*real\*\* do NVGT, baseada diretamente em \*\*ENet\*\*.



Diferente do BGT, o NVGT \*\*não\*\* possui:

\- `register\_handler()`

\- roteamento automático de pacotes

\- objetos cliente-servidor de alto nível



Assim, \*\*TODO o sistema de protocolo, parsing e distribuição de mensagens deve ser implementado manualmente\*\*.



---



\# 📌 Descrição Técnica



\## ✔ 1. Criar módulo `network\_server.nvgt`

Responsável por:

\- configurar servidor ENet via `network.setup\_server()`

\- realizar polling de eventos através de `network.request(timeout)`

\- detectar eventos:

&nbsp; - `event\_connect`

&nbsp; - `event\_disconnect`

&nbsp; - `event\_receive`

\- enviar pacotes usando:

&nbsp; - `send\_reliable(peer\_id, message, channel)`

&nbsp; - `send\_unreliable(peer\_id, message, channel)`

\- rotear mensagens recebidas para o dispatcher manual



---



\## ✔ 2. Definir seu próprio protocolo (obrigatório)

O NVGT só entrega uma \*\*string\*\* na propriedade `event.message`.  



Assim, você deve definir um protocolo simples, exemplo:



CHAT:mensagem...

CMD:/attack goblin

MOVE:X=40;Y=12



Ou JSON, se quiser:

{"type":"move","x":40,"y":12}



\## ✔ 3. Criar dispatcher manual (roteador)

Exemplo:

if message.starts\_with("CHAT:"):

&nbsp;  handle\_chat(...)

elif message.starts\_with("CMD:"):

&nbsp;  handle\_command(...)

else:

&nbsp;  handle\_unknown(...)

vamos expandir para

combate

• 

inventário

• 

mapa

• 

habilidades

• 

social

• 

admin

4\. Criar loop principal de rede

O loop deve:

1\. 

Chamar server.request(10) constantemente

2\. 

Verificar o tipo de evento

3\. 

Chamar os handlers apropriados

4\. 

Processar lógica do servidor entre um tick e outro

&nbsp;exemplo:

// Inclui o sistema de rede e funções de UI

\#include "networking.nvgt"

\#include "ui.nvgt"



// Tipos de evento (NVGT / ENet)

const int EVENT\_NONE = 0;

const int EVENT\_CONNECT = 1;

const int EVENT\_DISCONNECT = 2;

const int EVENT\_RECEIVE = 3;



// Protocolo simples baseado em prefixos

const string MSG\_CHAT = "CHAT:";

const string MSG\_CMD = "CMD:";



// Camada de roteamento manual

void handle\_received\_message(network\_event@ event, network@ server) {

&nbsp;   uint peer\_id = event.peer\_id;

&nbsp;   string message = event.message;



&nbsp;   if (message.starts\_with(MSG\_CHAT)) {

&nbsp;       string chat\_content = message.substr(MSG\_CHAT.length());

&nbsp;       alert("CHAT RECEBIDO", "Peer " + peer\_id + ": " + chat\_content);



&nbsp;       server.send\_reliable(peer\_id, "Servidor: Sua mensagem foi recebida.", event.channel);



&nbsp;   } else if (message.starts\_with(MSG\_CMD)) {

&nbsp;       string command = message.substr(MSG\_CMD.length());

&nbsp;       alert("COMANDO RECEBIDO", "Peer " + peer\_id + " executou: " + command);



&nbsp;       server.send\_unreliable(peer\_id, "Servidor: Comando processado rapidamente.", event.channel);



&nbsp;   } else {

&nbsp;       alert("DESCONHECIDO", "Pacote não identificado de Peer " + peer\_id);

&nbsp;   }

}



// Loop principal de rede

void server\_loop() {

&nbsp;   network server;

&nbsp;   uint port = 1234;

&nbsp;   uint max\_channels = 1;

&nbsp;   uint max\_peers = 32;



&nbsp;   if (!server.setup\_server(port, max\_channels, max\_peers)) {

&nbsp;       alert("ERRO", "Falha ao iniciar o servidor. Verifique a porta.");

&nbsp;       return;

&nbsp;   }



&nbsp;   show\_window("Servidor NVGT Ativo");

&nbsp;   alert("INFO", "Servidor iniciado na porta " + port);



&nbsp;   while (true) {

&nbsp;       network\_event@ event = server.request(10);

&nbsp;       

&nbsp;       if (@event == null)

&nbsp;           continue;



&nbsp;       if (event.type == EVENT\_CONNECT) {

&nbsp;           alert("CONEXÃO", "Peer conectado: " + event.peer\_id);

&nbsp;           server.send\_reliable(event.peer\_id, "Bem-vindo ao Servidor NVGT!", 0);



&nbsp;       } else if (event.type == EVENT\_DISCONNECT) {

&nbsp;           alert("DESCONEXÃO", "Peer desconectado: " + event.peer\_id);



&nbsp;       } else if (event.type == EVENT\_RECEIVE) {

&nbsp;           handle\_received\_message(event, server);

&nbsp;       }

&nbsp;   }

}



void main() {

&nbsp;   server\_loop();

}



