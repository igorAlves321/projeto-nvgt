import type { ConversionRule } from '../types/conversion.types.js';

export const windowRules: ConversionRule[] = [
  {
    pattern: /\bshow_game_window\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'show_window($1)',
    description: 'Converter show_game_window para show_window',
    category: 'window'
  },
  {
    pattern: /\bis_game_window_active\s*\(\s*\)/g,
    replacement: 'is_window_active()',
    description: 'Converter is_game_window_active para is_window_active',
    category: 'window'
  },
];
