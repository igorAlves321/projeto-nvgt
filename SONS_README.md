# 🎵 Sistema de Sons - Configuração

## ✅ Status Atual

- ✅ Pasta `sounds/` com **2205 arquivos .ogg**
- ✅ Config.nvgt configurado para usar pasta
- ✅ Sistema compilando corretamente

## 📁 Estrutura

```
cliente/
├── client.exe
└── sounds/
    ├── turn.ogg
    ├── areia_movedissaloop.ogg
    ├── beacon.ogg
    └── ... (2205 arquivos)
```

## ⚙️ Configuração Atual (config.nvgt)

```nvgt
const string SOUND_STORAGE="sounds";  // Usando pasta
```

## 🔧 Como Funciona

### Com Pasta (Atual):
1. `set_sound_storage("sounds")` detecta que é pasta
2. `global_sound_pack` fica como `null`
3. Sons são carregados diretamente: `sound.load("arquivo.ogg")`
4. O NVGT busca arquivos no diretório atual

### Possível Problema:
Os sons são chamados como `"turn.ogg"` mas estão em `"sounds/turn.ogg"`.

## 🛠️ Soluções Possíveis

### Opção 1: Copiar Sons para Raiz (Temporário para Teste)
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\cliente"
Copy-Item sounds\*.ogg .
```

### Opção 2: Modificar Chamadas (Trabalhoso)
Adicionar "sounds/" em cada chamada:
```nvgt
// Antes:
p.play_2d("turn.ogg", ...)

// Depois:
p.play_2d("sounds/turn.ogg", ...)
```

### Opção 3: Wrapper Automático (Recomendado)
Criar funções wrapper que adicionam o prefixo automaticamente.

## 📝 Próximos Passos

1. **Testar** se o cliente abre e tenta carregar sons
2. **Ver mensagens de erro** para identificar o problema exato
3. **Implementar solução** baseado no erro

## 🎮 Para Testar

```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\cliente"
.\client.exe
```

Verificar se:
- ✅ Cliente abre
- ✅ Mensagem sobre sons (se houver)
- ❌ Erros de arquivo não encontrado
