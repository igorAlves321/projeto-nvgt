# Agente Instructions - Projeto IG (NVGT Game)

## 1. Idioma e Interacao (OBRIGATORIO)
- **Idioma de Resposta:** O agente deve se comunicar exclusivamente em Portugues (Brasil).
- **Clareza:** Mantenha respostas objetivas e bem estruturadas.

## 2. Visao Geral e Conhecimento Base
Este e um jogo multiplayer online construido com **NVGT (NonVisual Gaming Toolkit)**.
- **Referencia Tecnica:** Consulte a documentacao local em `docks/nvgt-reference/nvgt-docks/`.
- **Exemplos de Codigo:** Use `docks/nvgt-reference/examples/` como referencia de sintaxe.
- **Prioridade:** A documentacao local destas pastas tem precedencia sobre conhecimento geral da IA.

## 3. Arquitetura do Sistema

### Servidor (`server/server.nvgt`)
- **Porta:** 9317 | **Banco de Dados:** SQLite (`#pragma plugin nvgt_sqlite`).
- **Seguranca:** Criptografia AES e autenticacao SHA-256 + salt.
- **Fluxo Critico:** `shared_globals.nvgt` deve ser incluido antes de modulos que dependem de SQLite/estado global.

### Cliente (`cliente/client.nvgt`)
- **Configuracao:** Centralizada em `config.nvgt`.
- **Interface:** Focada em audio e acessibilidade (I18N em `.lang`).
- **Fluxo Critico:** `globals.nvgt` deve vir antes de `sound_pool.nvgt`.

---

## 4. Diretrizes Tecnicas Obrigatorias

### Ordem de Includes (Compilacao Linear)
- **Servidor:** `shared_globals.nvgt` -> `globals.nvgt` -> demais arquivos.
- **Cliente:** `globals.nvgt` -> `sound_pool.nvgt` -> demais arquivos.

### Includes de biblioteca NVGT
- Muitos arquivos sao da propria linguagem/toolkit (ex.: `speech.nvgt`, `sound_pool.nvgt`, `form.nvgt`, `input_forms.nvgt`).
- Quando o include path do compilador estiver configurado, pode usar apenas `#include "nome_arquivo.nvgt"`.
- Se o include path nao estiver configurado no ambiente, use caminho relativo explicito (ex.: `../docks/include/nome_arquivo.nvgt`).
- Ao orientar mudancas, respeite o padrao ja usado no arquivo atual para evitar quebra de build.

### Comunicacao de Rede e Broadcast
- O NVGT nao trata `peer_id == 0` como broadcast automatico em todas as APIs.
- **Regra:** para broadcast, sempre iterar peers manualmente e enviar um a um.
- Essa iteracao pode usar `network::get_peer_list()` **ou** lista controlada pelo servidor (ex.: `connected_peers`), desde que cubra todos os peers validos.

### Manipulacao de Mapas (`.map`)
- **Performance:** Nao ler arquivo em loop de jogo. Carregar em memoria durante `init`.
- Use `:` como separador no parser dos mapas.

### APIs Modernas vs Legado
- **Web:** Priorize classe nativa `http`. Evite `nvgt_curl` em codigo novo.
- **Arrays:** Use `.length()` (metodo), nunca `.length` (propriedade).

---

## 5. Debugging e Acessibilidade
- **TTS (Fala):** No cliente, use `speak()` para debug.
- **Console:** Utilize `print()` ou `c_debug_message()`.
- **Wrapper:** `debug_log()` deve ser tratado como wrapper para console/arquivo.

## 6. Migracao BGT -> NVGT
- **Compatibilidade:** Incluir `bgt_compat.nvgt` quando houver dependencia legada real.
- **Handles:** Use sintaxe de handles (`@`) do AngelScript conforme documentacao.
