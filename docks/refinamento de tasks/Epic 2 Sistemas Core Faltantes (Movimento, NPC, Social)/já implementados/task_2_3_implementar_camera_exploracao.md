\# 🧭 Task 2.3: Implementar Câmera de Exploração (Visão do Mapa/G+Teclas)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Cliente / Usabilidade / Navegação

\*\*PRIORIDADE:\*\* MÉDIA-ALTA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO



\## 🎯 Objetivo



Reimplementar a \*\*Câmera de Exploração\*\* (\*G+Teclas\* no BGT), permitindo que o jogador se mova por uma \*\*visão estática do mapa\*\* sem sair de sua posição atual. Esta funcionalidade é crucial para a \*\*navegação espacial\*\* e para a visualização de objetos e zonas próximas antes de se mover.



\## 📝 Referências e Contexto



\* \*\*Gap Faltante:\*\* A Câmera de Exploração (G+teclas) foi listada como um \*gap\* de usabilidade na migração.

\* \*\*Mecanismo:\*\* O sistema não move o jogador; ele apenas move o \*\*ponto de escuta de áudio\*\* (\*listener\*) para simular a exploração do ambiente.

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Cliente:\*\* `client.nvgt` (Loop principal para detecção de teclas), `cliente/includes/audio.nvgt` (para manipulação do \*listener\* de áudio).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve cobrir a rotina de \*\*Ativação/Desativação\*\* do modo e a \*\*Manipulação do Listener\*\* de áudio (o "ouvido" do jogo).



\### Passo 1: Estrutura de Dados (Estado da Câmera)



1\.  \*\*Flag de Estado:\*\* Adicionar um \*flag\* booleano global no Cliente (Ex: `is\_exploring\_camera\_active`) e variáveis para armazenar a posição da câmera (Ex: `camera\_x`, `camera\_y`).

2\.  \*\*Posição Inicial:\*\* Ao ativar, a `camera\_x` e `camera\_y` devem ser inicializadas com a posição atual do jogador (`player.x`, `player.y`).



\### Passo 2: Ativação e Desativação (Teclas)



1\.  \*\*Ativação:\*\* Detectar a tecla de ativação (Ex: tecla `G`).

&nbsp;   \* \*\*Ação:\*\* Setar `is\_exploring\_camera\_active = true`.

&nbsp;   \* \*\*Ação:\*\* Iniciar o \*loop\* de atualização da câmera.

2\.  \*\*Desativação:\*\* Detectar a tecla de desativação (Ex: `G` novamente ou `ESC`).

&nbsp;   \* \*\*Ação:\*\* Setar `is\_exploring\_camera\_active = false`.

&nbsp;   \* \*\*Ação:\*\* Resetar o \*listener\* de áudio para a posição do jogador (`player.x`, `player.y`).



\### Passo 3: Loop de Exploração (Movimento do Listener)



O Cliente deve implementar um \*loop\* que só é ativo quando `is\_exploring\_camera\_active` é verdadeiro.



1\.  \*\*Detecção de Teclas:\*\* Dentro do \*loop\*, detectar as teclas de movimento (`WASD` ou Setas) para controlar a posição da câmera.

2\.  \*\*Atualização da Posição da Câmera:\*\* Mover as variáveis `camera\_x` e `camera\_y` com base nas teclas.

&nbsp;   \* \*Exemplo:\* Se o jogador pressionar 'W' (frente), `camera\_y += step\_size`.

3\.  \*\*Atualização do Listener de Áudio (CRÍTICO):\*\* A API de Áudio do NVGT deve ser chamada para informar ao \*engine\* que o ponto de escuta (o \*listener\*) está agora na `camera\_x`, `camera\_y`.

&nbsp;   \* \*\*API:\*\* Usar uma função como `sound\_set\_listener\_position(camera\_x, camera\_y, player.rotation)` para que o som 3D seja renderizado a partir da posição da câmera.



\### Passo 4: Feedback e Interação



\* Quando a câmera está ativa, \*\*qualquer comando de movimento do jogador deve ser ignorado\*\*.

\* Quando o jogador pressiona o botão de interação, ele deve interagir com \*\*o objeto mais próximo da posição da câmera (`camera\_x`, `camera\_y`)\*\*, e não da posição real do jogador.



---



\## ✅ Critérios de Aceitação



\* \*\*Controle Funcional:\*\* O jogador pode ativar e desativar o modo de Câmera de Exploração.

\* \*\*Movimento do Listener:\*\* Mover a câmera atualiza a \*\*posição do \*listener\* de áudio\*\*, permitindo que o jogador ouça sons e objetos 3D na nova posição.

\* \*\*Isolamento de Jogador:\*\* Os comandos de movimento do jogador são \*\*ignorados\*\* enquanto a câmera de exploração está ativa.

\* \*\*Usabilidade:\*\* A Câmera de Exploração pode ser usada para interagir com objetos distantes (Ex: ler um texto ou usar um item).

