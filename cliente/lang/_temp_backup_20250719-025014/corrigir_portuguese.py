#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import codecs
import sys

def fix_portuguese_file(input_file, output_file):
    # Lê o arquivo original com codificação ANSI
    with codecs.open(input_file, 'r', encoding='cp1252') as f:
        content = f.readlines()
    
    # Dicionário para substituir os caracteres malformados
    replacements = {
        "с": "ã", "р": "á", "з": "ó", "у": "ç", "ж": "é", "Ж": "Ê", 
        "Щ": "ú", "Э": "ú", "б": "v", "е": "e", "о": "o", "в": "v",
        "н": "n", "т": "t", "м": "m", "и": "i", "Я": "À", "ы": "y",
        "а": "a", "к": "k", "л": "l", "д": "d", "п": "p", "й": "y",
        "ц": "c", "х": "h", "з": "z", "Агора": "Agora"
    }
    
    print(f"Processando arquivo: {input_file}")
    print(f"Total de linhas: {len(content)}")
    
    # Processa linha por linha
    fixed_lines = []
    keys_seen = {}
    
    for i, line in enumerate(content):
        if line.strip() == "":
            fixed_lines.append(line)
            continue
        
        # Se a linha não tem o formato chave=valor, preserva como está
        if "=" not in line:
            fixed_lines.append(line)
            continue
        
        try:
            key, value = line.strip().split("=", 1)
            
            # Faz as substituições
            for old, new in replacements.items():
                value = value.replace(old, new)
            
            # Corrije erros específicos comuns
            value = value.replace("vocЖ", "você")
            value = value.replace("nсo", "não")
            value = value.replace("estр", "está")
            value = value.replace("sсo", "são")
            value = value.replace("jр", "já")
            value = value.replace("estaусo", "estação")
            value = value.replace("histзria", "história")
            value = value.replace("eletrЗnica", "eletrônica")
            value = value.replace("observaусo", "observação")
            value = value.replace("construусo", "construção")
            value = value.replace("proteусo", "proteção")
            value = value.replace("cartсo", "cartão")
            value = value.replace("forуa", "força")
            value = value.replace("serр", "será")
            value = value.replace("tЩmulo", "túmulo")
            value = value.replace("рgua", "água")
            value = value.replace("graуas", "graças")
            value = value.replace("atж", "até")
            value = value.replace("ж", "é")
            value = value.replace("cabaыa", "cabana")
            value = value.replace("lЩcifer", "lúcifer")
            value = value.replace("eletrЗnico", "eletrônico")
            value = value.replace("prзximo", "próximo")
            value = value.replace("tambжm", "também")
            
            # Verifica se a chave já foi vista
            if key in keys_seen:
                # Se o valor for diferente, mantém o mais longo
                if len(value) > len(keys_seen[key]):
                    keys_seen[key] = value
                    # Não adiciona duplicados ainda, atualizaremos depois
            else:
                keys_seen[key] = value
                fixed_lines.append(f"{key}={value}")
            
        except ValueError:
            # Se não conseguir separar em key=value, mantém a linha como está
            fixed_lines.append(line)
            print(f"Linha malformada mantida como está (linha {i+1}): {line.strip()}")
    
    print(f"Total de linhas após correção: {len(fixed_lines)}")
    print(f"Linhas removidas (duplicadas): {len(content) - len(fixed_lines)}")
    
    # Escreve o arquivo corrigido com codificação ANSI
    with codecs.open(output_file, 'w', encoding='cp1252') as f:
        f.writelines(fixed_lines)
    
    print(f"Arquivo corrigido salvo em: {output_file}")

if __name__ == "__main__":
    input_file = "portuguese.lang"
    output_file = "portuguese_corrigido.lang"
    
    # Cria backup
    backup_file = input_file + ".backup"
    if not os.path.exists(backup_file):
        with open(input_file, 'rb') as src, open(backup_file, 'wb') as dest:
            dest.write(src.read())
        print(f"Backup criado em: {backup_file}")
    
    fix_portuguese_file(input_file, output_file)
    print("Processo concluído!")
