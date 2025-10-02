# 🧪 GUIA DE TESTES - CONEXÃO CLIENTE-SERVIDOR

## 🚀 PREPARAÇÃO

### 1. Compilar o Servidor
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\server"
nvgt -c server.nvgt
```

**Erros esperados:**
- Se houver erros, anote a mensagem completa e me envie

### 2. Compilar o Cliente
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\cliente"
nvgt -c client.nvgt
```

**Erros esperados:**
- Se houver erros, anote a mensagem completa e me envie

---

## 🎯 TESTE 1: Iniciar Servidor

### Passo 1: Executar o Servidor
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\server"
.\server.exe
```

### O que deve acontecer:
1. ✅ Leitor de telas deve falar: **"Iniciando servidor EVM com banco de dados SQLite"**
2. ✅ Deve criar arquivo `server/database/evm.db` se não existir
3. ✅ Deve criar tabelas no banco de dados
4. ✅ Leitor de telas deve falar: **"Servidor EVM iniciado na porta 9317"**
5. ✅ Arquivo `log.md` deve ter mensagens como:
   ```
   [2025-10-02 ...] === SERVIDOR EVM INICIANDO ===
   [2025-10-02 ...] Inicializando banco de dados SQLite: server/database/evm.db
   [2025-10-02 ...] Banco de dados inicializado com sucesso
   [2025-10-02 ...] Servidor EVM rodando na porta 9317
   [2025-10-02 ...] === SERVIDOR PRONTO ===
   ```

### Se der erro:
- Verifique se a porta 9317 não está em uso
- Verifique permissões de escrita na pasta `server/database/`
- Me envie o conteúdo do `log.md`

---

## 🎯 TESTE 2: Conectar Cliente

### Passo 1: Executar o Cliente (Com servidor rodando)
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\cliente"
.\client.exe
```

### O que deve acontecer:
1. ✅ Logo do jogo ou som de inicialização
2. ✅ Menu principal aparece
3. ✅ Opções do menu são faladas pelo leitor de telas

### Passo 2: Tentar Conectar

**Opção A: Conta Nova (Recomendado para primeiro teste)**
1. No menu principal, escolha **"Criar Conta"** ou **"Registrar"**
2. Digite um nome de usuário (ex: "teste123")
3. Digite uma senha (ex: "senha123")
4. Digite um email (ex: "teste@teste.com")
5. Escolha gênero (Homem/Mulher)

**O que deve acontecer:**
- ✅ Cliente fala: "Conectando..."
- ✅ Conexão é estabelecida
- ✅ Servidor registra no `log.md`:
  ```
  [2025-10-02 ...] Nova conexão: [peer_id] (endereço desconhecido)
  ```
- ✅ Cliente fala: "Conta criada com sucesso! Pressione enter para logar-se."
- ✅ Entra automaticamente no jogo
- ✅ Cliente fala: "Logado com sucesso! Entrando no jogo..."

**Opção B: Conta Existente**
1. No menu principal, escolha **"Conectar"** ou **"Login"**
2. Digite nome de usuário
3. Digite senha
4. Aguarde conexão

---

## 🎯 TESTE 3: Verificar Conectividade

### No Cliente (Depois de logar):

#### Teste 3.1: Movimento
- Pressione **setas** ou **WASD**
- ✅ Deve ouvir som de passos
- ✅ Coordenadas devem mudar

#### Teste 3.2: Chat
- Pressione **T** (ou tecla de chat configurada)
- Digite: "oi"
- Pressione Enter
- ✅ Mensagem deve aparecer no chat
- ✅ Servidor deve registrar a mensagem

#### Teste 3.3: Comando
- Abra o chat e digite: `/help`
- ✅ Deve receber lista de comandos disponíveis

#### Teste 3.4: Inventário
- Pressione **I** (inventário)
- ✅ Deve abrir o inventário
- ✅ Itens iniciais devem aparecer

### No Servidor (Console/Logs):

Verifique o arquivo `log.md`:
```
[...] Nova conexão: [peer_id] (endereço desconhecido)
[...] Comando recebido de [peer_id]: h33j teste123 senha123 1.0 [computer_id]
[...] Comando: /help
```

---

## 🎯 TESTE 4: Múltiplos Clientes

### Passo 1: Abrir Segundo Cliente
Em outro terminal:
```powershell
cd "c:\Users\User\Documents\meus arquivos\nvgt\projetos\projetoIg\cliente"
.\client.exe
```

### Passo 2: Criar/Logar Segunda Conta
- Use nome diferente (ex: "teste456")
- Conecte ao servidor

### O que deve acontecer:
- ✅ Ambos os clientes devem estar conectados
- ✅ No cliente 1, deve aparecer mensagem: "[teste456] entrou no jogo"
- ✅ No cliente 2, deve aparecer mensagem: "[teste123] está online"
- ✅ Servidor deve mostrar 2 conexões ativas

