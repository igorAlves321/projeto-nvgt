# Correção de Codificação de Caracteres em Mapas

## Problema Identificado

Os mapas do jogo estavam com problemas de codificação UTF-8, onde caracteres acentuados em português estavam sendo representados incorretamente como `ï¿½`.

## Exemplo de Correção Realizada

**Arquivo:** `casa_de_sinistro.map`

### Antes:
```
z:1:40:0:10:Entrada de um lugar desconhecido. O silï¿½ncio invade o local.
z:42:42:0:10:Se vocï¿½ estï¿½ aqui, por serto teve a permiï¿½ï¿½o de alguï¿½m, nï¿½o?
z:94:200:100:120:Vocï¿½ se encontra diante de um belo jardim. diversas ï¿½rvores estï¿½o ao seu redor.
```

### Depois:
```
z:1:40:0:10:Entrada de um lugar desconhecido. O silêncio invade o local.
z:42:42:0:10:Se você está aqui, por certo teve a permissão de alguém, não?
z:94:200:100:120:Você se encontra diante de um belo jardim. diversas árvores estão ao seu redor.
```

## Mapeamento de Caracteres Corrigidos

| Caractere Corrompido | Caractere Correto | Contexto |
|---------------------|------------------|----------|
| `ï¿½` | `ê` | Maioria dos casos |
| `vocï¿½` | `você` | Pronome |
| `Vocï¿½` | `Você` | Pronome maiúsculo |
| `ï¿½rea` | `área` | Substantivo |
| `ï¿½rvore` | `árvore` | Substantivo |
| `ï¿½s ` | `às ` | Preposição contraída |
| `nï¿½o` | `não` | Advérbio de negação |
| `estï¿½` | `está` | Verbo estar |
| `estï¿½o` | `estão` | Verbo estar plural |
| `serï¿½` | `será` | Verbo ser futuro |
| `mï¿½sica` | `música` | Substantivo |
| `silï¿½ncio` | `silêncio` | Substantivo |
| `escritï¿½rio` | `escritório` | Substantivo |

## Ferramentas Criadas

### 1. Script PowerShell (fix_map_encoding.ps1)
- Corrige automaticamente a codificação de um arquivo de mapa
- Cria backup automático
- Mostra estatísticas de correção
- **Uso:** `.\fix_map_encoding.ps1 -MapPath "caminho\para\mapa.map"`

### 2. Script Batch (check_map_encoding.bat)
- Verifica quais mapas têm problemas de codificação
- Busca por caracteres problemáticos
- Lista arquivos que precisam de correção

## Como Usar para Outros Mapas

1. **Verificar problemas:**
   ```cmd
   check_map_encoding.bat
   ```

2. **Corrigir um mapa específico:**
   ```powershell
   PowerShell -ExecutionPolicy Bypass -File fix_map_encoding.ps1 -MapPath "servidor\maps\nome_do_mapa.map"
   ```

3. **Verificar resultado:**
   - O script cria um backup (.backup)
   - Mostra quantos caracteres foram corrigidos
   - Indica se ainda há problemas restantes

## Padrão de Referência

O mapa `casa_de_sinistro.map` foi totalmente corrigido e pode ser usado como referência para:
- Codificação UTF-8 correta
- Texto em português brasileiro bem formatado
- Estrutura de mapa sem problemas de caracteres

## Observações Importantes

- Sempre faça backup antes de aplicar correções
- Verifique o resultado após a correção
- Alguns casos específicos podem precisar de correção manual
- Mantenha a codificação UTF-8 nos arquivos editados

## Palavras Comuns Corrigidas

- **serto** → **certo**
- **avansa** → **avança**
- **diante** → **à frente** (quando apropriado)
- **vocï¿½** → **você**
- **nï¿½o** → **não**
- **estï¿½** → **está**
- **serï¿½** → **será**
