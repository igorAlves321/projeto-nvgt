import type { ConversionRule } from '../types/conversion.types.js';

export const filesRules: ConversionRule[] = [
  {
    pattern: /\bfile_open\s*\(\s*([^,]+),\s*"r"\s*\)/g,
    replacement: 'file f; f.open($1, "r")',
    description: 'Converter file_open modo leitura',
    category: 'files'
  },
  {
    pattern: /\bfile_open\s*\(\s*([^,]+),\s*"w"\s*\)/g,
    replacement: 'file f; f.open($1, "w")',
    description: 'Converter file_open modo escrita',
    category: 'files'
  },
  {
    pattern: /\bfile_open\s*\(\s*([^,]+),\s*"a"\s*\)/g,
    replacement: 'file f; f.open($1, "a")',
    description: 'Converter file_open modo append',
    category: 'files'
  },
  {
    pattern: /\bfile_close\s*\(\s*(\w+)\s*\)/g,
    replacement: '$1.close()',
    description: 'Converter file_close para método',
    category: 'files'
  },
  {
    pattern: /\bfile_read\s*\(\s*(\w+)\s*\)/g,
    replacement: '$1.read()',
    description: 'Converter file_read para método',
    category: 'files'
  },
  {
    pattern: /\bfile_write\s*\(\s*(\w+),\s*([^)]+)\)/g,
    replacement: '$1.write($2)',
    description: 'Converter file_write para método',
    category: 'files'
  },
  {
    pattern: /\bfile_get_contents\s*\(\s*([^)]+)\s*\)/g,
    replacement: '(file_get_contents($1))',
    description: 'Manter file_get_contents - existe em NVGT via include',
    category: 'files'
  },
  {
    pattern: /\bini\s+(\w+)\s*;/g,
    replacement: 'ini $1;',
    description: 'Manter ini - usar include ini.nvgt',
    category: 'files'
  },
  {
    pattern: /\bpack\s+(\w+)\s*;/g,
    replacement: 'pack $1;',
    description: 'Manter pack - compatível',
    category: 'files'
  },
  {
    pattern: /(\w+)\.open\s*\(\s*([^,]+),\s*PACK_OPEN_MODE_READ\s*\)/g,
    replacement: '$1.open($2, PACK_OPEN_MODE_READ)',
    description: 'Manter pack.open com PACK_OPEN_MODE_READ',
    category: 'files'
  },
];
