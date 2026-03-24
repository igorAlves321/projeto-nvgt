Chegamos à \*\*última grande mecânica de mundo\*\* da nossa lista! 🚗🚤🚁



O \*\*Sistema de Veículos\*\* é o que vai dar agilidade aos jogadores para explorarem os mapas enormes do seu jogo, ao mesmo tempo em que cria uma demanda constante na economia do jogo por \*\*Gasolina\*\*.



Os veículos no seu servidor NVGT não são apenas "mudanças de velocidade" no cliente; eles possuem física no servidor, gastam combustível por \*tile\* andado, salvam a quantidade de gasolina no arquivo de cada veículo do jogador e tocam o som do motor em 3D para quem estiver perto!



Vamos para a \*\*Mini-Task 24: Sistema Físico de Veículos (`vehicles.nvgt`)\*\*.



\### Passo 1: O Motor de Veículos no Servidor (`vehicles.nvgt`)



Abra o arquivo \*\*`server/includes/vehicles.nvgt`\*\*. Nós vamos substituir as funções de \*stubs\* (vazias) por um código completo que monitora o movimento do jogador enquanto ele está dirigindo e desconta a gasolina com precisão cirúrgica.



Substitua as funções vazias `cmd\_entrar`, `cmd\_sair`, `cmd\_abastecer` e `vehicles\_loop` por este código:



