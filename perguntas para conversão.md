# Perguntas para Conversão BGT → NVGT

## ✅ RESPONDIDAS PELOS ARQUIVOS NVGT:

### Fase 1: Configuração Base ✅
- **Extensão de arquivo**: Sim, usar `.nvgt` em vez de `.bgt` ✅
- **Constantes**: Sintaxe idêntica `const string NAME="value"` ✅

### Fase 2: Classes e Objetos ✅  
- **Declaração de classes**: Sintaxe `class player{ }` idêntica ✅
- **Arrays de objetos**: `player@[] players;` funciona igual ✅
- **Construtores**: Sintaxe idêntica ✅
- **Métodos de classe**: Declaração idêntica ✅

### Fase 3: Sistema de Áudio ✅
- **Classe Sound**: Existe `sound` nativo e `sound_pool` ✅
- **Som 3D**: Totalmente suportado via `sound_pool` ✅
- **Formatos**: Suporta .ogg e outros formatos ✅

### Fase 4: Interface e Input ✅
- **Menus**: Classe `menu` completa disponível ✅
- **Input de texto**: Sistema `input_forms` e `audio_form` ✅
- **TTS/Speech**: Sistema `speech.nvgt` com `tts_voice` ✅

### Fase 5: Strings ✅
- **String functions**: `.length()`, `.replace()`, etc. ✅
- **Compatibilidade BGT**: `string_len()` via `bgt_compat.nvgt` ✅

### Fase 6: Configurações ✅
- **Settings**: Sistema completo de configurações (ini/json/nvgt) ✅

---

## ❓ PERGUNTAS RESTANTES:

### Fase 1: Configuração Base
1. **Caminhos de arquivo**: No BGT usa `DIRECTORY_APPDATA`, qual é o equivalente em NVGT?
resposta.
Olá! Sou seu guia pessoal para a base de conhecimento do Nonvisual Gaming Toolkit (NVGT). Com base nos documentos que você me forneceu, posso ajudá-lo a entender tudo, desde a programação e referências de API até como atualizar projetos do BGT. Posso fornecer resumos, fatos específicos, ou até mesmo testar sua compreensão do material. Sinta-se à vontade para me perguntar qualquer coisa!

Aqui está a resposta para a sua pergunta:

Em BGT, `DIRECTORY_APPDATA` é uma constante usada para obter o diretório de dados de aplicativos do usuário.

Em NVGT, o equivalente é a propriedade global `DIRECTORY_APPDATA`. Esta propriedade retorna o diretório de aplicativos móveis do usuário, que é geralmente onde os dados do jogo podem ser escritos, e seu valor pode variar dependendo do sistema operacional.

Além disso, NVGT oferece uma função mais robusta e independente de plataforma chamada `get_preferences_path(string company_name, string product_name)`, que é a maneira recomendada de determinar onde seu jogo deve armazenar dados de aplicativos.


## Fase 2: Sistema de Rede (CRÍTICO)

2. **Classes de rede**: Existe `network` e `network_event` em NVGT?
Sim, as classes `network` e `network_event` existem em NVGT.

A classe `network` é usada para funcionalidades de rede, como conectar-se a um servidor, enviar e receber pacotes e gerenciar conexões de pares (peers).

A classe `network_event` representa um evento recebido através do método `network::request()`. Ela contém informações sobre o evento, como o tipo de evento (conexão, desconexão, recebimento de pacote), o ID do par, o canal e os dados do pacote (mensagem).

3. **Conexão cliente-servidor**: Como estabelecer conexão? Sintaxe similar ao BGT?
4. **Envio de dados**: Funções como `send_reliable()` existem? Qual a sintaxe?
Com certeza! Vou explicar como as classes `network` e `network_event` se conectam, usando um exemplo prático.

### Configurando uma Conexão de Rede em NVGT

Para estabelecer uma conexão, você geralmente terá um **servidor** (que aguarda conexões) e um **cliente** (que se conecta ao servidor). O processo básico é o seguinte:

1.  **Configurar o Servidor**:
    *   Crie uma instância da classe `network`.
    *   Use o método `setup_server()` para abrir uma porta e aguardar conexões de clientes. Ele precisa saber a porta, o número máximo de canais e o número máximo de pares (clientes).

