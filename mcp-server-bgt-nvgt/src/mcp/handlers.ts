// ============================================================
// Handlers de requisições MCP
// ============================================================

import type { MCPRequest, MCPResponse } from '../types/mcp.types.js';
import { toolDefinitions, dispatchTool } from '../tools/index.js';
import { createSuccessResponse, createErrorResponse, ErrorCodes } from './protocol.js';
import { totalRules } from '../rules/index.js';

/**
 * Handle da requisição 'initialize'
 */
function handleInitialize(request: MCPRequest): MCPResponse {
  return createSuccessResponse(request.id, {
    protocolVersion: "2024-11-05",
    capabilities: {
      tools: {}
    },
    serverInfo: {
      name: "bgt-nvgt-converter",
      version: "1.0.0"
    }
  });
}

/**
 * Handle da requisição 'tools/list'
 */
function handleToolsList(request: MCPRequest): MCPResponse {
  return createSuccessResponse(request.id, {
    tools: toolDefinitions
  });
}

/**
 * Handle da requisição 'tools/call'
 */
async function handleToolsCall(request: MCPRequest, projectRoot: string): Promise<MCPResponse> {
  const params = request.params as any;
  const toolName = params?.name;
  const toolArgs = params?.arguments || {};

  if (!toolName) {
    return createErrorResponse(
      request.id,
      ErrorCodes.INVALID_PARAMS,
      'Nome da ferramenta não especificado'
    );
  }

  const toolResult = await dispatchTool({ name: toolName, args: toolArgs }, projectRoot);

  return createSuccessResponse(request.id, {
    content: [
      {
        type: "text",
        text: JSON.stringify(toolResult.output || { error: toolResult.error }, null, 2)
      }
    ],
    isError: !toolResult.success
  });
}

/**
 * Handle da notificação 'notifications/initialized'
 */
function handleNotificationInitialized(request: MCPRequest): MCPResponse {
  // Notificações não precisam de resposta, mas retornamos um objeto vazio
  return createSuccessResponse(request.id, {});
}

/**
 * Handler principal de requisições MCP
 */
export async function handleRequest(request: MCPRequest, projectRoot: string): Promise<MCPResponse> {
  const { method } = request;

  switch (method) {
    case 'initialize':
      return handleInitialize(request);

    case 'tools/list':
      return handleToolsList(request);

    case 'tools/call':
      return await handleToolsCall(request, projectRoot);

    case 'notifications/initialized':
      return handleNotificationInitialized(request);

    default:
      return createErrorResponse(
        request.id,
        ErrorCodes.METHOD_NOT_FOUND,
        `Método não suportado: ${method}`
      );
  }
}

/**
 * Inicializa o servidor e exibe informações
 */
export function initializeServer(projectRoot: string): void {
  console.error(`[MCP] BGT->NVGT Converter iniciado`);
  console.error(`[MCP] PROJECT_ROOT=${projectRoot}`);
  console.error(`[MCP] ${totalRules} regras de conversão carregadas`);
}
