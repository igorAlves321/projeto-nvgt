import type { ConversionRule } from '../types/conversion.types.js';

export const handlesRules: ConversionRule[] = [
  {
    pattern: /@(\w+)\s+(\w+)\s*;/g,
    replacement: '$1@ $2;',
    description: 'Mover @ para depois do tipo (handle syntax)',
    category: 'handles'
  },
  {
    pattern: /if\s*\(\s*(\w+)\s*==\s*null\s*\)/g,
    replacement: 'if (@$1 == null)',
    description: 'Adicionar @ em comparação de null para handles',
    category: 'handles'
  },
  {
    pattern: /if\s*\(\s*(\w+)\s*!=\s*null\s*\)/g,
    replacement: 'if (@$1 != null)',
    description: 'Adicionar @ em comparação de null para handles',
    category: 'handles'
  },
];
