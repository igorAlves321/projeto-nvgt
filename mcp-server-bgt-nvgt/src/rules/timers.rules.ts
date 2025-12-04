import type { ConversionRule } from '../types/conversion.types.js';

export const timersRules: ConversionRule[] = [
  {
    pattern: /\btimer\s+(\w+)\s*;/g,
    replacement: 'timer $1;',
    description: 'Manter timer - compatível',
    category: 'timers'
  },
  {
    pattern: /\btimer_restart\s*\(\s*(\w+)\s*\)/g,
    replacement: '$1.restart()',
    description: 'Converter timer_restart para método',
    category: 'timers'
  },
  {
    pattern: /\btimer_elapsed\s*\(\s*(\w+)\s*\)/g,
    replacement: '$1.elapsed',
    description: 'Converter timer_elapsed para propriedade',
    category: 'timers'
  },
  {
    pattern: /(\w+)\.elapsed\s*\(\s*\)/g,
    replacement: '$1.elapsed',
    description: 'Converter .elapsed() para .elapsed (propriedade)',
    category: 'timers'
  },
];
