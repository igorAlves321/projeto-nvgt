\# 🎯 Task 2.1: Implementar Favoritos de Armas (F0-F9)



\*\*EPIC:\*\* Polimento e Sistemas Secundários (Epic 2)

\*\*DOMÍNIO:\*\* Cliente / Usabilidade / Combate

\*\*PRIORIDADE:\*\* MÉDIA-ALTA

\*\*ESFORÇO ESTIMADO:\*\* BAIXO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar o sistema de \*\*Favoritos de Armas (F0-F9)\*\*. O foco desta \*task\* é garantir a \*\*persistência\*\* das escolhas do jogador entre as sessões, utilizando a classe \*\*`settings`\*\* do NVGT para salvar e carregar os IDs das armas no lado do Cliente.



\## 📝 Contexto e Solução NVGT



\* \[cite\_start]\*\*API Recomendada:\*\* O NVGT recomenda a classe de alto nível \*\*`settings`\*\* para persistência de configurações do cliente, pois ela gerencia a localização do arquivo (`AppData`) e suporta o formato INI\[cite: 3].

\* \*\*Estrutura:\*\* As 10 teclas de favoritos (F0 a F9) serão mapeadas para chaves dinâmicas (`F0`, `F1`, etc.) na seção de configuração.



---



\## 💻 Descrição Detalhada da Implementação (Modelo NVGT - Persistência)



O desenvolvedor deve integrar este código nas rotinas de inicialização (`main`) e nas rotinas de \*setup\* (`Ctrl+Fx` ou `Shift+Fx`) do Cliente.



\### Passo 1: Configuração Inicial e Carregamento (Rotina `main` do Cliente)



A rotina de inicialização deve configurar a API de \*settings\* e carregar os dados salvos.



```nvgt

\#include "settings.nvgt"

const int FAVORITES\_COUNT = 10;

string\[] weapon\_favorites; // Array global para manter os IDs na memória

settings favorites\_config;  // Objeto de Configuração



void main() {

    // 1. Configurar o objeto settings na inicialização do cliente

    // Configura caminho e formato (ini, conforme solicitado).

    if (!favorites\_config.setup("MeuJogo", "ClientConfig", false, "ini")) {

        alert("Fatal", "Falha ao configurar o sistema de persistência.");

        return;

    }

    

    // 2. Carregar configurações antigas

    load\_weapon\_favorites(); 

    

    // ... (Restante do loop principal do jogo)

}



// ROTINA DE CARREGAMENTO (load\_weapon\_favorites)

void load\_weapon\_favorites() {

    // 1. Inicializa a array para o tamanho correto

    weapon\_favorites.resize(FAVORITES\_COUNT);



    if (!favorites\_config.active) {

        alert("Erro", "Sistema de Configuração não está ativo. Usando defaults.");

        return;

    }



    // 2. Itera e recupera cada ID salvo

    for (uint i = 0; i < FAVORITES\_COUNT; i++) {

        string key = "F" + string(i);

        

        // read\_string recupera o valor ou retorna "" (valor padrão) se a chave não existir.

        string stored\_id = favorites\_config.read\_string(key, ""); 

        

        weapon\_favorites\[i] = stored\_id;

    }

}

Passo 2: Rotina de Salvamento (Ação do Jogador/Encerramento)

Esta rotina deve ser chamada sempre que o jogador configurar um novo atalho e/ou no encerramento da sessão do Cliente.

// ROTINA DE SALVAMENTO (save\_weapon\_favorites)

bool save\_weapon\_favorites() {

    if (!favorites\_config.active) {

        alert("Erro", "Sistema de Configuração não está ativo.");

        return false;

    }

    

    bool success = true;



    // Itera sobre a array e salva cada item individualmente

    for (uint i = 0; i < weapon\_favorites.length(); i++) {

        string key = "F" + string(i);

        string item\_id = weapon\_favorites\[i];



        // write\_string salva o valor. instant\_save é true por padrão.

        if (!favorites\_config.write\_string(key, item\_id)) { 

            alert("Erro", "Falha ao salvar o favorito " + key);

            success = false;

        }

    }

    

    if (success) {

        alert("Configuração", "Favoritos de armas salvos com sucesso.");

    }

    return success;

}

Critérios de Aceitação

• 

API Corretamente Utilizada: O sistema de atalhos utiliza a classe settings (do settings.nvgt) para persistência.

• 

Carregamento Automático: As configurações são carregadas na inicialização do Cliente.

• 

Chaves Dinâmicas: O código utiliza o loop e a concatenação ("F" + string(i)) para gerenciar as 10 chaves de F0 a F9.

• 

Persistência Funcional: As configurações de atalho são salvas no disco após a definição e carregadas corretamente entre as sessões.

&nbsp;

