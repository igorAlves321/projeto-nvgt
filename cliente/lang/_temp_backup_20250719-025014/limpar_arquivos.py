# -*- coding: utf-8 -*-
"""
Script para limpar os arquivos temporários e manter apenas os arquivos oficiais de idioma
"""

import os
import shutil
import glob
import time

def limpar_arquivos():
    """
    Remove todos os scripts e backups desnecessários, mantendo apenas os arquivos oficiais
    """
    print("\033[1;34m⚙️ LIMPEZA DE ARQUIVOS\033[0m")
    print("="*50)
    print("Este script remove arquivos temporários e backups, mantendo apenas os arquivos oficiais de idioma.")
    
    # Lista de arquivos oficiais de idioma para manter
    arquivos_oficiais = [
        "English.lang",
        "spanish.lang",
        "portuguese.lang",
        "french.lang",
        "Turco.lang",
        "langs.version"
    ]
    
    # Obter lista de todos os arquivos no diretório atual
    todos_arquivos = os.listdir(".")
    
    # Criar uma pasta para mover os arquivos temporários (por precaução)
    pasta_temp = "_temp_backup_" + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(pasta_temp, exist_ok=True)
    print(f"📁 Pasta temporária criada: {pasta_temp}")
    
    # Contar arquivos removidos
    total_removidos = 0
    
    # Processar cada arquivo
    for arquivo in todos_arquivos:
        # Se não for um arquivo oficial, mova para a pasta temporária
        if arquivo not in arquivos_oficiais and os.path.isfile(arquivo):
            # Verifica se é um script Python ou arquivo de backup
            if arquivo.endswith(".py") or arquivo.endswith(".ps1") or "backup" in arquivo or "corrigido" in arquivo:
                shutil.move(arquivo, os.path.join(pasta_temp, arquivo))
                print(f"🔄 Movido para pasta temporária: {arquivo}")
                total_removidos += 1
    
    print(f"📊 Total de arquivos movidos: {total_removidos}")
    print(f"✅ Processo concluído!")
    print(f"\n⚠️ IMPORTANTE: Os arquivos não foram excluídos permanentemente.")
    print(f"⚠️ Eles foram movidos para a pasta '{pasta_temp}' por precaução.")
    print(f"⚠️ Verifique se tudo está funcionando corretamente antes de excluir esta pasta.")
    
    return True

if __name__ == "__main__":
    limpar_arquivos()
