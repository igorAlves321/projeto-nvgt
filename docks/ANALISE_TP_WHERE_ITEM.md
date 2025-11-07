# 🎯 Análise de Formatos: tp, where, item

## Data: 6 de novembro de 2025

### 1️⃣ Travel Point (tp)

**Exemplos reais**:
```
tp:30:30:200:200:30:200:academia_de_magos:Al intentar abrir el libro, este se deshace en tus manos.
tp:1:1:0:0:200:200:cima:Te alejas del acantilado.
tp:100:100:4005:4100:1:0:ciudad_taerus:Entras a la increíble ciudad flotante.
tp:1:1:0:0:300:300:llanuras:Te adentras en un largo terreno con grandes agujeros.
tp:100:100:4005:4005:800:0:ciudad_taerus:Te adentras en la magnífica ciudad.
```

**Formato**: `tp:zona_x1:zona_y1:zona_x2:zona_y2:dest_x:dest_y:mapa_destino:mensagem`

| Índice | Valor | Descrição |
|--------|-------|-----------|
| 0 | `tp` | Comando |
| 1 | `30` | Zona X mínima |
| 2 | `30` | Zona Y mínima |
| 3 | `200` | Zona X máxima |
| 4 | `200` | Zona Y máxima |
| 5 | `30` | Destino X (próximo mapa) |
| 6 | `200` | Destino Y (próximo mapa) |
| 7 | `academia_de_magos` | Mapa destino |
| 8+ | Mensagem (resto da linha) | Mensagem ao teleportar |

**Total mínimo**: 8 elementos

**Funcionalidade**:
- Define uma zona (retângulo) que ao entrar teleporta o player
- Teleporta para coordenadas específicas no próximo mapa
- Exibe mensagem ao teleportar

---

### 2️⃣ Where (Localização)

**Exemplos reais**:
```
where:en la historia
where:en la historia
where:oculto
```

**Formato**: `where:descrição_da_localização`

| Índice | Valor | Descrição |
|--------|-------|-----------|
| 0 | `where` | Comando |
| 1 | `en la historia` | Descrição da localização |

**Total**: 2 elementos (o texto pode ter espaços e ser parseado como parsed[1])

**Funcionalidade**:
- Define a descrição do local (para HUD ou TTS)
- Pode ser lido ao entrar no mapa

---

### 3️⃣ Item (Itens)

**Exemplos reais**:
```
item:995:955:100000:0:1:folleto5:papelembrulha:60000
item:432,490:60:50000:0:1:mg151:get7.62mm:60000
item:432,490:60:40000:0:900:20.19mm:get30mm:60000
item:1,100:0:30000:0:1:nsv:get9mm:50000
item:1,100:0:40000:0:300:12.70mm:get12mm:60000
```

**Formato**: `item:x:y:ouro:0:quantidade:tipo_item:acao:preco`

| Índice | Valor | Descrição |
|--------|-------|-----------|
| 0 | `item` | Comando |
| 1 | `995` | Coordenada X |
| 2 | `955` | Coordenada Y |
| 3 | `100000` | Ouro/moeda valor |
| 4 | `0` | Tipo? (sempre 0?) |
| 5 | `1` | Quantidade |
| 6 | `folleto5` | Tipo do item |
| 7 | `papelembrulha` | Ação ao coletar |
| 8 | `60000` | Preço? |

**Total**: 9 elementos

**Nota**: Algumas coordenadas têm vírgula (ex: `432,490`), que pode ser múltiplas posições

**Funcionalidade**:
- Spawna item no mapa
- Player pode coletar
- Executa ação ao coletar

---

## 📋 Implementação Recomendada

### Para `tp`:
- Criar zona que detecta entrada do player
- Ao entrar, teleportar para novo mapa
- Reproduzir mensagem (TTS ou chat)

### Para `where`:
- Armazenar localização global
- Exibir em HUD ou reproduzir via TTS ao carregar mapa

### Para `item`:
- Criar sistema básico de items
- Detectar coleta do player
- Executar ação correspondente

---

**Próximo passo**: Implementar handlers em map.nvgt

