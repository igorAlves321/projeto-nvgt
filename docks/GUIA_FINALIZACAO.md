# 🎯 GUIA PRÁTICO DE FINALIZAÇÃO - EVM NVGT

**Objetivo:** Completar os últimos 5% do projeto e lançar versão beta  
**Tempo Estimado:** 3-7 dias  
**Desenvolvedor:** igorAlves321

---

## 📋 **PASSO A PASSO - DIA A DIA**

### **DIA 1: CORREÇÕES CRÍTICAS** ⚡

#### **Manhã (3-4 horas): Sistema de Guardas**

1. **Analisar arquivo BGT original**
   ```bash
   # Abrir para referência
   code "docks/para claude.txt"  # Se tiver código BGT dos guardas
   
   # Verificar arquivo desabilitado
   code "server/includes/guarda.nvgt.bak"
   ```

2. **Identificar problemas de conversão**
   - Verificar sintaxe NVGT
   - Checar dependências (functions, classes)
   - Validar lógica de IA dos guardas

3. **Corrigir e testar**
   ```bash
   # Renomear de .bak para .nvgt
   mv "server/includes/guarda.nvgt.bak" "server/includes/guarda.nvgt"
   
   # Descomentar include no server.nvgt:78
   # De: # #include "includes/guarda.nvgt"
   # Para: #include "includes/guarda.nvgt"
   
   # Testar compilação
   nvgt -c server.nvgt
   ```

#### **Tarde (2-3 horas): Login e Autenticação**

4. **Expandir sistema de login**
   ```nvgt
   // Em server/includes/auth.nvgt
   
   // TODO: Implementar verificação de ban (linha 128)
   bool is_player_banned(string player_name) {
       if(!database_initialized || bancoJogo is null) return false;
       
       string query = "SELECT COUNT(*) FROM banned_players WHERE player_name = ? AND active = 1";
       sqlite3statement@ stmt = bancoJogo.prepare(query);
       
       if(stmt !is null) {
           stmt.bind_text(1, player_name);
           if(stmt.step() == SQLITE_ROW) {
               return stmt.column_int(0) > 0;
           }
       }
       
       return false;
   }
   
   // TODO: Implementar sistema de login completo (server.nvgt:474)
   void handle_login(uint64 peer_id, string username, string password) {
       // 1. Verificar se player está banido
       if(is_player_banned(username)) {
           send_reliable(peer_id, "msg Você foi banido do servidor!");
           network.disconnect_peer(peer_id);
           return;
       }
       
       // 2. Verificar credenciais
       if(!verify_credentials(username, password)) {
           send_reliable(peer_id, "msg Usuário ou senha incorretos!");
           return;
       }
       
       // 3. Carregar jogador do database
       player@ p = load_player_from_database(username);
       if(p is null) {
           send_reliable(peer_id, "msg Erro ao carregar dados do jogador!");
           return;
       }
       
       // 4. Adicionar ao array de players
       p.peer_id = peer_id;
       p.online = true;
       players.push_back(p);
       
       // 5. Notificar sucesso
       send_reliable(peer_id, "msg Bem-vindo(a), " + username + "!");
       update_statistics("login");
       log_action(username, "login", "Login bem-sucedido", p.map_name, p.x, p.y, p.z);
   }
   ```

5. **Testar autenticação**
   ```bash
   # Compilar
   nvgt -c server.nvgt
   
   # Criar usuário de teste no database (se necessário)
   sqlite3 server/database/game.db
   > INSERT INTO players (username, password_hash, ...) VALUES (...);
   ```

---

### **DIA 2: FEATURES E REFINAMENTOS** 🔧

#### **Manhã (2-3 horas): Sistema de Equipamentos**

