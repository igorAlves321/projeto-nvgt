import type { ConversionRule } from '../types/conversion.types.js';

export const reservedRules: ConversionRule[] = [
  {
    pattern: /\bint\s+var\b/g,
    replacement: 'int variable',
    description: 'Renomear variável var (palavra reservada em NVGT)',
    category: 'reserved'
  },
  {
    pattern: /\bstring\s+var\b/g,
    replacement: 'string variable',
    description: 'Renomear variável var (palavra reservada em NVGT)',
    category: 'reserved'
  },
  {
    pattern: /\bfloat\s+var\b/g,
    replacement: 'float variable',
    description: 'Renomear variável var (palavra reservada em NVGT)',
    category: 'reserved'
  },
  {
    pattern: /\bdouble\s+var\b/g,
    replacement: 'float variable',
    description: 'Renomear variável var (palavra reservada em NVGT)',
    category: 'reserved'
  },
];
