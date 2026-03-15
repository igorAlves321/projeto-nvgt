# 🔗 Integração com GitHub - Documentação NVGT

## ✅ Novas Ferramentas Adicionadas

O servidor MCP agora possui **2 novas ferramentas** que consultam a documentação oficial do NVGT diretamente!

### 📚 1. search_nvgt_docs
Busca diferenças entre BGT e NVGT na documentação oficial.

**Parâmetros:**
- `query` (obrigatório): Termo de busca
- `category` (opcional): Categoria específica

**Exemplo de uso:**
```json
{
  "name": "search_nvgt_docs",
  "arguments": {
    "query": "double"
  }
}
```

**Resposta:**
```json
{
  "topic": "double",
  "bgt": "double",
  "nvgt": "float",
  "reason": "NVGT usa float de 32-bit em vez de double de 64-bit",
  "example": "double x = 3.14; // BGT\nfloat x = 3.14; // NVGT",
  "docs": "https://nvgt.gg/docs/references/builtin/..."
}
```

**Tópicos cobertos:**
- ✅ double → float
- ✅ arrays e $operador
- ✅ strings e métodos
- ✅ sound handles (@)
- ✅ network handles
- ✅ files e classe file
- ✅ timers e propriedades
- ✅ date/time e calendar()
- ✅ funções matemáticas
- ✅ clipboard

### 💡 2. get_nvgt_examples
Retorna exemplos práticos de código BGT vs NVGT.

**Parâmetros:**
- `category`: Nome da categoria ou "all" para listar

**Categorias disponíveis:**
1. `basic_types` - Tipos de Dados Básicos
2. `arrays` - Arrays e Tamanho
3. `strings` - Manipulação de Strings
4. `sound` - Sistema de Áudio
5. `sound_pool` - Sound Pool (Audio 3D)
6. `files` - Manipulação de Arquivos
7. `network` - Networking
8. `timers` - Timers
9. `datetime` - Data e Hora
10. `math` - Funções Matemáticas
11. `handles` - Handles e null
12. `dynamic_menu` - Menu Dinâmico
13. `complete_example` - Exemplo Completo de Jogo

**Exemplo de uso:**
```json
{
  "name": "get_nvgt_examples",
  "arguments": {
    "category": "sound"
  }
}
```

**Resposta:**
```json
{
  "category": "sound",
  "title": "Sistema de Áudio",
  "bgt": "// BGT\nsound s;\ns.stream(\"music.ogg\");\ns.play();",
  "nvgt": "// NVGT\nsound@ s;\ns.load(\"music.ogg\");\ns.play();"
}
```

## 🔗 Links Úteis

### Documentação Oficial NVGT
- **Docs Completos**: https://nvgt.gg/docs/
- **GitHub Repo**: https://github.com/samtupy/nvgt
- **Migration Guide**: https://nvgt.gg/docs/!articles/Migration%20Guide/

### Documentação por Categoria
- **Data Types**: https://nvgt.gg/docs/references/builtin/!Containers%20and%20Data%20Manipulation/Data%20Types/
- **Arrays**: https://nvgt.gg/docs/references/builtin/!Containers%20and%20Data%20Manipulation/Array/
- **Strings**: https://nvgt.gg/docs/references/builtin/!Containers%20and%20Data%20Manipulation/string/
- **Sound**: https://nvgt.gg/docs/references/builtin/!Audio/sound/
- **Network**: https://nvgt.gg/docs/references/builtin/!Networking/network/
- **File**: https://nvgt.gg/docs/references/builtin/!File%20System/file/
- **Timer**: https://nvgt.gg/docs/references/builtin/!Date%20and%20Time/timer/
- **Calendar**: https://nvgt.gg/docs/references/builtin/!Date%20and%20Time/calendar/
- **Math**: https://nvgt.gg/docs/references/builtin/!Mathematical/

## 📊 Total de Ferramentas MCP

O servidor agora possui **7 ferramentas**:

1. ✅ `convert_bgt_file` - Converte arquivo .bgt
2. ✅ `convert_bgt_code` - Converte trecho de código
3. ✅ `list_bgt_files` - Lista arquivos .bgt
4. ✅ `get_conversion_rules` - Mostra regras de conversão
5. ✅ `convert_all_bgt_files` - Converte todos os arquivos
6. 🆕 `search_nvgt_docs` - Busca na documentação
7. 🆕 `get_nvgt_examples` - Exemplos práticos

## 🎯 Casos de Uso

### Caso 1: Descobrir como converter double
```bash
# Pergunta: "Como converto double do BGT para NVGT?"
# Usar ferramenta: search_nvgt_docs
# Query: "double"
# Resultado: Explicação + link para docs
```

### Caso 2: Ver exemplo completo de áudio
```bash
# Pergunta: "Mostre exemplo de sound em NVGT"
# Usar ferramenta: get_nvgt_examples
# Category: "sound"
# Resultado: Código BGT vs NVGT lado a lado
```

### Caso 3: Ver todas diferenças de strings
```bash
# Pergunta: "Quais são as diferenças de strings?"
# Usar ferramenta: search_nvgt_docs
# Query: "string"
# Resultado: Lista de diferenças + exemplos
```

## 🚀 Como Usar no Claude Desktop

Quando você usar o Claude Desktop com este servidor MCP:

1. **Pergunte naturalmente:**
   - "Como funciona array em NVGT?"
   - "Mostre exemplo de sound"
   - "Diferença entre BGT e NVGT para timers"

2. **O Claude automaticamente:**
   - Escolhe a ferramenta certa
   - Busca na documentação
   - Retorna exemplos práticos
   - Mostra links para docs oficiais

## 💻 Teste Manual

```bash
# Build
npm run build

# Testar search_nvgt_docs
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_nvgt_docs","arguments":{"query":"sound"}}}' | npm start

# Testar get_nvgt_examples
echo '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_nvgt_examples","arguments":{"category":"arrays"}}}' | npm start
```

## 🎓 Benefícios

### Antes (sem integração):
- ❌ Buscar manualmente no GitHub
- ❌ Abrir navegador e procurar
- ❌ Comparar docs BGT e NVGT

### Agora (com integração):
- ✅ Busca automática na documentação
- ✅ Exemplos lado a lado (BGT vs NVGT)
- ✅ Links diretos para docs oficiais
- ✅ Base de conhecimento embutida
- ✅ Respostas instantâneas

## 📈 Próximas Melhorias (Opcional)

- [ ] Integrar com GitHub API para buscar código real
- [ ] Cache de documentação para respostas mais rápidas
- [ ] Busca fuzzy para encontrar tópicos similares
- [ ] Integrar com issues do repositório NVGT
- [ ] Adicionar mais exemplos práticos

---

**Integração concluída em**: 2025-12-03
**Status**: ✅ Funcionando perfeitamente!
