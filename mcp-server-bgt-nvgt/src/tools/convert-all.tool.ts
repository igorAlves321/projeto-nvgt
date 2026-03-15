import * as path from 'path';
import type { ToolResult } from '../types/mcp.types.js';
import { convertBgtToNvgt } from '../converter/converter.js';
import { listBgtFiles, readFile, writeFile } from '../converter/file-utils.js';

export function toolConvertAllBgtFiles(
  args: Record<string, unknown>,
  projectRoot: string
): ToolResult {
  const dryRun = String(args['dryRun'] || 'false').toLowerCase() === 'true';

  const files = listBgtFiles(projectRoot);
  const results: { file: string; output: string; changes: string[] }[] = [];

  for (const file of files) {
    const content = readFile(file);
    const { converted, changes } = convertBgtToNvgt(content, { verbose: true });
    const outputFile = file.replace(/\.bgt$/i, '.nvgt');

    if (!dryRun) {
      writeFile(outputFile, converted);
    }

    results.push({
      file: path.relative(projectRoot, file),
      output: path.relative(projectRoot, outputFile),
      changes: changes
    });
  }

  return {
    success: true,
    output: {
      count: results.length,
      dryRun: dryRun,
      results: results
    }
  };
}
