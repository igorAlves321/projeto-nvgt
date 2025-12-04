import type { ConversionRule, ConversionResult, ConversionOptions } from '../types/conversion.types.js';
import { allRules } from '../rules/index.js';

/**
 * Converte código BGT para NVGT aplicando todas as regras de conversão
 */
export function convertBgtToNvgt(
  content: string,
  options?: ConversionOptions
): ConversionResult {
  let output = content;
  const changes: string[] = [];

  // Aplicar cada regra de conversão
  for (const rule of allRules) {
    const matches = output.match(rule.pattern);

    if (matches && matches.length > 0) {
      const beforeCount = matches.length;
      output = output.replace(rule.pattern, rule.replacement as string);

      if (options?.verbose) {
        changes.push(`[${rule.category}] ${rule.description} (${beforeCount} ocorrências)`);
      }
    }
  }

  // Adicionar cabeçalho de conversão
  const header = generateHeader();

  return {
    converted: header + output,
    changes: changes
  };
}

/**
 * Gera o cabeçalho do arquivo convertido
 */
function generateHeader(): string {
  const timestamp = new Date().toISOString();
  return `// Converted from BGT to NVGT
// Conversion date: ${timestamp}
// Please review and test all conversions

`;
}

/**
 * Converte código BGT para NVGT sem adicionar cabeçalho
 * Útil para converter trechos de código
 */
export function convertBgtCodeSnippet(
  code: string,
  options?: ConversionOptions
): ConversionResult {
  let output = code;
  const changes: string[] = [];

  for (const rule of allRules) {
    const matches = output.match(rule.pattern);

    if (matches && matches.length > 0) {
      const beforeCount = matches.length;
      output = output.replace(rule.pattern, rule.replacement as string);
      changes.push(`[${rule.category}] ${rule.description} (${beforeCount} ocorrências)`);
    }
  }

  return {
    converted: output,
    changes: changes
  };
}

/**
 * Obtém estatísticas sobre as regras de conversão
 */
export function getConversionStats() {
  const categories = new Map<string, number>();

  for (const rule of allRules) {
    const count = categories.get(rule.category) || 0;
    categories.set(rule.category, count + 1);
  }

  return {
    totalRules: allRules.length,
    categoriesCount: categories.size,
    rulesByCategory: Object.fromEntries(categories)
  };
}