6. **Expandir sistema de combate**
   ```nvgt
   // Em server/includes/combat.nvgt:162
   
   // Substituir TODO por implementação real
   
   // Estrutura de equipamento
   class Equipment {
       string slot; // head, chest, legs, feet, weapon, shield
       GameItem@ item;
       int durability;
       int max_durability;
       
       Equipment(string slot_type, GameItem@ equipped_item) {
           slot = slot_type;
           @item = equipped_item;
           durability = 100;
           max_durability = 100;
       }
       
       int get_defense_bonus() {
           if(item is null || durability <= 0) return 0;
           return item.defense * (durability / max_durability);
       }
       
       int get_attack_bonus() {
           if(item is null || durability <= 0) return 0;
           return item.damage * (durability / max_durability);
       }
       
       void reduce_durability(int amount = 1) {
           durability -= amount;
           if(durability < 0) durability = 0;
       }
   }
   
   // Adicionar na classe player (player.nvgt)
   dictionary equipment; // slot_name => Equipment@
   
   // Funções de gerenciamento
   bool equip_item(player@ player, string slot, GameItem@ item) {
       Equipment@ eq = Equipment(slot, item);
       player.equipment[slot] = @eq;
       return true;
   }
   
   int get_total_defense(player@ player) {
       int total = player.player_level + 5;
       
       // Adicionar defesa de equipamentos
       string[] slots = player.equipment.get_keys();
       for(uint i = 0; i < slots.length(); i++) {
           Equipment@ eq = cast<Equipment@>(player.equipment[slots[i]]);
           if(eq !is null) {
               total += eq.get_defense_bonus();
           }
       }
       
       return total;
   }
   
   // Atualizar calculate_damage para usar equipamentos
   int calculate_damage(string attacker_id, string defender_id, string weapon_type = "") {
       player@ attacker = get_player_by_id(attacker_id);
       player@ defender = get_player_by_id(defender_id);
       
       if(attacker is null || defender is null) return 0;
       
       // Damage base
       int base_damage = attacker.player_level * 2 + 10;
       
       // ✅ NOVO: Adicionar bônus de arma equipada
       if(attacker.equipment.exists("weapon")) {
           Equipment@ weapon = cast<Equipment@>(attacker.equipment["weapon"]);
           if(weapon !is null) {
               base_damage += weapon.get_attack_bonus();
           }
       }
       
       // ✅ NOVO: Defesa total do defensor (incluindo equipamentos)
       int defense = get_total_defense(defender);
       
       // Calcular damage final
       int final_damage = base_damage - defense;
       if(final_damage < 1) final_damage = 1;
       
       // Crítico, variação, etc (já implementado)
       // ...
       
       return final_damage;
   }
   ```

#### **Tarde (2 horas): Comando /time**

7. **Implementar tracking de tempo online**
   ```nvgt
   // Em server/includes/player.nvgt
   
   class player {
       // ... propriedades existentes ...
       
       // ✅ NOVO: Tracking de tempo
       uint64 session_start_time;
       uint64 total_playtime_seconds; // Carregado do database
       
       // Método para calcular tempo da sessão atual
       uint64 get_current_session_time() {
           return (get_time_stamp() - session_start_time) / 1000; // em segundos
       }
       
       // Método para obter tempo total de jogo
       uint64 get_total_playtime() {
           return total_playtime_seconds + get_current_session_time();
       }
       
       // Formatar tempo como string legível
       string get_playtime_formatted() {
           uint64 total_seconds = get_total_playtime();
           
           uint64 days = total_seconds / 86400;
           uint64 hours = (total_seconds % 86400) / 3600;
           uint64 minutes = (total_seconds % 3600) / 60;
           uint64 seconds = total_seconds % 60;
           
           string result = "";
           if(days > 0) result += days + " dias, ";
           if(hours > 0) result += hours + " horas, ";
           if(minutes > 0) result += minutes + " minutos, ";
           result += seconds + " segundos";
           
           return result;
       }
   }
   
   // Em server/includes/commands.nvgt:431
   
   // Substituir TODO por implementação real
   bool cmd_time(player@ player, string[] args) {
       string time_info = "=== TEMPO DE JOGO ===\\r\\n";
       time_info += "Sessão Atual: " + player.get_current_session_time() + " segundos\\r\\n";
       time_info += "Tempo Total: " + player.get_playtime_formatted() + "\\r\\n";
       time_info += "\\r\\n";
       time_info += "Servidor Online: " + ups() + " segundos";
       
       send_reliable(player.peer_id, "say " + time_info);
       return true;
   }
   
   // Adicionar comando ao sistema
   // Em server/includes/commands.nvgt (no registro de comandos)
   command_registry["time"] = @cmd_time;
   ```

8. **Atualizar database para salvar playtime**
   ```sql
   -- Adicionar coluna na tabela players (se não existir)
   ALTER TABLE players ADD COLUMN total_playtime_seconds INTEGER DEFAULT 0;
   
   -- Atualizar ao salvar jogador
   UPDATE players 
   SET total_playtime_seconds = ? 
   WHERE id = ?;
   ```

