// ============================================================
// Implementação do Protocolo MCP (JSON-RPC 2.0)
// ============================================================

import type { MCPResponse } from '../types/mcp.types.js';

/**
 * Envia uma resposta MCP via stdout
 */
export function sendResponse(response: MCPResponse): void {
  process.stdout.write(JSON.stringify(response) + '\n');
}

/**
 * Cria uma resposta de erro MCP
 */
export function createErrorResponse(
  id: number | string,
  code: number,
  message: string,
  data?: unknown
): MCPResponse {
  return {
    jsonrpc: "2.0",
    id,
    error: { code, message, data }
  };
}

/**
 * Cria uma resposta de sucesso MCP
 */
export function createSuccessResponse(
  id: number | string,
  result: unknown
): MCPResponse {
  return {
    jsonrpc: "2.0",
    id,
    result
  };
}

/**
 * Códigos de erro JSON-RPC 2.0
 */
export const ErrorCodes = {
  PARSE_ERROR: -32700,
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  INVALID_PARAMS: -32602,
  INTERNAL_ERROR: -32603,
} as const;
