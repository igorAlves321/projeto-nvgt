import type { ToolResult } from '../types/mcp.types.js';
import { allRules, getRulesByCategory } from '../rules/index.js';

export function toolGetConversionRules(args: Record<string, unknown>): ToolResult {
  const category = String(args['category'] || '').toLowerCase();

  const rules = category ? getRulesByCategory(category) : allRules;

  const grouped: Record<string, { pattern: string; replacement: string; description: string }[]> = {};

  for (const rule of rules) {
    if (!grouped[rule.category]) {
      grouped[rule.category] = [];
    }

    grouped[rule.category]!.push({
      pattern: rule.pattern.source,
      replacement: typeof rule.replacement === 'string' ? rule.replacement : '[funcao]',
      description: rule.description
    });
  }

  return {
    success: true,
    output: {
      totalRules: rules.length,
      categories: Object.keys(grouped),
      rules: grouped
    }
  };
}
