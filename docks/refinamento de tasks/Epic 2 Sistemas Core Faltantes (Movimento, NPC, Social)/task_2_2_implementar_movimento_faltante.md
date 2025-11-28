\# 🚶 Task 2.2: Implementar Sistemas de Movimento Faltantes (Eco, Agachar, Sentar)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Cliente / Acessibilidade / Movimento

\*\*PRIORIDADE:\*\* MÉDIA-ALTA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO



\## 🎯 Objetivo



Reimplementar três funcionalidades ausentes do BGT que são cruciais para a acessibilidade e o \*roleplay\*:

1\.  \*\*Sistema de Eco:\*\* Auxiliar de navegação para pessoas com deficiência visual.

2\.  \*\*Agachar (Crouch):\*\* Ação de \*gameplay\* (ex: para furtividade, passar por baixo de obstáculos).

3\.  \*\*Sentar/Levantar:\*\* Ação de \*roleplay\* e social.



\## 📝 Referências e Contexto



\* \*\*Gaps Faltantes:\*\* Eco, Agachar e Sentar/Levantar foram listados como funcionalidades ausentes na migração.

\* \*\*Impacto:\*\* O Sistema de Eco é uma ferramenta de navegação fundamental (acessibilidade).

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Cliente:\*\* `client.nvgt` (Loop principal para detecção de teclas), `cliente/includes/audio.nvgt` (para o Eco).

&nbsp;   \* \*\*Servidor:\*\* `server/includes/player.nvgt` (Atualização do estado do jogador: `is\_crouching`, `is\_sitting`), `server/includes/network.nvgt` (para sincronização dos estados).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



\### Passo 1: Sistema de Eco (Acessibilidade)



A lógica do Eco deve ser implementada no Cliente. Quando o jogador usa o comando/tecla (Ex: tecla `E`):



1\.  \*\*Emissão:\*\* O Cliente deve disparar um som de pulso (Ex: `sound\_pulse.ogg`).

2\.  \*\*Detecção de Colisão:\*\* O Cliente precisa verificar se há uma \*\*Parede\*\* ou \*\*Objeto Sólido\*\* na direção do pulso.

3\.  \*\*Cálculo:\*\* O Cliente calcula a \*\*distância\*\* até o primeiro objeto sólido encontrado (usando as coordenadas do mapa).

4\.  \*\*Feedback de Áudio:\*\* O Cliente reproduz um som de retorno (\*\*echo\*\*) com um \*\*volume\*\* inversamente proporcional à distância e um \*\*delay\*\* proporcional à distância.

5\.  \*\*Rotina:\*\* O Cliente deve incluir uma rotina `echocheck()` (mencionada no `client.nvgt`) para executar essa lógica.



\### Passo 2: Agachar e Sentar (Sincronização de Estado)



As ações de Agachar e Sentar são estados do jogador que precisam ser sincronizados entre Cliente e Servidor.



1\.  \*\*Modificação do `Player`:\*\* Adicionar novos \*flags\* booleanos ou inteiros na classe `Player` no Servidor (`server/includes/player.nvgt`):

&nbsp;   \* Ex: `int player\_stance` (0: De Pé, 1: Agachado, 2: Sentado).

2\.  \*\*Handler de Rede:\*\* Criar um \*handler\* de rede de Cliente para Servidor.

&nbsp;   \* \*\*Handler:\*\* `req\_update\_stance \[new\_stance]`.

3\.  \*\*Servidor (Validação):\*\* O Servidor recebe `req\_update\_stance`.

&nbsp;   \* \*\*Validação de Lógica:\*\* Verificar se a mudança é válida (Ex: O jogador não pode sentar enquanto está em combate).

&nbsp;   \* \*\*Atualização:\*\* Atualizar o `player.player\_stance` na memória do Servidor.

&nbsp;   \* \*\*Sincronização:\*\* Enviar um \*broadcast\* (`msg\_player\_stance\_update \[player\_id] \[new\_stance]`) para todos os jogadores no mapa.

4\.  \*\*Cliente (Loop Principal):\*\* No `client.nvgt`, detectar a tecla de Agachar (`C`) e Sentar (`X`). Enviar `req\_update\_stance` ao Servidor e atualizar a posição visual/sonora do jogador.

&nbsp;   \* \*Nota:\* Agachar pode reduzir a \*hitbox\* do jogador no Servidor (lógica de combate).



---



\## ✅ Critérios de Aceitação



\* \*\*Sistema de Eco Funcional:\*\* O jogador pode acionar o Eco, e o Cliente reproduz um som de retorno com volume/delay que reflete a distância real até o objeto mais próximo.

\* \*\*Sincronização de Estado:\*\* O estado de Agachar/Sentar é sincronizado via \*handlers\* de rede e o objeto `Player` no Servidor armazena o estado corretamente.

\* \*\*Acessibilidade:\*\* O Eco fornece um meio de navegação espacial essencial para jogadores com deficiência visual.

\* \*\*Usabilidade:\*\* A lógica de Agachar e Sentar é funcional e integrada ao \*game loop\*.

