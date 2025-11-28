\# 🛒 Task 1.4.1: Implementar Handlers e Lógica de Lojas NPC



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Rede / Economia / Comandos

\*\*PRIORIDADE:\*\* CRÍTICA (Nível 1)

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO-ALTO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar o \*\*handler de rede `req\_buy\_item`\*\* no lado do Servidor. O foco é na \*\*Validação Encadeada\*\* das transações de compra (Ouro → Inventário) para garantir a segurança econômica e a integridade de dados, fechando um dos \*\*4 Gaps Críticos\*\* identificados na migração.



\## 📝 Contexto e Notas



\* \*\*Moeda do Jogo:\*\* A propriedade `p.gold` nos exemplos refere-se à moeda primária do jogo (que pode ser \*\*Stryx, Créditos\*\* ou outra, conforme `player.nvgt`). O desenvolvedor deve usar a variável de moeda real do jogador.

\* \*\*Segurança:\*\* A implementação utiliza a estrutura `if/return` para garantir que a execução da transação só ocorra após todas as validações passarem.

\* \*\*Arquivos:\*\* `server/includes/network.nvgt` (para o Handler) e `server/includes/player.nvgt` (para as classes Player/Inventory).



---



\## 💻 Descrição Detalhada da Implementação (Modelo NVGT)



O desenvolvedor deve integrar a função `req\_buy\_item` no módulo de \*handlers\* de rede do servidor.



\### Passo 1: Definição de Classes



Garantir que as classes de suporte (`Item`, `Inventory`, `Player`) existam com as propriedades de controle relevantes (`gold`, `current\_space`, `max\_space`, etc.).



\### Passo 2: Implementar Handler `req\_buy\_item` (Validação Encadeada)



A lógica do \*handler\* é a parte crítica da segurança. Se qualquer `if` for verdadeiro (falha na validação), a função deve ser interrompida imediatamente com `return`.



```nvgt

// =========================================================

// HANDLER DE REDE CRÍTICO: req\_buy\_item

// (Implementado no módulo de rede do servidor)

// =========================================================



void req\_buy\_item(Player@ p, int item\_id, int quantity) {

&nbsp;   // Simulação: Recuperação dos dados do item da Loja NPC

&nbsp;   Item@ item\_to\_buy = get\_item\_details\_from\_id(item\_id);

&nbsp;   

&nbsp;   if (@item\_to\_buy == null || quantity <= 0) {

&nbsp;       send\_msg\_fail(p, "Detalhes da compra inválidos.");

&nbsp;       return; // Interrupção: Dados de entrada inválidos

&nbsp;   }



&nbsp;   int total\_cost = item\_to\_buy.cost \* quantity;

&nbsp;   // O desenvolvedor deve usar a variável de moeda correta (ex: p.stryx, p.creditos)

&nbsp;   

&nbsp;   // --- 1. Verificação de Ouro (Primeira Camada) ---

&nbsp;   if (p.gold < total\_cost) { 

&nbsp;       string message = "Ouro insuficiente. Requer: " + total\_cost;

&nbsp;       send\_msg\_fail(p, message);

&nbsp;       return; // Interrupção: Falha na Economia

&nbsp;   }



&nbsp;   // --- 2. Verificação de Inventário (Segunda Camada) ---

&nbsp;   if (!p.inv.check\_space(item\_to\_buy, quantity)) {

&nbsp;       string message = "Inventário cheio ou item muito pesado.";

&nbsp;       send\_msg\_fail(p, message);

&nbsp;       return; // Interrupção: Falha no Inventário

&nbsp;   }



&nbsp;   // --- 3. Execução da Transação (Sucesso) ---

&nbsp;   // A transação só é alcançada se ambas as validações passarem.

&nbsp;   

&nbsp;   // Ação: Subtrair a moeda correta do jogo (Ex: p.gold -= total\_cost;)

&nbsp;   p.gold -= total\_cost;

&nbsp;   

&nbsp;   // Ação: Adicionar o item ao inventário

&nbsp;   p.inv.add\_item(item\_to\_buy, quantity);



&nbsp;   // Feedback

&nbsp;   send\_msg\_success(p, "Compra realizada com sucesso.");

}

Passo 3: Implementar Handlers de Suporte

O desenvolvedor também deve implementar os handlers no Cliente para exibir o menu da loja e tratar as mensagens de sucesso/falha enviadas pelo servidor (send\_msg\_fail, send\_msg\_success).

&nbsp;

✅ Critérios de Aceitação

• 

Validação Encadeada: O código do handler utiliza dois blocos if separados (Ouro e Inventário) para validar a transação.

• 

Interrupção Forçada: Qualquer falha na validação resulta em uma mensagem de erro e uma interrupção imediata da função (return).

• 

Integridade Econômica: A subtração de moeda e a adição do item (p.gold -= cost e p.inv.add\_item) só ocorrem se ambas as checagens passarem.

• 

Comunicação: Os handlers de rede de sucesso e falha estão configurados para enviar feedback ao cliente.

OBS saiba que todos os cógiso implementados, são exemploq eue colocamos nas tasks pra vocês terem referencia ok, mas, o projeto tem seu contexto e tem que se levar em consideração, tipo o ouro, ele é substituído pelas moedas do jogo.

