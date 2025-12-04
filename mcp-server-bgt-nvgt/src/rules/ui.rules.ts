import type { ConversionRule } from '../types/conversion.types.js';

export const uiRules: ConversionRule[] = [
  {
    pattern: /\bdynamic_menu\s+(\w+)\s*;/g,
    replacement: 'dynamic_menu $1;',
    description: 'Manter dynamic_menu - usar include bgt_dynamic_menu.nvgt',
    category: 'ui'
  },
  {
    pattern: /(\w+)\.add_item\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.add_item($2)',
    description: 'Manter add_item - compatível',
    category: 'ui'
  },
  {
    pattern: /(\w+)\.run\s*\(\s*([^)]*)\s*\)/g,
    replacement: '$1.run($2)',
    description: 'Manter run - compatível',
    category: 'ui'
  },
  {
    pattern: /\bshow_window\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'show_window($1)',
    description: 'Manter show_window - compatível',
    category: 'ui'
  },
];
