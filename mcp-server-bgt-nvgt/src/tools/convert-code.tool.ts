import type { ToolResult } from '../types/mcp.types.js';
import { convertBgtCodeSnippet } from '../converter/converter.js';

export function toolConvertBgtCode(args: Record<string, unknown>): ToolResult {
  const code = String(args['code'] || '');

  if (!code) {
    return { success: false, error: 'Parâmetro "code" é obrigatório' };
  }

  const { converted, changes } = convertBgtCodeSnippet(code);

  return {
    success: true,
    output: {
      original: code,
      converted: converted,
      changes: changes
    }
  };
}
