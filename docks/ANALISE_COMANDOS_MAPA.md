# 📊 Análise Completa dos Comandos de Mapa (.map)

## 🔍 Problema Descoberto

Os arquivos `.map` no servidor usam **abreviações de comandos** para economizar espaço. Alguns desses comandos estão sendo **ignorados** em `map.nvgt`, o que causaria perda de dados de mapa.

---

## 📝 Estrutura de um Arquivo `.map`

Exemplo do arquivo `biblioteca.map`:

```
map:biblioteca                          # Nome do mapa
maxx:101                               # Limite X máximo
maxy:501                               # Limite Y máximo
p:0:101:0:concrete4                   # Plataforma
w:0:0:15:wall                         # Parede
z:1:100:0:500:-                       # Zona (vazia)
z:1:100:0:500:Biblioteca. Te...       # Zona com descrição
dlg:5:0:Há muita informação...:sound  # Diálogo NPC
teto:none                             # Teto/Ceiling
ss:5:5:0:0:person.ogg                # Sound source
sc:20:90:0:4:ladder                  # Staircase (escada)
dv:camera                             # Disable View (camera)
dv:coordenadas                        # Disable View (coords)
dv:auto                               # Disable View (auto)
safez:1:100:0:500                    # Safe zone
tp:1:1:0:0:40:100:mapa_destino:msg   # Travel point (portal)
where:em um local                     # Descrição de localização
ss2:0:100:0:500:musica.ogg:-12      # Sound stream (música)
item:90:0:300000:0:1:objeto:ação:60  # Item do mapa
```

---

## ✅ Mapeamento de Comandos Suportados vs Implementados

| Comando | Abreviação | Status | Implementação | Observações |
|---------|-----------|--------|---------------|----|
| `map` | - | ✅ Suportado | Funcional | Define nome do mapa |
| `maxx` | - | ✅ Suportado | Funcional | Limite X |
| `maxy` | - | ✅ Suportado | Funcional | Limite Y |
| `x` | - | ✅ Suportado | Funcional | Posição X do player |
| `y` | - | ✅ Suportado | Funcional | Posição Y do player |
| `platform` | `p` | ✅ Suportado | Funcional | Plataformas do mapa |
| `wall` | `w` | ✅ Suportado | Funcional | Paredes/colisões |
| `zone` | `z` | ✅ Suportado | Funcional | Zonas do mapa |
| `desc` | `dv` | ✅ Suportado | Funcional | Disable View (câmera, coords) |
| `sound_source` | `ss` | ✅ Suportado | Funcional | Sons 3D do mapa |
| `staircase` | `sc` | ✅ Suportado | Funcional | Escadas/transportes |
| `texto` | `txt` | ✅ Suportado | Funcional | Textos descritivos |
| `areia_movedissa` | `am` | ✅ Suportado | Funcional | Areia movediça |
| `door` | `dr` | ✅ Suportado | Funcional | Portas |
| `elevador` | `elv` | ✅ Suportado | Funcional | Elevadores |
| `teto` | - | ✅ Suportado | Funcional | Teto/ceiling |
| **`dialog`** | **`dlg`** | ❌ **IGNORADO** | **Não implementado** | **Diálogos de NPCs** |
| **`sound_stream`** | **`ss2`** | ❌ **IGNORADO** | **Não implementado** | **Música de fundo/streams** |
| **`travelpoint`** | **`tp`, `pm`, `portamapa`** | ❌ **IGNORADO** | **Não implementado** | **Portais/teleportes** |
| **`where`** | **-** | ❌ **IGNORADO** | **Não implementado** | **Descrição de localização** |
| **`item`** | **-** | ❌ **NÃO EXISTE** | **Não implementado** | **Itens do mapa** |
| **`safezone`** | **`safez`** | ⚠️ **Parcial** | **Tem alias, falta handler** | **Zonas seguras** |
| `reverb` | - | ❌ Ignorado | - | Efeito de áudio (BGT) |
| `congelar` | - | ❌ Ignorado | - | Congelar movimento (BGT) |
| `desativar` | - | ✅ Suportado | Funcional | Desativar features |
| `safemap` | - | ✅ Suportado | Funcional | Marcar mapa como seguro |
| `comment` | `//` | ✅ Suportado | Funcional | Comentários |

---

## 🔴 Comandos Críticos Faltando

### 1. **`dlg` (Dialog)** - CRÍTICO
```
dlg:5:0:Mensagem do NPC:sound_file.ogg
```
- **Uso**: Diálogos de NPCs que o player pode ouvir
- **Arquivo atual**: Ignorado em `map.nvgt` linha ~270
- **Impacto**: NPCs não terão diálogos salvos no mapa
- **Solução**: Implementar handler similar a BGT

### 2. **`ss2` (Sound Stream)** - CRÍTICO
```
ss2:0:100:0:500:musica.ogg:-12
```
- **Uso**: Música de fundo ou streams de áudio contínuos
- **Arquivo atual**: Ignorado em `map.nvgt` linha ~270
- **Impacto**: Sem música ambiente nos mapas
- **Solução**: Implementar com suporte a loops

