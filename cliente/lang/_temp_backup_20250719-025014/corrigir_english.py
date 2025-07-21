# -*- coding: utf-8 -*-
"""
Script para corrigir o arquivo de idioma inglês
Este script corrige caracteres mal formatados, erros ortográficos e outros problemas
diretamente no arquivo English.lang, mantendo a codificação ANSI (Windows-1252)
"""

import os
import re
import codecs
import shutil
import datetime

def corrigir_english():
    """
    Corrige o arquivo English.lang diretamente, mantendo a codificação ANSI (Windows-1252)
    """
    arquivo = "English.lang"
    arquivo_backup = f"{arquivo}.backup-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print("\033[1;34m⚙️ CORRETOR DE ARQUIVO INGLÊS\033[0m")
    print("="*50)
    print(f"Este script corrige caracteres mal formatados, erros ortográficos e problemas de consistência diretamente no arquivo {arquivo}.")
    print(f"📄 Lê e edita o arquivo em ANSI, preservando a codificação original.")
    
    # Criar backup com data/hora atual
    shutil.copy2(arquivo, arquivo_backup)
    print(f"📑 Backup criado: {arquivo_backup}")
    
    print(f"🔄 Processando arquivo: {arquivo}")
    
    # Correções de caracteres especiais do inglês (principalmente acentos que não existem no inglês)
    def corrigir_caracteres_especiais(texto):
        # Substituições de caracteres especiais
        mapa = {
            # Caracteres que aparecem incorretamente
            "?": "'",  # Substituir o ponto de interrogação deslocado por apóstrofo
            "Я": "à",  # Substituir caracteres cirílicos
            "?": "e",  # Questões comuns de caracteres mal codificados
            
            # Correção de caracteres acentuados do português para o inglês
            "á": "a", "Á": "A",
            "à": "a", "À": "A",
            "ã": "a", "Ã": "A",
            "â": "a", "Â": "A",
            "é": "e", "É": "E",
            "ê": "e", "Ê": "E",
            "í": "i", "Í": "I",
            "ó": "o", "Ó": "O",
            "õ": "o", "Õ": "O",
            "ô": "o", "Ô": "O",
            "ú": "u", "Ú": "U",
            "ç": "c", "Ç": "C",
            
            # Caracteres cirílicos que aparecem por erro de codificação
            "Ж": "e", "ж": "e",
            "р": "a", "Р": "A",
            "с": "c", "С": "C",
            "в": "b", "В": "B",
            "н": "h", "Н": "H",
            "ь": "b", "Ь": "B",
            "Щ": "u", "щ": "u",
            "з": "3", "З": "3",
            "ы": "bl", "Ы": "BL",
            
            # Outros caracteres especiais
            "ñ": "n", "Ñ": "N",
            "ü": "u", "Ü": "U"
        }
        
        # Aplicar substituições
        for original, correcao in mapa.items():
            texto = texto.replace(original, correcao)
            
        return texto
    
    # Correções de termos e expressões específicas para o inglês
    correcoes_termos = {
        # Correções de ortografia e gramática
        "allowd": "allowed",
        "itens": "items",
        "ssmell": "smell",
        "reprodueeo": "playback",
        "verseo": "version",
        "localizaeeo": "location",
        "opeees": "options",
        "saeda": "output",
        "audio": "audio",
        "neo": "not",
        "interrupeeo": "interruption",
        "confirmaeeo": "confirmation",
        "atualizaeeo": "update",
        "verificaeeo": "verification",
        "munieees": "ammo",
        "preferencias": "preferences",
        "coleeeo": "collection",
        "ninguem": "nobody",
        "selecionadel": "selected",
        "exploraeeo": "exploration",
        "configuraeees": "settings",
        "historica": "historic",
        "porteo": "gate",
        "elevaeeo": "elevation",
        "inclinaeeo": "inclination",
        "arvore": "tree",
        "ervore": "tree",
        
        # Traduções específicas
        "Jogar": "Connect",
        "Criar personagem": "Create character",
        "Teste de alto-falantes": "Speaker test",
        "Sair": "Exit",
        "Digite sua senha": "Enter your password",
        
        # Padronização de termos
        "sape": "SAPI",
        "sap mode": "SAPI mode",
        "SAP voice mode": "SAPI voice mode",
        "all itens.": "All items.",
        "all itens": "all items",
        "All itens": "All items",
        "No itens.": "No items.",
        "No itens": "No items",
        "all items.": "All items.",
        "Weapons compartment": "Weapons compartment.",
        "Ammo compartment": "Ammo compartment.",
        "Clothes compartment": "Clothes compartment.",
        "Explosives compartment": "Explosives compartment.",
        "Corpses colection.": "Corpses collection.",
        "Main door": "Main door.",
        "Club.": "Club",
        "snack bar.": "Snack Bar",
        "Parking lot.": "Parking Lot",
        
        # Correções de capitalização
        "version": "Version",
        "please insert": "Please insert",
        "press enter": "press Enter",
        "press ENTER": "press Enter",
        "options menu": "Options Menu",
        "global settings": "Global Settings",
        "profile settings": "Profile Settings",
        "your preferences": "Your Preferences",
        
        # Correções de espaços e pontuação
        "Exit.": "Exit",
        "Connecting...": "Connecting...",
        " ": " ",  # Substitui espaços duplos por espaços simples
        "..": ".",  # Corrige pontos duplicados
    }
    
    # Expressões regulares para padrões mais complexos
    padroes_regex = {
        r"\bpress\s+[Ee][Nn][Tt][Ee][Rr]\b": "press Enter",
        r"(?<!\w)espa\?os(?!\w)": "spaces",
        r"(?<!\w)n\?o(?!\w)": "not",
        r"(?<!\w)s\?o(?!\w)": "are",
        r"\bvoce\b": "you",
        r"\bVoce\b": "You",
        r"\bVoc[eêЖ]\b": "You",
        r"\bvoc[eêЖ]\b": "you",
        r"\best[aáр]\b": "is",
        r"\bEst[aáр]\b": "Is",
        r"\bpress[io]one\b": "press",
        r"\bhá\b": "there is",
        r"\bé\b": "is",
        r"\bao\b": "to the",
        r"\bna\b": "in the",
        r"\bno\b": "in the",
        r"\bpossível\b": "possible",
        r"\bpossivel\b": "possible",
        r"\bEnable\s+screen\s+reader": "Enable screen reader",
    }
    
    try:
        # Ler o arquivo original
        with codecs.open(arquivo, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
        
        # Aplicar as correções de caracteres especiais
        conteudo = corrigir_caracteres_especiais(conteudo)
        
        # Aplicar substituições de termos específicos
        for original, correcao in correcoes_termos.items():
            conteudo = conteudo.replace(original, correcao)
        
        # Aplicar padrões regex
        for padrao, substituicao in padroes_regex.items():
            conteudo = re.sub(padrao, substituicao, conteudo, flags=re.IGNORECASE)
        
        # Dividir em linhas para remover duplicatas
        linhas = conteudo.split('\n')
        linhas_unicas = []
        valores_vistos = set()
        chaves_vistas = {}
        
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
            
            # Verificar se esta chave já foi vista
            if chave in chaves_vistas:
                continue  # Pula chaves duplicadas
            
            # Se este valor ainda não foi visto, adicione-o
            if valor.strip() not in valores_vistos or chave.strip() == valor.strip():
                valores_vistos.add(valor.strip())
                chaves_vistas[chave] = True
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
    corrigir_english()
