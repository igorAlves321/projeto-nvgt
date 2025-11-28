\# 🗺️ Task 1.3.1: Parsing Completo de Mapas no Servidor (43 Tipos)



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Servidor / Conteúdo de Mapa / Integridade de Dados

\*\*PRIORIDADE:\*\* CRÍTICA (Nível 1)

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar o \*parsing\* completo de todos os \*\*43 tipos de elementos de mapa\*\* no lado do servidor. O servidor processa apenas 15-16 tipos, criando um \*\*gap de implementação\*\* de \*\*cerca de 27-28 tipos\*\* de elementos. A falha nessa implementação causa inconsistência e risco de \*exploits\*.



\## 📝 Referências e Contexto



\* \*\*Gap de Implementação:\*\* Cliente suporta 43 tipos de elementos (ex: `dlg`, `texto`, `am`), mas o Servidor só reconhece 15-16.

\* \*\*Arquivos Relevantes:\*\* `server/includes/server\_map.nvgt` (lógica de parsing) e `cliente/includes/map.nvgt` (lista completa dos 43 tipos).

\* \*\*Modelo de Parsing:\*\* O código a seguir utiliza o elemento \*\*`sound\_source` (`ss`)\*\* como modelo para a implementação dos tipos faltantes.



---



\## 💻 Descrição Detalhada da Implementação (Modelo NVGT)



O desenvolvedor deve aplicar a lógica de \*\*Reconhecimento, Validação Rígida e Armazenamento\*\* de forma modular, seguindo o padrão abaixo para cada um dos 27-28 tipos de elementos faltantes.



\### Passo 1: Configurar Classes e Constantes



1\.  \*\*Definir Classes:\*\* Criar as classes necessárias para os novos elementos (ex: `SoundSource`, `DialogObject`, `QuickSandZone`).

2\.  \*\*Definir Constantes:\*\* Criar constantes para o código do elemento e o número mínimo de parâmetros esperados (Ex: `SOUND\_SOURCE\_CODE = "ss"`).



\### Passo 2: Implementar a Rotina de Parsing (`parse\_map\_line`)



A lógica deve ser inserida na função de carga de mapa do servidor, que processa cada linha do arquivo `.map`.



```nvgt

// =========================================================

// MÓDULO DE PARSING DE LINHA (Exemplo para SoundSource)

// =========================================================



// Códigos de Elementos

const string SOUND\_SOURCE\_CODE = "ss";

const int SOUND\_SOURCE\_MIN\_PARAMS = 4; // Parâmetros esperados (X, Y, Arquivo, Raio)



// Função que processa cada linha lida do arquivo .map

void parse\_map\_line(ServerMapInstance@ current\_map, const string\& in map\_line) {

&nbsp;   if (@current\_map == null || map\_line.empty()) return;



&nbsp;   // 1. Dividir a linha em tokens/argumentos (tokens\[0] será o código do elemento)

&nbsp;   string\[]@ tokens = map\_line.split(" ", true);

&nbsp;   if (@tokens == null || tokens.length() == 0) return;



&nbsp;   string element\_code = tokens\[0]; // O primeiro token é o código do elemento

&nbsp;   

&nbsp;   // --- 1. RECONHECIMENTO (Adicionar 'else if' para os 27-28 tipos faltantes) ---

&nbsp;   if (element\_code == SOUND\_SOURCE\_CODE) {

&nbsp;       

&nbsp;       // --- 2. VALIDAÇÃO RÍGIDA DE PARÂMETROS ---

&nbsp;       

&nbsp;       // A. Validação de Quantidade de Argumentos

&nbsp;       if (tokens.length() != SOUND\_SOURCE\_MIN\_PARAMS + 1) {

&nbsp;           alert("Erro de Parsing", "Elemento 'ss' com número incorreto de argumentos.");

&nbsp;           return;

&nbsp;       }



&nbsp;       // B. Tipagem e Limites (Validação de coordenadas e raio)

&nbsp;       // O código de produção deve incluir string::is\_float/is\_number antes de parse\_float

&nbsp;       float x = parse\_float(tokens\[1]);

&nbsp;       float y = parse\_float(tokens\[2]);

&nbsp;       string sound\_name = tokens\[3];

&nbsp;       float radius = parse\_float(tokens\[4]);



&nbsp;       // Verificação de Limites do Mapa e Lógicos (Exemplo de X, Y, Raio)

&nbsp;       if (x < 0 || x > current\_map.MAP\_MAX\_X || y < 0 || y > current\_map.MAP\_MAX\_Y) {

&nbsp;           alert("Erro de Parsing", "SoundSource fora dos limites do mapa.");

&nbsp;           return;

&nbsp;       }

&nbsp;       if (radius <= 0 || radius > 1000) {

&nbsp;           alert("Erro de Parsing", "SoundSource com raio inválido.");

&nbsp;           return;

&nbsp;       }

&nbsp;       

&nbsp;       // C. Validação de Conteúdo (Ex: Nome do arquivo)

&nbsp;       if (sound\_name.empty() || !sound\_name.ends\_with(".ogg")) {

&nbsp;           alert("Erro de Parsing", "Nome de arquivo de som inválido.");

&nbsp;           return;

&nbsp;       }



&nbsp;       // --- 3. INSTANCIAÇÃO E ARMAZENAMENTO ---



&nbsp;       // Cria o novo objeto SoundSource

&nbsp;       SoundSource@ new\_source = SoundSource();

&nbsp;       new\_source.x = x;

&nbsp;       new\_source.y = y;

&nbsp;       new\_source.sound\_file = sound\_name;

&nbsp;       new\_source.radius = radius;



&nbsp;       // Adiciona a nova instância ao array do mapa (inserir na array correta)

&nbsp;       current\_map.sound\_sources.insert\_last(@new\_source); 

&nbsp;       alert("Parsing Sucesso", "SoundSource " + sound\_name + " instanciado.");



&nbsp;   } else if (element\_code == "sz") {

&nbsp;       // Lógica para SafeZone (Já existente ou a ser implementada)...

&nbsp;   } else {

&nbsp;       // ...

&nbsp;   }

}

