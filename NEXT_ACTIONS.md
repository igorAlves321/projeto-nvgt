# Próximas Ações - Migração BGT→NVGT

## Status Atual ✅

### Fase 1 Concluída - Fundamentos
- [x] `db.nvgt` - Database customizada funcionando
- [x] `config-test.nvgt` - Sistema de configuração global
- [x] `readable_time.nvgt` - Utilitários de tempo
- [x] `net.nvgt` - Wrapper básico TCP sobre NVGT
- [x] `server.nvgt` - Entry point do servidor
- [x] Testes básicos validados

## 🔍 Descoberta Importante

### Capacidades Nativas do NVGT Identificadas
1. **SQLite Plugin** (`nvgt_sqlite`) - Database nativo
2. **Threading Robusto** - async<T>, mutex, atomic operations
3. **Concorrência** - Primitives para operações assíncronas

## 🎯 Próximas Ações (Ordem de Prioridade)

### 1. Pesquisa e Avaliação Técnica (1-3 dias)

#### 1.1 SQLite Plugin Investigation
- [ ] **Pesquisar documentação detalhada** do plugin nvgt_sqlite
- [ ] **Criar POC** comparando SQLite vs. db.nvgt atual
- [ ] **Benchmark performance** para datasets típicos do jogo
- [ ] **Avaliar esforço** de migração dos dados atuais

```bash
# Arquivos para teste
projeto nvgt/tests/sqlite_poc.nvgt
projeto nvgt/tests/performance_comparison.nvgt
```

#### 1.2 Threading Investigation  
- [ ] **Testar async<T>** para operações de rede
- [ ] **Implementar POC** de NetworkManager assíncrono
- [ ] **Validar thread safety** em cenários típicos
- [ ] **Medir performance** gain de operações async

```bash
# Arquivos para teste
projeto nvgt/tests/async_networking_poc.nvgt
projeto nvgt/tests/threading_validation.nvgt
```

### 2. Decisão Arquitetural (1-2 dias)

#### 2.1 Database Strategy Decision
**Análise requerida**:
- Complexidade atual dos dados (arrays simples vs. relacional)
- Volume de dados típico no jogo
- Frequência de queries complexas
- Benefit/cost ratio da migração

**Outcomes possíveis**:
- **Opção A**: Migrar para SQLite (performance + features)
- **Opção B**: Manter db.nvgt (simplicidade + compatibility)
- **Opção C**: Híbrido (config→SQLite, cache→arrays)

#### 2.2 Threading Strategy Decision
**Análise requerida**:
- Bottlenecks atuais no networking
- Benefício real de async operations
- Complexidade de implementação thread-safe

**Outcome esperado**: **Migrar para async** (alto benefício, baixo risco)

### 3. Implementação (Dependente das decisões)

#### 3.1 Se Decisão = Manter Atual + Melhorias Pontuais
- [ ] **Otimizar db.nvgt** com melhor indexing
- [ ] **Async wrapper** para operações de rede críticas
- [ ] **Continuar Fase 2** do plano original

#### 3.2 Se Decisão = Modernização Arquitetural
- [ ] **Fase 2 NOVA**: Database Modernization 
- [ ] **Fase 3 NOVA**: Threading Modernization
- [ ] **Fase 4 MODIFICADA**: Networking com async

### 4. Testes e Validação (Contínuo)
- [ ] **Benchmarks** comparativos
- [ ] **Load testing** com múltiplos clientes
- [ ] **Stress testing** de threading
- [ ] **Backward compatibility** testing

## 📁 Arquivos de Trabalho Sugeridos

### Estrutura de Testes
```
projeto nvgt/
├── tests/
│   ├── sqlite_poc.nvgt              # POC SQLite vs arrays
│   ├── async_networking_poc.nvgt    # POC async operations
│   ├── performance_benchmarks.nvgt  # Comparações quantitativas
│   └── compatibility_tests.nvgt     # Validação BGT compatibility
├── modernized/                      # Versões modernizadas
│   ├── database_manager.nvgt        # SQLite implementation
│   ├── async_network_manager.nvgt   # Async networking
│   └── threading_utilities.nvgt     # Thread helpers
└── migration/                       # Ferramentas de migração
    ├── data_migrator.nvgt           # Arrays → SQLite
    └── compatibility_layer.nvgt     # BGT → NVGT adapters
```

## 🚦 Critérios de Decisão

### Para SQLite Migration
**Migrar se**:
- Performance gain > 20%
- Dados relacionais complexos
- Necessidade de queries avançadas
- Esforço de migração < 1 semana

**Manter arrays se**:
- Dados simples (key-value apenas)
- Performance atual adequada
- Timeline apertado

### Para Threading Modernization
**Implementar async se**:
- Operações de rede são bottleneck
- Múltiplos clientes simultâneos
- Responsividade é crítica

## 📅 Timeline Sugerido

### Semana Atual
- [ ] **Dias 1-2**: SQLite research + POC
- [ ] **Dias 3-4**: Threading research + POC  
- [ ] **Dia 5**: Decisões arquiteturais

### Próxima Semana
- [ ] **Implementação** baseada nas decisões
- [ ] **Testes** de performance e compatibility
- [ ] **Documentação** das mudanças

## 🎯 Objetivo Final

**Resultado esperado**: Arquitetura modernizada que aproveita capacidades nativas do NVGT mantendo compatibilidade com o sistema existente.

**Success criteria**:
- Performance igual ou superior
- Código mais limpo e maintível  
- Threading robusto para escalabilidade
- Backward compatibility preservada

## 📞 Support Resources

- **NVGT Documentation**: https://nvgt.gg/docs/
- **Community Discord**: Para dúvidas específicas
- **Source Examples**: Tests em NVGT repo
- **BGT Compatibility**: bgt_compat.nvgt include

---

**Next Action**: Começar com SQLite POC para avaliar viabilidade técnica.
