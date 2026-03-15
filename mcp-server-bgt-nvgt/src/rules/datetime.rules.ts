import type { ConversionRule } from '../types/conversion.types.js';

export const datetimeRules: ConversionRule[] = [
  // Funções date_*() e time_*()
  {
    pattern: /\bdate_year\s*\(\s*\)/g,
    replacement: 'calendar().year',
    description: 'Converter date_year para calendar',
    category: 'datetime'
  },
  {
    pattern: /\bdate_month\s*\(\s*\)/g,
    replacement: 'calendar().month',
    description: 'Converter date_month para calendar',
    category: 'datetime'
  },
  {
    pattern: /\bdate_day\s*\(\s*\)/g,
    replacement: 'calendar().day',
    description: 'Converter date_day para calendar',
    category: 'datetime'
  },
  {
    pattern: /\btime_hour\s*\(\s*\)/g,
    replacement: 'calendar().hour',
    description: 'Converter time_hour para calendar',
    category: 'datetime'
  },
  {
    pattern: /\btime_minute\s*\(\s*\)/g,
    replacement: 'calendar().minute',
    description: 'Converter time_minute para calendar',
    category: 'datetime'
  },
  {
    pattern: /\btime_second\s*\(\s*\)/g,
    replacement: 'calendar().second',
    description: 'Converter time_second para calendar',
    category: 'datetime'
  },
  {
    pattern: /\bticks\s*\(\s*\)/g,
    replacement: 'ticks()',
    description: 'Manter ticks - compatível',
    category: 'datetime'
  },

  // Propriedades globais DATE_* e TIME_*
  {
    pattern: /\bdate_year\b(?!\s*\()/g,
    replacement: 'DATE_YEAR',
    description: 'Converter date_year propriedade para DATE_YEAR',
    category: 'datetime'
  },
  {
    pattern: /\bdate_month\b(?!\s*\()/g,
    replacement: 'DATE_MONTH',
    description: 'Converter date_month propriedade para DATE_MONTH',
    category: 'datetime'
  },
  {
    pattern: /\bdate_day\b(?!\s*\()/g,
    replacement: 'DATE_DAY',
    description: 'Converter date_day propriedade para DATE_DAY',
    category: 'datetime'
  },
  {
    pattern: /\btime_hour\b(?!\s*\()/g,
    replacement: 'TIME_HOUR',
    description: 'Converter time_hour propriedade para TIME_HOUR',
    category: 'datetime'
  },
  {
    pattern: /\btime_minute\b(?!\s*\()/g,
    replacement: 'TIME_MINUTE',
    description: 'Converter time_minute propriedade para TIME_MINUTE',
    category: 'datetime'
  },
  {
    pattern: /\btime_second\b(?!\s*\()/g,
    replacement: 'TIME_SECOND',
    description: 'Converter time_second propriedade para TIME_SECOND',
    category: 'datetime'
  },
];
