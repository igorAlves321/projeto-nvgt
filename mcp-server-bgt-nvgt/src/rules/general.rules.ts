import type { ConversionRule } from '../types/conversion.types.js';

export const generalRules: ConversionRule[] = [
  {
    pattern: /\bwait\s*\(\s*(\d+)\s*\)/g,
    replacement: 'wait($1)',
    description: 'Manter wait - compatível',
    category: 'general'
  },
  {
    pattern: /\bexit\s*\(\s*\)/g,
    replacement: 'exit()',
    description: 'Manter exit - compatível',
    category: 'general'
  },
  {
    pattern: /\brandom\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: 'random($1, $2)',
    description: 'Manter random - compatível',
    category: 'general'
  },
  {
    pattern: /\bvoid\s+main\s*\(\s*\)/g,
    replacement: 'void main()',
    description: 'Manter void main() - compatível',
    category: 'general'
  },
  {
    pattern: /\bget_characters\s*\(\s*\)/g,
    replacement: 'get_characters()',
    description: 'Manter get_characters - compatível',
    category: 'input'
  },
];
