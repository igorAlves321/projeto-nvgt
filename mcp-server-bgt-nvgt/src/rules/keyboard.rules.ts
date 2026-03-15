import type { ConversionRule } from '../types/conversion.types.js';

export const keyboardRules: ConversionRule[] = [
  {
    pattern: /\bkey_pressed\s*\(\s*(\w+)\s*\)/g,
    replacement: 'key_pressed($1)',
    description: 'Manter key_pressed - compatível',
    category: 'keyboard'
  },
  {
    pattern: /\bkey_down\s*\(\s*(\w+)\s*\)/g,
    replacement: 'key_down($1)',
    description: 'Manter key_down - compatível',
    category: 'keyboard'
  },
  {
    pattern: /\bkey_up\s*\(\s*(\w+)\s*\)/g,
    replacement: 'key_up($1)',
    description: 'Manter key_up - compatível',
    category: 'keyboard'
  },
  {
    pattern: /\bKEY_(\w+)\b/g,
    replacement: 'KEY_$1',
    description: 'Manter constantes KEY_ - compatíveis',
    category: 'keyboard'
  },
];