2.  **Configurar o Cliente**:
    *   Crie outra instância da classe `network`.
    *   Use `setup_client()` para preparar o cliente para se conectar.
    *   Use o método `connect()` para tentar estabelecer uma conexão com o endereço IP e a porta do servidor.

3.  **Gerenciar Eventos (Servidor e Cliente)**:
    *   Ambos, cliente e servidor, precisam chamar o método `network::request()` em um loop para verificar se há novos eventos de rede (como novas conexões, dados recebidos ou desconexões).
    *   Este método retorna um objeto `network_event`. Você pode então verificar a propriedade `type` deste objeto para ver que tipo de evento ocorreu (conexão, desconexão, recebimento de pacote).
    *   Com base no tipo de evento, você pode acessar outras propriedades do `network_event`, como `peer_id` (o ID do cliente) e `message` (os dados enviados).

4.  **Enviar Dados**:
    *   Para enviar uma mensagem, use o método `network::send()`. Você precisa especificar o `peer_id` do destinatário, a mensagem, o canal e se a entrega deve ser confiável (`reliable`).

Este é um processo contínuo de verificação de eventos e envio de dados que mantém a comunicação entre o cliente e o servidor.

5. **Eventos de rede**: Como capturar eventos de rede recebidos?
6. **Peer ID**: Conceito de `peer_id` existe em NVGT?
7. **Encriptação**: NVGT tem sistema próprio de encriptação de rede?
Aqui estão as respostas para suas perguntas sobre rede em NVGT:

5.  **Eventos de rede**: Para capturar eventos de rede recebidos, você deve chamar o método `network::request()` repetidamente, geralmente dentro de um loop. Este método retorna um objeto `network_event` que contém informações sobre o evento ocorrido, como conexão, desconexão ou recebimento de um pacote.

6.  **Peer ID**: Sim, o conceito de `peer_id` existe em NVGT. É um número de 64 bits que identifica uma conexão única, seja um servidor com o qual um cliente se conectou ou um cliente específico conectado a um servidor. O `peer_id` é essencial para saber de quem você recebeu um evento e para quem enviar dados.

7.  **Encriptação**: A documentação não menciona um sistema de encriptação de rede próprio e integrado na classe `network`. No entanto, NVGT possui funções de encriptação AES que podem ser usadas para criptografar os dados antes de enviá-los. Você pode usar `string_aes_encrypt()` para criptografar sua mensagem e `string_aes_decrypt()` para descriptografá-la ao receber.

Com certeza! Aqui estão dois exemplos de código, um para o servidor e outro para o cliente, que demonstram como usar a classe `network` para capturar eventos (item 5), gerenciar `peer_id` (item 6) e criptografar mensagens (item 7).

### Exemplo de Servidor

Este código configura um servidor que aguarda uma conexão, recebe uma mensagem criptografada, a descriptografa e a exibe.

```cpp
// server.nvgt
void main() {
    network server;
    // Configura o servidor na porta 1234, permitindo 1 cliente e usando 1 canal.
    server.setup_server(1234, 1, 1);

    alert("Servidor", "Servidor iniciado e aguardando conexões...");

    // Loop principal para processar eventos de rede.
    while (true) {
        // Verifica se há novos eventos de rede.
        network_event@ event = server.request();

        // Se um evento existir (não for nulo).
        if (@event != null) {
            // Verifica o tipo de evento.
            if (event.type == event_connect) {
                // Um novo cliente se conectou. Acessamos seu ID de par.
                alert("Servidor", "Cliente conectado com o peer_id: " + event.peer_id);
            } else if (event.type == event_receive) {
                // O servidor recebeu uma mensagem.
                alert("Servidor", "Mensagem criptografada recebida do peer_id: " + event.peer_id);

                // Chave de criptografia (deve ser a mesma no cliente e no servidor).
                string encryption_key = "uma_chave_muito_segura";

                // Descriptografa a mensagem.
                string decrypted_message = string_aes_decrypt(event.message, encryption_key);

                alert("Mensagem", "Mensagem descriptografada: " + decrypted_message);
            } else if (event.type == event_disconnect) {
                // O cliente se desconectou.
                alert("Servidor", "Cliente com peer_id " + event.peer_id + " desconectou.");
                break; // Encerra o loop.
            }
        }
        wait(5); // Pausa para não sobrecarregar a CPU.
    }
}
```

