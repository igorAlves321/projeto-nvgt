import os
import codecs
from datetime import datetime

def carregar_caracteres_problematicos(arquivo_caracteres):
    """
    Carrega o arquivo caracteres.txt com a lista de caracteres problemáticos.
    Cada linha do arquivo deve conter um caractere problemático.
    """
    caracteres = []
    
    if not os.path.exists(arquivo_caracteres):
        print(f"Arquivo {arquivo_caracteres} não encontrado!")
        return caracteres
    
    try:
        # Força codificação ANSI (cp1252)
        with open(arquivo_caracteres, 'r', encoding='cp1252') as f:
            linha_num = 0
            for linha in f:
                linha_num += 1
                linha = linha.strip()
                
                # Ignora linhas vazias e comentários
                if not linha or linha.startswith('#'):
                    continue
                
                # Adiciona cada caractere da linha
                for char in linha:
                    if char not in caracteres and char != ' ':
                        caracteres.append(char)
                        print(f"Caractere problemático carregado: '{char}'")
        
        print(f"\nTotal de caracteres problemáticos carregados: {len(caracteres)}")
        return caracteres
        
    except Exception as e:
        print(f"Erro ao carregar caracteres problemáticos: {e}")
        return []

def tem_caracter_problematico(linha, caracteres_problematicos):
    """Verifica se a linha contém algum caractere problemático"""
    for char in caracteres_problematicos:
        if char in linha:
            return True, char
    return False, None

def criar_backup(arquivo_original):
    """Cria backup do arquivo original com timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_nome = f"{arquivo_original}.backup_{timestamp}"
    
    try:
        with open(arquivo_original, 'r', encoding='cp1252') as origem:
            with open(backup_nome, 'w', encoding='cp1252') as backup:
                backup.write(origem.read())
        print(f"Backup criado: {backup_nome}")
        return True
    except Exception as e:
        print(f"Erro ao criar backup: {e}")
        return False

def processar_arquivo_lang():
    """Processa o arquivo portuguese.lang removendo linhas com caracteres problemáticos"""
    
    # Configurações dos arquivos
    arquivo_lang = 'portuguese.lang'
    arquivo_caracteres = 'caracteres.txt'
    arquivo_corrigir = 'corrigir.txt'
    arquivo_relatorio = 'relatorio_remocoes.txt'
    
    print("=" * 70)
    print("CORRETOR DE CODIFICAÇÃO - REMOÇÃO DE LINHAS PROBLEMÁTICAS")
    print("=" * 70)
    
    # Verifica se os arquivos existem
    if not os.path.exists(arquivo_lang):
        print(f"Arquivo {arquivo_lang} não encontrado!")
        return False
    
    # Carrega os caracteres problemáticos
    print("1. Carregando caracteres problemáticos...")
    caracteres_problematicos = carregar_caracteres_problematicos(arquivo_caracteres)
    
    if not caracteres_problematicos:
        print("Nenhum caractere problemático encontrado!")
        return False
    
    print(f"Caracteres problemáticos: {caracteres_problematicos}")
    
    # Cria backup do arquivo original
    print(f"\n2. Criando backup do arquivo {arquivo_lang}...")
    if not criar_backup(arquivo_lang):
        return False
    
    # Lê o arquivo principal
    print(f"\n3. Processando arquivo {arquivo_lang}...")
    try:
        with open(arquivo_lang, 'r', encoding='cp1252') as f:
            linhas = f.readlines()
        print(f"Arquivo lido com sucesso. Total de linhas: {len(linhas)}")
    except Exception as e:
        print(f"Erro ao ler {arquivo_lang}: {e}")
        return False
    
    # Processa as linhas
    linhas_ok = []
    linhas_problematicas = []
    relatorio_remocoes = []
    
    print(f"\n4. Analisando linhas...")
    
    for i, linha in enumerate(linhas, 1):
        tem_problema, char_encontrado = tem_caracter_problematico(linha, caracteres_problematicos)
        
        if tem_problema:
            linha_problema = f"# Linha {i} (caractere '{char_encontrado}'): {linha}"
            linhas_problematicas.append(linha_problema)
            relatorio_remocoes.append(f"Linha {i}: Removida por conter '{char_encontrado}'")
            relatorio_remocoes.append(f"  Conteúdo: {linha.rstrip()}")
            relatorio_remocoes.append("")
            print(f"  Linha {i}: REMOVIDA (contém '{char_encontrado}') - {linha.strip()[:50]}...")
        else:
            linhas_ok.append(linha)
    
    # Estatísticas
    total_linhas = len(linhas)
    linhas_removidas = len(linhas_problematicas)
    linhas_mantidas = len(linhas_ok)
    
    print(f"\n" + "=" * 50)
    print("ESTATÍSTICAS:")
    print(f"Total de linhas: {total_linhas}")
    print(f"Linhas mantidas: {linhas_mantidas}")
    print(f"Linhas removidas: {linhas_removidas}")
    print("=" * 50)
    
    if linhas_problematicas:
        # Salva as linhas problemáticas no arquivo corrigir.txt
        print(f"\n5. Salvando linhas removidas em {arquivo_corrigir}...")
        try:
            with open(arquivo_corrigir, 'w', encoding='cp1252') as f:
                f.write(f"# LINHAS REMOVIDAS DO {arquivo_lang}\n")
                f.write(f"# Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"# Total de linhas removidas: {linhas_removidas}\n")
                f.write("# Corrija manualmente e depois adicione de volta ao arquivo principal\n")
                f.write("# " + "=" * 60 + "\n\n")
                
                for linha in linhas_problematicas:
                    f.write(linha)
            
            print(f"Linhas problemáticas salvas em: {arquivo_corrigir}")
        except Exception as e:
            print(f"Erro ao salvar {arquivo_corrigir}: {e}")
            return False
        
        # Salva o arquivo limpo
        print(f"\n6. Salvando arquivo limpo...")
        try:
            with open(arquivo_lang, 'w', encoding='cp1252') as f:
                for linha in linhas_ok:
                    f.write(linha)
            print(f"Arquivo {arquivo_lang} atualizado (linhas problemáticas removidas)")
        except Exception as e:
            print(f"Erro ao salvar {arquivo_lang}: {e}")
            return False
        
        # Gera relatório detalhado
        print(f"\n7. Gerando relatório...")
        try:
            with open(arquivo_relatorio, 'w', encoding='cp1252') as f:
                f.write(f"RELATÓRIO DE REMOÇÕES - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Arquivo processado: {arquivo_lang}\n")
                f.write(f"Arquivo de caracteres: {arquivo_caracteres}\n")
                f.write(f"Total de linhas originais: {total_linhas}\n")
                f.write(f"Linhas mantidas: {linhas_mantidas}\n")
                f.write(f"Linhas removidas: {linhas_removidas}\n\n")
                f.write(f"Caracteres problemáticos detectados: {caracteres_problematicos}\n\n")
                f.write("DETALHES DAS REMOÇÕES:\n")
                f.write("-" * 30 + "\n\n")
                
                for linha_relatorio in relatorio_remocoes:
                    f.write(linha_relatorio + "\n")
            
            print(f"Relatório salvo em: {arquivo_relatorio}")
        except Exception as e:
            print(f"Erro ao salvar relatório: {e}")
    
    else:
        print("\n✓ Nenhuma linha problemática encontrada!")
    
    # Resultado final
    print(f"\n" + "=" * 70)
    print("PROCESSO CONCLUÍDO!")
    print("=" * 70)
    print(f"Arquivo original: {arquivo_lang}")
    print(f"Backup criado com timestamp")
    if linhas_problematicas:
        print(f"Linhas removidas salvas em: {arquivo_corrigir}")
        print(f"Relatório detalhado em: {arquivo_relatorio}")
    print(f"Todas as operações realizadas em codificação ANSI (cp1252)")
    
    return True

def criar_arquivo_caracteres_exemplo():
    """Cria um arquivo de exemplo com caracteres problemáticos"""
    arquivo_exemplo = 'caracteres_exemplo.txt'
    
    conteudo_exemplo = """# ARQUIVO DE CARACTERES PROBLEMÁTICOS
