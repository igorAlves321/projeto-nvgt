# 📚 Documentação do Projeto EVM (NVGT)Note: this readme file is in spanish. Most code contained in this repository is still in portuguese. However, this situation may change in the future.



**Projeto:** EVM - Extreme Virtual Mudança  ## Introducción

**Engine:** NVGT (NonVisual Gaming Toolkit)  

**Status:** Em desenvolvimento ativo  Este repositorio contiene el código fuente del juego Entre a vida e a morte (Entre la vida y la muerte), un audiojuego on-line cuyo objetivo es matar animales y jugadores, obtener experiencia para subir niveles, y sobrevivir. Este juego deriva de otros muchos, cuyos nombres no se citarán en este documento. Tras intensas polémicas, su código fuente se ha puesto a disposición del público bajo la GNU General Public License, versión 2, cuyo texto en inglés se puede leer en el archivo copying.txt, en la raíz de este repositorio.

**Linguagem:** Português (Brasil)

## Primeros pasos

---

### Construcción del juego

## 📖 Documentação Disponível

Para compilar este juego necesitas instalar el software gratuito [Blastbay Game Toolkit](https://www.blastbay.com/bgt.php). En este repositorio encontrarás una copia del instalador de la versión 1.3. Una vez lo tengas instalado, sigue estos sencillos pasos:

### 🎮 **Conversão do Player (BGT → NVGT)**

1. Entra a la carpeta client.

**Arquivo principal:** [`PLAYER_CONVERSAO_COMPLETA.md`](./PLAYER_CONVERSAO_COMPLETA.md)2. Pulsa la tecla aplicaciones sobre el archivo client.bgt.

3. Pulsa enter sobre la opción "Compyle script (release).

Este documento contém a **documentação completa** da conversão da classe `player` de BGT para NVGT, incluindo:4. Acepta el mensaje indicando que todo ha salido bien, y accede a la carpeta server.

5. Repite los pasos 2 y 3 con el fichero server.bgt.

- ✅ **Estatísticas da conversão** (2091 linhas, 70+ métodos, 23 sistemas)6. Regresa a la carpeta client.

- ✅ **Lista de sistemas convertidos** (inventário, combate, economia, etc.)7. Pulsa aplicaciones sobre el archivo PackCreator.bgt, y pulsa enter sobre la opción "Run script".

- ✅ **Sistemas NÃO convertidos** (angelical/magias - intencional)8. ¡Todo listo! Ejecuta el archivo server.exe para activar el servidor, y el archivo client.exe para jugar. No olvides crear un usuario llamado igual que el valor de la constante ADMIN_NAME que encontrarás en el archivo config.bgt. Por defecto, si no lo has cambiado, es "admin".

- ✅ **Estrutura da classe** (~150 propriedades detalhadas)

- ✅ **Métodos principais** (~70+ métodos documentados)### Modificación de variables

- ✅ **Sistema de morte** (15 tipos diferentes)

- ✅ **Loop principal** (playerloop com 40+ subsistemas)Jugar solo está muy bien. EVM ofrece un gran abanico de posibilidades, mapas para explorar y enemigos con los que luchar. Sin embargo, a veces podemos querer jugar en compañía de alguien que no esté en nuestra misma red. En estas situaciones, el servidor queda accesible desde Internet y cualquiera podría atacarlo. Las precauciones que te ofrecemos no son infalibles, pero sí tremendamente eficaces. Lo mejor de todo es que para aplicarlas sólo debes editar el archivo config.bgt con el bloc de notas.

- ✅ **Novos métodos NVGT** (40+ helpers modernos)La sintaxis de cada línea de este archivo es muy simple: `const tipo variable=valor;`

- ✅ **Checklist de conversão** (100% core gameplay)De aquí sólo nos interesan los valores, situados a la derecha. A continuación te explicamos qué hace cada variable:

- ✅ **Próximos passos** (testes e validações)

* GAME_NAME: el nombre del juego. Si quieres crear tu propio juego basado en este código, puedes cambiar este valor. Recuerda respetar los términos de la GNU General Public License si lo haces.

**Leia este arquivo para entender:*** minversion: versión del juego.

- O que foi convertido do player.bgt para player.nvgt* version: tipo de versión.

- Como a classe player funciona no NVGT* EXECUTABLE_NAME: el nombre del fichero ejecutable del cliente. Cuando compiles el archivo client.bgt, renombra client.exe para que corresponda con el valor de esta variable.

- Quais sistemas estão ativos e funcionais* INSTALLER_NAME: nombre del archivo de instalación del juego.

- O que falta ser implementado (se houver)* DOWNLOAD_URL: dirección desde la que se puede descargar el instalador del juego.

* UPDATE_URL: dirección donde se encuentra un archivo de texto plano con la versión más reciente.

---* SOUND_STORAGE: nombre del archivo que almacena los sonidos cifrados.

* SOUND_ENCRYPTION_KEY: clave con la que se cifran los sonidos. Cámbiala para evitar que alguien con malas intenciones pueda quitártelos.

## 📁 Estrutura da Documentação* COMPUTER_ID_KEY: clave con la que se cifra el identificador de la máquina. Cámbiala para evitar que los usuarios que banees puedan saltarse el bloqueo.

* serveraddress: dirección del servidor al que se conectarán los clientes.

```* port: el puerto en el que escuchará el servidor. Importante, este valor no va entre comillas.

docks/* prefsdir: ruta en la que se almacenan los ajustes del juego en modo instalable.

├── PLAYER_CONVERSAO_COMPLETA.md    # ⭐ Documentação completa do player* PREFSFILE: nombre del archivo donde se almacenan los ajustes del cliente.

├── Doc NVGT.txt                    # Documentação geral do NVGT* PREFS_ENCRYPTION_KEY: clave para cifrar las preferencias. Cámbiala para que tus usuarios no puedan modificar los ajustes de una forma no permitida.

├── readme.md                       # Este arquivo* NETWORK_ENCRYPTION_KEY: clave para cifrar y asegurar las comunicaciones en la red. Por favor, te recomendamos que la cambies, esta es una de las más importantes.

├── plano de ação.md                # Planejamento do projeto* PASSWORD_ENCRYPTION_KEY: contraseña para cifrar las claves de tus usuarios en el servidor. Muy recomendable cambiarla.

├── plano.md                        # Plano geral* IP_LOCALE_API_KEY: clave para utilizar la API de IpInfoDB. Debes registrarte en este servicio y escribir la tuya entre las comillas para poder geolocalizar las direcciones IP de tus usuarios. Esta función es opcional.

└── perguntas para conversão.md    # Referências de conversão* IP_LOCALE_PHP_URL: dirección web del script PHP que hará las consultas al servicio IpInfoDB. Este script se incluye en la raíz del repositorio.

```* RECORD_POST_URL: dirección web del script php que registrará el récord del mejor jugador. Este script no se incluye.

* portable: indica si el juego es portable o no. Admite los valores false o true, que deberán ir sin comillas y en minúscula.

---

Cuando acabes de editar este archivo y guardes los cambios, vuelve a compilar tanto el cliente como el servidor.

## 🎯 Status do Projeto

## Añadir a alguien como administrador

### ✅ **Conversões Concluídas**

Tal vez quieras otorgar comandos de administración a alguien para que te ayude con tu juego. Para ello solo tienes que añadir un archivo con el nombre admintudo.usr dentro del directorio que contiene al personaje que deseas convertir en administrador.

#### **Player (100% funcional)**Después tendrás que buscar en server la carpeta qcomandos. Allí encontrarás archivos .md. Edítalos y añade los nombres de los administradores, uno por cada línea. Si no lo haces en algún comando, no podrá usarlo.

- ✅ `server/includes/player.nvgt` (2091 linhas)

- ✅ 23 sistemas críticos implementados## comandos de administración. Por favor, usar con cuidado.

- ✅ 70+ métodos funcionais

- ✅ Loop principal com 40+ subsistemas* En el menú que sacas con F5, si pulsas ctrl+z sobre un jugador, te harás invisible y verás lo que hace el jugador. Para dejar de observar, pulsa z desde el menú.

- ✅ Sistema de morte com 15 tipos* si pulsas f9, accedes a un editor de mapas.

- ✅ Inventário completo* /reboot: Reinicia el servidor.

- ✅ Economia (reais, stryx, créditos)* /invs: Activa o desactiva la invisibilidad.

- ✅ Equipes/Clãs* /lcoisas: Analiza las cosas que en realidad hay en el servidor.

- ✅ Combate e munição* /quantos nombre_de_item: Verifica cuantos objetos con ese nombre hay en el servidor.

- ✅ XP/Level* /inv nombre_de_jugador objeto=cantidad: Da la cantidad de objetos especificada al jugador seleccionado. No otorga objetos de la tienda virtual.

- ✅ Moderação (silêncio, prisão, anti-spam)* /inv2 nombre_de_jugador objeto de tienda virtual=cantidad: Da la cantidad de objetos especificada al jugador seleccionado. para usar con objetos de la tienda virtual.

* /backup: Realiza una copia de seguridad de las cuentas de jugadores. Ejecuta uno cada día como mínimo.

#### **Mapas do Servidor*** /vbackup jugador: Restaura el inventario del jugador a partir de una copia.

- ✅ `server/includes/server_map.nvgt` (conversão completa)* /vbackup2 jugador: Restaura la copia de seguridad del inventario para el jugador seleccionado. es la copia de seguridad que él hace con el comando /save.

* /move jugador X Y: Mueve al jugador a la coordenada seleccionada. si tecleas /move tu nombre nombre de un jugador sin coordenadas, te teletransportarás.

### 🔄 **Em Desenvolvimento*** /changemap jugador mapa X Y: Mueve al jugador indicado al mapa indicado. si no introduces coordenadas también funciona.

* /rawdata codigo_mapa: Actualiza el mapa.

- ⚠️ Testes de compilação* /delmap Mapa: borra el mapa. (No recomendado).

- ⚠️ Validação de gameplay* /newmap nombremapa max_coordenada_x max_coordenada_y ambiente: Crea mapa.

- ⚠️ Integração de sistemas* /add_map nombre_mapa: Deja objetos en el mapa. (Monedas y munición). (No recomendado).

* /getpassword jugador: Muestra la contraseña del jugador.

### ❌ **Não Convertido (Intencional)*** /setpassword jugador contraseña: Cambia la contraseña del jugador.

* /ip jugador: Muestra la ip del jugador.

- ❌ Sistema Angelical (fase angelical, magias avançadas)* /kick jugador: Expulsa al jugador. (En el menú de F5 pulsando  CTRL + E sobre un jugador también realizas la acción).

- ❌ Sistema de Loucura/Madness (opcional)* /banned: Muestra la lista de jugadores baneados.

* /clearbans: Limpia la lista de jugadores baneados.

---* /ban jugador: Banea al jugador. en el menú f5, ctrl+b realiza también esta acción.

* /unpin jugador: Desbanea un jugador.

## 🚀 Como Usar a Documentação* /killplayer jugador: mata al jugador seleccionado. en el menú f5, ctrl+m hace lo mismo.

* /pvp: Activa o desactiva el matar jugadores.

1. **Para entender a conversão do player:*** /gamestop: congela el juego.

   - Leia [`PLAYER_CONVERSAO_COMPLETA.md`](./PLAYER_CONVERSAO_COMPLETA.md)* /gamestart: Descongela el juego.

* /disable nombre mapa: Desactiva el mapa.

2. **Para consultar a API do NVGT:*** /activate nombre mapa: Activa el mapa.

   - Consulte `Doc NVGT.txt`* /frame numero: borra el mensaje indicado en el cuadro.

* /frame: Limpia mensajes del cuadro

3. **Para entender o planejamento:*** /msgpt Mensaje: Cambia el mensaje del día en portugués.

   - Veja `plano de ação.md` e `plano.md`* /msges Mensaje: Cambia el mensaje del día en español.

* /msgen Mensaje: Cambia el mensaje del día en inglés.

4. **Para referências de conversão:*** /msgfr Mensaje: Cambia el mensaje del día en francés.

   - Consulte `perguntas para conversão.md`* /npt archivo_sonido mensaje: envía mensaje al chat Portugués. si no especificas archivo de sonido no pasa nada.

* /nes archivo_sonido mensaje: envía mensaje al chat español. Si no especificas archivo de sonido no pasa nada.

---* /nen archivo_sonido mensaje: envía mensaje al chat inglés si no especificas archivo de sonido no pasa nada.

* /nfr archivo_sonido mensaje: envía mensaje al chat francés. si no especificas archivo de sonido no pasa nada.

## 📝 Arquivos do Código Fonte* /present cantidad_nombreobjeto: Envía el objeto a todos los jugadores en línea. (Presta atención a la hora de escribir el nombre del objeto que darás a los jugadores).

* /doublexp: Activa doble experiencia.

### **Player (Classe Principal)*** /doublegold: Activa el doble oro.

- **NVGT:** `server/includes/player.nvgt` (2091 linhas) ✅* /ascended jugador día_mes: Cambia a 25000 la vida al jugador durante el tiempo elegido.

- **BGT:** `server/includes/player.bgt` (1906 linhas) - Referência original* /discarded Jugador: devuelve a 5000 la vida del jugador.

* /slave jugador: Modifica la vida del jugador en la cantidad escogida.

### **Servidor*** /darxp jugador cantidad: Otorga xp al jugador.

- **Principal:** `server.nvgt`* /ncolete 5000 Jugador: añade 5000 disparos al chaleco salvavidas.

- **Mapas:** `server/includes/server_map.nvgt` ✅* /mdono jugador nombre apartamento: Otorga la administración de un departamento a un jugador.

- **Arena:** `server/includes/arena.nvgt`* /mlevel jugador nivel: Cambia el nivel del jugador.

- **Bounty:** `server/includes/bounty.nvgt`* /msexo jugador 1: Cambia el sexo del jugador a masculino. Pon 0 para femenino.

* /save: Salva tu cuenta de un borrado masivo de administradores.

### **Cliente*** /rsalvar: borra las cuentas que no han hecho un /save. Úsalo cada X tiempo previo aviso de un par de días.

- **Principal:** `client.nvgt`* /adm mensaje: envía un mensaje a los administradores.

- **Includes:** `client/includes/`* /nadm: Te retira el estado de admin hasta que reinicies el cliente. Útil para jugar.

* /ladm: Muestra los mensajes del comando /adm.

---* /aadm: borra los mensajes del comando /adm.

* /reply jugador mensage: Responde al jugador.

## 🔧 Desenvolvimento* /setinv jugador: actualiza el inventario del jugador seleccionado.



### **Compilação (NVGT)**## Tareas pendientes



```powershellFalta mucho por hacer en este juego, incluso en este mismo documento. Si te animas a abrir una pull request, aquí tienes sugerencias de tareas que puedes hacer:

# Compilar servidor

cd server* Redactar la documentación del usuario final. Los manuales de Desafío Mortal han sido eliminados.

nvgt server.nvgt* Indentar el código, de tal forma que sea más navegable y legible.

* Optimizar el código.

# Compilar cliente* Explicar qué archivos deben distribuirse a los usuarios y cuáles no.

cd client* Dar más detalles sobre cómo montar la infraestructura web que da soporte a descargas, actualizaciones y geolocalización de ip.

nvgt client.nvgt* Hacer pruebas y buscar errores derivados de la supresión de componentes.

```* Explicar qué archivos deben modificarse para dar permiso a un usuario en un comando concreto.

* Redactar un manual de creación de mapas.

### **Estrutura de Pastas*** Explicar qué archivo del cliente debe modificarse para evitar palabras ofensivas en los chats.

* Añadir un instalador, ya sea InnoSetup o NSIS.

```* Dar soporte al formato PortableApps.com para la versión portable.

projetoIg/
├── server/              # Servidor do jogo
│   ├── server.nvgt      # Principal
│   └── includes/        # Includes do servidor
│       ├── player.nvgt  # ⭐ Classe player (2091 linhas)
│       ├── server_map.nvgt
│       ├── arena.nvgt
│       └── bounty.nvgt
├── client/              # Cliente do jogo
│   ├── client.nvgt
│   └── includes/
├── include/             # Bibliotecas compartilhadas
├── docks/               # 📚 Documentação
│   ├── PLAYER_CONVERSAO_COMPLETA.md  # ⭐ Doc principal
│   └── readme.md        # Este arquivo
└── README.md            # README raiz do projeto
```

---

## 🎓 Para Desenvolvedores

### **Onde Começar?**

1. **Leia a documentação do player:**
   - [`PLAYER_CONVERSAO_COMPLETA.md`](./PLAYER_CONVERSAO_COMPLETA.md)

2. **Entenda a estrutura:**
   - Veja a seção "Estrutura da Classe Player"
   - Consulte a lista de métodos principais

3. **Explore os sistemas:**
   - Inventário (10 métodos)
   - Combate (8 métodos)
   - Economia (10 métodos)
   - Equipes (9 métodos)
   - Moderação (8 métodos)

4. **Teste o código:**
   - Compile o servidor
   - Execute testes de gameplay básico

### **Convenções de Código**

- **Idioma:** Português (Brasil)
- **Indentação:** Tabs
- **Comentários:** Em português, claros e descritivos
- **Organização:** Por sistemas funcionais
- **Nomenclatura:** snake_case para funções, camelCase para variáveis

---

## 📞 Suporte

Para dúvidas sobre a conversão do player ou outros sistemas:

1. Consulte [`PLAYER_CONVERSAO_COMPLETA.md`](./PLAYER_CONVERSAO_COMPLETA.md)
2. Veja os comentários no código-fonte
3. Consulte `Doc NVGT.txt` para referências da engine

---

## 🏆 Créditos

**Desenvolvedor:** igorAlves321  
**Assistente de Conversão:** GitHub Copilot  
**Engine Original:** BGT (Blastbay Game Toolkit)  
**Engine Nova:** NVGT (NonVisual Gaming Toolkit)  
**Licença:** GNU General Public License v2

---

**Última atualização:** 3 de outubro de 2025
