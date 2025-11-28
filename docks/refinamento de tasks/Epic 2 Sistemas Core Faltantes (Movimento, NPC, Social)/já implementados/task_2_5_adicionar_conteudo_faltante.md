\# 🦖 Task 2.5: Adicionar Conteúdo Faltante (NPCs e Itens)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Servidor / Conteúdo / Gameplay

\*\*PRIORIDADE:\*\* MÉDIA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO (Configuração de Dados)



\## 🎯 Objetivo



Eliminar o \*\*Gap de Conteúdo\*\* identificado na migração ao configurar e integrar os seguintes itens:

1\.  \*\*9 Tipos de NPCs/Monstros Faltantes:\*\* Configurar os dados (stats, loot, respawn) para os NPCs que existiam no BGT, mas ainda não foram integrados ao novo \*\*Sistema Genérico de NPCs\*\* do NVGT.

2\.  \*\*Itens e Mecânicas de Combate Faltantes:\*\* Adicionar itens, tipos de dano, e mecânicas menores (ex: ricochete, modo burst) que ainda não foram totalmente migrados do BGT.



\## 📝 Referências e Contexto



\* \*\*Gaps Faltantes:\*\* 9 Tipos de NPCs/Monstros (Ex: cachorro, lobo, dragões, sequestrador) e várias mecânicas de combate.

\* \*\*Vantagem NVGT:\*\* O novo \*\*Sistema Genérico de NPCs\*\* do NVGT simplifica esta tarefa, pois exige apenas a \*\*configuração de dados\*\* (stats, modelo de loot) e não a criação de classes inteiras.

\* \*\*Módulos Envolvidos:\*\*

&nbsp;   \* \*\*Servidor:\*\* `servidor/includes/npc.nvgt` (Sistema Genérico), `servidor/includes/monstruo.nvgt`, `servidor/includes/weapons.nvgt`, `servidor/includes/item.nvgt`.



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve focar em criar os arquivos de configuração de dados e integrar as mecânicas faltantes.



\### Passo 1: Configuração dos 9 Tipos de NPCs Faltantes



1\.  \*\*Criação de Arquivos de Dados:\*\* Criar os arquivos de configuração (Ex: JSON, INI, ou tabela DB) para cada um dos 9 tipos de NPCs/Monstros:

&nbsp;   \* `cachorro.data`

&nbsp;   \* `lobo.data`

&nbsp;   \* `urso.data`

&nbsp;   \* `macaco.data`

&nbsp;   \* `dragonsauro.data`

&nbsp;   \* `megadragonsauro.data`

&nbsp;   \* `guardacofre.data`

&nbsp;   \* `guardaandar.data`

&nbsp;   \* `sequestrador\_v1.data`

2\.  \*\*Definir Parâmetros:\*\* Para cada arquivo, definir os parâmetros que o Sistema Genérico de NPCs/Monstros exige:

&nbsp;   \* `MAX\_HP`, `DANO\_BASE`, `TIPO\_DE\_ATAQUE`.

&nbsp;   \* `EXPERIENCIA\_CONCEDIDA`.

&nbsp;   \* `LOOT\_TABLE` (Itens e chance de drop).

3\.  \*\*Integração:\*\* Adicionar os \*IDs\* desses novos NPCs à lista de \*spawns\* ou à lista global de tipos de NPCs reconhecidos pelo `npc.nvgt`.



\### Passo 2: Implementação de Mecânicas de Combate Faltantes



1\.  \*\*Ricochete:\*\* Verificar se a lógica de cálculo de `ricochete` (sons e lógica de dano) ainda está faltando. Se sim, integrar a lógica no módulo de combate.

2\.  \*\*Modo Burst:\*\* Implementar o \*\*Modo Burst\*\* (rajada de tiros) completo para armas que o suportavam no BGT. Isso exige modificações no \*handler\* de disparo (`playerfires.nvgt` ou similar) para gerenciar o \*delay\* entre os tiros da rajada.

3\.  \*\*Novos Tipos de Armas/Munição:\*\* Se houver tipos de armas ou munição específicas do BGT que não foram migradas (além das 30+ existentes), garantir que elas sejam definidas no módulo `weapons.nvgt`.



\### Passo 3: Feedback e Testes



\* Testar se o \*spawn\* dos novos NPCs funciona nos mapas.

\* Testar se a lógica de XP e \*loot\* funciona corretamente.

\* Testar se o Modo Burst e o Ricochete funcionam conforme esperado no cliente e servidor.



---



\## ✅ Critérios de Aceitação



\* \*\*NPCs Funcionais:\*\* Os 9 tipos de NPCs/Monstros faltantes estão configurados e podem ser \*spawnados\* e mortos, concedendo XP e \*loot\*.

\* \*\*Modo Burst:\*\* O Modo Burst (rajada de tiros) está implementado e funcional.

\* \*\*Integridade do Conteúdo:\*\* O \*gap\* de conteúdo de NPCs/Monstros entre BGT e NVGT é \*\*fechado\*\*.

\* \*\*Segurança:\*\* A nova lógica de combate/NPCs não introduz novos \*exploits\* ou \*memory leaks\*.

