É isso aí! Vamos armar os jogadores para que eles possam se defender das criaturas que acabamos de colocar no mapa! 🔫👾



Atualmente, o seu arquivo de projéteis (`bullet.nvgt`) tem uma função chamada `check\_npc\_collisions`, mas ela está com o código antigo comentado (que tentava acertar apenas os antigos "dragonsauros"). Nós precisamos conectar os tiros da arma do jogador ao novo "Cérebro" dos NPCs (`npcs\_global`) que ativamos na tarefa anterior.



Vamos para a \*\*Mini-Task 9: Sistema de Colisão de Tiros e Danos (Servidor)\*\*.



\### Passo Único: O Código de Colisão Universal (`bullet.nvgt`)



Abra o arquivo \*\*`server/includes/bullet.nvgt`\*\* no código do seu servidor. Procure pela função `check\_npc\_collisions` (que está logo abaixo de `bulletcheck`) e substitua toda ela por este código moderno e otimizado:



```cpp

// Função auxiliar para verificar colisões com TODOS os NPCs da nova arquitetura

void check\_npc\_collisions(int b, int dano) {

&nbsp;   if (b < 0 || b >= int(bullets.length())) return;



&nbsp;   // Varre o array unificado de NPCs e Monstros vivos

&nbsp;   for (uint i = 0; i < npcs\_global.length(); i++) {

&nbsp;       // Ignora NPCs mortos ou que já estão morrendo

&nbsp;       if (npcs\_global\[i].vida <= 0 || npcs\_global\[i].morreu) continue;



&nbsp;       // Verifica se a bala bateu exatamente na coordenada X e Y do NPC no mesmo mapa

&nbsp;       if (bullets\[b].x == npcs\_global\[i].x \&\& bullets\[b].y == npcs\_global\[i].y \&\& bullets\[b].mapname == npcs\_global\[i].map) {

&nbsp;           

&nbsp;           // 1. Toca som de impacto (carne/dano) em 3D para quem está no mapa

&nbsp;           server\_broadcast("play\_body " + bullets\[b].somarma + " " + bullets\[b].x + " " + bullets\[b].y, bullets\[b].mapname);

&nbsp;           

&nbsp;           // 2. Aplica o dano da arma na vida do monstro

&nbsp;           npcs\_global\[i].vida -= dano;

&nbsp;           

&nbsp;           // 3. Sistema de Aggro: O monstro agora sabe quem atirou nele e vai persegui-lo!

&nbsp;           npcs\_global\[i].golpeado = bullets\[b].owner; 

&nbsp;           

&nbsp;           // 4. Se a bala for um míssil ou algo com som contínuo (loop), destrói o som

&nbsp;           if (bullets\[b].loopid != "") {

&nbsp;               destroymsound(parse\_int(bullets\[b].loopid)); 

&nbsp;           }

&nbsp;           

&nbsp;           // 5. Destrói a bala física para que ela não atravesse e acerte outros monstros atrás

&nbsp;           bullets.remove\_at(b);

&nbsp;           return; // Sai da função pois a bala já colidiu

&nbsp;       }

&nbsp;   }

}

```



\### O que acontece nos bastidores agora?

1\. O jogador mira (usando as setas e o Radar que fizemos na Task 8) e aperta a tecla de atirar.

2\. O cliente manda o pacote do tiro e a classe genérica `bullet` do servidor processa a viagem da bala em tempo real (`bulletloop()`).

3\. Em cada passo que a bala dá, ela chama essa nossa nova função `check\_npc\_collisions`.

4\. Se ela encostar no X e Y de \*qualquer\* monstro (`npcs\_global`), ela subtrai o dano (`dano`), informa ao monstro quem atirou (`golpeado = bullets\[b].owner` para ele revidar) e desaparece!

5\. \*\*E o melhor de tudo:\*\* Como ativamos a inteligência artificial na Task 8, no exato milissegundo que a `vida` do monstro chegar a zero ou menos, a função nativa `npc\_global\_loop()` vai detectar a morte, tocar o som de morte do monstro e usar o nosso sistema de Loot da Task 6 para jogar as moedas e itens no chão para o jogador pegar!.



Tudo está \*\*interconectado\*\* agora.



