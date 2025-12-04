// ============================================================
// Índice de todas as ferramentas MCP
// ============================================================

import type { ToolDefinition, ToolResult, ToolCall } from '../types/mcp.types.js';
import { toolConvertBgtFile } from './convert-file.tool.js';
import { toolConvertBgtCode } from './convert-code.tool.js';
import { toolListBgtFiles } from './list-files.tool.js';
import { toolGetConversionRules } from './get-rules.tool.js';
import { toolConvertAllBgtFiles } from './convert-all.tool.js';
import { toolGetNvgtExamples } from './get-nvgt-examples.tool.js';
import { 
  searchGithubIssues, 
  searchGithubCode, 
  getGithubFile, 
  listGithubDirectory,
  searchNvgtDocumentation 
} from './github-search.tool.js';

/**
 * Definições de todas as ferramentas disponíveis
 */
export const toolDefinitions: ToolDefinition[] = [
  {
    name: "convert_bgt_file",
    description: "Converte um arquivo .bgt para .nvgt aplicando todas as regras de conversão conhecidas",
    inputSchema: {
      type: "object",
      properties: {
        file: { type: "string", description: "Caminho do arquivo .bgt a converter (relativo ao projeto)" },
        save: { type: "string", description: "Se 'true', salva o arquivo convertido. Se 'false' ou omitido, retorna apenas o resultado" }
      },
      required: ["file"]
    }
  },
  {
    name: "convert_bgt_code",
    description: "Converte um trecho de código BGT para NVGT",
    inputSchema: {
      type: "object",
      properties: {
        code: { type: "string", description: "Código BGT a ser convertido" }
      },
      required: ["code"]
    }
  },
  {
    name: "list_bgt_files",
    description: "Lista todos os arquivos .bgt no projeto",
    inputSchema: {
      type: "object",
      properties: {
        directory: { type: "string", description: "Diretório específico para buscar (opcional)" }
      }
    }
  },
  {
    name: "get_conversion_rules",
    description: "Retorna todas as regras de conversão disponíveis organizadas por categoria",
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Filtrar por categoria (opcional): includes, types, arrays, strings, files, audio, timers, keyboard, network, general, speech, database, ui, containers, handles, datetime" }
      }
    }
  },
  {
    name: "convert_all_bgt_files",
    description: "Converte todos os arquivos .bgt do projeto para .nvgt",
    inputSchema: {
      type: "object",
      properties: {
        dryRun: { type: "string", description: "Se 'true', apenas simula a conversão sem salvar arquivos" }
      }
    }
  },
  {
    name: "get_nvgt_examples",
    description: "Retorna exemplos práticos de código mostrando diferenças BGT vs NVGT",
    inputSchema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Categoria: all (lista), basic_types, arrays, strings, sound, files, network, timers, datetime, math, handles, complete_example" }
      }
    }
  },
  {
    name: "search_github_issues",
    description: "Busca issues no repositório oficial do NVGT (samtupy/nvgt) - útil para encontrar bugs conhecidos e soluções",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Termo de busca (ex: 'BGT compatibility', 'sound', 'network')" },
        state: { type: "string", description: "Estado das issues: 'open', 'closed' ou 'all' (padrão: all)" }
      },
      required: ["query"]
    }
  },
  {
    name: "search_github_code",
    description: "Busca código no repositório NVGT - útil para ver implementações reais",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Termo de busca no código" },
        extension: { type: "string", description: "Filtrar por extensão: nvgt, md, cpp, etc." }
      },
      required: ["query"]
    }
  },
  {
    name: "get_github_file",
    description: "Lê o conteúdo de um arquivo específico do repositório NVGT",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Caminho do arquivo (ex: 'doc/src/appendix/Migrating From BGT.md')" },
        branch: { type: "string", description: "Branch (padrão: main)" }
      },
      required: ["path"]
    }
  },
  {
    name: "list_github_directory",
    description: "Lista arquivos e diretórios no repositório NVGT",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string", description: "Caminho do diretório (ex: 'doc/src', 'include')" },
        branch: { type: "string", description: "Branch (padrão: main)" }
      }
    }
  },
  {
    name: "get_nvgt_documentation",
    description: "Busca documentação do NVGT por tópico (migration, sound, timer, file, string, array, network, speech, keyboard, etc.)",
    inputSchema: {
      type: "object",
      properties: {
        topic: { type: "string", description: "Tópico: migration, bgt, sound, timer, file, string, array, network, speech, keyboard, datetime, math" }
      },
      required: ["topic"]
    }
  }
];

/**
 * Dispatcher que chama a ferramenta apropriada
 */
export async function dispatchTool(call: ToolCall, projectRoot: string): Promise<ToolResult> {
  switch (call.name) {
    case 'convert_bgt_file':
      return toolConvertBgtFile(call.args, projectRoot);
    case 'convert_bgt_code':
      return toolConvertBgtCode(call.args);
    case 'list_bgt_files':
      return toolListBgtFiles(call.args, projectRoot);
    case 'get_conversion_rules':
      return toolGetConversionRules(call.args);
    case 'convert_all_bgt_files':
      return toolConvertAllBgtFiles(call.args, projectRoot);
    case 'get_nvgt_examples':
      return toolGetNvgtExamples(call.args);
    case 'search_github_issues':
      return await searchGithubIssues(call.args);
    case 'search_github_code':
      return await searchGithubCode(call.args);
    case 'get_github_file':
      return await getGithubFile(call.args);
    case 'list_github_directory':
      return await listGithubDirectory(call.args);
    case 'get_nvgt_documentation':
      return await searchNvgtDocumentation(call.args);
    default:
      return { success: false, error: `Ferramenta desconhecida: ${call.name}` };
  }
}