```cpp

// ============================================================================

// NÚCLEO FÍSICO E CONSUMO DE VEÍCULOS (Mini-Task 24)

// ============================================================================



// Dicionário extra para rastrear rapidamente quem está dirigindo o quê

dictionary active\_drivers; // player\_name -> vehicle\_type



// Comando: Entrar em veículo

void cmd\_entrar(int player\_index, string vehicle\_type) {

&#x20;   if(player\_index < 0 || player\_index >= int(players.length())) return;

&#x20;   player@ p = players\[player\_index];

&#x20;   if(!p.is\_logged\_in) return;

&#x20;   

&#x20;   // Verifica se já está dirigindo

&#x20;   if(active\_drivers.exists(p.charname)) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Você já está em um veículo! Digite /sair primeiro.", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Verifica se ele tem o veículo no inventário (Ex: item chamado "moto" ou "carro")

&#x20;   if(inv\_item\_number(p, vehicle\_type) <= 0) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Você não possui o veículo: " + vehicle\_type + ".", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Carrega a gasolina salva no banco de dados do veículo

&#x20;   double fuel = vehicle\_load\_fuel(p.charname, vehicle\_type);

&#x20;   if(fuel <= 0) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] O tanque do(a) " + vehicle\_type + " está vazio! Use /abastecer.", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Registra o jogador como motorista ativo

&#x20;   active\_drivers.set(p.charname, vehicle\_type);

&#x20;   vehicle\_runtime\_fuel.set(p.charname, fuel);

&#x20;   vehicle\_last\_x.set(p.charname, p.x);

&#x20;   vehicle\_last\_y.set(p.charname, p.y);



&#x20;   // Efeitos Audiovisuais

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary engine\_start.ogg", 0);

&#x20;   server\_broadcast("play\_body engine\_start.ogg " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&#x20;   send\_reliable\_text(p.peer\_id, "say \[Veículos] Você ligou o(a) " + vehicle\_type + ". Combustível: " + int(fuel) + "%", 0);

}



// Comando: Sair de veículo

void cmd\_sair(int player\_index) {

&#x20;   if(player\_index < 0 || player\_index >= int(players.length())) return;

&#x20;   player@ p = players\[player\_index];

&#x20;   if(!p.is\_logged\_in) return;

&#x20;   

&#x20;   string vtype;

&#x20;   if(!active\_drivers.get(p.charname, vtype)) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Você não está dirigindo nenhum veículo.", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Salva o combustível atual de volta no disco/DB

&#x20;   double fuel = 0;

&#x20;   vehicle\_runtime\_fuel.get(p.charname, fuel);

&#x20;   vehicle\_save\_fuel(p.charname, vtype, fuel);



&#x20;   // Limpa os registros

&#x20;   active\_drivers.delete(p.charname);

&#x20;   vehicle\_runtime\_fuel.delete(p.charname);



&#x20;   // Efeitos Audiovisuais

&#x20;   send\_reliable\_text(p.peer\_id, "play\_stationary engine\_stop.ogg", 0);

&#x20;   server\_broadcast("play\_body engine\_stop.ogg " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&#x20;   send\_reliable\_text(p.peer\_id, "say \[Veículos] Você desligou e saiu do veículo.", 0);

}



// Comando: Abastecer veículo

void cmd\_abastecer(int player\_index) {

&#x20;   if(player\_index < 0 || player\_index >= int(players.length())) return;

&#x20;   player@ p = players\[player\_index];

&#x20;   if(!p.is\_logged\_in) return;



&#x20;   string vtype;

&#x20;   if(!active\_drivers.get(p.charname, vtype)) {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Você precisa estar DENTRO do veículo para abastecê-lo.", 0);

&#x20;       return;

&#x20;   }



&#x20;   // Verifica se o jogador tem o galão de gasolina no inventário de forma segura

&#x20;   if(remove\_item\_with\_sync(p, "gasolina", 1)) {

&#x20;       double current\_fuel = 0;

&#x20;       vehicle\_runtime\_fuel.get(p.charname, current\_fuel);

&#x20;       

&#x20;       current\_fuel += 40.0; // Um galão enche 40% do tanque

&#x20;       if(current\_fuel > 100.0) current\_fuel = 100.0;

&#x20;       

&#x20;       // Atualiza a RAM e o Disco

&#x20;       vehicle\_runtime\_fuel.set(p.charname, current\_fuel);

&#x20;       vehicle\_save\_fuel(p.charname, vtype, current\_fuel);

&#x20;       

&#x20;       send\_reliable\_text(p.peer\_id, "play\_stationary glug.ogg", 0); // Som enchendo o tanque

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Tanque abastecido! Combustível atual: " + int(current\_fuel) + "%", 0);

&#x20;   } else {

&#x20;       send\_reliable\_text(p.peer\_id, "say \[Veículos] Você não tem um galão de 'gasolina' na mochila.", 0);

&#x20;   }

}



// Loop de cálculo de combustível (avaliado a cada tick)

void vehicles\_loop() {

&#x20;   if(vehicle\_loop\_timer.elapsed < VEHICLE\_LOOP\_INTERVAL\_MS) return;

&#x20;   vehicle\_loop\_timer.restart();



&#x20;   string\[] drivers = active\_drivers.get\_keys();

&#x20;   for(uint i = 0; i < drivers.length(); i++) {

&#x20;       string p\_name = drivers\[i];

&#x20;       int p\_idx = get\_player\_index\_from(p\_name);

&#x20;       

&#x20;       // Se o jogador desconectou enquanto dirigia, salmos e limpamos a vaga

&#x20;       if(p\_idx == -1) {

&#x20;           string vtype;

&#x20;           active\_drivers.get(p\_name, vtype);

&#x20;           double f = 0;

&#x20;           vehicle\_runtime\_fuel.get(p\_name, f);

&#x20;           vehicle\_save\_fuel(p\_name, vtype, f);

&#x20;           active\_drivers.delete(p\_name);

&#x20;           continue;

&#x20;       }



&#x20;       player@ p = players\[p\_idx];

&#x20;       string vtype;

&#x20;       active\_drivers.get(p\_name, vtype);



&#x20;       int last\_x = 0, last\_y = 0;

&#x20;       vehicle\_last\_x.get(p\_name, last\_x);

&#x20;       vehicle\_last\_y.get(p\_name, last\_y);



&#x20;       // Se as coordenadas mudaram, significa que ele andou com o veículo!

&#x20;       if(p.x != last\_x || p.y != last\_y) {

&#x20;           double fuel = 0;

&#x20;           vehicle\_runtime\_fuel.get(p\_name, fuel);



&#x20;           // Calcula distância percorrida neste intervalo

&#x20;           double dist = get\_distance(last\_x, last\_y, p.x, p.y);

&#x20;           

&#x20;           // Subtrai combustível baseado no tipo de veículo (moto gasta menos que helicóptero)

&#x20;           fuel -= (vehicle\_fuel\_cost\_per\_tile(vtype) \* dist);



&#x20;           // Se a gasolina acabou no meio do caminho

&#x20;           if(fuel <= 0) {

&#x20;               fuel = 0;

&#x20;               send\_reliable\_text(p.peer\_id, "play\_stationary engine\_fail.ogg", 0);

&#x20;               send\_reliable\_text(p.peer\_id, "say \[Veículos] O motor morreu. A GASOLINA ACABOU!", 0);

&#x20;               cmd\_sair(p\_idx); // Ejeta o jogador do veículo

&#x20;               continue;

&#x20;           }



&#x20;           // Atualiza os dados para o próximo cálculo

&#x20;           vehicle\_runtime\_fuel.set(p\_name, fuel);

&#x20;           vehicle\_last\_x.set(p\_name, p.x);

&#x20;           vehicle\_last\_y.set(p\_name, p.y);



&#x20;           // Emite o som do motor "acelerando" em 3D para quem estiver perto ouvir o carro passando!

&#x20;           server\_broadcast("play\_body engine\_drive.ogg " + p.x + " " + p.y, p.map, "" + p.peer\_id);

&#x20;       }

&#x20;   }

}

```



