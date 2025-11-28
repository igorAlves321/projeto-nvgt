\# 💰 Task 2.7: Implementar Lógica de Venda e Outras Moedas (Economia Secundária)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Servidor / Economia / Persistência

\*\*PRIORIDADE:\*\* MÉDIA



\## 🎯 Objetivo



Finalizar o fluxo econômico implementando a \*\*Lógica de Venda de Itens para NPCs\*\* e garantindo que o servidor suporte a \*\*Multi-Moeda\*\* que existia no BGT. O fluxo de Compra já foi estabelecido (Task 1.4.1), e esta \*task\* fecha o ciclo de Venda.



\## 📝 Referências e Contexto



\* \*\*Gap Faltante:\*\* Sistema de Venda de Itens para NPCs e suporte a múltiplas moedas (Ex: `Reais` + `Euros` no BGT, agora traduzido para `Gold`, `Stryx`, `Créditos`).

\* \*\*Integridade:\*\* A lógica deve ser threadsafe e validar o inventário do jogador antes de transferir a moeda (similar à Task 1.4.1).

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Servidor:\*\* `server/includes/network.nvgt` (para Handler de Venda), `server/includes/player.nvgt` (para manipulação de moedas e inventário), `server/includes/item.nvgt` (para obter o preço de venda).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve focar em modificar a estrutura de `Player` para suportar as moedas secundárias e implementar a transação segura de Venda.



\### Passo 1: Modificar Estrutura de Moedas do Jogador



1\.  \*\*Atualizar `Player`:\*\* Verificar se a classe `Player` no Servidor (`player.nvgt`) armazena corretamente as moedas secundárias (Ex: `stryx`, `creditos`, `gcoins`, etc.). Caso contrário, garantir que os campos sejam \*\*`atomic\_int`\*\* (Task 1.4.2) para segurança.



\### Passo 2: Lógica de Venda de Itens (`req\_sell\_item`)



Esta rotina inverte a lógica de `req\_buy\_item`.



1\.  \*\*Handler de Venda (Cliente → Servidor):\*\*

&nbsp;   \* \*\*Novo Handler:\*\* `req\_sell\_item \[npc\_id] \[item\_id] \[quantidade]`.

2\.  \*\*Processamento do Servidor (CRÍTICO):\*\*

&nbsp;   \* \*\*Validação 1 (Posse):\*\* Verificar se o jogador realmente \*\*possui\*\* o `item\_id` na `quantidade` especificada (`inv.item\_exists`) e se o NPC compra este item.

&nbsp;   \* \*\*Execução (Transação Segura):\*\*

&nbsp;       \* \*\*Remover o Item:\*\* Deletar o item do inventário do jogador (`inv.delete\_item`).

&nbsp;       \* \*\*Adicionar Moeda:\*\* Adicionar o `valor\_venda` (obtido de `item.nvgt`) à moeda correta do jogador (`p.gold += valor\_venda` ou `p.stryx += valor\_venda`).

&nbsp;   \* \*\*Transferência Atômica:\*\* Garantir que a adição da moeda utilize a operação segura do \*\*`atomic\_int`\*\*.

3\.  \*\*Feedback:\*\* Enviar uma mensagem de sucesso ou falha ao cliente.



\### Passo 3: Implementação da Venda com Multi-Moeda



1\.  \*\*Definir Moeda de Venda:\*\* Modificar a estrutura de itens (`item.nvgt`) para incluir qual \*\*tipo de moeda\*\* o item concede na venda (Ex: `sell\_currency\_type: STRYX`, `sell\_value: 50`).

2\.  \*\*Roteamento:\*\* O \*handler\* de venda deve rotear o valor de venda para o campo `p.stryx` ou `p.creditos` correspondente, em vez de assumir apenas `p.gold`.



---



\## ✅ Critérios de Aceitação



\* \*\*Venda Funcional:\*\* O \*handler\* de rede `req\_sell\_item` e sua lógica de validação estão implementados.

\* \*\*Integridade Atômica:\*\* A adição da moeda ao saldo do jogador na venda utiliza o tipo \*\*`atomic\_int`\*\* (Task 1.4.2).

\* \*\*Multi-Moeda:\*\* O sistema de Venda é capaz de recompensar o jogador com a \*\*moeda correta\*\* (Ex: Stryx ou Créditos) com base nas propriedades do item vendido.

\* \*\*Ciclo Econômico:\*\* O ciclo de Compra e Venda (Tasks 1.4.1 e 2.7) é fechado e seguro.

