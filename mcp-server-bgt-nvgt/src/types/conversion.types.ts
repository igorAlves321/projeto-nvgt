// ============================================================
// Tipos para Conversão BGT -> NVGT
// ============================================================

export interface ConversionRule {
  pattern: RegExp;
  replacement: string | ((match: string, ...args: string[]) => string);
  description: string;
  category: string;
}

export interface ConversionResult {
  converted: string;
  changes: string[];
}

export interface ConversionOptions {
  verbose?: boolean;
}
