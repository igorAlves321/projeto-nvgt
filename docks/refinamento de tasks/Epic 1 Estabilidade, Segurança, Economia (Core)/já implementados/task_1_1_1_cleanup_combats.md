\# 🛠️ Task 1.1.1: Implementar cleanup\_expired\_combats()



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Servidor / Performance

\*\*PRIORIDADE:\*\* CRÍTICA (Nível 1)

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar a função de limpeza de combates expirados no lado do servidor para \*\*remover e desalocar\*\* as instâncias de combate que não estão mais ativas ou que expiraram o tempo limite. Esta função é \*\*CRÍTICA\*\* para a \*\*estabilidade e performance\*\* do servidor, pois sua ausência pode levar a \*\*memory leaks\*\* (vazamento de memória) e degradação de desempenho em longas sessões.



\## 📝 Referências e Contexto



\* \*\*Necessidade:\*\* A função `cleanup\_expired\_combats()` é atualmente chamada, mas não está definida no código.

\* \*\*Arquivos Relevantes:\*\*

&nbsp;   \* `server/server.nvgt` (Onde a função é chamada no \*main loop\* do servidor).

&nbsp;   \* `server/includes/combat.nvgt` (Local provável para a implementação da lógica).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvedor deverá criar a lógica de limpeza utilizando os recursos de multithreading e gerenciamento de memória do NVGT para garantir que o \*game loop\* principal não seja afetado.



\### Passo 1: Configurar Estruturas de Dados Compartilhadas



1\.  \*\*Definir Mutex:\*\* Declarar um \*\*`mutex`\*\* global (ex: `combat\_mutex`) para proteger a \*array\* de combates ativos, que é um dado compartilhado acessado pela \*thread\* principal e pela \*thread\* de limpeza.



&nbsp;   ```nvgt

&nbsp;   mutex combat\_mutex;

&nbsp;   CombatInstance@\[] active\_combats; // Array de handles para os objetos

&nbsp;   ```



2\.  \*\*Definir Classe de Combate (Exemplo):\*\* Certificar-se de que a classe `CombatInstance` possui um meio de rastrear sua expiração, como um `timestamp` e um método de verificação.



&nbsp;   ```nvgt

&nbsp;   class CombatInstance {

&nbsp;       int64 expiration\_time;

&nbsp;       // ... outros atributos

&nbsp;       

&nbsp;       bool is\_expired(int64 current\_time) {

&nbsp;           // A lógica correta é: retorna true se o tempo atual > tempo de expiração

&nbsp;           return current\_time >= expiration\_time; 

&nbsp;       }

&nbsp;   }

&nbsp;   ```



\### Passo 2: Criar a Função de Limpeza Assíncrona



Crie uma função independente (ex: `cleanup\_expired\_combats\_task`) que será executada em uma \*thread\* separada usando `async`.



1\.  \*\*Travar o Mutex:\*\* Iniciar a função com \*\*`combat\_mutex.lock()`\*\* para garantir acesso exclusivo ao \*array\* `active\_combats`.

2\.  \*\*Iteração Segura:\*\* Usar o \*\*loop `for` no estilo C, iterando de trás para frente\*\* (do último ao primeiro índice). Isso é crucial para remover elementos de um \*array\* dinâmico sem pular itens ou causar erros de índice.



&nbsp;   ```nvgt

&nbsp;   void cleanup\_expired\_combats\_task() {

&nbsp;       combat\_mutex.lock(); 

&nbsp;       int64 current\_time = ticks(); // Captura o tempo atual usando a função 'ticks()' do NVGT

&nbsp;       

&nbsp;       // Iteração reversa (necessária para remover elementos de arrays NVGT sem erro)

&nbsp;       for(int i = active\_combats.length() - 1; i >= 0; i--) {

&nbsp;           CombatInstance@ combat = active\_combats\[i];

&nbsp;           

&nbsp;           // 3. Verificação: Se o combate expirou ou foi encerrado

&nbsp;           if (combat.is\_expired(current\_time) || combat.is\_finished) {

&nbsp;               // 4. Remoção: Usa o método de remoção do array.

&nbsp;               active\_combats.remove\_at(i);

&nbsp;               // NOTA: A desalocação da memória é automática pelo NVGT (contagem de referências)

&nbsp;           }

&nbsp;       }

&nbsp;       

&nbsp;       combat\_mutex.unlock(); // Libera o Mutex

&nbsp;   }

&nbsp;   ```



\### Passo 3: Agendar a Execução no Loop Principal



No `server.nvgt` (ou no \*main loop\* do servidor):



1\.  \*\*Definir Rastreamento:\*\* Criar uma variável para rastrear a tarefa assíncrona.

&nbsp;   ```nvgt

&nbsp;   async@ cleanup\_task; 

&nbsp;   ```

2\.  \*\*Agendar Periodicidade:\*\* Dentro do \*main loop\* (ou em um \*timer\*), agendar a tarefa, verificando se a anterior já terminou para evitar sobrecarga de \*threads\*.



&nbsp;   ```nvgt

&nbsp;   // Verifica se a tarefa de limpeza terminou (se cleanup\_task.is\_ready)

&nbsp;   if (@cleanup\_task == null || cleanup\_task.is\_ready) {

&nbsp;       // Agenda a execução da função em uma nova thread

&nbsp;       @cleanup\_task = async(cleanup\_expired\_combats\_task);

&nbsp;   }

&nbsp;   // ... O loop principal continua a processar o jogo ...

&nbsp;   ```



---



\## ✅ Critérios de Aceitação



\* A função de limpeza existe e está definida, encapsulada para execução assíncrona.

\* A `array` de instâncias de combate (`active\_combats`) é protegida por um \*\*`mutex`\*\* durante a limpeza.

\* A função utiliza o laço \*\*`for` de iteração reversa\*\* (`i = length() - 1; i >= 0; i--`) para garantir a remoção segura dos elementos com `array.remove\_at(i)`.

\* A lógica está agendada para rodar periodicamente usando a classe \*\*`async`\*\*.

\* Testes confirmam que \*\*não há aumento de memória\*\* após iniciar e abandonar longos combates, e que os combates expirados são removidos com sucesso da lista ativa.