---

### **DIA 3: COMPILAÇÃO E TESTES** 🧪

#### **Manhã (2-3 horas): Compilação Completa**

9. **Resolver erros de compilação**
   ```bash
   # Compilar servidor
   cd server
   nvgt -c server.nvgt
   
   # Se houver erros:
   # 1. Ler mensagem de erro cuidadosamente
   # 2. Localizar arquivo e linha do erro
   # 3. Corrigir sintaxe/lógica
   # 4. Repetir até compilar sem erros
   
   # Compilar cliente (se ainda não compilado)
   cd ../client
   nvgt -c client.nvgt
   ```

10. **Verificar dependências**
    ```bash
    # Verificar se todas as DLLs necessárias estão presentes
    cd server
    ls lib/  # ou dir lib\ no Windows
    
    # Deve ter:
    # - bass.dll
    # - bassmix.dll
    # - bass_fx.dll
    # - phonon.dll (para áudio 3D)
    # - sqlite3.dll (se necessário)
    ```

#### **Tarde (3-4 horas): Testes Funcionais**

11. **Smoke Tests**
    ```bash
    # Terminal 1: Iniciar servidor
    cd server
    ./server.exe  # ou server no Linux/Mac
    
    # Observar:
    # - Servidor inicia sem crashes
    # - Database conecta
    # - Porta de rede abre corretamente
    # - Mensagens de log aparecem
    
    # Terminal 2: Conectar cliente
    cd client
    ./client.exe
    
    # Testar:
    # 1. Criação de conta (se necessário)
    # 2. Login com credenciais
    # 3. Movimentação básica (WASD)
    # 4. Chat/mensagens
    # 5. Comandos básicos (/help, /time)
    ```

12. **Teste de Database**
    ```bash
    # Conectar ao database
    sqlite3 server/database/game.db
    
    # Verificar dados salvos
    > SELECT * FROM players LIMIT 5;
    > SELECT COUNT(*) FROM game_history;
    > SELECT * FROM combat_logs ORDER BY timestamp DESC LIMIT 10;
    
    # Verificar integridade
    > PRAGMA integrity_check;
    ```

13. **Teste de Combate**
    ```bash
    # No cliente (como admin):
    /spawn_item sword 1 0 0
    /spawn_item health_potion 2 0 0
    
    # Coletar items
    # Equipar espada (comando de equip)
    
    # Iniciar combate contra NPC (se disponível)
    # ou outro jogador (se PvP habilitado)
    
    # Verificar:
    # - Damage calculado corretamente
    # - HP atualiza
    # - Combate loga no database
    # - XP/gold ganha ao vencer
    ```

---

### **DIA 4-5: POLIMENTO E FEATURES OPCIONAIS** ✨

#### **Threading/Async (Opcional)**

14. **Implementar async para operações longas**
    ```nvgt
    // Quando sintaxe async<> for confirmada/disponível
    
    // Em server.nvgt
    
    // Exemplo: Backup assíncrono
    void perform_hourly_backup_async() {
        async<void> backup_task(perform_hourly_backup);
        // Continua execução enquanto backup roda em background
    }
    
    // Exemplo: Cleanup de itens expirados
    void cleanup_expired_items_async() {
        async<void> cleanup_task(cleanup_expired_world_items);
        // Não bloqueia servidor
    }
    ```

#### **Funcionalidades Avançadas**

15. **Cópia de arquivos para admin** (se NVGT suportar)
    ```nvgt
    // Em admin_commands.nvgt:134
    
    // Se NVGT adicionar file_copy():
    bool cmd_copyfile(player@ player, string[] args) {
        if(args.length() < 2) {
            player.send_message("Uso: /copyfile <origem> <destino>");
            return false;
        }
        
        string source = args[0];
        string dest = args[1];
        
        if(file_copy(source, dest)) {
            player.send_message("Arquivo copiado com sucesso!");
            return true;
        } else {
            player.send_message("Erro ao copiar arquivo!");
            return false;
        }
    }
    
    // Se não suportar, usar workaround:
    bool cmd_copyfile(player@ player, string[] args) {
        // Ler arquivo fonte
        string content = file_get_contents(args[0]);
        
        // Escrever em destino
        file f;
        if(f.open(args[1], "wb")) {
            f.write(content);
            f.close();
            player.send_message("Arquivo copiado!");
            return true;
        }
        
        return false;
    }
    ```

---

