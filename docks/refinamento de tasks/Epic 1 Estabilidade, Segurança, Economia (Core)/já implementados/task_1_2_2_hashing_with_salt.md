# 🔐 Task 1.2.2: Implementar Hashing com Salt

**EPIC:** Estabilidade e Funcionalidades Críticas (Epic 1)
**DOMÍNIO:** Servidor / Segurança / Autenticação
**PRIORIDADE:** CRÍTICA (Nível 1)
**ESFORÇO ESTIMADO:** MÉDIO
**STATUS:** TO DO

## 🎯 Objetivo

Melhorar a segurança do sistema de autenticação, migrando o *hashing* SHA-256 puro para um sistema que utilize **Salt** (Valor Aleatório Único). O objetivo é proteger as senhas armazenadas no banco de dados contra ataques de *Rainbow Table*. A implementação deve usar funções **nativas do NVGT** (`string_hash_sha256` e `generate_token`).

## 📝 Referências e Contexto

* **Vulnerabilidade:** SHA-256 puro é vulnerável a ataques de *Rainbow Table*.
* **Solução:** O Salt, único por usuário, torna o ataque ineficaz.
* **Funções Nativas NVGT:** `string_hash_sha256(data, binary)` e `generate_token(length, mode)`.
* **Arquivos:** `server/includes/auth.nvgt` (Lógica de autenticação) e `server/includes/db_auth.nvgt` (Interação com o DB).

---

## 💻 Descrição Detalhada da Implementação (Código NVGT Nativo)

O desenvolvedor deverá integrar este código, substituindo a lógica atual de *hashing* nas rotinas de criação (`net_create`) e login (`net_logar`).

### Passo 1: Configuração e Dependências

1.  **Incluir Dependências:** Certificar-se de que o módulo `token_gen.nvgt` está incluído.
2.  **Definir Constantes:** Definir o tamanho do *salt* e o *flag* de retorno do *hash*.

    ```nvgt
    #include "token_gen.nvgt" // Para generate_token()
    
    // NOTA: Assumimos que string_hash_sha256() está registrada no engine core.
    const int SALT_LENGTH = 16;
    const bool RETURN_HEX_STRING = false; // Retornar hash em string hexadecimal
    ```

3.  **Modificação do DB:** O campo `password_salt` (TEXT) deve ser adicionado à tabela `players` no SQLite.

### Passo 2: Rotina de Criação de Conta (`net_create`)

A função deve gerar um *salt*, concatená-lo à senha, calcular o *hash* e salvar **ambos** no banco de dados.

```nvgt
// 1. Geração e Armazenamento (Rotina net_create)
bool net_create(const string& in username, const string& in password_bruta) {
    // ... (Verificação se o usuário existe)
    
    // A. Gerar Salt (Valor aleatório alfanumérico)
    string new_salt = generate_token(SALT_LENGTH, TOKEN_CHARACTERS | TOKEN_NUMBERS);
    
    // B. Concatenar: Salt + Senha
    string salted_password = new_salt + password_bruta;
    
    // C. Aplicar o Hash (SHA-256) nativo
    string final_hash = string_hash_sha256(salted_password, RETURN_HEX_STRING);
    
    // D. Salvar o Hash e o Salt no DB (Novo campo 'password_salt')
    // Substituir por sua lógica de DB:
    // db.execute("INSERT INTO players (username, password_hash, password_salt) VALUES (?, ?, ?)", 
    //            username, final_hash, new_salt);
    
    // ... (Lógica de sucesso)
    return true;
}
Passo 3: Rotina de Verificação de Login (net_logar)
A função deve recuperar o salt do DB para calcular o hash da senha de entrada e comparar o resultado com o hash armazenado.
// 2. Verificação (Rotina net_logar)
bool net_logar(const string& in username, const string& in password_digitada) {
    // 1. Recuperar o Salt e o Hash armazenados do DB
    // Exemplo: PlayerRecord@ stored_record = db.query_player(username);
    
    if (@stored_record == null) {
        alert("Login Falhou", "Nome de usuário incorreto.");
        return false;
    }
    
    // 2. Concatenar: Salt Recuperado + Senha Digitada
    string salted_input_password = stored_record.salt + password_digitada;
    
    // 3. Aplicar o Hash (SHA-256) nativo
    string calculated_hash = string_hash_sha256(salted_input_password, RETURN_HEX_STRING);
    
    // 4. Comparar os Hashes
    if (calculated_hash == stored_record.stored_hash) {
        alert("Login Sucesso", "Bem-vindo, " + username + "!");
        return true;
    } else {
        alert("Login Falhou", "Senha incorreta.");
        return false;
    }
}
