import * as path from 'path';
import type { ToolResult } from '../types/mcp.types.js';
import { convertBgtToNvgt } from '../converter/converter.js';
import { readFile, writeFile, fileExists } from '../converter/file-utils.js';

export function toolConvertBgtFile(
  args: Record<string, unknown>,
  projectRoot: string
): ToolResult {
  const file = String(args['file'] || '');
  const save = String(args['save'] || 'false').toLowerCase() === 'true';

  if (!file) {
    return { success: false, error: 'Parâmetro "file" é obrigatório' };
  }

  const absolutePath = path.resolve(projectRoot, file);

  if (!fileExists(absolutePath)) {
    return { success: false, error: `Arquivo não encontrado: ${absolutePath}` };
  }

  const content = readFile(absolutePath);
  const { converted, changes } = convertBgtToNvgt(content, { verbose: true });

  if (save) {
    const outputFile = absolutePath.replace(/\.bgt$/i, '.nvgt');
    writeFile(outputFile, converted);

    return {
      success: true,
      output: {
        input: file,
        output: path.relative(projectRoot, outputFile),
        changes: changes,
        saved: true
      }
    };
  }

  return {
    success: true,
    output: {
      input: file,
      converted: converted,
      changes: changes,
      saved: false
    }
  };
}
