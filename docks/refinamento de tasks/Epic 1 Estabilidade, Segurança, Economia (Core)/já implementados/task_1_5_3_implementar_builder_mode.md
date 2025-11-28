# 🏗️ Task 1.5.3: Implementar Handlers e Lógica de Construção de Mapas (Builder Mode)

**EPIC:** Estabilidade e Funcionalidades Críticas (Epic 1)
**DOMÍNIO:** Rede / Construção / Conteúdo de Mapa
**PRIORIDADE:** ALTA
**ESFORÇO ESTIMADO:** MÉDIO-ALTO
**STATUS:** TO DO

## 🎯 Objetivo

Implementar o **handler de rede `req_builder_create_element`** no lado do Servidor. Este *handler* deve aplicar **validação rigorosa de Nível Admin** e de **Parâmetros** (X, Y, tamanho) antes de **instanciar e adicionar** o novo elemento (Ex: uma parede) à estrutura de mapa na memória.

## 📝 Contexto e Segurança

* **Risco:** O handler manipula o estado da memória do mapa do servidor, exigindo validação para evitar que dados inválidos ou *exploits* corrompam a estrutura de dados.
* **Permissão:** O acesso é restrito ao **Nível Admin 3** ou superior.
* **Persistência:** O salvamento no disco é uma etapa separada que deve usar `mutex` para I/O seguro (Task 1.1.2).
* **Arquivos:** `server/includes/network.nvgt` (para o Handler) e `server/includes/server_map.nvgt` (para a estrutura de mapa).

---

## 💻 Descrição Detalhada da Implementação (Modelo NVGT)

O desenvolvedor deve integrar este código, usando o objeto `Wall` (Parede) como modelo para todos os elementos de mapa que podem ser criados.

### Passo 1: Estruturas de Dados Essenciais

Garantir que as classes de objeto (`Wall`) e o mapa (`ServerMapInstance`) existam com as propriedades de limites e a *array* de destino.

```nvgt
// Estrutura do Mapa na Memória
class ServerMapInstance {
    // Definimos limites para validação de segurança
    const float MAP_MAX_X = 5000.0;
    const float MAP_MAX_Y = 5000.0;
    // Array para armazenar as instâncias de Parede
    Wall@[] walls; 
}
Passo 2: Implementar Handler req_builder_create_element
A função deve ser integrada ao módulo de handlers de rede e utiliza verificações em cascata para garantir a segurança antes da manipulação da memória.
// =========================================================
// HANDLER DE REDE: req_builder_create_element
// =========================================================

// Recebe o objeto do jogador e os parâmetros brutos do elemento (x, y, width, height)
void req_builder_create_element(Player@ p, float x, float y, float w, float h) {
    
    // Funções internas para feedback e interrupção (tratamento de erro)
    funcdef void send_msg_fail(const string& in msg) {
        alert("Builder Mode Falhou", p.name + ": " + msg);
        return; // Interrompe a execução
    }

    // --- 1. Validação de Segurança (Nível Admin) ---
    if (@p == null || p.admin_level < 3) {
        send_msg_fail("Permissão negada. Nível Admin 3 ou superior é exigido para construir.");
        return; 
    }

    // --- 1. Validação de Parâmetros (Formato e Limites) ---
    
    // Verifica se Largura e Altura são positivas (Lógica do Jogo)
    if (w <= 0.0 || h <= 0.0) {
        send_msg_fail("Largura e Altura devem ser maiores que zero.");
        return;
    }
    
    // Verifica se as Coordenadas estão dentro dos limites do mapa (Segurança do Mapa)
    if (x < 0.0 || y < 0.0 || x > current_map.MAP_MAX_X || y > current_map.MAP_MAX_Y) {
        send_msg_fail("Coordenadas fora dos limites seguros do mapa.");
        return;
    }

    // --- 2. Manipulação de Memória e Instanciação ---
    
    // Cria uma nova instância do objeto na memória (Handle necessário para objetos complexos) [1]
    Wall@ new_wall = Wall(x, y, w, h);
    
    // Adiciona o handle do novo objeto à array do mapa (Usamos insert_last() [2, 3])
    current_map.walls.insert_last(@new_wall);
    
    alert("Builder Sucesso", "Parede criada na memória em (" + x + ", " + y + ").");

    // --- 3. Persistência (Lembrar ao Admin) ---
    /*
    Lógica de salvamento (req_builder_save_map) deve ser executada separadamente
    e deve usar um MUTEX [4] para garantir que o acesso ao disco (I/O) seja seguro.
    */
}
Critérios de Aceitação
• 
Validação de Permissão: O código verifica p.admin_level < 3 e interrompe a execução se a permissão for insuficiente.
• 
Validação de Parâmetros: A lógica valida o formato (ex: w <= 0.0) e os limites (Ex: x > MAP_MAX_X) dos parâmetros.
• 
Instanciação Segura: O novo objeto é criado e adicionado à array do mapa usando array::insert_last().
• 
Interrupção: Qualquer falha na validação resulta em uma mensagem de erro e uma interrupção imediata da função (return).