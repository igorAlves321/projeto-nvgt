# 🚪 Análise: Comando `dr` (Door - Porta) Faltando

## Problema

O comando `dr` não tem handler em `map.nvgt`, causando erro "Invalid syntax" para todos os comandos de porta.

## Formato do Comando

**Exemplo do servidor**:
```
dr:1:0:2:0:200:none:none:door17open.ogg:door15close.ogg
```

**Parsing**:
| Índice | Valor | Descrição |
|--------|-------|-----------|
| 0 | `dr` | Comando (door abreviado) |
| 1 | `1` | X inicial da porta |
| 2 | `0` | Y inicial da porta |
| 3 | `2` | X final (destino) |
| 4 | `0` | Y final (destino) |
| 5 | `200` | Velocidade de movimento |
| 6 | `none` | Som 1 (pode ser "none") |
| 7 | `none` | Som 2 (pode ser "none") |
| 8 | `door17open.ogg` | Som ao abrir |
| 9 | `door15close.ogg` | Som ao fechar |

**Total: 10 elementos** (índices 0-9)

## Função Esperada

```nvgt
void spawn_door(int doorx, int doory, int finishx, int finishy, int velocidade, 
                string doorsnd, string doorsnd2, string doorsnd3, string doorsnd4)
```

## Implementação em BGT (Referência)

```bgt
else if(parsed[0]=="dr" and parsed.length()>=9||parsed[0]=="porta"&&parsed.length()>=9){
    int x=string_to_number(parsed[1]);
    int y=string_to_number(parsed[2]);
    int fx=string_to_number(parsed[3]);
    int fy=string_to_number(parsed[4]);
    int speed=string_to_number(parsed[5]);
    string snd1=parsed[6];
    string snd2=parsed[7];
    string snd3=parsed[8];
    string snd4=parsed[9];
    spawn_door(x, y, fx, fy,speed,snd1,snd2,snd3,snd4);
}
```

## Impacto

**Erros Encontrados**:
```
map error. An error has occured. Line: dr:20:0:22:0:200:none:none:door26open.ogg:door26close.ogg
. Error: Invalid syntax.
```

**Mapas Afetados**: Todos os mapas com portas (praticamente todos)

**Prioridade**: 🔴 CRÍTICA

## Solução

Adicionar handler para `dr` em `map.nvgt` com suporte para:
- Comando: `dr` ou `porta`
- Mínimo 10 elementos no array
- Tradução correta de índices
- Chamada a `spawn_door()`

