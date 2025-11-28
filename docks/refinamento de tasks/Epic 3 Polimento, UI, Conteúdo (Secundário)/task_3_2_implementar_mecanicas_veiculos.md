\# 🚗 Task 3.2: Implementar Mecânicas de Veículos e Outras Ações (Avançado)



\*\*EPIC:\*\* Fechamento de Gaps de Polimento (Epic 3)

\*\*DOMÍNIO:\*\* Servidor / Gameplay / Movimento

\*\*PRIORIDADE:\*\* MÉDIA-BAIXA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO-ALTO



\## 🎯 Objetivo



Finalizar os \*gaps\* de \*gameplay\* e movimentação identificados no Relatório Comparativo, implementando a lógica completa para:

1\.  \*\*Veículos:\*\* Integrar completamente a estrutura de veículos (Ex: carros, motos) no loop de jogo.

2\.  \*\*Paraquedas:\*\* Criar a mecânica de segurança de paraquedas (ligada ao uso de aeronaves).

3\.  \*\*Vidros Quebráveis:\*\* Criar a lógica de interação com o ambiente (quebrar vidros).



\## 📝 Referências e Contexto



\* \*\*Gaps Faltantes:\*\* Veículos estavam parcialmente integrados, e Paraquedas e Vidros Quebráveis estavam listados como \*\*NÃO MIGRADOS\*\*.

\* \*\*Persistência:\*\* O estado dos veículos (posição, HP, ocupante) deve ser sincronizado entre Cliente/Servidor e persistido no DB (SQLite).

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Servidor:\*\* `servidor/includes/vehicles.nvgt`, `server/includes/network.nvgt` (para sincronização de movimento de veículos), Módulo de Combate (para dano de queda/vidro).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve focar na integração do módulo de veículos e na lógica de \*gameplay\* que afeta o movimento e o ambiente.



\### Passo 1: Integração do Sistema de Veículos (Controle e Sincronização)



1\.  \*\*Lógica do Servidor:\*\* No \*game loop\* principal do Servidor, garantir que o módulo `vehicles.nvgt` seja chamado periodicamente para processar o movimento dos veículos e a sincronização de sua posição/estado.

2\.  \*\*Sincronização:\*\* Criar um \*handler\* de rede (`msg\_vehicle\_update \[vehicle\_id] \[x] \[y] \[rotation]`) que o Servidor envia para todos os jogadores no mapa para atualizar a posição dos veículos.

3\.  \*\*Controle de Entrada:\*\* Implementar \*handlers\* que permitem ao jogador entrar/sair de um veículo e assumir o controle (Servidor deve validar a proximidade e o estado do veículo).



\### Passo 2: Implementar a Mecânica de Paraquedas



O Paraquedas é uma mecânica crítica de segurança para aeronaves.



1\.  \*\*Handler de Ação:\*\* Criar um \*handler\* de Cliente para Servidor (Ex: `req\_deploy\_parachute`).

2\.  \*\*Lógica do Servidor (CRÍTICO):\*\* O Servidor recebe a requisição, \*\*valida\*\* se o jogador está em uma aeronave e se está a uma \*\*altura mínima/máxima\*\* para o \*deploy\*.

3\.  \*\*Execução:\*\* Se a validação for bem-sucedida, o Servidor:

&nbsp;   \* Altera o estado do jogador (`player.is\_parachuting = true`).

&nbsp;   \* Altera a lógica de queda (`fall\_damage\_multiplier = 0.0`).

&nbsp;   \* Sincroniza o novo estado com outros jogadores.



\### Passo 3: Implementar Vidros Quebráveis (Interação Ambiental)



Esta mecânica adiciona interatividade e \*feedback\* de áudio ao ambiente.



1\.  \*\*Estrutura de Dados:\*\* Criar uma classe (`GlassPanel`) para vidros, com propriedades como `is\_broken`.

2\.  \*\*Detecção de Colisão:\*\* Integrar o \*check\* de `GlassPanel` à rotina de colisão (módulo de combate/parede).

&nbsp;   \* \*\*Ação:\*\* Se um projétil ou jogador colidir com um vidro, o Servidor:

&nbsp;       \* Altera o estado para `is\_broken = true`.

&nbsp;       \* \*\*Broadcast\*\* um som de quebra de vidro para todos os jogadores próximos.

&nbsp;       \* Aplica dano mínimo ao jogador se ele quebrou o vidro com o corpo.



---



\## ✅ Critérios de Aceitação



\* \*\*Sincronização de Veículos:\*\* O Servidor sincroniza a posição e o estado dos veículos ativos.

\* \*\*Paraquedas Funcional:\*\* A lógica de \*deploy\* e a anulação de dano de queda estão implementadas e validadas pela altura.

\* \*\*Vidros Quebráveis:\*\* A lógica de colisão e o \*broadcast\* de áudio de quebra de vidro estão implementados.

