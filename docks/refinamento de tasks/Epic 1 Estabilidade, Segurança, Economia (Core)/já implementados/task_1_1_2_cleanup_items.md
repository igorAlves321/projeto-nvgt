\# 🗑️ Task 1.1.2: Implementar cleanup\_expired\_items()



\*\*EPIC:\*\* Estabilidade e Funcionalidades Críticas (Epic 1)

\*\*DOMÍNIO:\*\* Servidor / Performance / Conteúdo de Mapa

\*\*PRIORIDADE:\*\* ALTA

\*\*ESFORÇO ESTIMADO:\*\* MÉDIO

\*\*STATUS:\*\* TO DO



\## 🎯 Objetivo



Implementar a função `cleanup\_expired\_items\_task()` no lado do servidor. O objetivo é \*\*varrer todos os arquivos de mapa (`maps/\*.map`)\*\* para \*\*remover e desalocar\*\* objetos coletáveis (`MapObject`) que atingiram o tempo limite de permanência no chão. Esta função é vital para \*\*manter a saúde da memória do servidor\*\* e limpar o lixo digital dos mapas persistentes.



\## 📝 Referências e Contexto



\* \*\*Necessidade:\*\* A função `cleanup\_expired\_items()` é chamada no \*main loop\*, mas sua lógica está faltando.

\* \*\*Sistema de Mapa:\*\* O mapa é persistente e armazenado em \*\*arquivos (`.map`) no disco\*\*, o que exige I/O (leitura/escrita) durante a limpeza.

\* \*\*Arquivos Relevantes:\*\*

&nbsp;   \* `server/server.nvgt` (Onde a função é chamada/agendada).

&nbsp;   \* `include/file\_contents.nvgt` (Para I/O de disco: `file\_get\_contents`, `file\_put\_contents`).

&nbsp;   \* `server/includes/server\_map.nvgt` (Para classes de mapa).



---



\## 💻 Descrição Detalhada da Implementação (Passo a Passo)



O desenvolvedor deverá implementar a lógica de limpeza utilizando a API de I/O de arquivo e garantindo a segurança de \*thread\* durante o acesso ao disco.



\### Passo 1: Configurar Sincronização e I/O



1\.  \*\*Incluir Dependências:\*\* Garantir que os includes necessários para I/O de arquivo e \*threading\* estejam presentes (ex: `#include "file\_contents.nvgt"`, `#include "speech.nvgt"`).

2\.  \*\*Definir Mutex:\*\* Declarar um \*\*`mutex` global\*\* (ex: `map\_global\_mutex`) para proteger o acesso e a escrita dos arquivos de mapa no disco.



&nbsp;   ```nvgt

&nbsp;   mutex map\_global\_mutex; 

&nbsp;   ```



\### Passo 2: Criar a Função de Limpeza (`cleanup\_expired\_items\_task`)



Esta função será executada de forma \*\*assíncrona\*\* (`async`) no lado do servidor.



1\.  \*\*Bloquear o Mutex:\*\* Iniciar a função com \*\*`map\_global\_mutex.lock()`\*\*.

2\.  \*\*Listar Arquivos:\*\* Usar a função \*\*`glob("maps/\*.map")`\*\* do NVGT para listar todos os arquivos de mapa a serem processados.



\### Passo 3: Implementar o Fluxo de Varredura e Persistência



Dentro do \*loop\* sobre os arquivos listados (`map\_files`):



1\.  \*\*Ler:\*\* Usar \*\*`file\_get\_contents(filename)`\*\* para carregar o conteúdo do arquivo `.map` para uma \*string\*.

2\.  \*\*Desserializar:\*\* Criar uma instância de `MapInstance` e chamar um método (ex: `load\_from\_file\_content`) para popular a \*array\* de objetos (`objs\[]`) na memória, simulando a desserialização do formato do mapa.

3\.  \*\*Varredura Reversa (Limpeza):\*\* Iterar sobre a \*array\* de objetos (`current\_map.objs\[]`) \*\*de trás para frente\*\* (`for(int i = length() - 1; i >= 0; i--)`).

&nbsp;   \* Verificar `item.expiration\_time <= current\_time`.

&nbsp;   \* Se expirado, usar \*\*`current\_map.objs.remove\_at(i)`\*\* e marcar o mapa como modificado (`is\_dirty = true`).



4\.  \*\*Serializar e Escrever:\*\* Se o mapa foi modificado (`is\_dirty`), chamar um método de serialização (ex: `serialize\_to\_string`) e usar \*\*`file\_put\_contents(filename, updated\_content, false)`\*\* para gravar os dados de volta no arquivo.



5\.  \*\*Desbloquear:\*\* Garantir que, após o \*loop\* de arquivos, o \*\*`map\_global\_mutex.unlock()`\*\* seja chamado.



---



\### Exemplo de Lógica Principal de Varredura (Passo 3)



O desenvolvedor pode usar esta estrutura como base para a lógica central da varredura:



```nvgt

void cleanup\_expired\_items\_task() {

&nbsp;   map\_global\_mutex.lock(); 

&nbsp;   int64 current\_time = ticks();

&nbsp;   string\[]@ map\_files = glob("maps/\*.map"); 



&nbsp;   for(uint i = 0; i < map\_files.length(); i++) {

&nbsp;       string filename = map\_files\[i];

&nbsp;       

&nbsp;       string map\_content = file\_get\_contents(filename);

&nbsp;       if (map\_content.is\_empty()) continue; 

&nbsp;       

&nbsp;       MapInstance@ current\_map = MapInstance(filename);

&nbsp;       current\_map.load\_from\_file\_content(map\_content); // Simulação de desserialização



&nbsp;       // Varredura Reversa: CRÍTICA para a remoção segura

&nbsp;       for(int item\_index = current\_map.objs.length() - 1; item\_index >= 0; item\_index--) { 

&nbsp;           MapObject@ item = current\_map.objs\[item\_index];

&nbsp;           if (item.expiration\_time <= current\_time) {

&nbsp;               current\_map.objs.remove\_at(item\_index);

&nbsp;               current\_map.is\_dirty = true;

&nbsp;           }

&nbsp;       }

&nbsp;       

&nbsp;       // Persistência: Salvar no disco se houver alterações

&nbsp;       if (current\_map.is\_dirty) {

&nbsp;           string updated\_content = current\_map.serialize\_to\_string();

&nbsp;           file\_put\_contents(filename, updated\_content, false); 

&nbsp;       }

&nbsp;   }

&nbsp;   

&nbsp;   map\_global\_mutex.unlock();

}

