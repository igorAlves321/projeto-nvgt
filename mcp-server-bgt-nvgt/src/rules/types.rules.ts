import type { ConversionRule } from '../types/conversion.types.js';

export const typesRules: ConversionRule[] = [
  {
    pattern: /\bdouble\b/g,
    replacement: 'float',
    description: 'Substituir double por float (NVGT usa float)',
    category: 'types'
  },
];
