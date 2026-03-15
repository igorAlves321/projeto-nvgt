# Checklist Final - Hardening e Padronizacao NVGT

## 1) Build
- [ ] Compilar `server/server.nvgt`
- [ ] Compilar `cliente/client.nvgt`

## 2) Rede e Conexao
- [ ] Login normal com conta existente
- [ ] Criacao de conta (`xt55`) sem queda
- [ ] Timeout de conexao mostra mensagem correta
- [ ] Pacote malformado/oversize nao derruba servidor

## 3) Item Builder
- [ ] Listar itens abre submenu imediatamente
- [ ] Criar item retorna confirmacao real do servidor
- [ ] Editar item retorna confirmacao real do servidor
- [ ] Excluir item retorna confirmacao real do servidor
- [ ] Criar arma (`/create_weapon_tool`) retorna confirmacao real
- [ ] Erros aparecem no formato `[ERRO] /comando: ...`

## 4) Modulos Sociais
- [ ] Party: erros de comando aparecem com prefixo `[ERRO]`
- [ ] Guild: erros de comando aparecem com prefixo `[ERRO]`
- [ ] Friends: erros de comando aparecem com prefixo `[ERRO]`
- [ ] Mail: erros de comando aparecem com prefixo `[ERRO]`

## 5) Logs
- [ ] Servidor grava em `debug/erros_servidor_YYYY_MM_DD.log`
- [ ] Cliente grava em `debug/erros_client_YYYY_MM_DD.log`
- [ ] Payload em log vem truncado quando muito grande

## 6) Stubs Criticos
- [ ] Confirmado: nao ha stub critico novo bloqueando login/mapa/item builder
- [ ] Stubs remanescentes sao auxiliares/legado e nao bloqueiam fluxo principal
