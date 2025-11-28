# 🎯 Task 3.1: Implementar Navegação de Inventário e Seleção Múltipla

**EPIC:** Fechamento de Gaps de Polimento (Epic 3)
**DOMÍNIO:** Cliente / Usabilidade / Inventário
**PRIORIDADE:** MÉDIA-BAIXA
**ESFORÇO ESTIMADO:** BAIXO
**STATUS:** TO DO

## 🎯 Objetivo

Restaurar as funcionalidades avançadas de inventário (Seleção Múltipla, Busca por Letra e Reordenação). [cite_start]O foco é utilizar a classe **`audio_form`** do NVGT para as funcionalidades de UI e o **Swap Direto de Handles** para a reordenação otimizada.

## 📝 Contexto e Solução NVGT

* **Performance:** A reordenação utiliza **Swap Direto de Handles** (`O(1)`), que é o método mais rápido.
* **UI Simplificada:** A classe `audio_form` nativa do NVGT gerencia internamente a lógica complexa de seleção múltipla e busca por letra, reduzindo o código necessário no Cliente.
* **Módulos:** `form.nvgt` (para `audio_form`).

---

## 💻 Descrição Detalhada da Implementação (Modelo NVGT Completo)

O desenvolvedor deve usar a classe **`audio_form`** para o controle de lista e o **Swap Direto** para a lógica de reordenação.

### Passo 1: Inicialização da UI (Seleção Múltipla e Busca por Letra)

As funcionalidades de Seleção Múltipla e Busca por Letra são ativadas na inicialização do controle de lista (`inventory_list_control`).

```nvgt
#include "form.nvgt" 
// ... (Estruturas de dados omitidas)

// Rotina de Inicialização do Inventário (Cliente)
void init_inventory_ui() {
    // 1. Cria a lista de inventário com multiselect = TRUE
    inventory_list_control = inventory_form.create_list(
        "Inventário", 
        MAX_SLOTS, 
        true, // multiselect = TRUE (Habilita Seleção Múltipla) [14]
        false
    );
    
    // 2. Ativa a Busca por Letra (Multi-navegação)
    inventory_form.set_list_multinavigation(
        inventory_list_control, 
        true,  // letters: Permite navegação por letras
        true,  // numbers: Permite navegação por números
        true   // nav_translate: Ativa a tradução
    ); [10, 16]

    // Para obter o buffer de seleção para ações (venda, descarte em lote):
    // int[]@ selected_indices = inventory_form.get_list_selections(inventory_list_control); [19-21]
}
Passo 2: Lógica de Reordenação (Swap Direto)
O código para o swap e controle de cursor é inserido no game loop para detectar o comando Alt + Seta
// =========================================================
// 1. ROTINA DE SWAP OTIMIZADO (O(1))
// =========================================================

void swap_item_positions(Item@[]@ arr, int index_a, int index_b) {
    // ... (Verificação de Limites omitida)
    // Troca Direta de Handles (O(1))
    Item@ temp = arr[index_a];
    @arr[index_a] = arr[index_b];
    @arr[index_b] = temp;
}

// =========================================================
// 2. LÓGICA DE REORDENAÇÃO E CONTROLE DE CURSOR
// =========================================================

void handle_inventory_reorder() {
    
    if (inv_items.length() <= 1) return;

    bool alt_down = key_down(KEY_LALT) || key_down(KEY_RALT);
    // Obtemos a posição atual do cursor na lista de UI. [4, 5]
    int current_pos = inventory_form.get_list_position(inventory_list_control); 
    int new_cursor_position = current_pos;
    
    if (alt_down) {
        if (key_pressed(KEY_UP)) {
            int target_index = current_pos - 1;
            
            if (target_index >= 0) {
                // Executa o swap O(1) na array de dados
                swap_item_positions(@inv_items, current_pos, target_index);
                
                // ATUALIZAÇÃO DA UI E CURSOR:
                player_inventory_cursor = target_index;
                // Move o foco da UI para o novo índice do item movido. [9-11]
                inventory_form.set_list_position(inventory_list_control, target_index, true); 
            }
        } 
        // Lógica similar para KEY_DOWN...
    }
}
✅ Critérios de Aceitação
• 
Reordenação Otimizada: A função swap_item_positions usa a troca direta de handles (O(1)).
• 
Controle de Cursor: O cursor de inventário (player_inventory_cursor) é atualizado corretamente após o swap.
• 
Seleção Múltipla: A funcionalidade é habilitada pelo parâmetro multiselect = true.
• 
Busca por Letra: A funcionalidade é habilitada por set_list_multinavigation.
• 
API de Alto Nível: O código utiliza a classe audio_form do NVGT para gerenciar a lista.
 