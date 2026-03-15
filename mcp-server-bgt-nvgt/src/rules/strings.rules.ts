import type { ConversionRule } from '../types/conversion.types.js';

export const stringsRules: ConversionRule[] = [
  {
    pattern: /\bstring_to_number\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'parse_float($1)',
    description: 'Converter string_to_number para parse_float',
    category: 'strings'
  },
  {
    pattern: /\bstring_to_int\s*\(\s*([^)]+)\s*\)/g,
    replacement: 'parse_int($1)',
    description: 'Converter string_to_int para parse_int',
    category: 'strings'
  },
  {
    pattern: /\bstring_replace\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
    replacement: 'string_replace($1, $2, $3, true)',
    description: 'Adicionar parâmetro replace_all em string_replace',
    category: 'strings'
  },
  {
    pattern: /\bstring_left\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.substr(0, $2)',
    description: 'Converter string_left para substr',
    category: 'strings'
  },
  {
    pattern: /\bstring_right\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.substr($1.length() - $2)',
    description: 'Converter string_right para substr',
    category: 'strings'
  },
  {
    pattern: /\bstring_mid\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.substr($2, $3)',
    description: 'Converter string_mid para substr',
    category: 'strings'
  },
  {
    pattern: /\bstring_len\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.length()',
    description: 'Converter string_len para .length()',
    category: 'strings'
  },
  {
    pattern: /\bstring_contains\s*\(\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.contains($2)',
    description: 'Converter string_contains para .contains()',
    category: 'strings'
  },
  {
    pattern: /\bstring_split\s*\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)/g,
    replacement: '$1.split($2)',
    description: 'Converter string_split para .split()',
    category: 'strings'
  },
  {
    pattern: /\bstring_trim_left\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.trim_whitespace_left()',
    description: 'Converter string_trim_left',
    category: 'strings'
  },
  {
    pattern: /\bstring_trim_right\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.trim_whitespace_right()',
    description: 'Converter string_trim_right',
    category: 'strings'
  },
  {
    pattern: /\bstring_to_upper_case\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.upper()',
    description: 'Converter string_to_upper_case para .upper()',
    category: 'strings'
  },
  {
    pattern: /\bstring_to_lower_case\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.lower()',
    description: 'Converter string_to_lower_case para .lower()',
    category: 'strings'
  },
  {
    pattern: /\bstring_is_digits\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.is_digits()',
    description: 'Converter string_is_digits para .is_digits()',
    category: 'strings'
  },
  {
    pattern: /\bstring_is_alphabetic\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.is_alphabetic()',
    description: 'Converter string_is_alphabetic para .is_alphabetic()',
    category: 'strings'
  },
  {
    pattern: /\bstring_reverse\s*\(\s*([^)]+)\s*\)/g,
    replacement: '$1.reverse()',
    description: 'Converter string_reverse para .reverse()',
    category: 'strings'
  },
];