### **DIA 6-7: TESTES EXTENSIVOS E DOCUMENTAÇÃO** 📖

#### **Testes de Carga e Performance**

16. **Simular múltiplos jogadores**
    ```bash
    # Criar script de teste (Python, por exemplo)
    # test_load.py
    
    import socket
    import threading
    
    def simulate_player(player_id):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Simular login, movimentação, etc
        # ...
    
    # Criar 10, 50, 100 jogadores simulados
    for i in range(100):
        t = threading.Thread(target=simulate_player, args=(i,))
        t.start()
    
    # Observar:
    # - Uso de CPU/RAM do servidor
    # - Tempo de resposta
    # - Database performance
    # - Network latency
    ```

17. **Testes de Estresse**
    ```bash
    # Testes de database
    # - 1000 saves consecutivos
    # - 10000 queries de histórico
    # - Backup com server em uso intenso
    
    # Testes de rede
    # - Envio de muitas mensagens simultâneas
    # - Conexões/desconexões rápidas
    # - Packet loss/lag simulation
    
    # Testes de gameplay
    # - Spawnar 1000 items
    # - 100 NPCs simultâneos
    # - Combates massivos (10+ jogadores)
    ```

#### **Documentação Final**

18. **Atualizar toda documentação**
    ```markdown
    # README.md
    - Status: 100% Completo
    - Features implementadas
    - Guia de instalação
    - Guia de uso
    - Comandos disponíveis
    
    # CHANGELOG.md
    - Todas as mudanças BGT → NVGT
    - Features adicionadas
    - Bugs corrigidos
    - Breaking changes
    
    # CONTRIBUTING.md
    - Como contribuir
    - Code style
    - Pull request process
    
    # API_REFERENCE.md
    - Todas as funções públicas
    - Classes e métodos
    - Database schema
    - Network protocol
    ```

---

## 🎯 **CHECKLIST DE ENTREGA**

### **Antes de Lançar Beta:**

- [ ] ✅ Todos os TODOs resolvidos ou documentados
- [ ] ✅ Compilação sem erros/warnings
- [ ] ✅ Servidor inicia sem crashes
- [ ] ✅ Cliente conecta e joga normalmente
- [ ] ✅ Database funciona (save/load)
- [ ] ✅ Sistema de combate testado
- [ ] ✅ Sistema de items testado
- [ ] ✅ Comandos admin testados
- [ ] ✅ Auto-save funciona
- [ ] ✅ Backups funcionam
- [ ] ✅ Performance aceitável (50+ players simultâneos)
- [ ] ✅ Documentação atualizada
- [ ] ✅ README com instruções claras
- [ ] ✅ Changelog completo

### **Opcional (Para Lançamento Final):**

- [ ] ⭐ Threading/async implementado
- [ ] ⭐ Sistema de equipamentos avançado
- [ ] ⭐ Testes de carga (100+ players)
- [ ] ⭐ Logs de erro detalhados
- [ ] ⭐ Sistema de crash recovery
- [ ] ⭐ Monitoring/analytics dashboard

---

## 🚀 **COMANDO RÁPIDO - DIA 1**

Se você quiser começar **AGORA**, execute isto:

```bash
# 1. Corrigir guardas
mv "server/includes/guarda.nvgt.bak" "server/includes/guarda.nvgt"

# 2. Editar server.nvgt linha 78
# Descomentar: #include "includes/guarda.nvgt"

# 3. Compilar
cd server
nvgt -c server.nvgt

# 4. Se compilar com sucesso, iniciar servidor
./server.exe

# 5. Em outro terminal, testar cliente
cd ../client
./client.exe
```

---

## 📞 **PRECISA DE AJUDA?**

**Perguntas? Dúvidas? Problemas?**

1. Consulte `Doc NVGT.txt` para referências da API
2. Veja `FUNCOES_NAO_IMPLEMENTADAS.md` para detalhes técnicos
3. Leia `STATUS_FINAL.md` para visão geral do projeto
4. Abra uma issue no GitHub
5. Peça ajuda na comunidade NVGT

---

**🎊 BOA SORTE NA FINALIZAÇÃO! VOCÊ ESTÁ QUASE LÁ! 🎊**

**95% completo → 100% completo = 3-7 dias de trabalho focado!**

---

**Última Atualização:** 3 de outubro de 2025  
**Autor:** Claude AI + igorAlves321  
**Licença:** GNU General Public License v2
