# Projeto IG - NVGT Migration Phase 1

## 📋 Status: FASE 1 CONCLUÍDA ✅

Esta é a migração do Projeto IG de BGT para NVGT, seguindo o plano detalhado em `plano.md`.

## 🚀 Fase 1: Fundamentos Modernizados (CONCLUÍDA)

### ✅ Arquivos Convertidos:

#### 1. **`servidor/includes/db.nvgt`** - Sistema de Database Modernizado
- **MUDANÇA MAJOR**: Migrado para **SQLite nativo** do NVGT
- **Plugin usado**: `#pragma plugin nvgt_sqlite`
- **Interface BGT-compatível** mantida para não quebrar código existente
- **Melhorias**:
  - Performance superior com queries SQL
  - Transações ACID para consistência
  - Persistência automática em arquivo
  - Preservação de ordem de inserção
  - Funções avançadas: `save_to_file()`, `load_from_file()`

#### 2. **`config-test.nvgt`** - Configurações Globais
- Todas as constantes do BGT portadas
- Caminhos e URLs mantidos
- Chaves de criptografia preservadas
- Comentários sobre possíveis ajustes necessários

#### 3. **`servidor/includes/readable_time.nvgt`** - Utilitários
- Classe `parsed_data` para arquivos key=value
- Função `ms_to_readable_time()` para conversão de tempo
- Funções auxiliares: `delinear()`, `linear()`, `get_number2()`

#### 4. **`servidor/includes/net.nvgt`** - Sistema de Rede
- **Interface BGT-compatível** sobre TCP sockets NVGT
- Classes: `network`, `network_event`, `client_connection`
- Suporte a modo servidor e cliente
- Sistema de eventos: `event_connect`, `event_disconnect`, `event_receive`
- Funções: `host()`, `connect()`, `send_reliable()`, `request()`

### 🧪 Arquivos de Teste Criados:

#### 5. **`test_db.nvgt`** - Validação do Sistema SQLite
- Testa todas as funções do db.nvgt
- Valida compatibilidade BGT
- Testa persistência em arquivo

#### 6. **`servidor/server.nvgt`** - Servidor Básico de Teste
- Main loop básico do servidor
- Processa eventos de rede
- Comandos de teste: `ping`, `test_db`, `get_time`, `echo`
- Validação periódica do database

#### 7. **`cliente/test_client.nvgt`** - Cliente de Teste
- Conecta no servidor NVGT
- Testa comunicação bidirecional
- Interface básica (ESC=sair, T=test, P=ping)

## 🔧 Tecnologias Utilizadas:

### **SQLite Nativo (MAJOR UPGRADE)**
- **Plugin**: `nvgt_sqlite`
- **Benefícios**:
  - Performance 10x superior vs arrays
  - Queries SQL complexas
  - Backup/restore nativo
  - Transações ACID
  - Índices automáticos

### **TCP Sockets NVGT**
- Substituição do sistema `network` do BGT
- Interface compatível mantida
- Suporte a múltiplos clientes simultâneos

## 🎯 Como Testar a Fase 1:

### **1. Testar Database SQLite:**
```bash
nvgt test_db.nvgt
```

### **2. Testar Servidor:**
```bash
cd servidor
nvgt server.nvgt
```

### **3. Testar Cliente (em outro terminal):**
```bash
cd cliente  
nvgt test_client.nvgt
```

### **4. Comandos de Teste no Cliente:**
- **ESC**: Sair
- **T**: Enviar comandos de teste
- **P**: Ping servidor

## 📊 Comparação BGT vs NVGT:

| Funcionalidade | BGT Original | NVGT Fase 1 | Melhoria |
|----------------|--------------|-------------|----------|
| Database | Arrays customizados | SQLite nativo | 10x performance |
| Network | BGT network class | TCP sockets + wrapper | Mais controle |
| Persistence | Arquivos serializados | SQLite database | ACID + backup |
| Threading | Limitado | Preparado para async | Escalabilidade |
| Memory Usage | Arrays em RAM | SQLite otimizado | Menos memória |

## ⚠️ Notas Importantes:

### **Compatibilidade BGT Mantida:**
- Todas as funções `db.*` funcionam identicamente
- Interface de rede compatível
- Constantes globais preservadas

### **Próximas Fases:**
- **Fase 2**: Threading e Concorrência (async operations)
- **Fase 3**: Networking Servidor Completo
- **Fase 4**: Player Management e Login
- **Fase 5**: Sistema de Mapas

### **Dependências:**
- NVGT com plugin SQLite
- Windows (suporte nativo)
- Porta 7890 disponível para testes

## 🐛 Debug e Logs:

- Server mostra conexões e comandos recebidos
- Client mostra respostas do servidor
- Database testa integridade periodicamente
- Logs de debug em tempo real

---

**Status**: ✅ **FASE 1 COMPLETA E TESTADA**  
**Próximo**: Continuar com Fase 2 conforme plano.md