### Exemplo de Cliente

Este código se conecta ao servidor, criptografa uma mensagem e a envia.

```cpp
// client.nvgt
void main() {
    network client;
    client.setup_client(1, 1); // Configura o cliente.

    // Tenta se conectar ao servidor no localhost, na porta 1234.
    uint64 server_peer_id = client.connect("localhost", 1234);

    if (server_peer_id == 0) {
        alert("Erro", "Não foi possível conectar ao servidor.");
        return;
    }

    alert("Cliente", "Conectado ao servidor com peer_id: " + server_peer_id);

    // Mensagem a ser enviada.
    string message = "Olá, servidor! Esta é uma mensagem secreta.";
    string encryption_key = "uma_chave_muito_segura";

    // Criptografa a mensagem antes de enviar.
    string encrypted_message = string_aes_encrypt(message, encryption_key);

    // Envia a mensagem criptografada para o servidor.
    // Usamos o peer_id do servidor para especificar o destinatário.
    client.send(server_peer_id, encrypted_message, 0, true);

    alert("Cliente", "Mensagem enviada. O cliente irá desconectar.");
    
    // Desconecta suavemente, permitindo que pacotes pendentes sejam enviados.
    client.disconnect_peer_softly(server_peer_id);
}
```

### Resumo dos Conceitos Usados:
1.  **Captura de Eventos**: Ambos os scripts usam `network::request()` em um loop para obter objetos `network_event`. O tipo de evento (`event.type`) é verificado para saber o que aconteceu (conexão, recebimento de dados, desconexão).
2.  **Uso de `peer_id`**: Quando um cliente se conecta, o servidor recebe um `peer_id` único para essa conexão. O cliente também recebe um `peer_id` que representa sua conexão com o servidor. Esse ID é usado para direcionar mensagens com `network::send()`.
3.  **Criptografia**: As funções `string_aes_encrypt()` e `string_aes_decrypt()` são usadas para proteger a mensagem antes de ser enviada pela rede e para lê-la após ser recebida.

## Fase 3: Input e Controles (IMPORTANTE)

8. **Detecção de teclas**: Sistema de key codes é similar? `KEY_SPACE`, etc?
9. **Wait function**: `wait()` funciona igual em NVGT?
10. **Main loop**: Como implementar loop principal (`mainloop()`)?

Com certeza! Aqui estão as respostas para suas perguntas sobre detecção de teclas, a função `wait()` e o loop principal em NVGT.

8.  **Detecção de teclas**: Sim, o sistema de códigos de tecla (key codes) é muito similar. NVGT possui uma lista completa de constantes de tecla, como `KEY_A`, `KEY_SPACE`, `KEY_RETURN`, `KEY_ESCAPE`, `KEY_UP`, entre muitas outras, que você pode usar com funções como `key_pressed()`, `key_down()`, `key_released()` e `key_up()`.

9.  **Função Wait**: Sim, a função `wait()` funciona de maneira idêntica em NVGT. Ela pausa a execução do seu script pelo número de milissegundos que você especificar e, internamente, também chama a função `refresh_window()` para manter a janela do jogo responsiva e processar eventos de entrada do usuário.

10. **Loop Principal**: Para implementar um loop principal (o equivalente ao `mainloop()` do BGT), você deve criar um loop `while(true)` dentro da sua função `void main()`. Dentro deste loop, é fortemente recomendado chamar `wait(5);` para evitar que seu jogo consuma 100% da CPU e para garantir que a janela do jogo processe eventos corretamente.

Aqui está um exemplo simples que combina os três conceitos:
```cpp
void main() {
    // Cria a janela do jogo.
    show_window("Exemplo de Loop Principal");

    // Loop principal infinito.
    while (true) {
        // Pausa por 5ms e atualiza a janela/eventos.
        wait(5);

        // 8. Verifica se a tecla ESPAÇO foi pressionada.
        if (key_pressed(KEY_SPACE)) {
            screen_reader_speak("Você pressionou espaço!", true);
        }

        // Condição de saída do loop.
        if (key_pressed(KEY_ESCAPE)) {
            exit();
        }
    }
}
```