### Teste Interação:
**Cliente 1:**
- Digite no chat: "Olá teste456!"

**Cliente 2:**
- ✅ Deve receber a mensagem
- ✅ TTS deve falar a mensagem se configurado

---

## 🎯 TESTE 5: Persistência de Dados

### Passo 1: Mover Personagem
- Mova seu personagem para uma posição diferente (ex: x=10, y=10)

### Passo 2: Desconectar
- Pressione **ESC** e escolha "Sair"
- ✅ Cliente deve falar: "Saindo do servidor..."
- ✅ Servidor deve registrar: "Desconexão: [peer_id]"

### Passo 3: Reconectar
- Abra o cliente novamente
- Faça login com a mesma conta

### O que deve acontecer:
- ✅ Personagem deve estar na mesma posição (x=10, y=10)
- ✅ Inventário deve estar preservado
- ✅ Nível/experiência devem estar preservados

---

## 🐛 TROUBLESHOOTING

### Erro: "Servidor indisponível"
**Causa:** Cliente não consegue conectar ao servidor

**Soluções:**
1. Verifique se o servidor está rodando
2. Verifique se a porta 9317 está correta em ambos
3. Verifique firewall do Windows:
   ```powershell
   netstat -an | findstr :9317
   ```
4. Tente conectar com `localhost` em vez de IP

### Erro: "Conexão caiu"
**Causa:** Servidor fechou a conexão inesperadamente

**Soluções:**
1. Verifique logs do servidor em `log.md`
2. Procure por erros de exceção
3. Verifique se o servidor não crashou

### Erro: Sem som/áudio
**Causa:** Sistema de áudio não inicializou

**Soluções:**
1. Verifique se `sounds.dat` existe na pasta do cliente
2. Verifique se dispositivo de áudio está correto
3. No cliente, vá em Preferências > Áudio e teste

### Erro: Leitor de telas não fala
**Causa:** TTS não detectado

**Soluções:**
1. Certifique-se que NVDA, JAWS ou Narrator está rodando
2. Teste com `screen_reader_detect()`
3. Configure voz manual em Preferências

---

## 📊 CHECKLIST DE VALIDAÇÃO

### ✅ Servidor
- [ ] Servidor inicia sem erros
- [ ] Banco de dados é criado
- [ ] Porta 9317 está escutando
- [ ] Logs são gravados em `log.md`
- [ ] Aceita conexões de clientes

### ✅ Cliente
- [ ] Cliente inicia sem erros
- [ ] Menu principal aparece
- [ ] Conecta ao servidor
- [ ] Login funciona
- [ ] Criação de conta funciona

### ✅ Gameplay
- [ ] Movimento funciona
- [ ] Áudio 3D funciona
- [ ] Chat funciona
- [ ] Inventário funciona
- [ ] Comandos funcionam

### ✅ Múltiplos Jogadores
- [ ] Dois clientes podem conectar
- [ ] Mensagens são trocadas
- [ ] Posições são sincronizadas
- [ ] NPCs aparecem para ambos

### ✅ Persistência
- [ ] Dados são salvos no banco
- [ ] Dados são carregados na reconexão
- [ ] Backup automático funciona (aguardar 1 hora ou forçar)

---

## 📝 RELATÓRIO DE TESTE

Após executar os testes, preencha este relatório:

### Informações do Sistema
- **SO:** Windows [versão]
- **Leitor de Telas:** [NVDA/JAWS/Narrator]
- **Versão NVGT:** [versão]

### Resultados

| Teste | Status | Observações |
|-------|--------|-------------|
| Compilação Servidor | ⬜ OK / ⬜ ERRO | |
| Compilação Cliente | ⬜ OK / ⬜ ERRO | |
| Servidor Inicia | ⬜ OK / ⬜ ERRO | |
| Cliente Conecta | ⬜ OK / ⬜ ERRO | |
| Criar Conta | ⬜ OK / ⬜ ERRO | |
| Login | ⬜ OK / ⬜ ERRO | |
| Movimento | ⬜ OK / ⬜ ERRO | |
| Áudio 3D | ⬜ OK / ⬜ ERRO | |
| Chat | ⬜ OK / ⬜ ERRO | |
| Múltiplos Clientes | ⬜ OK / ⬜ ERRO | |
| Persistência | ⬜ OK / ⬜ ERRO | |

### Erros Encontrados
```
[Cole aqui mensagens de erro completas]
```

### Logs do Servidor
```
[Cole aqui últimas 20 linhas do log.md]
```

---

## 💬 PRECISA DE AJUDA?

Se encontrar problemas:
1. Anote a mensagem de erro **completa**
2. Anote o que você estava fazendo quando o erro ocorreu
3. Cole os logs relevantes
4. Me envie tudo isso que eu analiso e corrijo!

---

**Boa sorte com os testes! 🎮🎧**
