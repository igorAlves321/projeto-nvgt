# 🔊 Diagnóstico de Áudio - Cliente IG

## ✅ Melhorias Implementadas

### 1. **Verificação de Dispositivo de Áudio**
- ✅ Tenta abrir dispositivo salvo nas preferências (`numero_dispositivo`)
- ✅ Se falhar, tenta dispositivo padrão (0)
- ✅ Se ainda falhar, mostra erro detalhado e encerra

### 2. **Logs de Debug Detalhados**
Agora o cliente gera logs em `cliente/debug/client_log.txt` com:

```
🔊 Inicializando sistema de áudio...
✓ Dispositivo 0 aberto com sucesso
✓ Volume global configurado: 50
🔊 Testando reprodução de som...
✓ Som de teste enviado
📋 Entrando no menu principal...
🎵 Tentando carregar música: m3.ogg
✅ Música do menu tocando: m3.ogg
```

### 3. **Teste de Áudio no Início**
- Toca `door1open.ogg` ao iniciar
- Se você NÃO ouvir esse som, há problema no dispositivo de áudio

## 🔍 Como Diagnosticar Problemas

### **Cenário 1: Nenhum Som**

1. **Verifique o log:**
   - Abra `cliente/debug/client_log.txt`
   - Procure por linhas com ❌ ou ⚠️

2. **Possíveis causas:**

   **a) Dispositivo de áudio incorreto:**
   ```
   ⚠️ Falha ao abrir dispositivo 3, tentando dispositivo padrão (0)...
   ```
   **Solução:** Altere `numero_dispositivo` nas configurações

   **b) Nenhum dispositivo disponível:**
   ```
   ❌ ERRO CRÍTICO: Dispositivo de áudio não disponível!
   ```
   **Solução:** Verifique drivers de áudio do Windows

   **c) Volume muito baixo:**
   ```
   ✓ Volume global configurado: 0
   ```
   **Solução:** Aumente `volumejogo` nas configurações

### **Cenário 2: Menu Sem Música**

1. **Verifique o log:**
   ```
   ❌ ERRO: Não foi possível carregar música do menu!
      Tentou: m3.ogg e sounds/m3.ogg
   ```

2. **Possíveis causas:**

   **a) Arquivos de música ausentes:**
   - Verifique se existem `m1.ogg` até `m8.ogg` na pasta `sounds/`
   
   **b) Volume da música zerado:**
   - Configure `musicamenu` para 50% ou mais nas preferências
   - Ou use o slider no menu: Configurações → Gerais → Volume da música

### **Cenário 3: Sons do Jogo Funcionam, Menus Não**

1. **Verifique configuração de volume:**
   ```nvgt
   musicamenu = 50.0  // Volume da música dos menus (0-100)
   ```

2. **Teste manual:**
   - Menu Principal → "teste de alto-falantes"
   - Deve tocar `altofalante.ogg`

## 🛠️ Configurações de Áudio

### **Arquivo de Preferências**
Local: `%APPDATA%\IG\prefs` ou `prefs` (se modo portátil)

Variáveis importantes:
```ini
volumejogo=50.0        # Volume geral (0-100)
musicamenu=50.0        # Volume da música dos menus (0-100)
numero_dispositivo=0   # Dispositivo de áudio (0 = padrão)
```

### **Como Alterar Volume**
1. Menu Principal → Configurações → Gerais
2. Selecione "Volume da música do menu"
3. Use ⬅️➡️ para ajustar (0-100%)
4. ENTER para salvar

## 📝 Checklist de Solução de Problemas

- [ ] Verifique se pasta `sounds/` existe
- [ ] Verifique se `m1.ogg` até `m8.ogg` existem
- [ ] Abra `debug/client_log.txt` e procure por erros
- [ ] Teste som no Windows (YouTube, etc) para confirmar que áudio funciona
- [ ] Verifique `volumejogo` e `musicamenu` nas preferências
- [ ] Tente dispositivo de áudio padrão: configure `numero_dispositivo=0`
- [ ] Execute "teste de alto-falantes" no menu principal

## 🎵 Arquivos de Música Necessários

Devem estar em `cliente/sounds/`:
- `m1.ogg` 🎵
- `m2.ogg` 🎵
- `m3.ogg` 🎵
- `m4.ogg` 🎵
- `m5.ogg` 🎵
- `m6.ogg` 🎵
- `m7.ogg` 🎵
- `m8.ogg` 🎵

O jogo escolhe aleatoriamente uma dessas músicas ao abrir o menu.

## 🐛 Reportar Problema

Se após seguir todos os passos acima o áudio ainda não funcionar:

1. Anexe o arquivo `debug/client_log.txt`
2. Informe seu sistema operacional
3. Informe se outros jogos/programas de áudio funcionam
4. Copie a seção de erro do log (linhas com ❌ ou ⚠️)
