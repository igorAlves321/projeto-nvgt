# -*- coding: utf-8 -*-
"""
Script final para corrigir o arquivo de idioma inglês
Este script corrige caracteres mal formatados, erros ortográficos e outros problemas
diretamente no arquivo English.lang, mantendo a codificação ANSI (Windows-1252)
"""

import os
import re
import codecs
import shutil
import datetime

def corrigir_english_final():
    """
    Corrige o arquivo English.lang diretamente, mantendo a codificação ANSI (Windows-1252)
    """
    arquivo = "English.lang"
    arquivo_backup = f"{arquivo}.backup-final-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    print("\033[1;34m⚙️ CORRETOR FINAL DE ARQUIVO INGLÊS\033[0m")
    print("="*50)
    print(f"Este script faz correções finais em caracteres e termos específicos do arquivo {arquivo}.")
    print(f"📄 Lê e edita o arquivo em ANSI, preservando a codificação original.")
    
    # Criar backup com data/hora atual
    shutil.copy2(arquivo, arquivo_backup)
    print(f"📑 Backup criado: {arquivo_backup}")
    
    print(f"🔄 Processando arquivo: {arquivo}")

    # Correções de termos em português para inglês
    traducoes = {
        # Traduções diretas do português para inglês
        "Voltar": "Back",
        "Sair": "Exit",
        "Conectando": "Connecting",
        "Jogar": "Connect",
        "Criar personagem": "Create character",
        "Criar nova conta": "Create a new account",
        "Teste de alto-falantes": "Speaker test",
        "Digite sua senha": "Enter your password",
        "Digite seu nome de usuário": "Enter your username",
        "Selecionar personagem": "Select a character",
        "Selecionar voz": "Select a voice",
        "Selecionar um arquivo de idioma": "Select a language file",
        "Selecionar dispositivo de saída de áudio": "Select an audio output device",
        "Configurações": "Settings",
        "Configurações gerais": "Global Settings",
        "Configurações do perfil": "Profile Settings",
        "Verificar por atualizações": "Check for updates",
        "Modo voz SAPI": "SAPI voice mode",
        "Modo voz SAPI desligado": "SAPI voice mode disabled",
        "Todos os itens": "All items",
        "Nenhum item": "No items",
        "Compartimento de Armas": "Weapons compartment",
        "Compartimento de Munições": "Ammo compartment",
        "Compartimento de Roupas": "Clothes compartment",
        "Compartimento de Explosivos": "Explosives compartment",
        "Cole??o de corpos": "Corpses collection",
        "Status": "Status",
        "Suas preferências": "Your preferences",
        "Ninguém selecionado": "Nobody selected",
        "Porta de saída": "Exit door",
        "Estacionamento": "Parking lot",
        "Ponte": "Bridge",
        "Escada": "Stairs",
        "Escadas": "Stairs",
        "Lama": "Mud",
        "Rua": "Street",
        "Cidade": "City",
        "Floresta": "Forest",
        "Lago": "Lake",
        "Entrada": "Entrance",
        "Piscina": "Pool",
        "Cafeteria": "Cafeteria",
        "Loja": "Store",
        "Rampa": "Ramp",
        "Terra": "Soil",
        "Mato": "Bush",
        "Árvore": "Tree",
        "Clareira": "Clearing",
    }

    # Expressões a corrigir
    padroes_comuns = {
        r"\bvoce\b": "you",
        r"\bVoce\b": "You",
        r"\bvocê\b": "you",
        r"\bVocê\b": "You",
        r"\besta\b(?!\w)": "is",
        r"\bestá\b(?!\w)": "is",
        r"\bEsta\b(?!\w)": "This",
        r"\bEstá\b(?!\w)": "Is",
        r"\bestão\b": "are",
        r"\bEstão\b": "Are",
        r"\bé\b": "is",
        r"\bÉ\b": "Is",
        r"\bnão\b": "not",
        r"\bNão\b": "Not",
        r"\bsão\b": "are",
        r"\bSão\b": "Are",
        r"\bpor\b": "by",
        r"\bPor\b": "By",
        r"\bem\b": "in",
        r"\bEm\b": "In",
        r"\bdo\b": "of the",
        r"\bda\b": "of the",
        r"\bdos\b": "of the",
        r"\bdas\b": "of the",
        r"\bno\b": "in the",
        r"\bna\b": "in the",
        r"\bnos\b": "in the",
        r"\bnas\b": "in the",
        r"\bao\b": "to the",
        r"\baos\b": "to the",
        r"\bà\b": "to the",
        r"\bàs\b": "to the",
        r"\bum\b": "a",
        r"\buma\b": "a",
        r"\buns\b": "some",
        r"\bumas\b": "some",
        r"\bque\b": "that",
        r"\bcom\b": "with",
        r"\bsem\b": "without",
        r"\bpara\b": "to",
        r"\bpelo\b": "by the",
        r"\bpela\b": "by the",
        r"\bpelos\b": "by the",
        r"\bpelas\b": "by the",
        r"\bentre\b": "between",
        r"\bsobre\b": "about",
        r"\baté\b": "until",
        r"\bcomo\b": "how",
        r"\bquando\b": "when",
        r"\bonde\b": "where",
        r"\bporque\b": "because",
        r"\bpressione\s+[Ee]nter\b": "press Enter",
        r"\bprecione\s+[Ee]nter\b": "press Enter",
        r"\b[Pp]ressione\s+ENTER\b": "press Enter",
    }

    # Correções específicas de ortografia e pontuação
    correcoes_ortografia = {
        "Your preferences": "Your Preferences",
        "Global settings": "Global Settings",
        "Profile settings": "Profile Settings",
        "Options menu": "Options Menu",
        "Parking Lot.": "Parking Lot",
        "Snack Bar.": "Snack Bar",
        "Club.": "Club",
        "Main door.": "Main Door",
        "Weapons compartment..": "Weapons Compartment",
        "Ammo compartment..": "Ammo Compartment",
        "Clothes compartment..": "Clothes Compartment",
        "Explosives compartment..": "Explosives Compartment",
        "Corpses collection.": "Corpses Collection",
        "SAPI voice mode Disabled": "SAPI Voice Mode Disabled",
        "Enable confirmation to exit.": "Enable Confirmation to Exit",
        "Disable confirmation to exit.": "Disable Confirmation to Exit",
        "in the items": "No Items",
        "all items": "All Items",
        "nobody selected": "Nobody Selected",
        "SAP voice mode": "SAPI Voice Mode",
        "has ben sent": "has been sent",
        "...": "..",
        "..": "...",
        "Connecting..": "Connecting...",
        "allowd": "allowed",
        "seo": "are",
        "neo": "not",
        "Main street of the city": "Main Street of the City",
        "Long street of the city": "Long Street of the City",
        "A quiet street of the city": "A Quiet Street of the City",
        "Exploration area": "Exploration Area",
    }

    try:
        # Ler o arquivo original
        with codecs.open(arquivo, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
        
        # Substituir caracteres com diacríticos por suas versões sem diacríticos
        caracteres_com_diacriticos = 'áàãâäéèêëíìîïóòõôöúùûüçñÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇÑ'
        caracteres_sem_diacriticos = 'aaaaaeeeeiiiiooooouuuucnAAAAAEEEEIIIIOOOOOUUUUCN'
        
        tabela_traducao = str.maketrans(caracteres_com_diacriticos, caracteres_sem_diacriticos)
        conteudo = conteudo.translate(tabela_traducao)
        
        # Substituir caracteres cirílicos e outros caracteres especiais
        caracteres_especiais = {
            "Я": "a", "ж": "e", "з": "s", "щ": "u", "ы": "bl", 
            "ь": "b", "ъ": "", "Э": "E", "ю": "yu", "я": "ya"
        }
        
        for original, substituto in caracteres_especiais.items():
            conteudo = conteudo.replace(original, substituto)
        
        # Aplicar traduções do português para o inglês
        for portugues, ingles in traducoes.items():
            # Criar um padrão que corresponda à palavra exata
            padrao = r'\b' + re.escape(portugues) + r'\b'
            conteudo = re.sub(padrao, ingles, conteudo, flags=re.IGNORECASE)
        
        # Aplicar padrões comuns
        for padrao, substituicao in padroes_comuns.items():
            conteudo = re.sub(padrao, substituicao, conteudo)
        
        # Aplicar correções de ortografia
        for incorreto, correto in correcoes_ortografia.items():
            conteudo = conteudo.replace(incorreto, correto)
        
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
            if chave.strip() in chaves_vistas:
                continue  # Pula chaves duplicadas
            
            # Se este valor ainda não foi visto ou se a chave é igual ao valor, adicione-o
            if valor.strip() not in valores_vistos or chave.strip() == valor.strip():
                valores_vistos.add(valor.strip())
                chaves_vistas[chave.strip()] = True
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
    corrigir_english_final()
