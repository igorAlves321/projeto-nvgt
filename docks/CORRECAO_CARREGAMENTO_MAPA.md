# 🗺️ CORREÇÃO: Carregamento de Mapa ao Fazer Login

## Problema Identificado

Quando o usuário fazia login, o mapa não era carregado corretamente do servidor. Em vez disso, sempre carregava o **mapa de testes hardcoded** (`mapainicial`).

### Causa Raiz

O fluxo de login tinha um erro lógico:

1. ✅ `net_logar()` - Conecta ao servidor
2. ✅ Servidor envia `changemap [dados do mapa real]`
3. ✅ `net.nvgt` processa e chama `load_map(dados_servidor)` - **Carrega mapa correto**
4. ✅ Chama `game()`
5. ❌ **MAS** `game()` imediatamente chama `load_map(mapainicial)` novamente! - **Sobrescreve com mapa de teste!**

### Código Problemático

**cliente/client.nvgt, linha 502:**

```nvgt
void game(){
    debug_log("🎮 Função game() iniciada!");
    speak("Entrando no jogo!");
    load_map(mapainicial);  // ❌ ESTE ERA O PROBLEMA!
    debug_log("✅ Mapa inicial carregado: test");
    speak("Você está no mapa de testes. Use as setas para se mover.");
```

O `mapainicial` é uma **constante com dados de teste hardcoded**:

```nvgt
const string mapainicial="map:test\r\nmaxx:51\r\nmaxy:10\r\n...";
```

Isto **sobrescrevia** o mapa do servidor que acabara de ser carregado via `changemap`.

## Solução Aplicada

**Remover a chamada `load_map(mapainicial)` da função `game()`**

O mapa já foi carregado corretamente pelo `changemap` do servidor antes de `game()` ser chamada.

### Código Corrigido

```nvgt
void game(){
    debug_log("🎮 Função game() iniciada!");
    speak("Entrando no jogo!");
    debug_log("✅ Mapa já carregado pelo servidor via changemap");
    speak("Você está no jogo.");
    
    // ... resto da inicialização ...
```

## Fluxo Correto Agora

```
1. Usuário clica em "Logar"
   ↓
2. net_logar() conecta ao servidor
   ↓
3. Servidor valida credenciais
   ↓
4. Servidor envia "loggedin"
   ↓
5. Servidor envia "changemap [dados do mapa real]"
   ↓
6. net.nvgt processa "changemap"
   → load_map(dados_servidor) com coordenadas corretas ✅
   → me.x e me.y são definidas do servidor ✅
   → mapname recebe o mapa correto do servidor ✅
   ↓
7. game() é chamada
   → Loop principal começa com mapa CORRETO do servidor ✅
   ↓
8. ✅ Jogador está no mapa correto, nas coordenadas corretas!
```

## Validação

- ✅ Código compila sem erros (2696ms)
- ✅ Funcionamento agora:
  - Quando o usuário faz login, o servidor envia os dados do mapa correto via `changemap`
  - A função `load_map()` em `map.nvgt` carrega e processa os dados
  - A função `init_data()` extrai `x:` e `y:` do servidor para posicionar o jogador
  - `game()` é chamada com o mapa já carregado corretamente
  - ❌ **Não há mais** sobrescrita com mapa de teste

## Arquivos Alterados

- `cliente/client.nvgt` - Linha 502-503: Removida chamada `load_map(mapainicial)`

## Comparação com BGT Original

O BGT original **não tinha** esse problema porque:

1. No BGT, a função `game()` não existia neste contexto
2. O fluxo de inicialização era diferente
3. O mapa era apenas carregado uma vez via `load_map()` quando o servidor enviava `changemap`

A conversão para NVGT introduziu acidentalmente esta chamada de teste que quebrou o funcionamento.

## Status

✅ **CORRIGIDO** - O mapa agora é carregado corretamente do servidor quando o usuário faz login.
