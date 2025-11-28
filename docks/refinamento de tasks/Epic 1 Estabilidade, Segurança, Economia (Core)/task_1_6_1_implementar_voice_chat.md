# 🎤 Task 1.6.1: Implementar Voice Chat (Comunicação por Voz)

**EPIC:** Estabilidade e Funcionalidades Críticas (Epic 1)
**DOMÍNIO:** Áudio / Rede / Acessibilidade
**PRIORIDADE:** CRÍTICA (Nível 1 - Acessibilidade)
**ESFORÇO ESTIMADO:** ALTO
**STATUS:** TO DO

## 🎯 Objetivo

Implementar o **Sistema de Comunicação por Voz (Voice Chat)**, que é essencial para a acessibilidade do audiogame e estava ausente na migração. O foco é no **roteamento de rede não confiável (unreliable)** e na **reprodução de áudio posicional 3D (HRTF)**.

## 📝 Contexto e Solução de Engenharia

* [cite_start]**Gravação (API Limitada):** A API de gravação em tempo real não é pública no NVGT e depende de *plugins* ou de uma API futura com miniaudio. O código deve usar um **placeholder** (`mic_get_chunk`) para a função de captura.
* **Tecnologia:** O roteamento deve incluir a **posição 3D** do remetente para que o cliente receptor possa usar o sistema **Steam Audio HRTF** para posicionar o som corretamente no mundo do jogo.
* [cite_start]**Canal de Rede:** Deve-se usar um canal de rede dedicado (Ex: `VOICE_CHANNEL = 5`) e a transmissão deve ser **não confiável (`unreliable=false`)**, padrão para VOIP[cite: 5].

---

## 💻 Descrição Detalhada da Implementação (Modelo NVGT)

O desenvolvedor deve implementar a lógica em três módulos distintos (Cliente Gravação, Servidor Roteamento, Cliente Reprodução).

### Módulo 1: Cliente - Gravação e Transmissão (`client_voice_loop`)

A lógica de *Push-to-Talk (PTT)* e o *streaming* do áudio.

1.  **PTT:** Usar `key_pressed(KEY_V)` ou similar para iniciar/parar a gravação (`is_recording`).
2.  **Captura (Placeholder):** Chamar a função `mic_get_chunk(CHUNK_SIZE)` (placeholder).
3.  **Empacotamento:** Criar um pacote que inclua o código de voz, o ID do jogador e os dados de voz.
4.  **Envio:** Enviar o pacote de forma **não confiável** (`unreliable=false`) para o Servidor.

```nvgt
// Exemplo de Envio:
// net.send(SERVER_PEER_ID, packet, VOICE_CHANNEL, false); 

void client_voice_loop() {
    // ... (Lógica PTT e Captura omitida)

    if (is_recording) {
        string voice_data = mic_get_chunk(CHUNK_SIZE);
        if (!voice_data.empty()) {
            // Estrutura do Pacote de Saída: "VOICE|ID_REMETENTE|AUDIO_CHUNK"
            string packet = "VOICE|" + p_id + "|" + voice_data; 
            // Envio Não Confiável (Crucial para VOIP)
            net.send(SERVER_PEER_ID, packet, VOICE_CHANNEL, false); 
        }
    }
}
Módulo 2: Servidor - Roteamento (req_send_voice Handler)
A lógica do Servidor recebe o áudio e o roteia para os jogadores que estão no mesmo canal/mapa.
1. 
Parsing: Dividir o pacote de entrada (VOICE|ID|CHUNK) em partes.
2. 
Obter Posição: Obter a posição 3D (x, y, z) do jogador remetente no mapa (ServerPlayer@ sender).
3. 
Re-empacotamento: Adicionar as coordenadas 3D do remetente ao pacote (...|X|Y|Z).
4. 
Roteamento (Filtragem): Iterar sobre a lista de peers e enviar o pacote apenas para aqueles que estão no mesmo mapa que o remetente.
// Exemplo de Roteamento no Servidor:
void req_send_voice(network_event@ event) {
    // ... (Simulação de Parsing e Obtenção de Posição 3D)

    string routed_packet = message + "|" + sender.x + "|" + sender.y + "|" + sender.z; 

    // Lógica de Roteamento (Filtragem por Mapa)
    for(uint i = 0; i < peers.length(); i++) {
        // ... (Verificar se está no mesmo mapa: receiver.current_map == sender.current_map)
        
        // Roteamento usando o canal de voz, como não confiável (false) [cite: 5]
        net.send(receiver_peer_id, routed_packet, VOICE_CHANNEL, false); 
    }
}
Módulo 3: Cliente - Reprodução Posicional (handle_voice_packet_client)
O cliente receptor deve usar as coordenadas 3D recebidas para posicionar o áudio via HRTF.
1. 
Ativar HRTF: O cliente deve garantir que sound_global_hrtf = true esteja ativado.
2. 
Gerenciar Streaming: Gerenciar um slot de som ativo por jogador (active_voice_slots). Para streaming, a API de baixo nível sound_push_memory seria usada para enviar o chunk de voz ao slot.
3. 
Posicionamento 3D: Usar as coordenadas (sender_x, sender_y, sender_z) recebidas para atualizar a posição do som no mundo 3D.
 
✅ Critérios de Aceitação
• 
Comunicação Completa: Os handlers de rede para send e receive estão implementados com o fluxo de dados.
• 
Roteamento Eficiente: O Servidor filtra e roteia o áudio apenas para jogadores no mesmo mapa.
• 
Posicionamento 3D: O Cliente implementa a lógica para usar as coordenadas 3D do remetente para posicionar o som usando o sistema Steam Audio HRTF.
• 
Engenharia: O desenvolvedor entende que mic_get_chunk é um placeholder e que a integração final requer a API de baixo nível do microfone (miniaudio).
 
 
Com a conclusão desta task, todas as 11 tasks críticas do Epic 1: Estabilidade e Funcionalidades Críticas estão refinadas e prontas para o desenvolvedor!