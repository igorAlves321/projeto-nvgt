#!/usr/bin/env python3
"""
Script detalhado para encontrar chaves não balanceadas
"""

def detailed_check_braces(filename):
    """Verifica chaves com detalhes linha por linha"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except:
        with open(filename, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    stack = []
    in_string = False
    in_multiline_comment = False
    
    for line_num, line in enumerate(lines, 1):
        i = 0
        in_single_comment = False
        
        while i < len(line):
            char = line[i]
            
            # Handle single line comments
            if char == '/' and i + 1 < len(line) and line[i + 1] == '/' and not in_string and not in_multiline_comment:
                in_single_comment = True
            
            # Handle multiline comments
            elif char == '/' and i + 1 < len(line) and line[i + 1] == '*' and not in_string and not in_single_comment:
                in_multiline_comment = True
                i += 1  # Skip the *
            elif char == '*' and i + 1 < len(line) and line[i + 1] == '/' and in_multiline_comment:
                in_multiline_comment = False
                i += 1  # Skip the /
            
            # Handle strings
            elif char == '"' and not in_single_comment and not in_multiline_comment:
                in_string = not in_string
            
            # Handle braces
            elif not in_string and not in_single_comment and not in_multiline_comment:
                if char == '{':
                    stack.append(('{', line_num, line.strip()))
                    print(f"Linha {line_num}: Abrindo chave - {line.strip()}")
                elif char == '}':
                    if not stack:
                        print(f"ERRO na linha {line_num}: '}' sem '{' correspondente")
                        print(f"Linha: {line.strip()}")
                        return False
                    
                    open_brace, open_line_num, open_line = stack.pop()
                    print(f"Linha {line_num}: Fechando chave (aberta na linha {open_line_num}) - {line.strip()}")
            
            i += 1
        
        # Reset single line comment flag at end of line
        in_single_comment = False
    
    # Check for unmatched opening braces
    if stack:
        print(f"\nERROS ENCONTRADOS: {len(stack)} chave(s) não fechada(s):")
        for brace, line_num, line_content in stack:
            print(f"  Linha {line_num}: '{' não fechada - {line_content}")
        return False
    
    print("\n✅ Todas as chaves estão balanceadas!")
    return True

if __name__ == "__main__":
    filename = r"d:\programação\bgt\projetoIg\servidor\includes\voids.bgt"
    detailed_check_braces(filename)
