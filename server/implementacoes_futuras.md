# Implementações Futuras - EVM Server NVGT

## Status da Compilação
✅ **O servidor compila com sucesso!**
- Compilado em: 2.7 segundos
- Executável gerado: `server.zip`

---

## 🔴 Implementações Críticas (Alta Prioridade)

### 1. Sistema de NPCs
**Localização:** `server_map.nvgt` linhas 1256, 1278

**Problema:** Construtor NPC não compatível com npc_data

**O que fazer:**
- Criar construtor adicional na classe `npc` (placeholder_classes.nvgt) que aceite 26 parâmetros vindos de `npc_data`
- Assinatura necessária:
```nvgt
npc(int x, int y, int vida, int xp, int distanciaataques,
    int danoquerecibira, int danoquedara, int danodelespejo,
    int tiempoparaatacar, int tiempoparacaminar, int tiempodelossonidos,
    string itemsadar, string sonidoataque, string sonidonervioso,
    string sonidomuerte, string nombrenpc, string msgmuerte,
    int tiempoaparicion, bool enablerespawn, bool enablebombs,
    string map, string pasosnpc, int left_range, int right_range,
    string impactosbala, string degradation)
```

**Impacto:** NPCs não spawnam (respawn desabilitado temporariamente)

---

### 2. Sistema de Armas (Weapons)
**Localização:** `server_map.nvgt` linhas 886, 915, 935, 1032, 1046

**Problema:** `weapons` retorna string ao invés de objeto weapon

**O que fazer:**
- Verificar se `weapons` é array de objetos ou array de strings
- Se for array de strings, criar/usar classe `weapon` apropriada
- Descomentar as linhas de som de impacto:
```nvgt
// Exemplo:
send_packet(5, "play_wall " + weapons[bullets[b].weapon - 1].sounds_impact[random(0, ...)] + ".ogg", x, y);
```

**Impacto:** Sons de impacto de balas não tocam em:
- Árvores
- Paredes
- NPCs
- Jogadores
- Terreno

---

### 3. Serialização de Timers
**Localização:** `server_map.nvgt` linhas 587, 639, 667, 729

**Problema:** NVGT não permite concatenar timer com string

**O que fazer:**
- Criar função para converter timer.elapsed para string
- Usar int para armazenar tempo ao invés de timer
- Exemplo:
```nvgt
// Solução 1: Usar elapsed
replace_line("arbol:" + x + ":" + y + ":" + trespawn.elapsed + "...");

// Solução 2: Armazenar int ao invés de timer
int trespawn_time = 5000; // ms
```

**Impacto:**
- Árvores não salvam estado de respawn no arquivo de mapa
- Paredes não salvam estado de respawn no arquivo de mapa

---

### 4. Sistema de Fogo Contínuo (Player Fire)
**Localização:** `player.nvgt` linha 2078

**Problema:** Método `spawn_playerfire()` está vazio

**O que fazer:**
- Implementar sistema de dano contínuo por fogo
- Criar timer para dano periódico
- Adicionar efeitos visuais/sonoros
- Sistema de cura/antídoto

**Impacto:** Bolas de fogo não causam dano contínuo aos jogadores

---

## 🟡 Implementações Importantes (Média Prioridade)

### 5. Sistema de Crafting
**Localização:** `crafting.nvgt` linhas 15, 21, 27, 33

**O que implementar:**
- `can_craft()` - Verificar se jogador tem itens para receita
- `craft()` - Executar crafting e remover itens
- `add_recipe()` - Adicionar novas receitas
- Carregar receitas de arquivo

**Impacto:** Sistema de crafting não funciona

---

### 6. Sistema de Autenticação
**Localização:** `auth.nvgt` linha 128

**O que implementar:**
- Verificação de ban no banco de dados
- Sistema de whitelist/blacklist
- Logs de tentativas de login

**Impacto:** Bans não são verificados no banco de dados

---

### 7. Sistema de Combate Avançado
**Localização:** `combat.nvgt` linha 162

**O que implementar:**
- Sistema de equipamentos com stats
- Bônus de armas/armaduras
- Multiplicadores de dano

**Impacto:** Sistema de equipamento não afeta combate

---

### 8. Comandos Administrativos
**Localização:** `commands.nvgt` linhas 337, 350, 397, 419, 426, 462, 702

**O que implementar:**
- `/playtime` - Mostrar tempo de jogo
- `/kick` - Desconexão graceful
- `/inventory` - Sistema de inventário
- `/freezeall` - Freeze global
- `/backup` - Sistema de backup
- `/forcedc` - Desconexão forçada
- Sistema de defesa temporária

**Impacto:** Comandos admin não funcionam completamente

---

## 🟢 Implementações Opcionais (Baixa Prioridade)

### 9. Sistema de Estatísticas
**Localização:** `stubs.nvgt` linhas 10, 16, 22

**O que implementar:**
- Tracking de kills/deaths/assistências
- Estatísticas por arma
- Rankings
- Histórico de ações

---

### 10. Sistema Temporal
**Localização:** `stubs.nvgt` linha 52

**O que implementar:**
- Ciclo dia/noite
- Eventos temporais
- Meteorologia

---

### 11. Sistema de Equipes
**Localização:** `stubs.nvgt` linha 120

