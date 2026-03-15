import type { ToolResult } from '../types/mcp.types.js';

/**
 * Exemplos de código BGT -> NVGT organizados por categoria
 */
const examples: Record<string, any> = {
  'basic_types': {
    title: 'Tipos de Dados Básicos',
    bgt: `// BGT
double pi = 3.14159;
string message = "Hello";
int count = 10;`,
    nvgt: `// NVGT
float pi = 3.14159;  // float em vez de double
string message = "Hello";
int count = 10;`
  },

  'arrays': {
    title: 'Arrays e Tamanho',
    bgt: `// BGT
string[] names;
names.resize(10);
int size = $names;  // $ para tamanho
names[$names - 1] = "Last";`,
    nvgt: `// NVGT
string[] names;
names.resize(10);
int size = names.length();  // .length() para tamanho
names[names.length() - 1] = "Last";`
  },

  'strings': {
    title: 'Manipulação de Strings',
    bgt: `// BGT
string text = "Hello World";
int len = string_len(text);
string upper = string_to_upper_case(text);
string sub = string_mid(text, 0, 5);`,
    nvgt: `// NVGT
string text = "Hello World";
int len = text.length();
string upper = text.upper();
string sub = text.substr(0, 5);`
  },

  'sound': {
    title: 'Sistema de Áudio',
    bgt: `// BGT
sound s;
s.stream("music.ogg");
s.play();`,
    nvgt: `// NVGT
sound@ s;  // Handle com @
s.load("music.ogg");
s.play();`
  },

  'sound_pool': {
    title: 'Sound Pool (Audio 3D)',
    bgt: `// BGT
sound_pool pool;
pool.play_extended("step.ogg", x, y, z, 0, 0, 0, false, 1, 1, 1);`,
    nvgt: `// NVGT
sound_pool pool;
pool.play("step.ogg", x, y, z, 0, 0, 0, false, 1, 1, 1);`
  },

  'files': {
    title: 'Manipulação de Arquivos',
    bgt: `// BGT
file f = file_open("data.txt", "r");
string content = file_read(f);
file_close(f);`,
    nvgt: `// NVGT
file f;
f.open("data.txt", "r");
string content = f.read();
f.close();`
  },

  'network': {
    title: 'Networking',
    bgt: `// BGT
network net;
net.setup_server(6432, 10);
net.send_reliable(id, "message");`,
    nvgt: `// NVGT
network@ net;  // Handle com @
net.setup_server(6432, 10);
net.send_reliable(id, "message");`
  },

  'timers': {
    title: 'Timers',
    bgt: `// BGT
timer t;
timer_restart(t);
if (timer_elapsed(t) > 1000) {
  // código
}`,
    nvgt: `// NVGT
timer t;
t.restart();
if (t.elapsed > 1000) {  // propriedade, não função
  // código
}`
  },

  'datetime': {
    title: 'Data e Hora',
    bgt: `// BGT
int year = date_year();
int month = date_month();
int day = date_day();`,
    nvgt: `// NVGT
// Opção 1: calendar()
int year = calendar().year;
int month = calendar().month;
int day = calendar().day;

// Opção 2: variáveis globais
int year = DATE_YEAR;
int month = DATE_MONTH;
int day = DATE_DAY;`
  },

  'math': {
    title: 'Funções Matemáticas',
    bgt: `// BGT
double abs_val = absolute(-5);
double root = square_root(16);
double pwr = power(2, 8);
double ang = arc_sine(0.5);`,
    nvgt: `// NVGT
float abs_val = abs(-5);
float root = sqrt(16);
float pwr = pow(2, 8);
float ang = asin(0.5);`
  },

  'handles': {
    title: 'Handles e Comparação com null',
    bgt: `// BGT
sound s;
if (s == null) {
  s = sound();
}`,
    nvgt: `// NVGT
sound@ s;  // @ indica handle
if (@s == null) {  // @ na comparação
  @s = sound();
}`
  },

  'dynamic_menu': {
    title: 'Menu Dinâmico',
    bgt: `// BGT
#include "dynamic_menu.bgt"
dynamic_menu menu;
menu.add_item("Opção 1");
menu.add_item("Opção 2");
int result = menu.run();`,
    nvgt: `// NVGT
#include "bgt_dynamic_menu.nvgt"  // nome diferente
dynamic_menu menu;
menu.add_item("Opção 1");
menu.add_item("Opção 2");
int result = menu.run();`
  },

  'complete_example': {
    title: 'Exemplo Completo de Jogo',
    bgt: `// BGT - Exemplo de jogo simples
#include "sound_pool.bgt"

void main() {
  show_window("Meu Jogo");
  sound_pool pool;

  double x = 0, y = 0;
  timer update_timer;

  while (true) {
    wait(5);

    if (key_pressed(KEY_LEFT)) x -= 1;
    if (key_pressed(KEY_RIGHT)) x += 1;

    if (timer_elapsed(update_timer) > 100) {
      pool.play_extended_stationary("ambient.ogg", x, y, 0, true);
      timer_restart(update_timer);
    }
  }
}`,
    nvgt: `// NVGT - Mesmo jogo convertido
#include "sound_pool.nvgt"

void main() {
  show_window("Meu Jogo");
  sound_pool pool;

  float x = 0, y = 0;  // float em vez de double
  timer update_timer;

  while (true) {
    wait(5);

    if (key_pressed(KEY_LEFT)) x -= 1;
    if (key_pressed(KEY_RIGHT)) x += 1;

    if (update_timer.elapsed > 100) {  // propriedade elapsed
      pool.play_stationary("ambient.ogg", x, y, 0, true);  // play_stationary
      update_timer.restart();  // método restart()
    }
  }
}`
  }
};

/**
 * Retorna exemplos de código BGT -> NVGT
 */
export function toolGetNvgtExamples(args: Record<string, unknown>): ToolResult {
  const category = String(args['category'] || 'all').toLowerCase();

  if (category === 'all' || category === 'list') {
    return {
      success: true,
      output: {
        message: 'Exemplos disponíveis de conversão BGT -> NVGT',
        categories: Object.keys(examples),
        total: Object.keys(examples).length,
        usage: 'Use category="nome_categoria" para ver o exemplo específico',
        availableCategories: Object.entries(examples).map(([key, value]) => ({
          key: key,
          title: value.title
        }))
      }
    };
  }

  const example = examples[category];

  if (!example) {
    return {
      success: false,
      error: `Categoria "${category}" não encontrada. Use category="all" para listar todas.`
    };
  }

  return {
    success: true,
    output: {
      category: category,
      title: example.title,
      bgt: example.bgt,
      nvgt: example.nvgt,
      explanation: example.explanation || 'Veja as diferenças entre BGT e NVGT no código acima.'
    }
  };
}
