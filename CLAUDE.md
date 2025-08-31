Atue como um desenvolvedor sênior de audio games, especialista em BGT e NVGT. Sua missão é planejar (sem alterar código neste momento) a migração completa de um projeto existente em BGT para NVGT, seguindo estritamente a documentação oficial do NVGT.
Importante: Nesta primeira fase, não escreva nem modifique código-fonte. Foque em análise e planejamento. Toda recomendação deve citar a seção correspondente da documentação do NVGT (use links/seções quando disponíveis).
Entradas e Premissas
• 
Repositório raiz: [REPO_ROOT] (use o ambiente do Claude Code para ler todos os arquivos).
• 
Documentação NVGT: [DOC_URL_NVGT] ou /docs do repositório (se houver).
• 
Linguagem de saída: Português do Brasil (pt-BR).
• 
Contexto: projeto possivelmente com cliente/servidor (se existir, identificar claramente limites e contratos entre eles).
Entregáveis desta fase (apenas texto/artefatos de análise)
Produza um relatório em Markdown com as seções abaixo, nesta ordem:
1. 
Resumo Executivo do Projeto
• 
Finalidade do jogo/sistema.
• 
Plataformas-alvo (Windows/Linux/macOS).
• 
Principais features de áudio, TTS, entrada, rede, filesystem, timers, UI, etc.
• 
Pontos sensíveis (performance de áudio/latência, dependências nativas, etc.).
2. 
Inventário do Código
• 
Árvore de diretórios e arquivos relevantes (com extensões), destacando scripts BGT, módulos/utilitários, assets (áudio, configs), build scripts.
• 
Tamanho aproximado (linhas por módulo).
• 
Grafo de dependências entre arquivos/módulos (quem importa/usa quem).
• 
Mapa de camadas (ex.: Core, Áudio/TTS, Input, Rede, Gameplay, Persistência, UI/CLI).
3. 
Contratos e Fronteiras (Cliente/Servidor) (se aplicável)
• 
Identifique onde está o cliente e o servidor.
• 
Protocolo de comunicação (TCP/UDP/WebSocket/etc.), portas, handshake, autenticação, serialização (texto/binário/JSON).
• 
Esquema de mensagens (tipos, campos, direção, frequência).
• 
Dependências específicas do ambiente (bibliotecas, SO, permissões).
4. 
Matriz de Migração BGT → NVGT (por capacidade)
Crie uma tabela com colunas:
• 
Capacidade (Áudio, TTS, Entrada/Teclado/Mouse, Rede/Socket, Temporização, Arquivos/FS, Threads/Concorrência, Aleatoriedade, Log/Diagnóstico, Build/Distribuição, Configuração, Internacionalização, etc.)
• 
API/uso atual em BGT (funções, módulos, padrões de uso, pontos de entrada)
• 
Equivalente recomendado em NVGT (classe/função/módulo NVGT) com referência à documentação (seção/link)
• 
Notas de compatibilidade (diferenças de comportamento, limites, deprecações)
• 
Risco (Baixo/Médio/Alto) e complexidade (1–5)
5. 
Lacunas e Adaptações Necessárias
• 
Onde não existe equivalente direto no NVGT, proponha adapters/shims e descreva a interface.
• 
Itens que exigem refatoração de arquitetura (ex.: loop principal, modelo de eventos, threading).
• 
Restrições do NVGT citando documentação.
6. 
Plano de Ação Detalhado e Ordem Lógica de Conversão
Apresente um roadmap sequencial, com justificativa técnica para a ordem. Inclua:
• 
Ponto de partida: cliente ou servidor (explique a escolha considerando dependências, risco e testabilidade).
• 
Fases (exemplo):
1. 
Preparação do ambiente NVGT (build, tooling, lint, CI)
2. 
Camada de Fundamentos (logging, configuração, utilitários, adapters)
3. 
Infra de Áudio/TTS (provar que reproduz/loca e fala com latência adequada)
4. 
Entrada/Controles
5. 
Temporização/Loop de Jogo
6. 
Persistência/FS
7. 
Rede (protocolos, reconexão, heartbeat, compressão se houver)
8. 
Gameplay/Regra de Negócio
9. 
UI/CLI
10. 
Empacotamento/Distribuição
• 
Para cada fase, liste arquivos afetados, dependências precedentes, critérios de pronto e testes mínimos.
• 
Aponte arquivos/ módulos que bloqueiam outros (nós críticos do grafo) para definir a sequência.
7. 
Checklist de Conformidade com a Documentação NVGT
• 
Para cada capacidade usada, cite a seção exata da doc NVGT que será seguida.
• 
Itens de segurança/estabilidade (tratamento de erros, limites de buffer, threads seguros).
• 
Itens de performance (latência de áudio, uso de threads, timers).
• 
APIs NVGT deprecadas a evitar.
8. 
Estratégia de Testes e Paridade de Comportamento
• 
Testes de fumaça por capacidade (áudio reproduz?, TTS fala?, eventos de input?), com exemplos de casos.
• 
Testes de contrato cliente↔servidor (validação de payload e ordem de mensagens).
• 
Oráculos de paridade: como verificar que o comportamento migrado é idêntico ao do BGT (logs comparáveis, gravações de áudio, scripts de simulação de input).
• 
Métricas de aceitação (latência máxima, taxa de erro, estabilidade por N minutos).
9. 
Riscos, Mitigações e Plano de Rollback
• 
Riscos técnicos por área (rede, áudio, TTS, loop, assets).
• 
Mitigações propostas e pontos de controle.
• 
Como isolar mudanças (branches/feature flags/adapters) e rollback.
10. 
Próximas Ações Concretas
• 
Lista numerada das 3–7 primeiras tarefas imediatamente executáveis (ex.: “Gerar grafo de dependências”, “Levantar APIs NVGT para áudio”, “Escrever adapters de logging”).
• 
Cada tarefa com objetivo, insumos, saída esperada.
Método de Trabalho (como você deve proceder)
1. 
Varrer o repositório
• 
Liste todos os arquivos e classifique por papel (cliente, servidor, comum, assets, build, docs).
• 
Identifique pontos de entrada (main/loop) e inicializações de subsistemas (áudio, TTS, input, rede).
• 
Extraia assinaturas de funções e chamadas cruzadas importantes para o grafo.
2. 
Ler a documentação NVGT
• 
Para cada capacidade usada no BGT, localize o equivalente NVGT e anote requisitos/limitações.
• 
Registre links/seções específicos a serem citados no relatório.
3. 
Construir a Matriz BGT→NVGT (Seção 4)
• 
Preencher com exemplos concretos do projeto (trechos/identificadores e caminhos de arquivo).
4. 
Definir Ordem de Conversão (Seção 6)
• 
Baseie-se no grafo de dependências e na testabilidade.
• 
Se cliente e servidor existirem, prefira começar por aquele que:
• 
Possui menos dependências externas;
• 
Permite testes isolados mais cedo;
• 
Destrava mais módulos dependentes.
• 
Justifique a decisão com dados do inventário.
5. 
Produzir o Relatório Final
• 
Entregar as 10 seções acima, em Markdown, com tabelas quando couber.
• 
Sem alterações de código nesta fase.
• 
Inclua um sumário no topo com links âncora para cada seção.
Formato e Qualidade da Saída
• 
Use títulos #, ##, ###, listas, tabelas e blocos de código para trechos curtos de exemplo (sem alterar arquivos).
• 
Cite caminhos absolutos/relativos dos arquivos ao mencioná-los.
• 
Ao referenciar a documentação do NVGT, inclua link/ seção entre parênteses.
• 
Seja objetivo, técnico e verificável.
• 
Sinalize incertezas/lacunas explicitamente.
Critérios de Aceitação
• 
Todas as 10 seções entregues, completas e coerentes.
• 
Matriz BGT→NVGT com pelo menos 1 mapeamento por capacidade usada no projeto.
• 
Ordem de conversão justificada pelo grafo de dependências.
• 
Pelo menos 5 testes de fumaça e 3 testes de contrato propostos.
• 
Checklist de conformidade com doc NVGT com referências explícitas.
 
Quando terminar, apresente o relatório completo. Se algum insumo estiver ausente (ex.: link exato da doc NVGT), cite as lacunas na seção “Lacunas e Adaptações Necessárias” e prossiga com o melhor 