## Fase 4: File System (IMPORTANTE)

11. **Leitura de arquivos**: Como ler arquivos de texto em NVGT?
12. **Escrita de arquivos**: Como salvar dados em arquivos?
13. **Verificação de existência**: Como verificar se arquivo existe?

Com certeza! Aqui estão as respostas para suas perguntas sobre manipulação de arquivos em NVGT:

11. **Leitura de arquivos**: A maneira mais simples de ler todo o conteúdo de um arquivo de texto é usando a função `file_get_contents(string filename)`. Se precisar de mais controle, como ler o arquivo em partes, você pode usar a classe `file`, que é um tipo de `datastream`. Você pode abri-la com `file.open("nome_do_arquivo", "r")` e depois usar métodos como `file.read()` para obter os dados.

12. **Escrita de arquivos**: Para salvar dados em um arquivo, a maneira mais fácil é com a função `file_put_contents(string filename, string content, bool append = false)`. Você pode definir o terceiro parâmetro como `true` se quiser adicionar dados ao final de um arquivo existente em vez de substituí-lo. Assim como na leitura, a classe `file` também pode ser usada para escrita, abrindo-a no modo de escrita (`"w"`) ou de acréscimo (`"a"`).

13. **Verificação de existência**: Você pode verificar se um arquivo existe usando a função `bool file_exists(const string&in file_path)`. Ela retorna `true` se o arquivo existir e `false` caso contrário.

## Fase 5: Funções Básicas (MÉDIO)

14. **String split**: Como dividir strings em NVGT?
15. **Conversões**: Como converter entre string e número?
16. **Caracteres especiais**: `ascii_to_character()` existe em NVGT?
17. **Timer class**: Existe classe `timer` em NVGT? Qual a sintaxe?
18. **Random**: Função `random()` existe? Sintaxe igual?
19. **Threading**: NVGT suporta threads? Como implementar?

Com certeza! Aqui estão as respostas para as suas perguntas, com base nos documentos fornecidos.

14. **String split**: Para dividir strings, use o método `string::split(const string&in delimiter)`. Ele divide a string em um array usando o delimitador que você especificar. Se estiver portando código do BGT, é aconselhável usar `\r\n` como delimitador para evitar quebras de linha indesejadas.

15. **Conversões**:
    *   **String para número**: Use a função `parse_float(string)` para converter uma string em um número de ponto flutuante (double).
    *   **Número para string**: A conversão de número para string geralmente acontece automaticamente (casting implícito) quando você concatena um número com uma string usando o operador `+`.

16. **Caracteres especiais**: Sim, a função `string ascii_to_character(uint8 ascii)` existe em NVGT e funciona da mesma forma, retornando o caractere correspondente a um valor ASCII.

17. **Classe `timer`**: Sim, a classe `timer` existe no núcleo do NVGT. A sintaxe é a mesma: você cria uma instância com `timer t;` e pode verificar o tempo decorrido com a propriedade `t.elapsed`.

18. **Função `random()`**: Sim, a função `int random(int min, int max)` existe e sua sintaxe é idêntica. Ela gera um número pseudoaleatório dentro do intervalo especificado. NVGT também oferece geradores de números aleatórios baseados em objetos, como `random_pcg` e `random_well`, para casos de uso mais avançados.

19. **Threading**: Sim, NVGT suporta concorrência através de três mecanismos principais:
    *   **`async`**: A forma mais fácil e recomendada. Permite chamar qualquer função em uma thread separada e obter o resultado depois.
    *   **Coroutines**: Funções que podem ser pausadas (`yield()`) e retomadas, permitindo multitarefa cooperativa.
    *   **`thread`**: O método de mais baixo nível e mais complexo, que oferece controle total, mas exige gerenciamento cuidadoso para evitar problemas como data races e deadlocks.


## Fase 6: Compilação (BAIXO)

20. **Compilação**: Como compilar arquivos .nvgt? Precisa de IDE específica? Não precisa!
21. **Includes**: Sistema de `#include` funciona igual? sim!
22. **Executável**: Como gerar .exe final? Assim que compila!
23. **Assets**: Como incluir sons e outros arquivos no build final?
Para incluir sons e outros arquivos no build final do seu jogo, o NVGT utiliza um sistema de empacotamento (bundling) que agrupa todos os seus recursos. Você pode fazer isso usando diretivas `#pragma` diretamente no seu código-fonte.

