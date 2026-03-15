import type { ConversionRule } from '../types/conversion.types.js';

export const audioRules: ConversionRule[] = [
  // SOUND
  {
    pattern: /\bsound\s+(\w+)\s*;/g,
    replacement: 'sound@ $1;',
    description: 'Adicionar @ em declaração de sound handle',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.stream\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.load($2)',
    description: 'Converter .stream() para .load()',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.load\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.load($2)',
    description: 'Manter .load() - compatível',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.set_sound_position\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\s*\)/g,
    replacement: '$1.set_position($2, $3, $4, $5, $6, $7)',
    description: 'Converter set_sound_position para set_position',
    category: 'audio'
  },

  // SOUND_POOL
  {
    pattern: /\bsound_pool\s+(\w+)\s*;/g,
    replacement: 'sound_pool $1;',
    description: 'Manter sound_pool - compatível',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.play_stationary\s*\(\s*([^,]+),\s*([^)]*)\)/g,
    replacement: '$1.play_stationary($2, $3)',
    description: 'Manter play_stationary - compatível',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.play_extended\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.play($2)',
    description: 'Converter play_extended para play',
    category: 'audio'
  },
  {
    pattern: /(\w+)\.play_extended_stationary\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.play_stationary($2)',
    description: 'Converter play_extended_stationary para play_stationary',
    category: 'audio'
  },
  {
    pattern: /\bset_sound_storage\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'sound_default_pack = $1',
    description: 'Converter set_sound_storage para sound_default_pack',
    category: 'audio'
  },
];
