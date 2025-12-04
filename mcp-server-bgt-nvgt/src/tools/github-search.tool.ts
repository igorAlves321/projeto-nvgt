import type { ToolResult } from '../types/mcp.types.js';
import https from 'https';

// Tipos para os argumentos das funções
interface GithubIssuesArgs {
  query: string;
  state?: string;
}

interface GithubCodeArgs {
  query: string;
  extension?: string;
}

interface GithubFileArgs {
  path: string;
  branch?: string;
}

interface GithubDirectoryArgs {
  path?: string;
  branch?: string;
}

interface NvgtDocArgs {
  topic: string;
}

/**
 * Faz requisição HTTPS GET
 */
function fetchUrl(url: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const options = {
      headers: {
        'User-Agent': 'MCP-BGT-NVGT-Converter/1.0',
        'Accept': 'application/vnd.github.v3+json'
      }
    };

    https.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          resolve(data);
        } else if (res.statusCode === 403) {
          reject(new Error('Rate limit atingido. Tente novamente em alguns minutos.'));
        } else if (res.statusCode === 404) {
          reject(new Error('Recurso não encontrado no GitHub.'));
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
      res.on('error', reject);
    }).on('error', reject);
  });
}

/**
 * Busca issues no repositório NVGT
 */
export async function searchGithubIssues(args: Record<string, unknown>): Promise<ToolResult> {
  try {
    const { query, state = 'all' } = args as unknown as GithubIssuesArgs;
    const searchQuery = encodeURIComponent(`${query} repo:samtupy/nvgt is:issue state:${state}`);
    const url = `https://api.github.com/search/issues?q=${searchQuery}&per_page=10`;

    const response = await fetchUrl(url);
    const data = JSON.parse(response);

    if (data.total_count === 0) {
      return {
        success: true,
        output: {
          query: query,
          found: false,
          message: 'Nenhuma issue encontrada.',
          suggestion: 'Tente termos diferentes ou verifique a documentação diretamente.'
        }
      };
    }

    const issues = data.items.map((issue: any) => ({
      number: issue.number,
      title: issue.title,
      state: issue.state,
      url: issue.html_url,
      created: issue.created_at,
      labels: issue.labels.map((l: any) => l.name),
      body_preview: issue.body?.substring(0, 200) + (issue.body?.length > 200 ? '...' : '')
    }));

    return {
      success: true,
      output: {
        query: query,
        found: true,
        total: data.total_count,
        showing: issues.length,
        issues: issues
      }
    };

  } catch (error: any) {
    return {
      success: false,
      error: `Erro ao buscar issues: ${error?.message || error}`
    };
  }
}

/**
 * Busca código no repositório NVGT
 */
export async function searchGithubCode(args: Record<string, unknown>): Promise<ToolResult> {
  try {
    const { query, extension } = args as unknown as GithubCodeArgs;
    let searchQuery = `${query} repo:samtupy/nvgt`;
    if (extension) {
      searchQuery += ` extension:${extension}`;
    }
    
    const url = `https://api.github.com/search/code?q=${encodeURIComponent(searchQuery)}&per_page=10`;

    const response = await fetchUrl(url);
    const data = JSON.parse(response);

    if (data.total_count === 0) {
      return {
        success: true,
        output: {
          query: query,
          found: false,
          message: 'Nenhum código encontrado.',
          suggestion: 'Tente termos diferentes.'
        }
      };
    }

    const results = data.items.map((item: any) => ({
      name: item.name,
      path: item.path,
      url: item.html_url,
      repository: item.repository.full_name
    }));

    return {
      success: true,
      output: {
        query: query,
        found: true,
        total: data.total_count,
        showing: results.length,
        files: results
      }
    };

  } catch (error: any) {
    return {
      success: false,
      error: `Erro ao buscar código: ${error?.message || error}`
    };
  }
}

/**
 * Lê arquivo raw do repositório NVGT
 */
export async function getGithubFile(args: Record<string, unknown>): Promise<ToolResult> {
  try {
    const { path, branch = 'main' } = args as unknown as GithubFileArgs;
    const url = `https://raw.githubusercontent.com/samtupy/nvgt/${branch}/${path}`;

    const content = await fetchUrl(url);

    return {
      success: true,
      output: {
        path: path,
        branch: branch,
        content: content,
        url: `https://github.com/samtupy/nvgt/blob/${branch}/${path}`
      }
    };

  } catch (error: any) {
    return {
      success: false,
      error: `Erro ao ler arquivo: ${error?.message || error}`
    };
  }
}

/**
 * Lista arquivos de um diretório no repositório NVGT
 */
export async function listGithubDirectory(args: Record<string, unknown>): Promise<ToolResult> {
  try {
    const { path = '', branch = 'main' } = args as GithubDirectoryArgs;
    const url = `https://api.github.com/repos/samtupy/nvgt/contents/${path}?ref=${branch}`;

    const response = await fetchUrl(url);
    const data = JSON.parse(response);

    if (!Array.isArray(data)) {
      return {
        success: false,
        error: 'Caminho não é um diretório ou não existe.'
      };
    }

    const items = data.map((item: any) => ({
      name: item.name,
      type: item.type, // 'file' ou 'dir'
      path: item.path,
      size: item.size,
      url: item.html_url
    }));

    return {
      success: true,
      output: {
        path: path || '/',
        branch: branch,
        count: items.length,
        items: items
      }
    };

  } catch (error: any) {
    return {
      success: false,
      error: `Erro ao listar diretório: ${error?.message || error}`
    };
  }
}

/**
 * Busca na documentação online do NVGT (nvgt.gg/docs)
 */
