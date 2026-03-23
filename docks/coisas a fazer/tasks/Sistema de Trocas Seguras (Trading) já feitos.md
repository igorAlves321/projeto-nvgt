Vamos para a Mini-Task 15: Sistema de Trocas Seguras (Trading).

Faremos a lógica do servidor primeiro, garantindo que ninguém consiga roubar o amiguinho ou bugar os itens.

Passo 1: O Núcleo do Trade no Servidor (trading.nvgt)

Abra o arquivo server/includes/trading.nvgt

2

. Lá você tem os stubs (esqueletos) de várias funções. Substitua as funções cmd\_trade, cmd\_accept e execute\_trade por este código blindado:

// ============================================================================

// NÚCLEO DO SISTEMA DE TROCAS (Mini-Task 15)

// ============================================================================



// Comando: Iniciar troca

void cmd\_trade(int player\_index, string target\_name) {

&nbsp;   if(players\[player\_index].charname == target\_name) {

&nbsp;       send\_reliable\_text(players\[player\_index].peer\_id, "say \[ERRO] Você não pode trocar consigo mesmo!", 0);

&nbsp;       return;

na real, o fluxo vai ser bem parecido com o que acontece no bgt, 

