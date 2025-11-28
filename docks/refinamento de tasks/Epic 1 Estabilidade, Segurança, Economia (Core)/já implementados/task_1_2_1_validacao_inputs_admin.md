\# 🔒 Task 1.2.1: Implementar Validação de Inputs Admin



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Servidor / Segurança / Comandos

\*\*PRIORIDADE:\*\* CRÍTICA (Nível 1)

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO



\## 🎯 Objetivo



Implementar a \*\*validação rigorosa de todos os argumentos (inputs)\*\* nos comandos de Administração. Focar em comandos de alto risco (Ex: `/set\_level`, `/give\_item`, `/ban`) para garantir que o \*\*tipo, formato e limites\*\* de cada argumento sejam verificados antes de qualquer execução de lógica, prevenindo \*exploits\* e erros de \*runtime\*.



\## 📝 Referências e Contexto



\* \*\*Vulnerabilidade:\*\* A falta de validação em comandos de Admin é um risco de segurança.

\* \*\*Arquivo Principal:\*\* `server/includes/commands.nvgt` (Onde a lógica de comando será implementada).

\* \*\*Modelo:\*\* Utilizar o comando `/set\_level \[nome\_jogador] \[novo\_nível]` como modelo de segurança.



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvedor deverá integrar a lógica de validação no início da função de tratamento de comandos, utilizando as funções de \*string\* e o fluxo de controle do NVGT.



\### Passo 1: Configurar Constantes e Ferramentas



1\.  \*\*Definir Limites:\*\* No módulo de comandos (`commands.nvgt`), defina as constantes (`const`) para os limites de segurança.

2\.  \*\*Ferramenta de Erro:\*\* Implementar uma função local (ou \*funcdef\*) que envie um erro formatado para o Admin e \*\*interrompa (`return`)\*\* a execução do comando.



\### Passo 2: Implementar Validação de Argumentos (Modelo `/set\_level`)



A lógica deve ser inserida na função de tratamento do comando (`handle\_set\_level\_command`), seguindo a ordem de criticidade.



| Ordem | Tipo de Validação | NVGT Implementation | Objetivo de Segurança |

| :--- | :--- | :--- | :--- |

| \*\*1. Contagem\*\* | Argumentos Faltando | \*\*`if (args.length() < EXPECTED\_ARGS)`\*\* | Garante que a sintaxe básica foi seguida. |

| \*\*2. Entidade\*\* | Jogador Alvo | \*\*`if (@target\_player == null)`\*\* | Impede a execução se o jogador não estiver online ou não existir (busca com `get\_player\_by\_name()`). |

| \*\*3. Tipagem\*\* | Formato Numérico | \*\*`if (!level\_str.is\_digits())`\*\* | Previne erros de \*runtime\* ao tentar converter uma \*string\* não numérica usando `parse\_int()`. |

| \*\*4. Limites\*\* | Valor Lógico | \*\*`if (new\_level < MIN\_LEVEL || new\_level > MAX\_LEVEL)`\*\* | Impede que o Admin defina níveis que quebrem o jogo (Ex: Nível 999). |



\### Código NVGT de Exemplo para Validação de Comando



O desenvolvedor deve aplicar este padrão a \*\*todos os comandos de alto risco\*\* (ex: `/set\_gold`, `/goto`, `/ban`).



```nvgt

const int MAX\_LEVEL = 100;

const int MIN\_LEVEL = 1;

const int EXPECTED\_ARGS = 2;



// Função Admin: /set\_level \[nome\_jogador] \[novo\_nível]

void handle\_set\_level\_command(string\[]@ args, const string\& in admin\_name) {

&nbsp;   // Tratamento de Erro e Interrupção

&nbsp;   funcdef void send\_admin\_error(const string\& in msg) {

&nbsp;       alert("Comando Admin Falhou: /set\_level", admin\_name + ", " + msg);

&nbsp;       return; // Interrompe a execução aqui.

&nbsp;   }



&nbsp;   // 1. Validação de Contagem (Ex: Se faltar o nível)

&nbsp;   if (@args == null || args.length() < EXPECTED\_ARGS) {

&nbsp;       send\_admin\_error("Uso: /set\_level \[nome\_jogador] \[novo\_nível]");

&nbsp;       return;

&nbsp;   }

&nbsp;   

&nbsp;   // Argumentos 

&nbsp;   string target\_name = args\[0].trim\_whitespace();

&nbsp;   string level\_str = args\[1].trim\_whitespace();



&nbsp;   // 2. Validação de Entidade (Jogador Existe?)

&nbsp;   Player@ target\_player = get\_player\_by\_name(target\_name);

&nbsp;   if (@target\_player == null) {

&nbsp;       send\_admin\_error("Jogador '" + target\_name + "' não encontrado ou offline.");

&nbsp;       return;

&nbsp;   }



&nbsp;   // 3. Validação de Tipagem (É um número inteiro?)

&nbsp;   if (!level\_str.is\_digits() || level\_str.empty()) {

&nbsp;       send\_admin\_error("O valor do nível deve ser um número inteiro positivo.");

&nbsp;       return;

&nbsp;   }



&nbsp;   // Conversão após validação de formato

&nbsp;   int new\_level = parse\_int(level\_str); 

&nbsp;   

&nbsp;   // 4. Validação de Limites (Está entre 1 e 100?)

&nbsp;   if (new\_level < MIN\_LEVEL || new\_level > MAX\_LEVEL) {

&nbsp;       send\_admin\_error(

&nbsp;           "Nível " + new\_level + " fora dos limites permitidos (" + 

&nbsp;           string(MIN\_LEVEL) + " a " + string(MAX\_LEVEL) + ")."

&nbsp;       );

&nbsp;       return;

&nbsp;   }



&nbsp;   // --- EXECUÇÃO DA LÓGICA (Validação bem-sucedida) ---

&nbsp;   target\_player.level = new\_level;

&nbsp;   alert("Admin Sucesso", target\_player.name + " teve o nível definido para " + new\_level + ".");

}

