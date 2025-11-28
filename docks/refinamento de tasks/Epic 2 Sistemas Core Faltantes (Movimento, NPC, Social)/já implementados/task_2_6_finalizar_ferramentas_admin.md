# 🛠️ Task 2.6: Finalizar Ferramentas e Utilitários (Rastreador e Lógica de Chat)

**EPIC:** Polimento e Sistemas Secundários (Epic 2)
**DOMÍNIO:** Servidor / Administração / Ferramentas & Social
**PRIORIDADE:** MÉDIA
**ESFORÇO ESTIMADO:** MÉDIO

## 🎯 Objetivo

Implementar utilitários avançados e fechar os gaps de ferramentas de moderação e social, conforme as novas especificações:
1.  **Rastreador de Jogadores:** Implementar o Rastreador como um **função de Uso Geral quando o jogador precionar f4 o jogo vai falar se não tiver ninguem no mapa, ninguem np mapa, caso tenha mais jogadores, ele vai perguntar quem você deseja rastriar, e vai abrir a lista pro jogador rastriar.**, validando a posse do item para todos os jogadores.
2.  **Indicação de Título Social ("bugueiro"):** Exibir um **logo/ícone** no chat administrativo para jogadores com o título/patente **"bugueiro"**.
3.  **Equipamentos Especiais de Admin:** Implementar Lanterna e Detector (restritos a Admins).

## 📝 Referências e Contexto

* **Módulos Envolvidos:**
    * **Servidor:** Módulo de Comandos Admin (`admin_commands.nvgt`), Lógica de Itens (`server/includes/item.nvgt`), Lógica de Chat (`chat.nvgt`).
    * **Cliente:** `client.nvgt` (para detecção de teclas e renderização do logo).
* **Restrição de Acesso:** O uso da Lanterna e Detector deve ser restrito a Níveis Admin 2 ou 3.

---

## 💻 Descrição Detalhada da Implementação (Passo a Passo)

### Passo 1: Implementar o Rastreador de Jogadores (Uso Geral)

O Rastreador permite a qualquer jogador com o item saber a posição (X, Y, Mapa) de um alvo.

1.  **Handler de Ativação (Cliente → Servidor):**
    * **Handler:** `req_start_tracking [target_name]`.
    * **Lógica de Validação:** O Servidor recebe a requisição e **VERIFICA se o jogador possui o item "Rastreador"** no inventário. Se sim, armazena o `target_name`.
2.  **Handler de Atualização (Servidor → Cliente):**
    * O Servidor cria um *timer* periódico (Ex: a cada 2 segundos) que envia silenciosamente um pacote de atualização de posição do alvo para o jogador rastreando.
    * **Handler:** `msg_tracking_update [target_x] [target_y] [target_map]`.
    * **Cliente:** O Cliente reproduz *feedback* de áudio (Ex: um "bip" com as coordenadas TTS) com as informações do alvo.

### Passo 2: Indicação de Título "Chatter" no Chat Administrativo

Permitir que um jogador com o título "Chatter" tenha um indicador especial no chat de moderação/administração.

1.  **Lógica do Servidor (`chat.nvgt`):** Modificar a função que constrói e envia mensagens para o chat administrativo.
    * **Verificação de Patente:** Antes de enviar a mensagem, verificar se o remetente tem a patente/título `CHATTER`.
    * **Injeção de Código:** Se sim, prefixar a mensagem com um código de renderização que o Cliente entenda.
        ```nvgt
        string msg_prefix = "";
        if (player.title == "CHATTER") {
            msg_prefix = "[LOGO_CHATTER] "; // Tag que aciona o ícone/TTS no Cliente
        }
        send_to_admin_chat(msg_prefix + player.name + ": " + message);
        ```
2.  **Lógica do Cliente (`client.nvgt`):** O *parser* de chat administrativo deve reconhecer e renderizar o `[LOGO_CHATTER]` como um som ou uma leitura TTS (Ex: "Chatter:") antes do nome do jogador.

### Passo 3: Implementar Ferramentas de Admin (Lanterna e Detector)

A Lanterna e o Detector permanecem restritos a Admins (Nível 2 ou 3).

1.  **Lanterna (Visão e Áudio):** Implementar `req_admin_toggle_light` no Servidor para atualizar o estado do Admin. O Cliente reproduz o som posicional da "luz" para os outros jogadores próximos.
2.  **Detector:** Implementar `req_admin_use_detector` no Servidor. A lógica deve procurar por **objetos invisíveis** (`is_hidden` ou `is_cloaked`) e anomalias em um raio de alcance, e retornar o *feedback* sonoro apenas ao Admin.

---

## ✅ Critérios de Aceitação

* **Rastreador Funcional (Geral):** Qualquer jogador com o item Rastreador pode usá-lo, recebendo a posição do alvo periodicamente no Cliente.
* **Chatter Logo:** Mensagens de jogadores com o título "Chatter" no chat administrativo são prefixadas com um código que o Cliente renderiza como um logo/som.
* **Ferramentas Admin Seguras:** Lanterna e Detector são funcionais e estritamente restritos a Níveis Admin 2 ou 3.

---
Você deseja ir para a próxima *task* do **Epic 2** (Task 2.7) agora, que deve lidar com os *gaps* de economia e social (Ex: Lojas/Venda de Itens)?