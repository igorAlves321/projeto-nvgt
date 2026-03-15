// ============================================================
// Tipos do Protocolo MCP (Model Context Protocol)
// ============================================================

export interface MCPRequest {
  jsonrpc: "2.0";
  id: number | string;
  method: string;
  params?: Record<string, unknown>;
}

export interface MCPResponse {
  jsonrpc: "2.0";
  id: number | string;
  result?: unknown;
  error?: { code: number; message: string; data?: unknown };
}

export interface ToolDefinition {
  name: string;
  description: string;
  inputSchema: {
    type: "object";
    properties: Record<string, { type: string; description: string }>;
    required?: string[];
  };
}

export interface ToolResult {
  success: boolean;
  output?: unknown;
  error?: string;
}

export interface ToolCall {
  name: string;
  args: Record<string, unknown>;
}