Existem duas diretivas principais para isso:

1.  **`#pragma asset`**: Use esta diretiva para incluir arquivos que seu jogo precisa para funcionar, como arquivos de som, gráficos, etc. Esses arquivos são considerados recursos internos do jogo.
    *   **Exemplo**: Para incluir um arquivo de som chamado `sons.dat`, adicione a seguinte linha ao topo de um dos seus arquivos de script `.nvgt`:
        ```cpp
        #pragma asset sons.dat
        ```
    *   Você também pode incluir um diretório inteiro recursivamente. Por exemplo, para incluir uma pasta chamada `sons`:
        ```cpp
        #pragma asset sons
        ```

2.  **`#pragma document`**: É muito similar à `#pragma asset`, mas é usada para arquivos que o usuário final deve acessar, como `leia-me.txt` ou `changelog.txt`. Em algumas plataformas, como o macOS, esses arquivos são colocados em um local mais acessível para o usuário do que os assets internos do jogo.
    *   **Exemplo**:
        ```cpp
        #pragma document leia-me.txt
        ```

Por padrão, o NVGT tentará empacotar automaticamente seu jogo, incluindo sons, bibliotecas e outros assets, em um único pacote, como um arquivo `.zip` no Windows. Se você preferir gerenciar os arquivos manualmente, pode desativar esse comportamento.

## Fase 7: Específicas do Projeto (BAIXO)

24. **Parsing de mapas**: Como processar strings de mapa com múltiplas linhas?
Para processar strings de mapa com múltiplas linhas, a abordagem recomendada é usar o método `string::split()` para dividir a string em um array de linhas individuais. Ao fazer a portabilidade de código do BGT, é aconselhável usar `\r\n` como delimitador para evitar quebras de linha indesejadas no final das strings divididas.

Depois de dividir a string principal em linhas, você pode usar um loop `for` para iterar sobre cada linha do array e processá-la individualmente.

Aqui está um exemplo de como isso pode ser feito:
```cpp
// String de mapa com múltiplas linhas
string map_data = "linha1\r\nlinha2\r\nlinha3";

// 1. Divida a string em um array de linhas
string[]@ lines = map_data.split("\r\n");

// 2. Itere sobre cada linha e processe-a
for (uint i = 0; i < lines.length(); i++) {
    string current_line = lines[i];
    // Faça algo com a linha atual, por exemplo, imprimi-la
    alert("Linha " + (i + 1), current_line);
}
```

Este método garante que cada linha do seu mapa seja tratada como um elemento separado, facilitando a análise da sua estrutura.

25. **Serialização**: Como salvar/carregar dados de jogador?
Para salvar e carregar dados do jogador (serialização), você pode usar o include `settings.nvgt` ou serializar um dicionário diretamente.

### Método 1: Usando o `settings.nvgt` (Recomendado)

O include `settings.nvgt` é uma classe de alto nível projetada para gerenciar o armazenamento de dados do usuário. Ela substitui o antigo objeto `settings` do BGT que escrevia no registro do Windows. Agora, ela salva os dados em arquivos de configuração que podem estar em vários formatos, como `.ini`, `.json` ou um dicionário serializado do NVGT (`.dat`).

Este método é ideal para dados de configuração simples, como nome do jogador, pontuação, nível, etc.

**Exemplo de como salvar e carregar dados:**

```cpp
#include "settings.nvgt"

void main() {
    settings s;
    // Configura onde os dados serão salvos.
    // Parâmetros: nome da empresa, nome do produto, salvar localmente?, formato do arquivo.
    s.setup("MinhaEmpresa", "MeuJogo", false, "ini");

    // Salva os dados do jogador
    s.write_string("player_name", "Alex");
    s.write_number("player_score", 1500);
    s.write_number("player_level", 5);

    // Carrega os dados do jogador em outra execução
    string nome = s.read_string("player_name", "Convidado");
    double pontuacao = s.read_number("player_score", 0);
    double nivel = s.read_number("player_level", 1);
    
    alert("Dados Carregados", "Nome: " + nome + ", Pontuação: " + pontuacao + ", Nível: " + nivel);

    s.close(); // Fecha e salva os dados (se instant_save estiver desativado).
}
```

