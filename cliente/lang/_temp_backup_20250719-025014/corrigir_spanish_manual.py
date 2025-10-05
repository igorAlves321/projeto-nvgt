# -*- coding: utf-8 -*-
"""
Script para corrigir manualmente o arquivo spanish.lang
Para corrigir problemas específicos de codificação ANSI com caracteres espanhóis
"""

import os
import codecs
import shutil

def corrigir_manualmente():
    """Corrige manualmente os principais problemas de codificação ANSI no arquivo spanish.lang"""
    
    arquivo_entrada = "spanish.lang"
    arquivo_saida = "spanish_corrigido_manual.lang"
    
    print("\033[1;34m🔧 CORREÇÃO MANUAL DO ARQUIVO ESPANHOL\033[0m")
    print("="*50)
    
    # Criar backup se necessário
    if not os.path.exists(arquivo_entrada + ".backup-manual"):
        shutil.copy2(arquivo_entrada, arquivo_entrada + ".backup-manual")
        print(f"📑 Backup criado: {arquivo_entrada}.backup-manual")
    
    # Mapeamento direto de caracteres espanhóis
    mapeamentos = {
        '¿': '¿',  # Interrogação invertida
        '¡': '¡',  # Exclamação invertida
        'ñ': 'ñ',  # n com til
        'Ñ': 'Ñ',  # N com til
        'á': 'á',  # a com acento agudo
        'é': 'é',  # e com acento agudo
        'í': 'í',  # i com acento agudo
        'ó': 'ó',  # o com acento agudo
        'ú': 'ú',  # u com acento agudo
        'ü': 'ü',  # u com trema
        'Á': 'Á',  # A com acento agudo
        'É': 'É',  # E com acento agudo
        'Í': 'Í',  # I com acento agudo
        'Ó': 'Ó',  # O com acento agudo
        'Ú': 'Ú',  # U com acento agudo
        'Ü': 'Ü',  # U com trema
        
        # Caracteres que aparecem incorretamente no arquivo
        '?': '¿',
        '!': '¡',
        'ж': 'é',
        'р': 'á',
        'ь': 'í',
        'Щ': 'ú',
        'з': 'ó',
        'ы': 'ñ',
        'в': 'ú',
        '¿': '¿',
        
        # Erros de palavras
        'Op??es': 'Opciones',
        'sa?da': 'salida',
        '?udio': 'audio',
        'n?o': 'no',
        'interrup??o': 'interrupción',
        'confirma??o': 'confirmación',
        'atualiza??o': 'actualización',
        'vers?o': 'versión',
        'localiza??o': 'localización',
        'n?vel': 'nivel',
        'sele??o': 'selección',
        'selecioen la': 'selecciona',
        'desativadel': 'desactivado',
        'conprar': 'comprar',
        'persoen laje': 'personaje',
        'persoen lagem': 'personaje',
        'a??o': 'acción',
        'teln': 'ton',
        'gelen la': 'gola',
        'deen la': 'dona',
        'delnde': 'donde',
        'en elche': 'noche',
        'munici?n': 'munición',
        'daыo': 'mal',
        'ladel': 'lado'
    }
    
    # Corrigir palavras problemáticas específicas
    substituicoes_palavras = {
        'uen la': 'una',
        'todel': 'todo',
        'toe los': 'todos',
        'uuna': 'una',
        'munici?n': 'munición',
        'contrase?a': 'contraseña',
        'comestibles': 'comestibles',
        'desse conectado': 'desconectado',
        'conectandel': 'conectando',
        'servidelr': 'servidor',
        'desarrolladelr': 'desarrollador',
        'examen lar': 'examinar',
        'abandon': 'abandon',
        'jugadelr': 'jugador',
        'activadel': 'activado',
        'desactivadel': 'desactivado',
        'persounaje': 'personaje',
        'conectadel': 'conectado',
        'iniciadel': 'iniciado',
        'selecciounar': 'seleccionar'
    }
    
    try:
        # Lê o conteúdo do arquivo
        with codecs.open(arquivo_entrada, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
        
        # Aplica os mapeamentos
        for origem, destino in mapeamentos.items():
            conteudo = conteudo.replace(origem, destino)
        
        # Aplica as substituições de palavras
        for origem, destino in substituicoes_palavras.items():
            conteudo = conteudo.replace(origem, destino)
        
        # Remove duplicatas
        linhas = conteudo.split("\n")
        linhas_unicas = []
        valores_vistos = set()
        
        for linha in linhas:
            if not linha.strip() or '=' not in linha:
                continue
                
            # Verifica se o valor após o = já foi visto
            _, valor = linha.split('=', 1)
            
            if valor.strip() not in valores_vistos:
                valores_vistos.add(valor.strip())
                linhas_unicas.append(linha)
        
        # Salva o arquivo corrigido
        with codecs.open(arquivo_saida, 'w', encoding='cp1252', errors='replace') as f:
            f.write("\n".join(linhas_unicas))
        
        print(f"📊 Linhas duplicadas removidas: {len(linhas) - len(linhas_unicas)}")
        print(f"✅ Arquivo corrigido salvo em: {arquivo_saida}")
        print(f"✅ Processo concluído!")
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        return False
        
    return True

if __name__ == "__main__":
    corrigir_manualmente()
