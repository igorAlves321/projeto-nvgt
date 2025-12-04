import type { ConversionRule } from '../types/conversion.types.js';

export const clipboardRules: ConversionRule[] = [
  {
    pattern: /\bclipboard_get_text\s*\(\s*\)/g,
    replacement: 'clipboard_get_text()',
    description: 'Manter clipboard_get_text - compatível',
    category: 'clipboard'
  },
  {
    pattern: /\bclipboard_set_text\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'clipboard_set_text($1)',
    description: 'Manter clipboard_set_text - compatível',
    category: 'clipboard'
  },
  {
    pattern: /\bclipboard_copy_text\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'clipboard_set_text($1)',
    description: 'Converter clipboard_copy_text para clipboard_set_text',
    category: 'clipboard'
  },
  {
    pattern: /\bclipboard_read_text\s*\(\s*\)/g,
    replacement: 'clipboard_get_text()',
    description: 'Converter clipboard_read_text para clipboard_get_text',
    category: 'clipboard'
  },
];
