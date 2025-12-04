import type { ConversionRule } from '../types/conversion.types.js';

export const arraysRules: ConversionRule[] = [
  {
    pattern: /\$(\w+)/g,
    replacement: '$1.length()',
    description: 'Converter $array para array.length()',
    category: 'arrays'
  },
  {
    pattern: /(\w+)\s*\[\s*\$\s*\]/g,
    replacement: '$1[]',
    description: 'Converter array[$] para array[] na declaração',
    category: 'arrays'
  },
  {
    pattern: /\.resize\s*\(\s*0\s*\)/g,
    replacement: '.resize(0)',
    description: 'Manter resize(0) - compatível',
    category: 'arrays'
  },
  {
    pattern: /(\w+)\.length(?!\s*\()/g,
    replacement: '$1.length()',
    description: 'Converter .length propriedade para .length() método',
    category: 'arrays'
  },
];