# Cada linha pode conter um ou mais caracteres problemáticos
# Linhas que começam com # são comentários e serão ignoradas
# Salve este arquivo como 'caracteres.txt' em codificação ANSI

# Caracteres cirílicos que aparecem por erro de codificação
ж
с
р
з
у
Ж
н
Щ
ы
ь
ј
Я
ъ
м
Л
ш
В
Г

# Você também pode colocar múltiplos caracteres em uma linha
# Exemplo: жсрз

# Adicione outros caracteres problemáticos conforme necessário
"""
    
    try:
        with open(arquivo_exemplo, 'w', encoding='cp1252') as f:
            f.write(conteudo_exemplo)
        print(f"Arquivo de exemplo criado: {arquivo_exemplo}")
        return True
    except Exception as e:
        print(f"Erro ao criar arquivo de exemplo: {e}")
        return False

if __name__ == "__main__":
    print("Corretor de Codificação - Remoção de Linhas Problemáticas")
    print("Desenvolvido para trabalhar com codificação ANSI (cp1252)")
    print()
    
    # Verifica se existe o arquivo de caracteres, se não, cria um exemplo
    if not os.path.exists('caracteres.txt'):
        print("Arquivo 'caracteres.txt' não encontrado.")
        print("Criando arquivo de exemplo...")
        if criar_arquivo_caracteres_exemplo():
            print("✓ Edite o arquivo 'caracteres_exemplo.txt' com seus caracteres problemáticos")
            print("✓ Renomeie para 'caracteres.txt'")
            print("✓ Execute novamente este script")
        exit()
    
    # Executa o processamento
    sucesso = processar_arquivo_lang()
    
    if sucesso:
        print("\n✓ Processo executado com sucesso!")
    else:
        print("\n✗ Processo executado com erros!")