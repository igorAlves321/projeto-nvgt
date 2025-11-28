\# 🌎 Task 3.4: Implementar Sistema de Localização de Texto (I18N)



\*\*EPIC:\*\* Fechamento de Gaps de Polimento (Epic 3)

\*\*DOMÍNIO:\*\* Cliente / Configuração / Acessibilidade

\*\*PRIORIDADE:\*\* ALTA (Necessária para suporte multi-idioma)

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar o sistema robusto de \*\*Localização de Texto (I18N)\*\* no Cliente para que todas as \*strings\* estáticas da interface (menus, comandos, mensagens de erro) possam ser carregadas de um arquivo externo (`.lang`). A solução utiliza a API \*\*`ini.nvgt`\*\* para carregamento e \*\*`string::format()`\*\* para strings dinâmicas.



\## 📝 Contexto e Solução NVGT



\* \[cite\_start]\*\*Carregamento:\*\* A classe `ini` do NVGT é usada para ler e fazer o \*parsing\* do arquivo `.lang` no formato \*\*CHAVE=VALOR\*\*\[cite: 5].

\* \[cite\_start]\*\*Formatação:\*\* O método `string::format()` permite substituir placeholders (Ex: `%0`, `%1`) dentro das \*strings\* localizadas por variáveis dinâmicas do jogo (Ex: nome do jogador, quantidade de ouro)\[cite: 2].

\* \*\*Fallback:\*\* O `ini.get\_string()` garante um \*fallback\* seguro, retornando a chave original se a tradução não for encontrada.

\* \*\*Arquivos:\*\* `cliente/includes/localization.nvgt` (NOVO MÓDULO).



---



\## 💻 Descrição Detalhada da Implementação (Modelo NVGT)



O desenvolvedor deve criar um novo módulo (`localization.nvgt`) com as três funções de acesso a seguir.



\### Passo 1: Rotina de Carregamento (`load\_language\_file`)



Esta função é chamada na inicialização do Cliente.



```nvgt

\#include "ini.nvgt"  

ini@ localization\_data;

const string LANGUAGE\_SECTION = "STRINGS";



// Carrega o arquivo de idioma (Ex: strings\_pt.lang)

bool load\_language\_file(const string\& in filename) {

    @localization\_data = ini(); 

    // O método load() lê e faz o parsing do formato CHAVE=VALOR \[5].

    if (!localization\_data.load(filename)) {

        alert("Erro Localização", "Falha ao carregar arquivo '" + filename + "'.");

        return false;

    }

    alert("Localização", "Arquivo de idioma carregado: " + localization\_data.loaded\_filename);

    return true;

}

Passo 2: Função de Acesso Básico (localize)

Usada para todas as strings estáticas (Ex: nomes de menu, títulos de janelas).

// Acessa uma chave e retorna o valor localizado (ou a chave como fallback).

string localize(const string\& in key) {

    if (@localization\_data == null || localization\_data.is\_empty()) {

        return key; // Retorna a chave se o arquivo não estiver carregado

    }

    

    // get\_string retorna a chave (terceiro argumento) se ela não for encontrada \[6, 7].

    return localization\_data.get\_string(LANGUAGE\_SECTION, key, key);

}

Passo 3: Função de Acesso com Formatação Dinâmica (localize\_format)

Usada para mensagens que contêm variáveis do jogo (Ex: mensagens de erro, saudações).

// Localiza a string e a formata com até 16 argumentos dinâmicos (placeholders %0, %1, etc.) \[2].

string localize\_format(const string\& in key, const string\& in arg0 = "", const string\& in arg1 = "", const string\& in arg2 = "") {

    

    string localized\_string = localize(key);

    

    // O método string::format é usado para substituir placeholders (%0, %1...) \[2, 8].

    return localized\_string.format(arg0, arg1, arg2);

}

OBS, use o sistema de tradução em bgt de base para implementar esse, ou o que falta desse.

