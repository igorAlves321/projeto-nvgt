# -*- coding: utf-8 -*-
"""
Script para substituir o arquivo original spanish.lang pelo arquivo corrigido
"""

import os
import shutil
import datetime

def substituir_arquivo():
    """Substitui o arquivo original pelo arquivo corrigido, mantendo um backup com data."""
    
    # Definição dos arquivos
    arquivo_original = "spanish.lang"
    arquivo_corrigido = "spanish_corrigido_manual.lang"
    
    # Verificar se os arquivos existem
    if not os.path.exists(arquivo_original):
        print(f"❌ Arquivo original não encontrado: {arquivo_original}")
        return False
    
    if not os.path.exists(arquivo_corrigido):
        print(f"❌ Arquivo corrigido não encontrado: {arquivo_corrigido}")
        return False
    
    # Data atual para o nome do backup
    data_atual = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    nome_backup = f"{arquivo_original}.backup-{data_atual}"
    
    print(f"📑 Criando backup do arquivo original: {nome_backup}")
    try:
        # Criar backup com data/hora
        shutil.copy2(arquivo_original, nome_backup)
        
        # Substituir arquivo original pelo corrigido
        print(f"🔄 Substituindo {arquivo_original} pelo arquivo corrigido {arquivo_corrigido}")
        shutil.copy2(arquivo_corrigido, arquivo_original)
        
        print(f"✅ Substituição concluída com sucesso!")
        print(f"✅ O arquivo original foi substituído e um backup foi criado como {nome_backup}")
        
        return True
    except Exception as e:
        print(f"❌ Erro ao substituir arquivo: {str(e)}")
        return False

if __name__ == "__main__":
    print("\033[1;34m📂 SUBSTITUIDOR DE ARQUIVO DE IDIOMA\033[0m")
    print("="*50)
    print("Este script vai substituir o arquivo original de idioma pelo arquivo corrigido.")
    print("Um backup do arquivo original será criado antes da substituição.")
    
    resposta = input("Deseja continuar com a substituição? (s/n): ").strip().lower()
    if resposta == 's':
        substituir_arquivo()
    else:
        print("❌ Operação cancelada pelo usuário.")
