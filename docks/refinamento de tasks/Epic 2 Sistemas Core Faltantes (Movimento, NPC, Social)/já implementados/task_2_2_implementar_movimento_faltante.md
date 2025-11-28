# 🚶 Task 2.2: Implementar Sistemas de Movimento Faltantes (Eco, Agachar, Sentar)

**EPIC:** Polimento e Sistemas Secundários (Epic 2)
**DOMÍNIO:** Cliente / Acessibilidade / Movimento
**PRIORIDADE:** MÉDIA-ALTA
**ESFORÇO ESTIMADO:** MÉDIO
**STATUS:** TO DO

## 🎯 Objetivo

Implementar a **funcionalidade de Eco** (auxílio de navegação por áudio) e os estados de **Agachar/Sentar**. Esta *task* foca em usar as APIs matemáticas e de áudio do NVGT para calcular a **distância** até um obstáculo e modular o **volume/delay** do som de retorno, garantindo a acessibilidade.

## 📝 Contexto e Solução NVGT

* **Funcionalidade de Eco:** Usa o *yaw* (rotação) do jogador e a **Fórmula Euclidiana** (via `get_2d_distance`) para calcular a distância e modular o *feedback* de áudio.
* **APIs Envolvidas:** `rotation.nvgt` (para distância e conversão de ângulo), `audio.nvgt` (para `sound::set_volume`).
* **Sistemas Adicionais:** A lógica de **Agachar/Sentar** requer a sincronização de um novo *flag* (`player_stance`) entre Cliente e Servidor via *handlers* de rede.

---

## 💻 Descrição Detalhada da Implementação (Modelo NVGT - Sistema de Eco)

O desenvolvedor deve integrar esta lógica ao loop principal do Cliente (`client.nvgt`) e garantir que os módulos `rotation.nvgt`, `audio.nvgt` e `math.nvgt` estejam incluídos.

### Passo 1: Funções de Raycasting e Geometria

A lógica de simulação de **Raycasting** é usada para encontrar onde o pulso de eco atinge a parede.

```nvgt
#include "rotation.nvgt" // Para get_2d_distance e calculate_theta
#include "math.nvgt"     // Para cos() e sin()

// Converte a rotação do jogador (p.yaw) para o formato de radianos exigido
double calculate_theta(float yaw_degrees) { /* ... implementação da API rotation.nvgt ... */ }

// Simula o lançamento de raio na direção do jogador para encontrar uma parede
RaycastHit@ simulate_raycast(Player@ p) {
    RaycastHit@ hit = RaycastHit();
    double theta = calculate_theta(p.yaw); // Converte graus para radianos
    double target_distance = MAX_ECHO_DISTANCE;

    // Se houver acerto (simulado aqui a 30.0 unidades)
    if (target_distance > 30.0) {
        hit.distance = 30.0;
        hit.hit = true;
        // Calcula o ponto de acerto usando trigonometria: X = X_inicial + Distância * cos(Theta)
        hit.x_hit = p.x + float(30.0 * cos(theta)); 
        hit.y_hit = p.y + float(30.0 * sin(theta));
    } 
    // ... (retorna hit)
    return @hit;
}
Passo 2: Função de Feedback (Modulação de Áudio)
Esta rotina dispara o som e calcula o volume e o atraso com base na distância.
// Constantes de modulação
const float MAX_ECHO_DISTANCE = 50.0;
const float MIN_VOLUME = -100.0; // Silêncio
const float MAX_VOLUME = 0.0;    // Volume Padrão

void calculate_echo_feedback(Player@ p) {
    RaycastHit@ hit = simulate_raycast(@p);
    
    if (!hit.hit || hit.distance > MAX_ECHO_DISTANCE) {
        alert("Eco", "Nenhuma parede detectada dentro do alcance.");
        return;
    }
    
    double distance = hit.distance;

    // CÁLCULO DO VOLUME (Interpolação Inversa)
    float normalized_distance = float(distance / MAX_ECHO_DISTANCE);
    float volume_range = MAX_VOLUME - MIN_VOLUME; 
    // Quanto mais próximo (menor normalized_distance), maior o volume
    float calculated_volume = MIN_VOLUME + (1.0 - normalized_distance) * volume_range; 
    
    // CÁLCULO DO DELAY (Simulação do Atraso)
    int delay_ms = int(distance * 10); 
    
    // Dispara o som de pulso
    sound@ echo_pulse = sound(); 
    echo_pulse.load(ECHO_SOUND_FILE); 
    echo_pulse.set_volume(calculated_volume); // Define o volume

    // Aplica o atraso e toca o som.
    wait(delay_ms); // Bloqueia a thread do cliente pelo tempo do atraso.
    echo_pulse.play();
    
    alert("Eco Recebido", "Distância: " + round(distance, 2) + "m. Volume: " + round(calculated_volume, 2) + "dB.");
}
Passo 3: Sincronização de Estado (Agachar/Sentar)
Implementar o flag player_stance no Servidor e o handler de rede para sincronizar os estados de Agachar e Sentar (movimento e roleplay).
 
✅ Critérios de Aceitação
• 
Sistema de Eco Funcional: O Cliente pode acionar o Eco, e o volume/delay do retorno são modulados de forma inversamente/diretamente proporcional à distância.
• 
Cálculo Correto: O código usa calculate_theta e cos/sin para simular a direção do pulso.
• 
Sincronização de Estado: O estado de Agachar/Sentar é sincronizado via handlers de rede e o objeto Player armazena o estado corretamente.
• 
Acessibilidade: O Eco fornece um meio de navegação espacial essencial para jogadores com deficiência visual.