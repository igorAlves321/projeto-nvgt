import type { ConversionRule } from '../types/conversion.types.js';

export const mathRules: ConversionRule[] = [
  {
    pattern: /\babsolute\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'abs($1)',
    description: 'Converter absolute para abs',
    category: 'math'
  },
  {
    pattern: /\bcosine\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'cos($1)',
    description: 'Converter cosine para cos',
    category: 'math'
  },
  {
    pattern: /\bsine\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'sin($1)',
    description: 'Converter sine para sin',
    category: 'math'
  },
  {
    pattern: /\btangent\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'tan($1)',
    description: 'Converter tangent para tan',
    category: 'math'
  },
  {
    pattern: /\barc_cosine\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'acos($1)',
    description: 'Converter arc_cosine para acos',
    category: 'math'
  },
  {
    pattern: /\barc_sine\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'asin($1)',
    description: 'Converter arc_sine para asin',
    category: 'math'
  },
  {
    pattern: /\barc_tangent\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'atan($1)',
    description: 'Converter arc_tangent para atan',
    category: 'math'
  },
  {
    pattern: /\bpower\s*\(\s*([^,]+),\s*([^)]+)\s*\)/g,
    replacement: 'pow($1, $2)',
    description: 'Converter power para pow',
    category: 'math'
  },
  {
    pattern: /\bsquare_root\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'sqrt($1)',
    description: 'Converter square_root para sqrt',
    category: 'math'
  },
  {
    pattern: /\bceiling\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'ceil($1)',
    description: 'Converter ceiling para ceil',
    category: 'math'
  },
];
