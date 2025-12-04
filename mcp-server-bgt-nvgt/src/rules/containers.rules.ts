import type { ConversionRule } from '../types/conversion.types.js';

export const containersRules: ConversionRule[] = [
  {
    pattern: /\bdictionary\s+(\w+)\s*;/g,
    replacement: 'dictionary $1;',
    description: 'Manter dictionary - compatível',
    category: 'containers'
  },
];
