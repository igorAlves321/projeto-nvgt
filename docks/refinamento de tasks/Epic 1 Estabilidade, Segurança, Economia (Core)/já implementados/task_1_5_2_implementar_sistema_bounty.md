\# 💰 Task 1.5.2: Implementar Handlers e Lógica do Sistema de Recompensas (Bounty)



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Rede / Recompensas / Combate

\*\*PRIORIDADE:\*\* ALTA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO



\## 🎯 Objetivo



Implementar o \*\*Sistema de Recompensas (Bounty)\*\* no lado do Servidor. Este sistema permite que jogadores coloquem um valor em ouro/moeda na cabeça de outro jogador, incentivando o combate PvP e a justiça (\*player-driven justice\*). A implementação deve cobrir a \*\*Criação da Recompensa\*\* e o \*\*Recebimento da Recompensa\*\* após a morte.



\## 📝 Referências e Contexto



\* \*\*Estrutura Existente:\*\* O Relatório de Análise indica que a estrutura de `bounty` já existe na classe `Player` (ex: `bounty\_on\_head`, `bounty\_value`, `bounty\_owner`). A tarefa é implementar a lógica de rede e os cálculos.

\* \*\*Handlers Estimados:\*\* Cerca de 3+ \*handlers\* de rede são necessários para gerenciar a criação e a notificação de status.

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Servidor:\*\* `server/includes/network.nvgt` (para handlers), `server/includes/player.nvgt` (para manipulação de \*bounty\* e ouro), módulo de Combate (para detecção de morte).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve focar na \*\*segurança da transação\*\* ao colocar a recompensa e na lógica de \*\*transferência de moeda\*\* ao receber a recompensa.



\### Passo 1: Criação da Recompensa (Cliente → Servidor)



1\.  \*\*Ação do Cliente:\*\* O jogador usa um comando (ex: `/bounty \[alvo] \[valor]`).

&nbsp;   \* \*\*Novo Handler (Saída do Cliente):\*\* Ex: `req\_place\_bounty \[target\_id] \[amount]`.

2\.  \*\*Processamento do Servidor (CRÍTICO):\*\*

&nbsp;   \* \*\*Validação:\*\*

&nbsp;       \* O `amount` é positivo e atende ao mínimo exigido?

&nbsp;       \* O jogador tem ouro suficiente (`player.gold >= amount`)?

&nbsp;   \* \*\*Execução (Transação Segura):\*\*

&nbsp;       \* Subtrair o ouro do jogador que coloca a recompensa (`p.gold -= amount`).

&nbsp;       \* \*\*Bloquear\*\* o \*bounty\* no objeto `Player` alvo (Ex: `target.bounty\_value += amount`, `target.bounty\_owner = p.id`).

&nbsp;   \* \*\*Feedback:\*\* Notificar o alvo (se online) e \*broadcast\* a nova recompensa.



\### Passo 2: Liquidação da Recompensa (Lógica de Morte)



1\.  \*\*Detecção de Morte:\*\* No \*handler\* de Combate do Servidor (ou na rotina de morte de jogador), após a morte do `target`, a lógica deve ser ativada.

2\.  \*\*Verificação:\*\* Verificar se o `target` possui uma recompensa ativa (`target.bounty\_value > 0`).

3\.  \*\*Execução (Transferência):\*\*

&nbsp;   \* Obter o objeto `Player` do `killer` (quem matou).

&nbsp;   \* \*\*Transferir o Valor:\*\* Adicionar o `target.bounty\_value` ao ouro do `killer` (`killer.gold += target.bounty\_value`).

&nbsp;   \* \*\*Zerar:\*\* Limpar os campos de \*bounty\* do `target` (`target.bounty\_value = 0`).

&nbsp;   \* \*\*Feedback:\*\* Notificar o `killer` sobre o ouro recebido.



\### Passo 3: Handlers de Suporte



\* Implementar um \*handler\* para que os jogadores possam verificar o valor da recompensa na cabeça de um alvo (`req\_check\_bounty`).

\* Implementar um \*handler\* para \*\*cancelamento de recompensa\*\* (se o jogo permitir, com devolução de moeda).



---



\## ✅ Critérios de Aceitação



\* \*\*Comunicação Completa:\*\* Os novos \*handlers\* de rede para `req\_place\_bounty`, `req\_check\_bounty` e os \*handlers\* de notificação estão implementados.

\* \*\*Integridade Econômica:\*\* A lógica de `req\_place\_bounty` subtrai o ouro do jogador antes de registrar o valor.

\* \*\*Liquidação:\*\* A lógica de morte no Servidor detecta a recompensa e transfere a moeda para o jogador que matou.

\* \*\*Estrutura Utilizada:\*\* A implementação reutiliza as estruturas de \*bounty\* existentes na classe `Player`.

