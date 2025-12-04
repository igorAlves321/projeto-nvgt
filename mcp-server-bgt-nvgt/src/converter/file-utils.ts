import * as fs from 'fs';
import * as path from 'path';

/**
 * Lista todos os arquivos .bgt recursivamente em um diretório
 */
export function listBgtFiles(dir: string): string[] {
  if (!fs.existsSync(dir)) return [];

  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const result: string[] = [];

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);

    if (entry.isDirectory()) {
      result.push(...listBgtFiles(fullPath));
    } else if (entry.isFile() && fullPath.toLowerCase().endsWith('.bgt')) {
      result.push(fullPath);
    }
  }

  return result;
}

/**
 * Lê o conteúdo de um arquivo
 */
export function readFile(filePath: string): string {
  return fs.readFileSync(filePath, 'utf-8');
}

/**
 * Escreve conteúdo em um arquivo
 */
export function writeFile(filePath: string, content: string): void {
  fs.writeFileSync(filePath, content, 'utf-8');
}

/**
 * Verifica se um arquivo existe
 */
export function fileExists(filePath: string): boolean {
  return fs.existsSync(filePath);
}

/**
 * Verifica se um diretório existe
 */
export function directoryExists(dirPath: string): boolean {
  return fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory();
}
