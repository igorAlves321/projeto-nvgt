import type { ConversionRule } from '../types/conversion.types.js';

export const speechRules: ConversionRule[] = [
  {
    pattern: /\bspeak\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'speak($1)',
    description: 'Manter speak - usar include speech.nvgt',
    category: 'speech'
  },
  {
    pattern: /\bscreen_reader_speak\s*\(\s*([^,)]+)\s*\)/g,
    replacement: 'screen_reader_speak($1, true)',
    description: 'Adicionar parâmetro interrupt em screen_reader_speak',
    category: 'speech'
  },
  {
    pattern: /\bscreen_reader_speak\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'screen_reader_output($1, true)',
    description: 'Converter screen_reader_speak',
    category: 'speech'
  },
];
