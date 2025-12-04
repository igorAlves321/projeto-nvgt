\# Task 7 — Sistema de Loot / Drops no Mapa

\*\*Epic:\*\* 1 — Estabilidade, Segurança, Economia (Core)  

\*\*Arquivo:\*\* `/epic1/tasks/loot\_drops\_no\_mapa.md`  

\*\*Status:\*\* A fazer  

\*\*Dependências:\*\*  

\- Task 5 — Sistema de Inventário + Sincronização Realtime  

\- Task 6 — Sistema de Equipamentos e Buffs  

\- Task 3 — Sistema de Rede e Handlers (dispatcher)  

\- Task 4 — Sistema de Movimento (para pickup range / colisão)  

\- `items\_def.json` e `player\_inventory` já definidos



---



\# 🎯 Objetivo

Implementar o sistema de \*\*loot\*\* e \*\*drops\*\* no mapa: geração de itens em eventos (monstros, containers, quests), spawn de itens no chão com persistência temporária, mecânicas de pickup (coleta), regras de prioridade/visibilidade (loot rights), e sincronização eficiente com jogadores próximos. O sistema deve integrar-se com inventário, economia e combate (quando um mob morre).



---



\# 📌 Requisitos Principais



\- Spawnar drops ao ocorrer eventos (morte de mob, abrir baú, evento do mapa)

\- Representar itens no mapa como entidades com:

&nbsp; - `drop\_id`, `item\_id`, `instance\_id?`, `qty`, `x`, `y`, `map\_id`, `owner\_id?`, `expire\_at`

\- Regras de loot:

&nbsp; - `owner\_only` window (ex.: 30s apenas para killer/party)

&nbsp; - depois virar loot `public` (first come, first serve) ou `roll`/`share`

\- Persistência temporária:

&nbsp; - drops sobrevivem reinícios por X tempo (configurável) ou são recalculados

\- Pickup:

&nbsp; - cliente envia `{"type":"pickup","drop\_id":...}`

&nbsp; - servidor valida distância, existência, autorização e espaço no inventário

&nbsp; - remove do mapa, adiciona ao inventário, notifica players próximos

\- Garbage collection:

&nbsp; - drops expiram após `expire\_at` → se configurado, drop some ou vira loot público e depois remove

\- Anti-exploit:

&nbsp; - verificar distance/speedhacks (usar `player.last\_position`/timestamps)

&nbsp; - atomicidade ao transferir do drop para inventário (locks)

\- Eficiência:

&nbsp; - enviar apenas updates para jogadores no mesmo mapa e dentro de radius relevante

&nbsp; - usar `send\_unreliable` para updates de posição/estado de drops e `send\_reliable` para confirmações de pickup



---



\# 📌 Protocolo JSON (mínimo)



\### Server → Client

\- `{"type":"drop\_spawn","drop":{drop\_id,item\_id,qty,x,y,map\_id,owner\_id,visible\_until}}` — spawn inicial

\- `{"type":"drop\_update","drop\_id":...,"state":"picked|expired|public"}` — updates

\- `{"type":"drop\_pickup\_result","status":"ok|error","reason":""}` — resposta ao pedido de pickup



\### Client → Server

\- `{"type":"pickup","drop\_id":<id>}` — solicita pegar item

\- `{"type":"drop\_request\_list","map\_id":<id>}` — pede lista de drops visíveis no mapa (on join)



---



\# 📌 Estruturas de Dados Sugeridas (Servidor)



```nvgt

// Use 'class' em vez de 'struct'

class drop\_entity {

&nbsp;   string drop\_id;        

&nbsp;   string item\_id;

&nbsp;   string instance\_id;    

&nbsp;   int qty;

&nbsp;   int map\_id;

&nbsp;   int x;

&nbsp;   int y;

&nbsp;   uint owner\_id;         

&nbsp;   int64 spawned\_at;      

&nbsp;   int64 owner\_until;     

&nbsp;   int64 expire\_at;       

&nbsp;   string state;          

}



// NVGT usa 'dictionary' (não tipado) em vez de map<T,T>

dictionary drops; // Armazenará: string -> drop\_entity@ (handle)



// Chaves de dicionário devem ser strings. 

// Ao usar, converta o int map\_id para string: drops\_by\_map.set("" + map\_id, array\_handle)

dictionary drops\_by\_map; // Armazenará: string(map\_id) -> string\[]@ (handle de array)

Dicas Adicionais:

• Armazenamento: Ao guardar objetos (drop\_entity) no dicionário, lembre-se de que o NVGT armazena cópias ou handles. Para objetos complexos como sua classe, geralmente é melhor trabalhar com handles (@).

    ◦ Exemplo de inserção: drops.set(id, @nova\_entidade);

    ◦ Exemplo de recuperação: drop\_entity@ e; drops.get(id, @e);4.

• Arrays: Para o valor de drops\_by\_map, você usará handles para arrays de string (string\[]@)56.

