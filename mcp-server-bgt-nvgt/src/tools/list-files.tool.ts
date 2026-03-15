import * as path from 'path';
import type { ToolResult } from '../types/mcp.types.js';
import { listBgtFiles, directoryExists } from '../converter/file-utils.js';

export function toolListBgtFiles(
  args: Record<string, unknown>,
  projectRoot: string
): ToolResult {
  const directory = String(args['directory'] || '');
  const searchDir = directory ? path.resolve(projectRoot, directory) : projectRoot;

  if (!directoryExists(searchDir)) {
    return { success: false, error: `Diretório não encontrado: ${searchDir}` };
  }

  const files = listBgtFiles(searchDir);
  const relativeFiles = files.map(f => path.relative(projectRoot, f));

  return {
    success: true,
    output: {
      count: files.length,
      files: relativeFiles
    }
  };
}