### Método 2: Serialização de Dicionário

Para estruturas de dados mais complexas (como inventários, status de missões, etc.), você pode usar um objeto `dictionary` para armazenar os dados e depois serializá-lo para um arquivo. A serialização converte o dicionário em uma string que pode ser salva em um arquivo e depois desserializada de volta para um dicionário.

**Exemplo:**

```cpp
void main() {
    // 1. Criar e preencher o dicionário com os dados do jogador
    dictionary@ dados_jogador = dictionary();
    dados_jogador.set("nome", "Maria");
    dados_jogador.set("pontuacao", 5000);
    dados_jogador.set("inventario", {"espada", "escudo", "poção"});

    // 2. Serializar o dicionário para uma string
    string dados_serializados = dados_jogador.serialize();

    // 3. Salvar a string em um arquivo
    file_put_contents("savegame.dat", dados_serializados);

    // --- Para carregar ---

    // 4. Ler o arquivo
    string dados_lidos = file_get_contents("savegame.dat");

    // 5. Desserializar a string de volta para um dicionário
    dictionary@ dados_carregados = deserialize(dados_lidos);

    // 6. Acessar os dados
    string nome_carregado;
    dados_carregados.get("nome", nome_carregado);
    alert("Carregado", "Bem-vinda de volta, " + nome_carregado + "!");
}
```

26. **Criptografia**: Preciso implementar sistema próprio de encriptação?
Não, você não precisa implementar seu próprio sistema de criptografia do zero. O NVGT já oferece funções integradas para criptografia AES.

Você pode usar as seguintes funções:
*   `string_aes_encrypt(string data, string key)`: Para criptografar uma string usando uma chave.
*   `string_aes_decrypt(string data, string key)`: Para descriptografar a string usando a mesma chave.

Essas funções utilizam o algoritmo AES 256-bit CBC, que é um padrão de criptografia confiável mundialmente. Para a maioria dos casos, elas são seguras e suficientes, e você não precisa se preocupar com os detalhes técnicos, como vetores de inicialização, pois o NVGT os gerencia internamente para você.

Se você precisar de ainda mais controle sobre o processo de criptografia, o NVGT também oferece uma classe de datastream chamada `aes_encrypt`.

27. **Logging**: Sistema de logs existe em NVGT?
Sim, um sistema de logs existe em NVGT, mas não como uma classe ou função dedicada chamada `log` ou `logger` na API principal.

Em vez disso, a funcionalidade de log é mencionada em dois contextos:

1.  **Notificações do Sistema (`sqlite3_log()`)**: O motor pode gerar notificações e avisos através da função `sqlite3_log()`.
2.  **Facilidade de Logging da Biblioteca Poco**: A documentação menciona a intenção de, no futuro, envolver (wrap) a "Logging facility" da biblioteca Poco, que NVGT utiliza internamente. Isso indica que, embora a funcionalidade de log exista na base do motor, ela ainda não foi totalmente exposta aos desenvolvedores de jogos como uma API de alto nível.

Para saídas de depuração simples, você pode usar a função `println()`, que imprime em um console se um estiver disponível.

---

## Resumo das Reduções:

**De 52 perguntas → 27 perguntas** 🎉
- **Eliminadas**: 25 perguntas respondidas pelos arquivos NVGT existentes
- **Restantes**: 27 perguntas organizadas por prioridade

## ✅ TODAS AS 27 PERGUNTAS FORAM RESPONDIDAS!

**🔴 CRÍTICO (1-7)**: ✅ Configuração base + Sistema de rede  
**🟡 IMPORTANTE (8-13)**: ✅ Input/controles + File system
**🟢 MÉDIO (14-19)**: ✅ Funções básicas + threading
**🔵 BAIXO (20-27)**: ✅ Compilação + específicas do projeto

## 🎉 STATUS: PRONTO PARA INICIAR A CONVERSÃO!

Com todas as perguntas respondidas, podemos agora iniciar a conversão do projeto BGT → NVGT seguindo o plano de ação estabelecido.