\# 🫂 Task 2.8: Finalizar Sistemas Sociais (Guilds, Parties, Friends)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Servidor / Social / Persistência

\*\*PRIORIDADE:\*\* MÉDIA-ALTA



\## 🎯 Objetivo



Finalizar e testar completamente os sistemas sociais avançados que já possuem estrutura de código, mas que podem estar incompletos ou sem persistência final em \*\*SQLite\*\*. O foco é garantir a funcionalidade e a persistência de:

1\.  \*\*Guilds/Clãs:\*\* Criação, gerenciamento de membros/patentes, e chat de guilda.

2\.  \*\*Parties (Grupos):\*\* Criação, convite, divisão de experiência (XP), e chat de grupo.

3\.  \*\*Friends (Amigos):\*\* Adicionar/remover amigos e sincronização de status (\*online/offline\*).



\## 📝 Referências e Contexto



\* \*\*Status:\*\* Estes sistemas estão na \*\*FASE 4\*\* e possuem estrutura de código (Ex: `trading.nvgt`, `party.nvgt`, `friends.nvgt`, `guilds.nvgt`).

\* \*\*Persistência:\*\* O desafio reside em garantir que os relacionamentos e os dados da Guilda (Ex: Nome, Lista de Membros, Patentes) sejam persistidos corretamente em tabelas \*\*SQLite\*\* dedicadas ou em campos da tabela `players`.

\* \*\*Módulos Envolvidos:\*\* Módulos de Chat (para canais específicos), `server/includes/network.nvgt` (para \*handlers\* de convite/status) e o módulo `db.nvgt`.



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvimento deve se concentrar em \*\*fechar o ciclo de vida\*\* de cada sistema social, desde a criação até a persistência.



\### Passo 1: Finalizar Sistema de Guilds/Clãs



1\.  \*\*Criação/Persistência:\*\* Implementar a lógica de rede (`req\_create\_guild`) e a persistência em DB (SQLite) para o registro da guilda (nome, líder, \*tag\*).

2\.  \*\*Gerenciamento:\*\* Criar \*handlers\* de rede para `invite\_member`, `remove\_member`, `set\_rank`.

3\.  \*\*Chat Dedicado:\*\* Assegurar que o canal de Chat de Guilda (`CHAT\_TEAM` ou canal similar) funcione corretamente e filtre mensagens apenas para membros.



\### Passo 2: Finalizar Sistema de Parties (Grupos)



1\.  \*\*Convite/Criação:\*\* Implementar \*handlers\* para `req\_create\_party` e `req\_invite\_party`.

2\.  \*\*Sincronização:\*\* Garantir que o Servidor mantenha a lista de membros do grupo na memória e a sincronize com todos os membros.

3\.  \*\*Divisão de XP:\*\* Implementar a lógica de divisão de experiência (XP) no módulo de combate (`combat.nvgt` ou similar): quando um monstro morre, o XP é dividido entre os membros da \*party\* que estão próximos (`get\_2d\_distance` - Task 2.2).



\### Passo 3: Finalizar Sistema de Amigos (Friends)



1\.  \*\*Adição/Remoção:\*\* Implementar \*handlers\* para `req\_add\_friend` e `req\_remove\_friend`.

2\.  \*\*Persistência:\*\* Persistir a lista de amigos no DB (`friends\_list` campo na tabela `players` ou tabela separada).

3\.  \*\*Status Sync:\*\* Criar um \*handler\* que notifica todos os amigos de um jogador quando ele faz \*\*login\*\* ou \*\*logout\*\*, permitindo a sincronização do status \*online/offline\* no Cliente.



---



\## ✅ Critérios de Aceitação



\* \*\*Guilds Persistentes:\*\* Guilds podem ser criadas, os membros são salvos no DB e o chat de guilda é funcional.

\* \*\*XP Compartilhado:\*\* O Servidor implementa a lógica de \*\*divisão de XP\*\* entre os membros da \*party\* (Grupos) próximos.

\* \*\*Status Sync:\*\* O sistema de amigos notifica o Cliente quando amigos fazem login/logout.

\* \*\*Ciclo de Vida:\*\* Todos os sistemas sociais têm \*handlers\* para a criação, convite/aceitação e remoção/ruptura.

