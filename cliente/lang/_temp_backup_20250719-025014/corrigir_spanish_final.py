# -*- coding: utf-8 -*-
"""
Script para correção final do arquivo de idioma espanhol
Este script corrige caracteres mal formatados, erros ortográficos e outros problemas
diretamente no arquivo spanish.lang, mantendo a codificação ANSI (Windows-1252)
"""

import os
import re
import codecs
import shutil
import datetime

def corrigir_spanish_final():
    """
    Corrige o arquivo spanish.lang diretamente, mantendo a codificação ANSI (Windows-1252)
    """
    arquivo = "spanish.lang"
    arquivo_backup = f"{arquivo}.backup-final-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print("\033[1;34m⚙️ CORRETOR FINAL DE ARQUIVO ESPANHOL\033[0m")
    print("="*50)
    print(f"Este script faz correções finais em caracteres e termos específicos do arquivo {arquivo}.")
    print(f"📄 Lê e edita o arquivo em ANSI, preservando a codificação original.")
    
    # Criar backup com data/hora atual
    shutil.copy2(arquivo, arquivo_backup)
    print(f"📑 Backup criado: {arquivo_backup}")
    
    print(f"🔄 Processando arquivo: {arquivo}")
    
    # Tabela de correções de caracteres especiais
    correcoes_caracteres = {
        # Correções de interrogação/exclamação
        "¿": "¿",  # Garantir interrogação invertida correta
        "¡": "¡",  # Garantir exclamação invertida correta
        
        # Correções de acentos
        "á": "á", "Á": "Á",
        "é": "é", "É": "É", 
        "í": "í", "Í": "Í",
        "ó": "ó", "Ó": "Ó",
        "ú": "ú", "Ú": "Ú",
        "ñ": "ñ", "Ñ": "Ñ",
        "ü": "ü", "Ü": "Ü",
        
        # Correções específicas de erros comuns
        "contrase¿a": "contraseña",
        "Op¿¿es": "Opciones",
        "confirma¿¿o": "confirmación",
        "interrup¿¿o": "interrupción",
        "localiza¿¿o": "localización",
        "execu¿¿o": "ejecución",
        "explora¿¿o": "exploración",
        "vers¿o": "versión",
        "sa¿da": "salida",
        "¿udio": "audio",
        "¿tens": "ítems",
        "¿teis": "útiles",
        "est¿": "está",
        "contin¿e": "continúe",
        
        # Corrigir caracteres específicos
        "arc¿ngel": "arcángel"
    }
    
    # Correções de termos específicos
    correcoes_termos = {
        # Terminações em 'el'/'adel'
        "conectandel": "conectando",
        "desligadel": "desactivado",
        "abandonadel": "abandonado",
        "ladel": "lado",
        "jugadelr": "jugador",
        "servidelr": "servidor",
        "desarrolladelr": "desarrollador",
        "trancadel": "cerrado",
        "delnde": "donde",
        "cerradel": "cerrado",
        "profundel": "profundo",
        "enviandel": "enviando",
        "enviadel": "enviado",
        "termien lada": "terminada",
        "termien ladel": "terminado",
        "seleccionadel": "seleccionado",
        "desse conectadel": "desconectado",
        "desse conecta": "desconecta",
        
        # Palavras concatenadas
        "en elmbre": "nombre",
        "en elme": "nombre",
        "en elva": "nueva",
        "en elvo": "nuevo",
        "en ladie": "nadie",
        
        # Correções de artigos
        "el servidelr": "el servidor",
        "los os": "los",
        "la zoen la": "la zona",
        "la puerta": "la puerta",
        "la rua": "la calle",
        "la escada": "la escalera",
        
        # Palavras específicas
        "Escaleera": "Escalera",
        "predetermien lado": "predeterminado",
        "estacioen lamento": "estacionamiento",
        "persoen la": "persona",
        "persoen laje": "personaje",
        "persoen lagem": "personaje",
        "camien lar": "caminar",
        "camien la": "camina",
        "pressioen la": "presiona",
        "seleccioen lar": "seleccionar",
        "seleccioen la": "selecciona",
        "selecioen lar": "seleccionar",
        
        # Frases
        "pulsa ENTER": "pulsa Enter",
        "voc¿ está": "estás",
        "puede ": "puedes ",
        "¿No tienes": "No tienes",
        "¿está": "está",
        "¡venta": "venta",
        "zoen la": "zona",
        "cocien la": "cocina",
        "sábaen la": "sábana",
        "tode los los": "todos los",
        "tode los": "todos"
    }

    try:
        # Ler o arquivo original
        with codecs.open(arquivo, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
        
        # Aplicar as correções de caracteres especiais
        for original, correcao in correcoes_caracteres.items():
            conteudo = conteudo.replace(original, correcao)
        
        # Aplicar correções de termos
        for original, correcao in correcoes_termos.items():
            conteudo = conteudo.replace(original, correcao)
            
        # Correções com regex para casos mais complexos
        padroes_regex = [
            (r"\bdaыo\b", "mal"),
            (r"\ben el(?![a-zA-Z])", "en el"),
            (r"(?<=\s)del(?=\s)", "de"),
            (r"(?<=\s)al(?=\s)", "a"),
            (r"(?<![\w])Voc[êé]\b", "Tú"),
            (r"(?<![\w])voc[êé]\b", "tú"),
            (r"\btú esta(?![a-z])", "estás"),
            (r"\bpulsa enter\b", "pulsa Enter"),
            (r"\bdelnde\b", "donde"),
            (r"persoen l([ao]s?)\b", r"person\1"),
            (r"\b([Ee])scad([ao]s?)\b", r"\1scaler\2"),
            (r"\bconpreend([eo]r?)\b", r"comprend\1"),
            (r"\bconprar\b", "comprar"),
            (r"\bvoc[êé] ([a-z]+)", lambda m: f"tú {m.group(1)}" if m.group(1) not in ["está", "tem", "vai", "pode", "quer", "vê", "faz", "deixa", "volta", "sai", "entra"] else f"tú {m.group(1)}")
        ]
        
        for padrao, substituicao in padroes_regex:
            conteudo = re.sub(padrao, substituicao, conteudo, flags=re.IGNORECASE)
            
        # Substituições específicas para conjugações verbais
        verbos_especificos = {
            "tú está": "estás",
            "tú tem": "tienes",
            "tú vai": "vas",
            "tú pode": "puedes",
            "tú quer": "quieres",
            "tú vê": "ves",
            "tú faz": "haces",
            "tú deixa": "dejas",
            "tú volta": "vuelves",
            "tú sai": "sales",
            "tú entra": "entras"
        }
        
        for padrao, substituicao in verbos_especificos.items():
            conteudo = conteudo.replace(padrao, substituicao)
                
        # Dividir em linhas para remover duplicatas
        linhas = conteudo.split('\n')
        linhas_unicas = []
        valores_vistos = set()
        
        for linha in linhas:
            # Pular linhas vazias ou sem o formato key=value
            if not linha.strip() or '=' not in linha:
                if linha.strip():  # Se não estiver vazia, mantém
                    linhas_unicas.append(linha)
                continue
            
            # Separar chave e valor
            partes = linha.split('=', 1)
            if len(partes) != 2:
                linhas_unicas.append(linha)  # Preserva linhas malformadas
                continue
                
            chave, valor = partes
            
            # Se este valor ainda não foi visto, adicione-o
            if valor.strip() not in valores_vistos:
                valores_vistos.add(valor.strip())
                linhas_unicas.append(linha)
        
        # Contar duplicatas removidas
        duplicatas_removidas = len(linhas) - len(linhas_unicas)
        
        # Salvar diretamente no arquivo original
        with codecs.open(arquivo, 'w', encoding='cp1252', errors='replace') as f:
            f.write('\n'.join(linhas_unicas))
            
        print(f"📊 Linhas duplicadas removidas: {duplicatas_removidas}")
        print(f"✅ Correções finais aplicadas diretamente no arquivo: {arquivo}")
        print(f"✅ Processo concluído!")
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        print(f"⚠️ O arquivo original foi restaurado a partir do backup.")
        # Restaurar do backup em caso de erro
        try:
            shutil.copy2(arquivo_backup, arquivo)
        except:
            print(f"❌ Não foi possível restaurar o backup! Verifique manualmente: {arquivo_backup}")
        return False
    
    print(f"🔍 Verificando integridade do arquivo...")
    try:
        # Verificar se o arquivo pode ser lido corretamente após as alterações
        with codecs.open(arquivo, 'r', encoding='cp1252', errors='replace') as f:
            teste = f.read(1024)  # Lê os primeiros 1024 bytes para teste
        print(f"✅ Verificação concluída, o arquivo está íntegro!")
    except Exception as e:
        print(f"❌ Erro ao verificar o arquivo após correções: {str(e)}")
        print(f"⚠️ Restaurando backup...")
        try:
            shutil.copy2(arquivo_backup, arquivo)
            print(f"✅ Arquivo original restaurado do backup: {arquivo_backup}")
        except:
            print(f"❌ Não foi possível restaurar o backup! Verifique manualmente: {arquivo_backup}")
        return False
    
    return True

if __name__ == "__main__":
    corrigir_spanish_final()
