import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
// Pasta raiz do projeto
const PROJECT_ROOT = process.env.PROJECT_ROOT || path.resolve(process.cwd(), '..');
const conversionRules = [
    // === INCLUDES ===
    {
        pattern: /#include\s+"([^"]+)\.bgt"/g,
        replacement: '#include "$1.nvgt"',
        description: 'Alterar extensÃ£o de includes de .bgt para .nvgt',
        category: 'includes'
    },
    // === TIPOS DE DADOS ===
    {
        pattern: /\bdouble\b/g,
        replacement: 'float',
        description: 'Substituir double por float (NVGT usa float)',
        category: 'types'
    },
    // === ARRAYS ===
    {
        pattern: /\$(\w+)/g,
        replacement: '$1.length()',
        description: 'Converter $array para array.length()',
        category: 'arrays'
    },
    {
        pattern: /(\w+)\s*\[\s*\$\s*\]/g,
        replacement: '$1[]',
        description: 'Converter array[$] para array[] na declaraÃ§Ã£o',
        category: 'arrays'
    },
    {
        pattern: /\.resize\s*\(\s*0\s*\)/g,
        replacement: '.resize(0)',
        description: 'Manter resize(0) - compatÃ­vel',
        category: 'arrays'
    },
    // === STRINGS ===
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
        description: 'Adicionar parÃ¢metro replace_all em string_replace',
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
    // === ARQUIVOS ===
    {
        pattern: /\bfile_open\s*\(\s*([^,]+),\s*"r"\s*\)/g,
        replacement: 'file f; f.open($1, "r")',
        description: 'Converter file_open modo leitura',
        category: 'files'
    },
    {
        pattern: /\bfile_open\s*\(\s*([^,]+),\s*"w"\s*\)/g,
        replacement: 'file f; f.open($1, "w")',
        description: 'Converter file_open modo escrita',
        category: 'files'
    },
    {
        pattern: /\bfile_open\s*\(\s*([^,]+),\s*"a"\s*\)/g,
        replacement: 'file f; f.open($1, "a")',
        description: 'Converter file_open modo append',
        category: 'files'
    },
    {
        pattern: /\bfile_close\s*\(\s*(\w+)\s*\)/g,
        replacement: '$1.close()',
        description: 'Converter file_close para mÃ©todo',
        category: 'files'
    },
    {
        pattern: /\bfile_read\s*\(\s*(\w+)\s*\)/g,
        replacement: '$1.read()',
        description: 'Converter file_read para mÃ©todo',
        category: 'files'
    },
    {
        pattern: /\bfile_write\s*\(\s*(\w+),\s*([^)]+)\)/g,
        replacement: '$1.write($2)',
        description: 'Converter file_write para mÃ©todo',
        category: 'files'
    },
    {
        pattern: /\bfile_get_contents\s*\(\s*([^)]+)\s*\)/g,
        replacement: '(file_get_contents($1))',
        description: 'Manter file_get_contents - existe em NVGT via include',
        category: 'files'
    },
    // === ÃUDIO - SOUND ===
    {
        pattern: /\bsound\s+(\w+)\s*;/g,
        replacement: 'sound@ $1;',
        description: 'Adicionar @ em declaraÃ§Ã£o de sound handle',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.stream\s*\(\s*([^)]+)\s*\)/g,
        replacement: '$1.load($2)',
        description: 'Converter .stream() para .load()',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.load\s*\(\s*([^)]+)\s*\)/g,
        replacement: '$1.load($2)',
        description: 'Manter .load() - compatÃ­vel',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.set_sound_position\s*\(\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\s*\)/g,
        replacement: '$1.set_position($2, $3, $4, $5, $6, $7)',
        description: 'Converter set_sound_position para set_position',
        category: 'audio'
    },
    // === ÃUDIO - SOUND_POOL ===
    {
        pattern: /\bsound_pool\s+(\w+)\s*;/g,
        replacement: 'sound_pool $1;',
        description: 'Manter sound_pool - compatÃ­vel',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.play_stationary\s*\(\s*([^,]+),\s*([^)]*)\)/g,
        replacement: '$1.play_stationary($2, $3)',
        description: 'Manter play_stationary - compatÃ­vel',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.play_extended\s*\(\s*([^)]+)\s*\)/g,
        replacement: '$1.play($2)',
        description: 'Converter play_extended para play',
        category: 'audio'
    },
    {
        pattern: /(\w+)\.play_extended_stationary\s*\(\s*([^)]+)\s*\)/g,
        replacement: '$1.play_stationary($2)',
        description: 'Converter play_extended_stationary para play_stationary',
        category: 'audio'
    },
    // === TIMERS ===
    {
        pattern: /\btimer\s+(\w+)\s*;/g,
        replacement: 'timer $1;',
        description: 'Manter timer - compatÃ­vel',
        category: 'timers'
    },
    {
        pattern: /\btimer_restart\s*\(\s*(\w+)\s*\)/g,
        replacement: '$1.restart()',
        description: 'Converter timer_restart para mÃ©todo',
        category: 'timers'
    },
    {
        pattern: /\btimer_elapsed\s*\(\s*(\w+)\s*\)/g,
        replacement: '$1.elapsed',
        description: 'Converter timer_elapsed para propriedade',
        category: 'timers'
    },
    // === TECLADO ===
    {
        pattern: /\bkey_pressed\s*\(\s*(\w+)\s*\)/g,
        replacement: 'key_pressed($1)',
        description: 'Manter key_pressed - compatÃ­vel',
        category: 'keyboard'
    },
    {
        pattern: /\bkey_down\s*\(\s*(\w+)\s*\)/g,
        replacement: 'key_down($1)',
        description: 'Manter key_down - compatÃ­vel',
        category: 'keyboard'
    },
    {
        pattern: /\bkey_up\s*\(\s*(\w+)\s*\)/g,
        replacement: 'key_up($1)',
        description: 'Manter key_up - compatÃ­vel',
        category: 'keyboard'
    },
    {
        pattern: /\bKEY_(\w+)\b/g,
        replacement: 'KEY_$1',
        description: 'Manter constantes KEY_ - compatÃ­veis',
        category: 'keyboard'
    },
    // === REDE ===
    {
        pattern: /\bnetwork\s+(\w+)\s*;/g,
        replacement: 'network@ $1;',
        description: 'Adicionar @ em declaraÃ§Ã£o de network handle',
        category: 'network'
    },
    {
        pattern: /(\w+)\.setup_server\s*\(\s*(\d+),\s*(\d+)\s*\)/g,
        replacement: '$1.setup_server($2, $3)',
        description: 'Manter setup_server - compatÃ­vel',
        category: 'network'
    },
    {
        pattern: /(\w+)\.connect\s*\(\s*([^,]+),\s*(\d+)\s*\)/g,
        replacement: '$1.connect($2, $3)',
        description: 'Manter connect - compatÃ­vel',
        category: 'network'
    },
    {
        pattern: /(\w+)\.request\s*\(\s*\)/g,
        replacement: '$1.request()',
        description: 'Manter request - compatÃ­vel',
        category: 'network'
    },
    {
        pattern: /(\w+)\.send_reliable\s*\(\s*([^,]+),\s*([^)]+)\)/g,
        replacement: '$1.send_reliable($2, $3)',
        description: 'Manter send_reliable - compatÃ­vel',
        category: 'network'
    },
    {
        pattern: /(\w+)\.send_unreliable\s*\(\s*([^,]+),\s*([^)]+)\)/g,
        replacement: '$1.send_unreliable($2, $3)',
        category: 'network',
        description: 'Manter send_unreliable - compatÃ­vel'
    },
    // === FUNÃ‡Ã•ES GERAIS ===
    {
        pattern: /\bwait\s*\(\s*(\d+)\s*\)/g,
        replacement: 'wait($1)',
        description: 'Manter wait - compatÃ­vel',
        category: 'general'
    },
    {
        pattern: /\bexit\s*\(\s*\)/g,
        replacement: 'exit()',
        description: 'Manter exit - compatÃ­vel',
        category: 'general'
    },
    {
        pattern: /\brandom\s*\(\s*([^,]+),\s*([^)]+)\)/g,
        replacement: 'random($1, $2)',
        description: 'Manter random - compatÃ­vel',
        category: 'general'
    },
    {
        pattern: /\bspeak\s*\(\s*([^)]+)\s*\)/g,
        replacement: 'speak($1)',
        description: 'Manter speak - usar include speech.nvgt',
        category: 'speech'
    },
    {
        pattern: /\bscreen_reader_speak\s*\(\s*([^)]+)\s*\)/g,
        replacement: 'screen_reader_output($1, true)',
        description: 'Converter screen_reader_speak',
        category: 'speech'
    },
    {
        pattern: /\bclipboard_get_text\s*\(\s*\)/g,
        replacement: 'clipboard_get_text()',
        description: 'Manter clipboard_get_text - compatÃ­vel',
        category: 'general'
    },
    {
        pattern: /\bclipboard_set_text\s*\(\s*([^)]+)\s*\)/g,
        replacement: 'clipboard_set_text($1)',
        description: 'Manter clipboard_set_text - compatÃ­vel',
        category: 'general'
    },
    // === SQLITE ===
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
    // === MENU DINÃ‚MICO ===
    {
        pattern: /\bdynamic_menu\s+(\w+)\s*;/g,
        replacement: 'dynamic_menu $1;',
        description: 'Manter dynamic_menu - usar include bgt_dynamic_menu.nvgt',
        category: 'ui'
    },
    {
        pattern: /(\w+)\.add_item\s*\(\s*([^)]+)\s*\)/g,
        replacement: '$1.add_item($2)',
        description: 'Manter add_item - compatÃ­vel',
        category: 'ui'
    },
    {
        pattern: /(\w+)\.run\s*\(\s*([^)]*)\s*\)/g,
        replacement: '$1.run($2)',
        description: 'Manter run - compatÃ­vel',
        category: 'ui'
    },
    // === INI FILES ===
    {
        pattern: /\bini\s+(\w+)\s*;/g,
        replacement: 'ini $1;',
        description: 'Manter ini - usar include ini.nvgt',
        category: 'files'
    },
    // === SHOW WINDOW ===
    {
        pattern: /\bshow_window\s*\(\s*([^)]+)\s*\)/g,
        replacement: 'show_window($1)',
        description: 'Manter show_window - compatÃ­vel',
        category: 'ui'
    },
    // === PACKS ===
    {
        pattern: /\bpack\s+(\w+)\s*;/g,
        replacement: 'pack $1;',
        description: 'Manter pack - compatÃ­vel',
        category: 'files'
    },
    {
        pattern: /(\w+)\.open\s*\(\s*([^,]+),\s*PACK_OPEN_MODE_READ\s*\)/g,
        replacement: '$1.open($2, PACK_OPEN_MODE_READ)',
        description: 'Manter pack.open com PACK_OPEN_MODE_READ',
        category: 'files'
    },
    // === DICIONÃRIOS ===
    {
        pattern: /\bdictionary\s+(\w+)\s*;/g,
        replacement: 'dictionary $1;',
        description: 'Manter dictionary - compatÃ­vel',
        category: 'containers'
    },
    // === SCRIPT HANDLE ===
    {
        pattern: /@(\w+)\s+(\w+)\s*;/g,
        replacement: '$1@ $2;',
        description: 'Mover @ para depois do tipo (handle syntax)',
        category: 'handles'
    },
    // === VOID MAIN ===
    {
        pattern: /\bvoid\s+main\s*\(\s*\)/g,
        replacement: 'void main()',
        description: 'Manter void main() - compatÃ­vel',
        category: 'general'
    },
    // === GET_CHARACTERS ===
    {
        pattern: /\bget_characters\s*\(\s*\)/g,
        replacement: 'get_characters()',
        description: 'Manter get_characters - compatÃ­vel',
        category: 'input'
    },
    // === DATE/TIME ===
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
        description: 'Manter ticks - compatÃ­vel',
        category: 'datetime'
    },
];
// FunÃ§Ã£o principal de conversão
function convertBgtToNvgt(content, options) {
    let out = content;
    const changes = [];
    for (const rule of conversionRules) {
        const matches = out.match(rule.pattern);
        if (matches && matches.length > 0) {
            const beforeCount = matches.length;
            out = out.replace(rule.pattern, rule.replacement);
            changes.push(`[${rule.category}] ${rule.description} (${beforeCount} ocorrÃªncias)`);
        }
    }
    // Adicionar comentÃ¡rio no topo
    const header = `// Converted from BGT to NVGT\n// Conversion date: ${new Date().toISOString()}\n// Please review and test all conversions\n\n`;
    return { converted: header + out, changes };
}
// Listar arquivos BGT recursivamente
function listBgtFiles(dir) {
    if (!fs.existsSync(dir))
        return [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    const result = [];
    for (const e of entries) {
        const full = path.join(dir, e.name);
        if (e.isDirectory())
            result.push(...listBgtFiles(full));
        else if (e.isFile() && full.toLowerCase().endsWith('.bgt'))
            result.push(full);
    }
    return result;
}
// ============================================================
// DEFINIÃ‡ÃƒO DAS FERRAMENTAS MCP
// ============================================================
const tools = [
    {
        name: "convert_bgt_file",
        description: "Converte um arquivo .bgt para .nvgt aplicando todas as regras de conversão conhecidas",
        inputSchema: {
            type: "object",
            properties: {
                file: { type: "string", description: "Caminho do arquivo .bgt a converter (relativo ao projeto)" },
                save: { type: "string", description: "Se 'true', salva o arquivo convertido. Se 'false' ou omitido, retorna apenas o resultado" }
            },
            required: ["file"]
        }
    },
    {
        name: "convert_bgt_code",
        description: "Converte um trecho de cÃ³digo BGT para NVGT",
        inputSchema: {
            type: "object",
            properties: {
                code: { type: "string", description: "CÃ³digo BGT a ser convertido" }
            },
            required: ["code"]
        }
    },
    {
        name: "list_bgt_files",
        description: "Lista todos os arquivos .bgt no projeto",
        inputSchema: {
            type: "object",
            properties: {
                directory: { type: "string", description: "DiretÃ³rio especÃ­fico para buscar (opcional)" }
            }
        }
    },
    {
        name: "get_conversion_rules",
        description: "Retorna todas as regras de conversão disponÃ­veis organizadas por categoria",
        inputSchema: {
            type: "object",
            properties: {
                category: { type: "string", description: "Filtrar por categoria (opcional): includes, types, arrays, strings, files, audio, timers, keyboard, network, general, speech, database, ui, containers, handles, datetime" }
            }
        }
    },
    {
        name: "convert_all_bgt_files",
        description: "Converte todos os arquivos .bgt do projeto para .nvgt",
        inputSchema: {
            type: "object",
            properties: {
                dryRun: { type: "string", description: "Se 'true', apenas simula a conversão sem salvar arquivos" }
            }
        }
    }
];
function tool_convert_bgt_file(args) {
    const file = String(args['file'] || '');
    const save = String(args['save'] || 'false').toLowerCase() === 'true';
    if (!file) {
        return { success: false, error: 'ParÃ¢metro "file" Ã© obrigatÃ³rio' };
    }
    const abs = path.resolve(PROJECT_ROOT, file);
    if (!fs.existsSync(abs)) {
        return { success: false, error: `Arquivo Não encontrado: ${abs}` };
    }
    const content = fs.readFileSync(abs, 'utf-8');
    const { converted, changes } = convertBgtToNvgt(content);
    if (save) {
        const outFile = abs.replace(/\.bgt$/i, '.nvgt');
        fs.writeFileSync(outFile, converted, 'utf-8');
        return {
            success: true,
            output: {
                input: file,
                output: path.relative(PROJECT_ROOT, outFile),
                changes: changes,
                saved: true
            }
        };
    }
    return {
        success: true,
        output: {
            input: file,
            converted: converted,
            changes: changes,
            saved: false
        }
    };
}
function tool_convert_bgt_code(args) {
    const code = String(args['code'] || '');
    if (!code) {
        return { success: false, error: 'ParÃ¢metro "code" Ã© obrigatÃ³rio' };
    }
    const { converted, changes } = convertBgtToNvgt(code);
    return {
        success: true,
        output: {
            original: code,
            converted: converted,
            changes: changes
        }
    };
}
function tool_list_bgt_files(args) {
    const directory = String(args['directory'] || '');
    const searchDir = directory ? path.resolve(PROJECT_ROOT, directory) : PROJECT_ROOT;
    if (!fs.existsSync(searchDir)) {
        return { success: false, error: `DiretÃ³rio Não encontrado: ${searchDir}` };
    }
    const files = listBgtFiles(searchDir);
    const relativeFiles = files.map(f => path.relative(PROJECT_ROOT, f));
    return {
        success: true,
        output: {
            count: files.length,
            files: relativeFiles
        }
    };
}
function tool_get_conversion_rules(args) {
    const category = String(args['category'] || '').toLowerCase();
    const rules = category
        ? conversionRules.filter(r => r.category === category)
        : conversionRules;
    const grouped = {};
    for (const rule of rules) {
        if (!grouped[rule.category]) {
            grouped[rule.category] = [];
        }
        grouped[rule.category].push({
            pattern: rule.pattern.source,
            replacement: typeof rule.replacement === 'string' ? rule.replacement : '[funcao]',
            description: rule.description
        });
    }
    return {
        success: true,
        output: {
            totalRules: rules.length,
            categories: Object.keys(grouped),
            rules: grouped
        }
    };
}
function tool_convert_all_bgt_files(args) {
    const dryRun = String(args['dryRun'] || 'false').toLowerCase() === 'true';
    const files = listBgtFiles(PROJECT_ROOT);
    const results = [];
    for (const f of files) {
        const content = fs.readFileSync(f, 'utf-8');
        const { converted, changes } = convertBgtToNvgt(content);
        const outFile = f.replace(/\.bgt$/i, '.nvgt');
        if (!dryRun) {
            fs.writeFileSync(outFile, converted, 'utf-8');
        }
        results.push({
            file: path.relative(PROJECT_ROOT, f),
            output: path.relative(PROJECT_ROOT, outFile),
            changes: changes
        });
    }
    return {
        success: true,
        output: {
            count: results.length,
            dryRun: dryRun,
            results: results
        }
    };
}
// ============================================================
// DISPATCHER DE FERRAMENTAS
// ============================================================
function dispatchTool(call) {
    switch (call.name) {
        case 'convert_bgt_file':
            return tool_convert_bgt_file(call.args);
        case 'convert_bgt_code':
            return tool_convert_bgt_code(call.args);
        case 'list_bgt_files':
            return tool_list_bgt_files(call.args);
        case 'get_conversion_rules':
            return tool_get_conversion_rules(call.args);
        case 'convert_all_bgt_files':
            return tool_convert_all_bgt_files(call.args);
        default:
            return { success: false, error: `Ferramenta desconhecida: ${call.name}` };
    }
}
// ============================================================
// PROTOCOLO MCP (JSON-RPC 2.0 via stdin/stdout)
// ============================================================
function sendResponse(response) {
    process.stdout.write(JSON.stringify(response) + '\n');
}
function handleRequest(request) {
    const { id, method, params } = request;
    switch (method) {
        case 'initialize':
            return {
                jsonrpc: "2.0",
                id,
                result: {
                    protocolVersion: "2024-11-05",
                    capabilities: {
                        tools: {}
                    },
                    serverInfo: {
                        name: "bgt-nvgt-converter",
                        version: "1.0.0"
                    }
                }
            };
        case 'tools/list':
            return {
                jsonrpc: "2.0",
                id,
                result: { tools }
            };
        case 'tools/call':
            const toolName = params?.name;
            const toolArgs = params?.arguments || {};
            const toolResult = dispatchTool({ name: toolName, args: toolArgs });
            return {
                jsonrpc: "2.0",
                id,
                result: {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify(toolResult.output || { error: toolResult.error }, null, 2)
                        }
                    ],
                    isError: !toolResult.success
                }
            };
        case 'notifications/initialized':
            // NotificaÃ§Ã£o, Não precisa resposta
            return { jsonrpc: "2.0", id, result: {} };
        default:
            return {
                jsonrpc: "2.0",
                id,
                error: { code: -32601, message: `MÃ©todo Não suportado: ${method}` }
            };
    }
}
// Leitura linha por linha via readline
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
});
rl.on('line', (line) => {
    if (!line.trim())
        return;
    try {
        const request = JSON.parse(line);
        const response = handleRequest(request);
        // Não enviar resposta para notificações
        if (request.method && !request.method.startsWith('notifications/')) {
            sendResponse(response);
        }
    }
    catch (err) {
        sendResponse({
            jsonrpc: "2.0",
            id: 0,
            error: { code: -32700, message: `Erro de parse: ${err?.message || err}` }
        });
    }
});
// Log de inicialização (stderr para Não interferir com o protocolo)
console.error(`[MCP] BGT->NVGT Converter iniciado`);
console.error(`[MCP] PROJECT_ROOT=${PROJECT_ROOT}`);
console.error(`[MCP] ${conversionRules.length} regras de conversão carregadas`);
//# sourceMappingURL=server.js.map