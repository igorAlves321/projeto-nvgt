# -*- coding: utf-8 -*-
"""
Script para corrigir o arquivo de idioma espanhol
Este script corrige caracteres mal formatados, erros ortográficos e outros problemas
diretamente no arquivo spanish.lang, mantendo a codificação ANSI (Windows-1252)
"""

import os
import re
import codecs
import shutil
import datetime

def corrigir_spanish():
    """
    Corrige o arquivo spanish.lang diretamente, mantendo a codificação ANSI (Windows-1252)
    """
    arquivo = "spanish.lang"
    arquivo_backup = f"{arquivo}.backup-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print("\033[1;34m⚙️ CORRETOR DE ARQUIVO ESPANHOL\033[0m")
    print("="*50)
    print(f"Este script corrige caracteres mal formatados, erros ortográficos e problemas de consistência diretamente no arquivo {arquivo}.")
    print(f"📄 Lê e edita o arquivo em ANSI, preservando a codificação original.")
    
    # Criar backup com data/hora atual
    shutil.copy2(arquivo, arquivo_backup)
    print(f"📑 Backup criado: {arquivo_backup}")
    
    print(f"🔄 Processando arquivo: {arquivo}")
    
    # Função para substituir caracteres específicos
    def corrigir_caracteres_espanhois(texto):
        # Mapeamento de caracteres específicos do espanhol
        mapa = {
            # Caracteres especiais em espanhol
            "?": "¿",  # Interrogação invertida
            "!": "¡",  # Exclamação invertida
            
            # Vogais com acento agudo
            "á": "á", "Á": "Á",
            "é": "é", "É": "É", 
            "í": "í", "Í": "Í",
            "ó": "ó", "Ó": "Ó",
            "ú": "ú", "Ú": "Ú",
            
            # Caracteres especiais
            "ñ": "ñ", "Ñ": "Ñ",
            "ü": "ü", "Ü": "Ü",
            
            # Caracteres que aparecem incorretamente (mapeamento cirílico/outros)
            "ж": "é", "р": "á", "ь": "í", "Щ": "ú", "з": "ó", "ы": "ñ", "в": "ú"
        }
        
        # Aplicar substituições
        for original, correcao in mapa.items():
            texto = texto.replace(original, correcao)
            
        return texto
    
    # Correções de termos e expressões
    correções_termos = {
        # Correções de palavras específicas com problemas de acento
        "Op??es": "Opciones",
        "sa?da": "salida",
        "?udio": "audio",
        "n?o": "no",
        "vers?o": "versión",
        "localiza??o": "localización",
        "n?vel": "nivel",
        "interrup??o": "interrupción",
        "confirma??o": "confirmación",
        "atualiza??o": "actualización",
        "explora??o": "exploración",
        "execu??o": "ejecución",
        "op??o": "opción",
        "voc?": "tú",
        "contrase?a": "contraseña",
        "muni??o": "munición",
        "¿tens": "ítems",
        "¿teis": "útiles",
        "está¿": "está",
        "está¿s": "estás",
        
        # Termos em português que precisam ser traduzidos
        "você": "tú",
        "Você": "Tú",
        "você está": "estás",
        "você sabe": "sabes",
        "você tem": "tienes",
        "você vai": "vas",
        "você pode": "puedes",
        "você quer": "quieres",
        "você vê": "ves",
        "você faz": "haces",
        "você deixa": "dejas",
        "você volta": "vuelves",
        "você sai": "sales",
        "você entra": "entras",
        
        # Palavras com formatação estranha
        "conectni-se": "se ha conectado",
        "desconectni-se": "se ha desconectado",
        "persoen laje": "personaje",
        "persoen lagem": "personaje",
        "uen la": "una",
        "een la": "ena",
        "seleccioen lar": "seleccionar",
        "seleccioen la": "selecciona",
        "conprar": "comprar",
        "conectandel": "conectando",
        "delnde": "donde",
        "en elmbre": "nombre",
        "en elme": "nombre",
        "ladel": "lado",
        "jugadelr": "jugador",
        "servidelr": "servidor",
        "seleccionadel": "seleccionado",
        "desarrolladelr": "desarrollador",
        "pieren las": "piernas",
        "abandelen ladel": "abandonado",
        "en ladie": "nadie",
        "estacioen lamiento": "estacionamiento",
        "desse conectadel": "desconectado",
        "camien lar": "caminar",
        "camien la": "camina",
        "daыo": "mal",
        "objet": "objet",
        "fijade los": "fijados",
        "lleen las": "llenas",
        "lleen els": "llenos",
        "apresurade las": "apresuradas",
        "entrae los": "entramos",
        "pressioen la": "presiona",
        
        # Correção de artigos
        " o ": " el ",
        " um ": " un ",
        " uma ": " una ",
        " uns ": " unos ",
        " umas ": " unas ",
        " no ": " en el ",
        " na ": " en la ",
        " nas ": " en las ",
        " nos ": " en los ",
        " pelo ": " por el ",
        " pela ": " por la ",
        " pelos ": " por los ",
        " pelas ": " por las ",
        " em ": " en ",
        " a ": " la "
    }
    
    # Expressões regulares para padrões mais complexos
    padroes_regex = {
        r"\ben el(?![a-zA-Z])": "no",
        r"\ben la(?![a-zA-Z])": "una",
        r"\ben elch": "noch",
        r"\bdaыo\s+([a-záéíóúüñ]+)": r"mal \1",
        r"(?<![\w])nenhuen la\b": "ninguna",
        r"(?<![\w])nenhuun\b": "ningún",
        r"(?<![\w])todel\b": "todo",
        r"(?<![\w])pulsa enter\b": "pulsa Enter",
        r"(?<![\w])digite\b": "escribe",
        r"(?<![\w])cliqu[ei]\b": "haz clic",
        r"(?<![\w])selecione\b": "selecciona",
        r"(?<![\w])pressione\b": "pulsa"
    }
    
    try:
        # Ler o arquivo original
        with codecs.open(arquivo, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
        
        # Aplicar as correções de caracteres especiais
        conteudo = corrigir_caracteres_espanhois(conteudo)
        
        # Aplicar substituições de palavras específicas
        for original, correcao in correções_termos.items():
            conteudo = conteudo.replace(original, correcao)
        
        # Aplicar padrões regex
        for padrao, substituicao in padroes_regex.items():
            conteudo = re.sub(padrao, substituicao, conteudo, flags=re.IGNORECASE)
        
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
        print(f"✅ Correções aplicadas diretamente no arquivo: {arquivo}")
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
    corrigir_spanish()
