import type { ConversionRule } from '../types/conversion.types.js';

export const networkRules: ConversionRule[] = [
  {
    pattern: /\bnetwork\s+(\w+)\s*;/g,
    replacement: 'network@ $1;',
    description: 'Adicionar @ em declaração de network handle',
    category: 'network'
  },
  {
    pattern: /(\w+)\.setup_server\s*\(\s*(\d+),\s*(\d+)\s*\)/g,
    replacement: '$1.setup_server($2, $3)',
    description: 'Manter setup_server - compatível',
    category: 'network'
  },
  {
    pattern: /(\w+)\.connect\s*\(\s*([^,]+),\s*(\d+)\s*\)/g,
    replacement: '$1.connect($2, $3)',
    description: 'Manter connect - compatível',
    category: 'network'
  },
  {
    pattern: /(\w+)\.request\s*\(\s*\)/g,
    replacement: '$1.request()',
    description: 'Manter request - compatível',
    category: 'network'
  },
  {
    pattern: /(\w+)\.send_reliable\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.send_reliable($2, $3)',
    description: 'Manter send_reliable - compatível',
    category: 'network'
  },
  {
    pattern: /(\w+)\.send_unreliable\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.send_unreliable($2, $3)',
    category: 'network',
    description: 'Manter send_unreliable - compatível'
  },
];
