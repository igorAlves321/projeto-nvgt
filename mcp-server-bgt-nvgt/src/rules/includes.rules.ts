import type { ConversionRule } from '../types/conversion.types.js';

export const includesRules: ConversionRule[] = [
  {
    pattern: /#include\s+"([^"]+)\.bgt"/g,
    replacement: '#include "$1.nvgt"',
    description: 'Alterar extensão de includes de .bgt para .nvgt',
    category: 'includes'
  },
  {
    pattern: /#include\s+"dynamic_menu\.bgt"/g,
    replacement: '#include "bgt_dynamic_menu.nvgt"',
    description: 'Renomear dynamic_menu.bgt para bgt_dynamic_menu.nvgt',
    category: 'includes'
  },
  {
    pattern: /#include\s+"sound_pool\.bgt"/g,
    replacement: '#include "sound_pool.nvgt"',
    description: 'Renomear sound_pool.bgt para sound_pool.nvgt',
    category: 'includes'
  },
  {
    pattern: /#include\s+"([^"]+)\.dat"/g,
    replacement: '#pragma embed "$1.dat"',
    description: 'Converter #include de .dat para #pragma embed',
    category: 'includes'
  },
];