**O que implementar:**
- Verificação de mesma equipe
- Chat de equipe
- Objetivos de equipe

---

### 12. Sistema de Arena
**Localização:** `stubs.nvgt` linha 168

**O que implementar:**
- Matchmaking
- Modos de jogo
- Recompensas
- Ranking

---

### 13. Sistema de Veículos
**Localização:** `server_map.nvgt` linha 107

**O que implementar:**
- Conversão da classe `vehicle` de BGT para NVGT
- Sistema de direção
- Dano de colisão
- Combustível

---

### 14. Sons Móveis 3D
**Localização:** `server_map.nvgt` linha 109

**O que implementar:**
- Sistema de som posicional 3D
- Sons em movimento
- Atenuação por distância

---

### 15. Zonas Desabilitadas (Game Disabled)
**Localização:** `globals.nvgt` linha 343, `server_map.nvgt` linha 114

**O que implementar:**
- Zonas onde jogos/combate são desabilitados
- Sistema de safe zones avançado

---

### 16. Sistema de Itens Magnéticos
**Localização:** `stubs.nvgt` linha 104

**O que implementar:**
- Itens que atraem outros itens
- Sistema de coleta automática
- Raio de atração configurável

---

### 17. Sistema de Experiência
**Localização:** `stubs.nvgt` linhas 76, 82

**O que implementar:**
- XP duplo em eventos
- Ganho de XP por ações
- Sistema de níveis
- Recompensas por nível

---

### 18. Gerenciamento de Variáveis
**Localização:** `var_management.nvgt` linha 240

**O que implementar:**
- Reload de configurações sem reiniciar
- Hot-reload de variáveis do jogador

---

### 19. Sistema de Inventário Completo
**Localização:** `items.nvgt` linha 458

**O que implementar:**
- Limites de peso/espaço
- Organização automática
- Transferência de itens entre jogadores

---

### 20. Sistema de Helicóptero
**Localização:** `helicoptero.nvgt` linha 67

**O que implementar:**
- Reimplementar `spawn_maxbomba`
- Sistema de bombardeio aéreo
- Controles de helicóptero

---

## 📊 Estatísticas do Projeto

### Arquivos Modificados Durante Conversão
- `server_map.nvgt` - Sistema de mapas (principal)
- `placeholder_classes.nvgt` - Classes temporárias
- `player.nvgt` - Sistema de jogadores
- `mina.nvgt` - Sistema de minas
- `portals.nvgt` - Sistema de portais
- `plasmabomb.nvgt` - Bombas de plasma
- `stubs.nvgt` - Funções temporárias
- `wall.nvgt` - Sistema de paredes
- `item.nvgt` - Sistema de itens

### TODOs por Categoria
- **Críticos:** 4 itens
- **Importantes:** 4 itens
- **Opcionais:** 16 itens
- **Total:** 24 implementações pendentes

---

## 🚀 Roadmap Sugerido

### Fase 1: Funcionalidade Básica (1-2 semanas)
1. ✅ Compilação bem-sucedida
2. ⬜ Sistema de NPCs funcionando
3. ⬜ Sistema de armas/sons de impacto
4. ⬜ Sistema de fogo contínuo

### Fase 2: Sistemas Core (2-3 semanas)
5. ⬜ Serialização de timers
6. ⬜ Sistema de crafting
7. ⬜ Comandos administrativos completos
8. ⬜ Sistema de autenticação/ban

### Fase 3: Features Avançadas (3-4 semanas)
9. ⬜ Sistema de veículos
10. ⬜ Sistema de arena
11. ⬜ Sistema de equipes
12. ⬜ Estatísticas e rankings

### Fase 4: Polish e Otimização (1-2 semanas)
13. ⬜ Sistema temporal
14. ⬜ Sons 3D
15. ⬜ Itens magnéticos
16. ⬜ Otimizações de performance

---

## 📝 Notas Importantes

### Limitações Conhecidas
1. **Timers não concatenam com strings** - Usar `.elapsed` ou converter para int
2. **Construtor NPC incompleto** - NPCs não spawnam automaticamente
3. **Array weapons não tipado** - Sons de impacto desabilitados
4. **Sistema de fogo vazio** - Bolas de fogo não causam DoT

### Padrões de Código
- Usar `timer` para contadores temporais
- Usar `int` para armazenar tempos em ms quando precisar serializar
- Usar ternário `(condition ? 1 : 0)` para converter bool → int
- Adicionar TODO com descrição clara para código incompleto

### Testes Recomendados
Após cada implementação, testar:
- [ ] Servidor inicia sem crashes
- [ ] Jogadores conseguem conectar
- [ ] Funcionalidade implementada funciona
- [ ] Não há memory leaks
- [ ] Performance aceitável

---

## 🔗 Referências

- **Documentação NVGT:** https://nvgt.gg/docs/
- **Código BGT Original:** `dockss/` (arquivos .bgt)
- **Erros de Compilação:** `compile_errors.txt`, `compile_final.txt`
- **Perguntas Respondidas:** `dockss/perguntas respondidas 2.txt`

---

**Última Atualização:** 2025-10-03
**Status:** Servidor compilando com sucesso, aguardando implementações
