# Servidor EVM - Guia de Uso

## 🚀 Como Iniciar o Servidor

1. Execute o arquivo `server.nvgt`
2. Uma janela será aberta mostrando:
   - Porta do servidor (9317)
   - Número de jogadores online
   - Tempo de atividade (uptime)

## ⌨️ Controles

- **ESC** - Desligar servidor graciosamente
- **Alt+F4** - Desligar servidor (Windows padrão)

## ❌ Erro: "Falha ao inicializar servidor de rede"

### Causa
A porta 9317 já está em uso por outra instância do servidor.

### Solução 1: Script Automático (Recomendado)
Execute o arquivo `kill_server.bat` antes de iniciar o servidor.

### Solução 2: Gerenciador de Tarefas
1. Abra o Gerenciador de Tarefas (Ctrl+Shift+Esc)
2. Procure por processos `nvgtw.exe`
3. Clique com botão direito → "Finalizar Tarefa"
4. Tente rodar o servidor novamente

### Solução 3: PowerShell
```powershell
Stop-Process -Name nvgtw -Force
```

### Solução 4: Mudar a Porta
Edite o arquivo `server.nvgt` e altere:
```nvgt
const int SERVER_PORT = 9317;  // Mude para outra porta, ex: 9318
```

## 📊 Informações do Servidor

- **Porta padrão:** 9317
- **Máximo de jogadores:** 100
- **Banco de dados:** server/database/evm.db
- **Logs:** server/log.md

## 🔐 Sistema de Autenticação

O servidor usa hash SHA-256 para senhas:
- ✅ Senhas nunca trafegam em texto plano
- ✅ Hash SHA-256 armazenado no banco
- ✅ Criptografia AES 256-bit para dados do jogador

## 📝 Comandos de Rede

### Criar Conta
```
xt55 <username> <password_hash> <email> <gender>
```

### Login
```
h33j <username> <password_hash> <version> <computer_id>
```

## 🐛 Debug

Mensagens de log são exibidas na janela do servidor em tempo real:
- Conexões/desconexões
- Logins/criação de contas
- Erros e avisos

## 🔄 Auto-save

- **A cada 5 minutos:** Salva todos os jogadores online
- **A cada 1 hora:** Backup automático do banco de dados
- **Ao fechar:** Salva todos os jogadores antes de desligar
