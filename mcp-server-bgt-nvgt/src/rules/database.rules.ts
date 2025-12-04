import type { ConversionRule } from '../types/conversion.types.js';

export const databaseRules: ConversionRule[] = [
  {
    pattern: /\bsqlite3_open\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'sqlite3 db; db.open($1)',
    description: 'Converter sqlite3_open',
    category: 'database'
  },
  {
    pattern: /\bsqlite3_close\s*\(\s*(\w+)\s*\)/g,
    replacement: '$1.close()',
    description: 'Converter sqlite3_close',
    category: 'database'
  },
  {
    pattern: /\bsqlite3_execute\s*\(\s*(\w+),\s*([^)]+)\)/g,
    replacement: '$1.execute($2)',
    description: 'Converter sqlite3_execute',
    category: 'database'
  },
];