export async function searchNvgtDocumentation(args: Record<string, unknown>): Promise<ToolResult> {
  try {
    const { topic } = args as unknown as NvgtDocArgs;
    
    // Mapeamento de tópicos para URLs da documentação online
    const docUrls: Record<string, { url: string; description: string }> = {
      // Migração e introdução
      'migration': { 
        url: 'https://nvgt.gg/docs/advanced/BGT%20Upgrading%20Tutorial/',
        description: 'Guia de migração BGT para NVGT'
      },
      'bgt': { 
        url: 'https://nvgt.gg/docs/advanced/BGT%20Upgrading%20Tutorial/',
        description: 'Tutorial de upgrade do BGT'
      },
      'introduction': { 
        url: 'https://nvgt.gg/docs/',
        description: 'Introdução ao NVGT'
      },
      'getting_started': { 
        url: 'https://nvgt.gg/docs/manual/Getting%20Started/',
        description: 'Primeiros passos com NVGT'
      },
      
      // Tipos e containers
      'array': { 
        url: 'https://nvgt.gg/docs/references/builtin/Datatypes/array/',
        description: 'Documentação de arrays'
      },
      'dictionary': { 
        url: 'https://nvgt.gg/docs/references/builtin/Datatypes/dictionary/',
        description: 'Documentação de dicionários'
      },
      'string': { 
        url: 'https://nvgt.gg/docs/references/builtin/Datatypes/string/',
        description: 'Documentação de strings'
      },
      
      // Áudio
      'sound': { 
        url: 'https://nvgt.gg/docs/references/builtin/Audio/sound/',
        description: 'Classe sound para áudio'
      },
      'audio': { 
        url: 'https://nvgt.gg/docs/references/builtin/Audio/',
        description: 'Sistema de áudio do NVGT'
      },
      'mixer': { 
        url: 'https://nvgt.gg/docs/references/builtin/Audio/mixer/',
        description: 'Mixer de áudio'
      },
      
      // Rede
      'network': { 
        url: 'https://nvgt.gg/docs/references/builtin/Networking/',
        description: 'Sistema de rede do NVGT'
      },
      
      // Data e tempo
      'timer': { 
        url: 'https://nvgt.gg/docs/references/builtin/Date%20and%20Time/timer/',
        description: 'Classe timer'
      },
      'datetime': { 
        url: 'https://nvgt.gg/docs/references/builtin/Date%20and%20Time/',
        description: 'Data e hora'
      },
      'calendar': { 
        url: 'https://nvgt.gg/docs/references/builtin/Date%20and%20Time/calendar/',
        description: 'Funções de calendário'
      },
      
      // Sistema de arquivos
      'file': { 
        url: 'https://nvgt.gg/docs/references/builtin/Filesystem/',
        description: 'Sistema de arquivos'
      },
      
      // Interface
      'keyboard': { 
        url: 'https://nvgt.gg/docs/references/builtin/User%20Interface/Keyboard/',
        description: 'Input de teclado'
      },
      'input': { 
        url: 'https://nvgt.gg/docs/references/builtin/User%20Interface/',
        description: 'Interface de usuário'
      },
      
      // Speech
      'speech': { 
        url: 'https://nvgt.gg/docs/references/include/speech/',
        description: 'Text-to-speech'
      },
      'tts': { 
        url: 'https://nvgt.gg/docs/references/include/speech/',
        description: 'Text-to-speech'
      },
      
      // Matemática
      'math': { 
        url: 'https://nvgt.gg/docs/references/builtin/Mathematical/',
        description: 'Funções matemáticas'
      }
    };

    const topicLower = topic.toLowerCase();
    const docInfo = docUrls[topicLower];

    if (!docInfo) {
      return {
        success: true,
        output: {
          topic: topic,
          found: false,
          message: `Tópico "${topic}" não mapeado diretamente.`,
          availableTopics: Object.keys(docUrls),
          mainDocs: 'https://nvgt.gg/docs/',
          apiReference: 'https://nvgt.gg/docs/references/',
          suggestion: 'Consulte a documentação principal ou use search_github_code para buscar no código fonte.'
        }
      };
    }

    // Tenta buscar o conteúdo da página
    try {
      const content = await fetchUrl(docInfo.url);
      
      // Extrai o conteúdo principal (remove HTML tags básicas)
      const cleanContent = content
        .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
        .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
        .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '')
        .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, '')
        .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '')
        .replace(/<[^>]+>/g, ' ')
        .replace(/\s+/g, ' ')
        .trim()
        .substring(0, 5000); // Limita tamanho

      return {
        success: true,
        output: {
          topic: topic,
          found: true,
          description: docInfo.description,
          url: docInfo.url,
          content: cleanContent,
          relatedLinks: {
            mainDocs: 'https://nvgt.gg/docs/',
            apiReference: 'https://nvgt.gg/docs/references/',
            github: 'https://github.com/samtupy/nvgt'
          }
        }
      };
    } catch (fetchError) {
      // Se não conseguir buscar, retorna só o link
      return {
        success: true,
        output: {
          topic: topic,
          found: true,
          description: docInfo.description,
          url: docInfo.url,
          note: 'Não foi possível buscar o conteúdo. Acesse o link diretamente.',
          relatedLinks: {
            mainDocs: 'https://nvgt.gg/docs/',
            apiReference: 'https://nvgt.gg/docs/references/'
          }
        }
      };
    }

  } catch (error: any) {
    return {
      success: false,
      error: `Erro ao buscar documentação: ${error?.message || error}`
    };
  }
}
