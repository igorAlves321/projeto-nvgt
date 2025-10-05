# 📘 plano.md — Análise Cliente/Servidor em NVGT/BGT

## 🧠 Objetivo

Este plano tem como finalidade revisar e validar a estrutura cliente-servidor do projeto desenvolvido em NVGT (prioritário) e BGT (suporte lógico), garantindo que:

- A comunicação entre cliente e servidor esteja correta e funcional.
- As funções, classes e protocolos internos da linguagem NVGT estejam sendo utilizados conforme especificação.
- A lógica em NVGT esteja coerente com o fluxo de criação de conta e conexão.

## 📁 Estrutura de Referência

- /include → Códigos originais da linguagem NVGT, desenvolvidos pelos criadores.
- /doc.txt → Documentação da linguagem NVGT.
  -  pergunta para conversão.md → Perguntas e referências úteis para ajustes e correções.

## 🔍 Etapas da Análise

### 1. Verificação da Estrutura Cliente-Servidor

- Validar se o cliente NVGT está utilizando corretamente os protocolos de conexão.
- Checar se o servidor NVGT está escutando na porta correta e aceitando conexões simultâneas.
- Confirmar se há tratamento de erro para servidor indisponível.
- Verificar se há handshake inicial entre cliente e servidor (autenticação, troca de chaves, etc).

### 2. Revisão das Funções e Classes NVGT

- Analisar todas as funções relacionadas à conexão: `connect()`, `send()`, `receive()`, `disconnect()`.
- Verificar se as classes estão encapsulando corretamente os dados do usuário.
- Validar se há uso correto de buffers de áudio e eventos NVGT.
- Checar se há uso de threads ou timers para manter a conexão ativa.

### 3. Revisão da Lógica em BGT

- Validar se a lógica de criação de conta está sincronizada com o fluxo NVGT.
- Checar se os dados do formulário (nome, email, senha, sexo) estão sendo corretamente armazenados.
- Verificar se há validação de campos antes do envio ao servidor.
- Confirmar se o client está chamando corretamente as funções NVGT servidor após o preenchimento do último campo e o preiconar enter.

## 🔄 Fluxo de Criação de Conta

1. Usuário inicia o cliente NVGT.
2. Navega até a opção "Criar Conta".
3. Preenche os campos:
   - Nome
   - Email
   - Senha
   - Sexo (Homem ou Mulher)
4. Ao pressionar ENTER no último campo:
   - Cliente tenta se conectar ao servidor NVGT.
   - Se servidor estiver online:
     - Conta é criada e armazenada corretamente.
   - Se servidor estiver offline:
     - Mensagem: "Servidor indisponível no momento, tente novamente mais tarde."

## ✅ Critérios de Validação

- Conexão NVGT deve ser estabelecida automaticamente após o preenchimento do formulário.
- Conta deve ser criada com persistência (banco de dados ou arquivo).
- Mensagens de erro devem ser claras e acessíveis via áudio.
- Código deve seguir padrões da linguagem NVGT conforme documentação em /docks.
- Funções e classes devem estar organizadas e comentadas.

## 🛠️ Próximos Passos

- [ ] Ler e interpretar conversão.md para ajustes finos.
- [ ] Validar protocolos NVGT na pasta /include.
- [ ] Testar fluxo completo de criação de conta com servidor ativo e inativo.
- [ ] Revisar chamadas BGT que interagem com NVGT.
- [ ] Documentar pontos de falha e propor correções.
