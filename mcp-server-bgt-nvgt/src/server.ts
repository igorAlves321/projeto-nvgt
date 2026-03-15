#!/usr/bin/env node

// ============================================================
// MCP Server para conversão BGT -> NVGT
// Baseado no Model Context Protocol (MCP) da Anthropic
// ============================================================

import * as path from 'path';
import * as readline from 'readline';
import type { MCPRequest } from './types/mcp.types.js';
import { handleRequest, initializeServer } from './mcp/handlers.js';
import { sendResponse, createErrorResponse, ErrorCodes } from './mcp/protocol.js';

// Configuração
const PROJECT_ROOT = process.env.PROJECT_ROOT || path.resolve(process.cwd(), '..');

// Inicializar servidor
initializeServer(PROJECT_ROOT);

// Criar interface de leitura
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

// Processar linhas recebidas
rl.on('line', async (line: string) => {
  if (!line.trim()) return;

  try {
    const request: MCPRequest = JSON.parse(line);
    const response = await handleRequest(request, PROJECT_ROOT);

    // Não enviar resposta para notificações
    if (request.method && !request.method.startsWith('notifications/')) {
      sendResponse(response);
    }
  } catch (err: any) {
    const errorResponse = createErrorResponse(
      0,
      ErrorCodes.PARSE_ERROR,
      `Erro de parse: ${err?.message || err}`
    );
    sendResponse(errorResponse);
  }
});

// Tratamento de erros não capturados
process.on('uncaughtException', (error) => {
  console.error('[MCP] Erro não capturado:', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('[MCP] Promise rejeitada não tratada:', reason);
  process.exit(1);
});
