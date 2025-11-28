\# 🔧 Task 3.3: Finalizar Outras Funções e Comandos Faltantes (QoL Final)



\*\*EPIC:\*\* Fechamento de Gaps de Polimento (Epic 3)

\*\*DOMÍNIO:\*\* Servidor / Cliente / QoL

\*\*PRIORIDADE:\*\* MÉDIA-BAIXA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO-ALTO (Devido à Tradução)

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Finalizar as funcionalidades de Qualidade de Vida (QoL), com \*\*ênfase na integração do Sistema de Tradução Automática\*\* usando a infraestrutura \*\*assíncrona\*\* do NVGT (classes `async` e `http`) para dar suporte à comunidade internacional.



\## 📝 Contexto e Solução NVGT



\* \[cite\_start]\*\*Tradução:\*\* O Servidor age como intermediário, usando `async` e `http` para chamar APIs externas (Ex: Google/DeepL) sem bloquear o \*game loop\*\[cite: 3, 4].

\* \*\*Vocalização:\*\* O Cliente utiliza a função global \*\*`speak(text, interrupt)`\*\* para garantir que a tradução seja vocalizada imediatamente e que qualquer fala anterior seja interrompida.

\* \*\*Frases Rápidas:\*\* As frases são pré-configuradas no Servidor para evitar \*spoofing\*.



---



\## 💻 Descrição Detalhada da Implementação (Modelo NVGT Completo)



O desenvolvedor deve implementar a lógica em três rotinas: Frases Rápidas, Iniciação da Tradução e Coleta do Resultado (no \*main loop\* do Servidor).



\### Módulo 1: Handler de Frases Rápidas (`req\_send\_quick\_phrase`)



Esta função recebe um índice e transmite a frase correspondente para todos no mesmo mapa, usando o canal de chat.



```nvgt

// Lista de Frases Rápidas (pré-configuradas no servidor)

string\[] QUICK\_PHRASES = { "Vou recuar.", "Preciso de ajuda.", ... };



void req\_send\_quick\_phrase(network\_event@ event) {

    // 1. Receber e validar o índice...

    uint index = parse\_uint(event.message); 

    if (index >= QUICK\_PHRASES.length()) return;



    string phrase = QUICK\_PHRASES\[index];

    string sender\_map = get\_player\_map(event.peer\_id); // Obter o mapa do remetente



    // Formato de transmissão: "QUICK|SENDER\_ID|FRASE"

    string broadcast\_msg = "QUICK|" + string(event.peer\_id) + "|" + phrase;



    // 2. Transmissão para o Mapa (Roteamento)

    // Roteia apenas para quem está no mesmo mapa (filtragem)

    // net.send(receiver\_id, broadcast\_msg, CHAT\_CHANNEL, false); // Não confiável (false) para chat \[2]

}

Módulo 2: Estrutura de Tradução (Servidor Assíncrono)

A tradução é executada em uma thread separada (usando async) para evitar o bloqueio do Servidor.

1\. 

Handler de Iniciação (req\_translate\_message): Inicia a tarefa assíncrona.

void req\_translate\_message(network\_event@ event) {

&nbsp;   // ... (Parsing para obter message\_id, text\_to\_translate, target\_lang)



&nbsp;   // 1. Criar a Tarefa Assíncrona para a tradução de alto esforço

&nbsp;   // A função call\_translation\_api é executada em uma thread do engine \[3, 5].

&nbsp;   async<string>@ translation\_task = async(

&nbsp;       call\_translation\_api, 

&nbsp;       text\_to\_translate, 

&nbsp;       target\_lang

&nbsp;   );



&nbsp;   // 2. Armazenar o contexto para posterior verificação no main loop

&nbsp;   // active\_translation\_tasks.set(message\_id, @ctx);

&nbsp;   // alert("Servidor", "Iniciada tradução assíncrona para ID: " + message\_id);

}



// Função Auxiliar (Executada na Thread Separada): Simula a chamada HTTP BLOCANTE

string call\_translation\_api(const string\& in text, const string\& in target\_lang) {

&nbsp;   http h; // Facilitador de requisições HTTP assíncronas \[4]

&nbsp;   // ... (Lógica de construção da URL e h.get(api\_url) )

&nbsp;   h.wait(); // Espera pela conclusão da requisição HTTP \[6]

&nbsp;   // ... (Retorna o resultado traduzido ou erro)

}

2\. 

Rotina de Checagem (Servidor Main Loop): Verifica periodicamente o resultado.

void check\_translation\_results() {

&nbsp;   // Itera sobre o 'dictionary' active\_translation\_tasks

&nbsp;   // Se ctx.task.is\_ready, obtém o resultado:

&nbsp;   // string translated\_text = ctx.task.get\_result(); \[5]



&nbsp;   // Envia o resultado de volta ao Cliente solicitante

&nbsp;   // net.send(ctx.client\_peer\_id, response\_packet, TRANSLATION\_CHANNEL, true); // reliable=true \[2, 9]



&nbsp;   // Limpa a tarefa concluída.

}

Módulo 3: Cliente - Vocalização da Tradução (TTS)

A vocalização deve ser imediata e interromper qualquer fala anterior.

\#include "speech.nvgt" // Inclui tts\_voice e a função global speak()



void handle\_translated\_message(network\_event@ event) {

    // O pacote esperado do Servidor é: "TRANSLATED|MESSAGE\_ID|TEXTO\_TRADUZIDO"

    // ... (Parsing para obter o texto traduzido)



    string translated\_text = parts\[5];

    

    if (!translated\_text.empty()) {

        // A função speak() é recomendada. O 'true' interrompe a fala atual \[6-8].

        speak("Tradução: " + translated\_text, INTERRUPT\_PREVIOUS\_SPEECH);

    }

}

Use o código principalmente de tradução do bgt de base, e faça essa task, usando os exemplos ta certo?