\### Passo 2: Os Comandos dos Jogadores (`commands.nvgt`)



Para que o jogador consiga usar tudo isso que fizemos, abra o seu arquivo \*\*`server/includes/commands.nvgt`\*\* e adicione os comandos de chat apontando para as novas funções:



```cpp

// Comando /entrar (Ex: /entrar moto)

bool cmd\_entrar(player@ player, string\[] args) {

&#x20;   if(args.length() < 1) {

&#x20;       player.send\_message("say Uso: /entrar <tipo> (ex: moto, carro, lancha)");

&#x20;       return false;

&#x20;   }

&#x20;   int p\_index = get\_player\_index\_from(player.charname);

&#x20;   cmd\_entrar(p\_index, args);

&#x20;   return true;

}



// Comando /sair

bool cmd\_sair\_veiculo(player@ player, string\[] args) {

&#x20;   int p\_index = get\_player\_index\_from(player.charname);

&#x20;   cmd\_sair(p\_index);

&#x20;   return true;

}



// Comando /abastecer

bool cmd\_abastecer\_veiculo(player@ player, string\[] args) {

&#x20;   int p\_index = get\_player\_index\_from(player.charname);

&#x20;   cmd\_abastecer(p\_index);

&#x20;   return true;

}

```



\*(Não esqueça de registrá-los caso você use aquele sistema de `register\_command("entrar", ...)` que vi no seu `commands.txt`)\*



\### Passo 3: Ativando a Chave de Ignição



Abra o arquivo principal \*\*`server.nvgt`\*\* (no `tprincipais` ou `main\_loop`) e certifique-se de que o motor global esteja girando:



```cpp

&#x20;   vehicles\_loop(); // O motor global que processa a queima de combustível

```



\### O Círculo Completo Está Formado! 🏁



1\. Você compra a `"moto"` na Loja.

2\. Digita `/entrar moto`. O servidor valida a sua propriedade, escuta o estampido da partida, e deixa você "dirigir". 

3\. Você passa a andar muito mais rápido no seu cliente.

4\. A cada \*Tile\* que você pisa, o `vehicles\_loop()` calcula a distância 2D e chupa uma gota do tanque. Se outros jogadores estiverem perto, eles ouvem o motor pelo \*Steam Audio\* (HRTF 3D) vindo na direção deles.

5\. Se secar, o motor engasga e você é ejetado! Precisa ir caminhando até a Loja, comprar "gasolina" com moedas (economia girando!), voltar até o carro e dar `/abastecer`.



\---



🎉 \*\*PARABÉNS ÉPICOS!\*\* 🎉



