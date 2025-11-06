# 🔧 Correção: Menu "Configurar Personagem"

**Data:** 5 de outubro de 2025  
**Arquivo:** `cliente/includes/menu.nvgt`  
**Problema:** Menu impedia configurar credenciais de contas existentes

---

## ❌ PROBLEMA ENCONTRADO

### **Comportamento Incorreto:**
Quando usuário clicava em **"Configurar personagem"** no menu principal:
- ❌ Sistema verificava se `net_un == ""`
- ❌ Se vazio, mostrava erro: *"Você não tem uma conta criada"*
- ❌ Impedia usuário de **ENTRAR** com conta já existente no servidor

### **Impacto:**
- Usuário com conta criada no servidor não conseguia configurar credenciais localmente
- Única opção era criar conta nova (duplicaria contas)
- Confusão entre "criar conta" vs "configurar credenciais"

---

## ✅ SOLUÇÃO IMPLEMENTADA

### **Código Anterior (ERRADO):**
```nvgt
else if(selected_id == "personagem") {
    debug_log("📋 Usuário selecionou CONFIGURAR PERSONAGEM");
    // ❌ VERIFICAÇÃO INCORRETA - impedia configurar credenciais
    if(net_un == "" && un == "") {
        dlg(pu.get_value("Você não tem uma conta criada. Por favor, crie uma conta primeiro em 'Criar nova conta'."));
        menuprincipal();
        return;
    }
    
    if(prompt_login_form(pu.get_value("Configurar personagem"))) {
        dlg(pu.get_value("Preferências atualizadas."));
    }
    menuprincipal();
}
```

### **Código Corrigido (CORRETO):**
```nvgt
else if(selected_id == "personagem") {
    debug_log("📋 Usuário selecionado CONFIGURAR PERSONAGEM");
    // ✅ REMOVIDA verificação - permite configurar sempre
    if(prompt_login_form(pu.get_value("Configurar personagem"))) {
        dlg(pu.get_value("Credenciais salvas com sucesso! Agora você pode conectar."));
    }
    menuprincipal();
}
```

---

## 🎯 FLUXO CORRETO AGORA

### **Opção 1: "Configurar Personagem"**
**Propósito:** Salvar credenciais de conta EXISTENTE para login automático

**Fluxo:**
1. Usuário clica "Configurar personagem"
2. Sistema abre formulário: `prompt_login_form()`
3. Usuário digita:
   - Username da conta (já criada no servidor)
   - Senha da conta
4. Sistema salva em:
   - `net_un` e `un` (username)
   - `net_pw` e `pw` (password)
   - Chama `writeprefs()` → Salva em arquivo local
5. Mensagem: **"Credenciais salvas com sucesso!"**

**Quando usar:**
- ✅ Você JÁ tem conta no servidor
- ✅ Quer salvar credenciais para não digitar toda vez
- ✅ Mudou de computador e quer configurar novamente

---

### **Opção 2: "Criar Nova Conta"**
**Propósito:** Criar conta NOVA no servidor

**Fluxo:**
1. Usuário clica "Criar nova conta"
2. Sistema abre formulário: `collect_account_creation_data()`
3. Usuário digita:
   - Username (novo)
   - Email
   - Senha (mínimo 8 caracteres)
   - Confirmar senha
4. Sistema envia ao servidor: `xt55 username hash email gender`
5. Servidor cria no banco de dados
6. Sistema salva credenciais localmente
7. **Login automático**

**Quando usar:**
- ✅ Primeira vez no jogo
- ✅ Quer criar personagem novo
- ✅ Não tem conta ainda

---

### **Opção 3: "Conectar"**
**Propósito:** Fazer login com credenciais salvas

**Fluxo:**
1. Usuário clica "Conectar"
2. Sistema verifica se `net_un` e `net_pw` existem
3. Se **NÃO existem:**
   - ❌ Mostra erro: *"Configure suas credenciais primeiro"*
   - Direciona para "Configurar personagem" ou "Criar nova conta"
4. Se **EXISTEM:**
   - ✅ Conecta automaticamente ao servidor
   - Envia login: `xt53 username hash`

**Quando usar:**
- ✅ Credenciais já configuradas
- ✅ Quer entrar no jogo rapidamente

---

## 📊 CENÁRIOS DE USO

### **Cenário 1: Novo Jogador**
```
1. Menu → "Criar nova conta"
2. Preenche dados
3. Conta criada no servidor + credenciais salvas localmente
4. Login automático
```

