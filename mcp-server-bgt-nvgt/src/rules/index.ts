// ============================================================
// Índice de todas as regras de conversão BGT -> NVGT
// ============================================================

import { includesRules } from './includes.rules.js';
import { typesRules } from './types.rules.js';
import { arraysRules } from './arrays.rules.js';
import { stringsRules } from './strings.rules.js';
import { mathRules } from './math.rules.js';
import { audioRules } from './audio.rules.js';
import { filesRules } from './files.rules.js';
import { networkRules } from './network.rules.js';
import { timersRules } from './timers.rules.js';
import { keyboardRules } from './keyboard.rules.js';
import { datetimeRules } from './datetime.rules.js';
import { generalRules } from './general.rules.js';
import { speechRules } from './speech.rules.js';
import { databaseRules } from './database.rules.js';
import { uiRules } from './ui.rules.js';
import { containersRules } from './containers.rules.js';
import { handlesRules } from './handles.rules.js';
import { reservedRules } from './reserved.rules.js';
import { clipboardRules } from './clipboard.rules.js';
import { windowRules } from './window.rules.js';
import { warningsRules } from './warnings.rules.js';

import type { ConversionRule } from '../types/conversion.types.js';

// Exportar regras individuais por categoria
export {
  includesRules,
  typesRules,
  arraysRules,
  stringsRules,
  mathRules,
  audioRules,
  filesRules,
  networkRules,
  timersRules,
  keyboardRules,
  datetimeRules,
  generalRules,
  speechRules,
  databaseRules,
  uiRules,
  containersRules,
  handlesRules,
  reservedRules,
  clipboardRules,
  windowRules,
  warningsRules,
};

// Exportar todas as regras combinadas
export const allRules: ConversionRule[] = [
  ...includesRules,
  ...typesRules,
  ...arraysRules,
  ...stringsRules,
  ...mathRules,
  ...audioRules,
  ...filesRules,
  ...networkRules,
  ...timersRules,
  ...keyboardRules,
  ...datetimeRules,
  ...generalRules,
  ...speechRules,
  ...databaseRules,
  ...uiRules,
  ...containersRules,
  ...handlesRules,
  ...reservedRules,
  ...clipboardRules,
  ...windowRules,
  ...warningsRules,
];

// Exportar total de regras
export const totalRules = allRules.length;

// Função helper para obter regras por categoria
export function getRulesByCategory(category: string): ConversionRule[] {
  return allRules.filter(rule => rule.category === category);
}

// Função helper para listar todas as categorias
export function getCategories(): string[] {
  const categories = new Set(allRules.map(rule => rule.category));
  return Array.from(categories).sort();
}
