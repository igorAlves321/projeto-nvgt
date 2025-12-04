import type { ConversionRule } from '../types/conversion.types.js';

export const warningsRules: ConversionRule[] = [
  {
    pattern: /while\s*\(\s*true\s*\)\s*\{(?!\s*[\s\S]*?wait\s*\()/g,
    replacement: 'while (true) { // AVISO: Adicione wait(5) dentro deste loop!',
    description: 'Aviso sobre loop infinito sem wait',
    category: 'warnings'
  },
];