### **Cenário 2: Jogador Existente (Novo Computador)**
```
1. Menu → "Configurar personagem"
2. Digita username e senha da conta existente
3. Credenciais salvas localmente
4. Menu → "Conectar"
5. Login com credenciais salvas
```

### **Cenário 3: Jogador com Credenciais Salvas**
```
1. Menu → "Conectar"
2. Login automático (usa credenciais salvas)
```

---

## 🔍 FUNÇÃO `prompt_login_form()`

**Localização:** `cliente/includes/menu.nvgt` linha 76

**Comportamento Correto:**
```nvgt
bool prompt_login_form(const string &in title = "") {
    string form_title = title != "" ? title : pu.get_value("Conectar");

    while(true) {
        input_form form(form_title);
        form.description = pu.get_value("Informe suas credenciais e pressione enter.");
        
        // Campos pré-preenchidos se já tiver algo salvo
        form.add_text_field("username", pu.get_value("Digite seu nome de usuário."), net_un != "" ? net_un : un, true);
        form.add_text_field("password", pu.get_value("Digite sua senha."), net_pw, true, true);

        dictionary@ result = form.run();
        if(form.user_canceled) return false;

        string username_candidate = "";
        string password_candidate = "";
        result.get("username", username_candidate);
        result.get("password", password_candidate);

        // Validações
        if(msginvalida(username_candidate)) {
            dlg(pu.get_value("Nome de usuário inválido. Espaços não são aceitos."));
            continue;
        }
        if(password_candidate == "" || msginvalida(password_candidate)) {
            dlg(pu.get_value("Senha inválida. Espaços não são aceitos."));
            continue;
        }

        // ✅ SALVA CREDENCIAIS
        net_un = username_candidate;
        un = username_candidate;
        net_pw = password_candidate;
        pw = password_candidate;
        writeprefs();  // ← Salva em arquivo local
        
        return true;
    }
    return false;
}
```

**Características:**
- ✅ Valida entrada (sem espaços)
- ✅ Salva em 4 variáveis globais
- ✅ Persiste com `writeprefs()`
- ✅ Pré-preenche campos se já houver dados

---

## 📝 ARQUIVO DE PREFERÊNCIAS

**Localização:** `client.dat` (ou similar)

**Conteúdo Salvo:**
```
net_un=jogador123
net_pw=minhasenha
un=jogador123
pw=minhasenha
```

**Função:** `writeprefs()`
- Salva todas as preferências do usuário
- Credenciais incluídas

**Função:** `readprefs()` (chamada no startup)
- Carrega preferências ao iniciar jogo
- Restaura `net_un`, `net_pw`, etc.

---

## ✅ RESULTADO FINAL

### **Antes da Correção:**
```
Menu Principal
├── Conectar (requer credenciais salvas)
├── Configurar personagem ❌ (bloqueado se não tiver conta salva)
├── Criar nova conta ✅
└── Sair
```

### **Depois da Correção:**
```
Menu Principal
├── Conectar (requer credenciais salvas)
├── Configurar personagem ✅ (SEMPRE disponível - para logar com conta existente)
├── Criar nova conta ✅ (para criar conta nova no servidor)
└── Sair
```

---

## 🧪 TESTE

### **Como Testar a Correção:**

1. **Executar cliente compilado**
   ```bash
   cd cliente
   client.exe
   ```

2. **No menu principal:**
   - Escolher "Configurar personagem"

3. **Preencher formulário:**
   - Username: `jogador123` (conta que existe no servidor)
   - Senha: `suasenha`

4. **Resultado esperado:**
   - ✅ Mensagem: "Credenciais salvas com sucesso!"
   - ✅ Volta ao menu
   - ✅ Opção "Conectar" agora funciona

5. **Testar conexão:**
   - Escolher "Conectar"
   - ✅ Deve conectar com as credenciais salvas

---

## 🎯 BENEFÍCIOS DA CORREÇÃO

### **Para o Usuário:**
- ✅ Pode configurar credenciais de contas existentes
- ✅ Não precisa criar conta nova se já tem uma
- ✅ Menu mais intuitivo e lógico
- ✅ Separação clara entre "criar" e "configurar"

### **Para o Sistema:**
- ✅ Evita duplicação de contas
- ✅ Permite migração entre computadores
- ✅ Credenciais persistentes
- ✅ Fluxo de login mais robusto

---

**Status:** ✅ CORRIGIDO E COMPILADO  
**Última Atualização:** 5 de outubro de 2025
