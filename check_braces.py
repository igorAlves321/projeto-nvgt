#!/usr/bin/env python3
"""
Script para verificar o balanceamento de chaves em arquivos BGT
"""
import sys

def check_braces(filename):
    """Verifica se as chaves estão balanceadas no arquivo"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        with open(filename, 'r', encoding='latin-1') as f:
            content = f.read()
    
    stack = []
    line_number = 1
    in_string = False
    in_comment = False
    i = 0
    
    while i < len(content):
        char = content[i]
        
        # Handle newlines
        if char == '\n':
            line_number += 1
            in_comment = False  # Single line comments end at newline
        
        # Handle strings
        elif char == '"' and not in_comment:
            in_string = not in_string
        
        # Handle comments
        elif not in_string:
            if char == '/' and i + 1 < len(content):
                if content[i + 1] == '/':
                    in_comment = True
                elif content[i + 1] == '*':
                    # Multi-line comment start
                    j = i + 2
                    while j < len(content) - 1:
                        if content[j] == '*' and content[j + 1] == '/':
                            i = j + 1
                            break
                        if content[j] == '\n':
                            line_number += 1
                        j += 1
            
            elif char == '{' and not in_comment:
                stack.append(('{', line_number))
                print("Abrindo chave na linha " + str(line_number))
            
            elif char == '}' and not in_comment:
                if not stack:
                    print("ERRO: Chave de fechamento sem abertura na linha " + str(line_number))
                    return False
                
                open_brace, open_line = stack.pop()
                print("Fechando chave da linha " + str(open_line) + " na linha " + str(line_number))
        
        i += 1
    
    # Check for unmatched opening braces
    if stack:
        print("ERRO: Chaves não fechadas:")
        for brace, line in stack:
            print("  - Chave aberta na linha " + str(line) + " não foi fechada")
        return False
    
    print("Todas as chaves estão balanceadas!")
    return True

if __name__ == "__main__":
    filename = r"d:\programação\bgt\projetoIg\servidor\includes\voids.bgt"
    check_braces(filename)
