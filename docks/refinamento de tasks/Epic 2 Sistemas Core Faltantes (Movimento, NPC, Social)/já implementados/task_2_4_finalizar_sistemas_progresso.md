\# 🌟 Task 2.4: Finalizar Sistemas de Progresso (Quests, Achievements, Daily Rewards)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Servidor / Conteúdo / Progressão

\*\*PRIORIDADE:\*\* MÉDIA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO-ALTO (Mais em Conteúdo do que em Código)



\## 🎯 Objetivo



Finalizar e testar a estrutura dos sistemas de progressão que foram implementados parcialmente durante a migração:

1\.  \*\*Quests (Missões):\*\* Ativar o fluxo de missões e criar a primeira leva de conteúdo.

2\.  \*\*Achievements (Conquistas):\*\* Definir as conquistas e integrá-las aos \*game events\*.

3\.  \*\*Daily Rewards (Recompensas Diárias):\*\* Testar o fluxo de tempo e a distribuição de recompensas.



\## 📝 Referências e Contexto



\* \*\*Status Atual:\*\* Estes sistemas estão em \*\*FASE 5\*\* (Progressão) ou com estrutura criada, mas conteúdo limitado ou não testado.

\* \*\*Persistência:\*\* Todos estes sistemas dependem da leitura e escrita em \*\*SQLite\*\* (tabelas `quests`, `achievements`, `daily\_rewards\_log`).

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Servidor:\*\* `servidor/includes/quests.nvgt`, `servidor/includes/achievements.nvgt`, `servidor/includes/daily\_rewards.nvgt`, e o módulo `db.nvgt`.



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O foco deve ser em mover a estrutura de \*framework\* para a fase de \*\*produção de conteúdo\*\* e \*\*integração de eventos\*\*.



\### Passo 1: Sistema de Quests (Missões)



1\.  \*\*Definir Estrutura do Conteúdo:\*\* Criar um formato de dados (Ex: arquivo INI/JSON ou tabela DB) para armazenar: `quest\_id`, `requisito` (Ex: "Matar 10 ratos"), `recompensa` (Ex: "100 Gold"), `texto\_npc`.

2\.  \*\*Integração de Eventos:\*\* Modificar os \*handlers\* de eventos relevantes (Ex: `OnNPCKill`, `OnItemCollect`) para \*\*chamar o módulo `quests.nvgt`\*\*, que deve verificar se o evento satisfaz algum requisito de missão ativa do jogador.

3\.  \*\*Fluxo de Sucesso:\*\* Implementar a lógica de \*\*entrega de recompensa\*\* (adicionar moeda, XP, ou item) e marcar a missão como concluída no DB.



\### Passo 2: Sistema de Achievements (Conquistas)



1\.  \*\*Definir Conteúdo:\*\* Criar as definições das primeiras 10-20 conquistas (Ex: "Primeira Morte", "Alcançar Nível 10", "Visitar 5 Mapas").

2\.  \*\*Integração de Eventos:\*\* Implementar \*listeners\* de eventos no módulo `achievements.nvgt` que são acionados por eventos globais do servidor.

&nbsp;   \* \*Exemplo:\* Quando um jogador atinge Nível 10, o evento chama `achievements.check\_player\_progress(p, "LEVEL\_UP")`.

3\.  \*\*Execução:\*\* Quando uma conquista é alcançada, atualizar o DB e enviar uma notificação especial ao Cliente.



\### Passo 3: Daily Rewards (Recompensas Diárias)



1\.  \*\*Validar Temporizador:\*\* Testar rigorosamente a lógica de tempo no módulo `daily\_rewards.nvgt`. O sistema deve usar o tempo do servidor e persistir a \*\*última data de coleta\*\* no DB do jogador.

2\.  \*\*Verificação de Login:\*\* Implementar a rotina que é acionada no \*\*Login do Jogador\*\*.

&nbsp;   \* \*\*Ação:\*\* Verificar se \*current\_day\* > \*last\_collected\_day\*.

&nbsp;   \* \*\*Ação:\*\* Se for o dia seguinte, transferir a recompensa (moeda/item) para o jogador e atualizar o `last\_collected\_day` no DB.

3\.  \*\*Testes de Segurança:\*\* Garantir que não seja possível explorar o sistema de tempo (Ex: redefinindo a data do Cliente).



---



\## ✅ Critérios de Aceitação



\* \*\*Quests Funcionais:\*\* O fluxo de aceitar, progredir e completar missões (usando os \*handlers\* de eventos do Servidor) é funcional.

\* \*\*Achievements Integrados:\*\* O Servidor detecta eventos de jogo e marca conquistas no DB, notificando o Cliente.

\* \*\*Daily Rewards Seguros:\*\* O sistema de recompensa diária usa a persistência do Servidor (SQLite) para garantir que as recompensas só possam ser coletadas uma vez por período.

\* \*\*Engajamento:\*\* A primeira leva de conteúdo (missões/conquistas) é criada e testada.