### 3. **`tp` (Travel Point)** - CRÍTICO
```
tp:1:1:0:0:40:100:mapa_destino:Mensagem de saída
```
- **Uso**: Portais/teleportes entre mapas
- **Arquivo atual**: Ignorado em `map.nvgt` linha ~270
- **Impacto**: Sem navegação entre mapas
- **Solução**: Implementar com detecção de zona + teletransporte

### 4. **`where`** - IMPORTANTE
```
where:em um local bonito da cidade
```
- **Uso**: Descrição da localização (lido quando player entra)
- **Arquivo atual**: Ignorado em `map.nvgt` linha ~270
- **Impacto**: Sem descrição de localização na HUD
- **Solução**: Executar speak() ou adicionar ao chat

### 5. **`item`** - IMPORTANTE
```
item:90:0:300000:0:1:elemental_news:getcard:60000
```
- **Uso**: Itens coleccionáveis no mapa
- **Arquivo atual**: Não existe em `map.nvgt`
- **Impacto**: Sem items para coletar
- **Solução**: Implementar sistema de items do mapa

### 6. **`safez`** (Safe Zone Alias)** - IMPORTANTE
```
safez:1:100:0:500
```
- **Uso**: Define zona segura (alias para `safezone`)
- **Arquivo atual**: Handler existe, mas alias não está no `if`
- **Impacto**: Zonas seguras de `safez` não são reconhecidas
- **Solução**: Adicionar `|| parsed[0] == "safez"` ao handler

---

## 📊 Estatísticas de Impacto

**Total de comandos suportados**: 16/22 (73%)
**Comandos que causarão ERRO**: 6 (27%)
- dlg (diálogos) ❌
- ss2 (streams) ❌
- tp (teleportes) ❌
- where (localização) ❌
- item (itens) ❌
- safez (zonas - alias faltando) ❌

---

## 🛠️ Plano de Ação

### Fase 1 - IMEDIATO (Bugs críticos)
1. [ ] Adicionar alias `safez` ao handler `safezone`
2. [ ] Implementar handler `dlg` para diálogos
3. [ ] Implementar handler `ss2` para streams de áudio

### Fase 2 - PRÓXIMAS (Features importantes)
4. [ ] Implementar handler `tp` para teletransportes
5. [ ] Implementar handler `where` para descrição de localização

### Fase 3 - OPCIONAL (Enhancements)
6. [ ] Implementar handler `item` para itens do mapa
7. [ ] Testes com vários mapas reais

---

## 📌 Próximas Etapas

1. **Verificar**: Quantos mapas usam `dlg`, `ss2`, `tp` nesses 4658 `.map` arquivos?
   ```powershell
   Get-Content *.map | Select-String "^dlg:" | Measure-Object
   Get-Content *.map | Select-String "^ss2:" | Measure-Object
   Get-Content *.map | Select-String "^tp:" | Measure-Object
   Get-Content *.map | Select-String "^where:" | Measure-Object
   Get-Content *.map | Select-String "^item:" | Measure-Object
   ```

2. **Implementar**: Os 6 handlers faltantes na ordem de criticidade

3. **Testar**: Carregar um mapa com todos os comandos e verificar se funciona

4. **Documentar**: Adicionar documentação de cada comando novo

---

## 🔍 Referência de Formato

### Dialog (dlg)
```
dlg:X:Y:Mensagem:som.ogg
```
- X: Coordenada X do NPC
- Y: Coordenada Y (0 = sem restrição Y)
- Mensagem: Texto do diálogo
- Som: Arquivo de som a tocar

### Sound Stream (ss2)
```
ss2:X1:X2:Y1:Y2:arquivo.ogg:volume
```
- X1:X2: Range X
- Y1:Y2: Range Y
- arquivo.ogg: Arquivo de áudio
- volume: Volume em dB (ex: -12)

### Travel Point (tp)
```
tp:X1:Y1:X2:Y2:DestX:DestY:mapa_destino:Mensagem
```
- X1:Y1: Posição de entrada (zona de ativação)
- X2:Y2: Tamanho da zona de ativação
- DestX:DestY: Posição no mapa destino
- mapa_destino: Nome do mapa para teleportar
- Mensagem: Mensagem de saída (opcional)

### Where
```
where:descrição do local
```
- Simples: descrição de 1 linha

### Item
```
item:X:Y:gold_amount:0:quantity:item_type:action:price
```
- X:Y: Posição
- gold_amount: Ouro do item
- 0: Tipo (sempre 0?)
- quantity: Quantidade
- item_type: Tipo do item
- action: Ação ao pegar
- price: Preço

---

**Data**: 6 de novembro de 2025
**Status**: 🔴 CRÍTICO - 6 comandos sem suporte
**Prioridade**: 🚨 ALTA - Afeta funcionalidade de mapas
