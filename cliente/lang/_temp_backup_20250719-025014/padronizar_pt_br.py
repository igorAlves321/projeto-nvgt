# -*- coding: utf-8 -*-
"""
Script para padronizar português de Portugal (PT-PT) para português do Brasil (PT-BR)
"""

import os
import re
import codecs
import shutil

def padronizar_pt_br(arquivo_entrada, arquivo_saida):
    print("\033[1;34m⚙️ PADRONIZADOR PT-BR\033[0m")
    print("="*40)
    print(f"Este script padroniza o texto de português de Portugal (PT-PT) para português do Brasil (PT-BR).")
    print(f"📄 Lê arquivos em ANSI e salva o resultado também em ANSI.")
    
    # Backup do arquivo original se já não existir
    if not os.path.exists(arquivo_entrada + ".backup"):
        shutil.copy2(arquivo_entrada, arquivo_entrada + ".backup")
        print(f"📑 Backup criado: {arquivo_entrada}.backup")
    
    print(f"🔄 Processando arquivo: {arquivo_entrada}")
    
    # Dicionário de substituições PT-PT para PT-BR
    substituicoes = {
        # Verbos conjugados
        r'\bresides\b': 'reside',
        r'\brescebes\b': 'recebe',
        r'\brecebestes\b': 'recebeu',
        r'\bfazes\b': 'faz',
        r'\bpodes\b': 'pode',
        r'\bdeves\b': 'deve',
        r'\bestavas\b': 'estava',
        r'\bqueres\b': 'quer',
        r'\bpercebestes\b': 'percebeu',
        r'\bentregas\b': 'entrega',
        r'\brecebes\b': 'recebe',
        r'\bestas\b': 'está',
        r'\bvoltes\b': 'volte',
        r'\bfizeram\b': 'fizeram',
        r'\bcomeçastes\b': 'começou',
        r'\bpensastes\b': 'pensou',
        r'\bterás\b': 'terá',
        r'\bacharás\b': 'achará',
        r'\bpoderás\b': 'poderá',
        
        # Pronomes
        r'\btu\b': 'você',
        r'\bvós\b': 'vocês',
        r'\bcontigo\b': 'com você',
        r'\bconvosco\b': 'com vocês',
        
        # Vocabulário PT-PT vs PT-BR
        r'\bautocarros?\b': 'ônibus',
        r'\bautocarro\b': 'ônibus',
        r'\becrã\b': 'tela',
        r'\becrans\b': 'telas',
        r'\bcomboio\b': 'trem',
        r'\brápido\b': 'rápido',
        r'\bsanita\b': 'vaso sanitário',
        r'\bfato\b': 'terno',
        r'\bcapacete\b': 'capacete',
        r'\bcarro\b': 'carro',
        r'\bduche\b': 'chuveiro',
        r'\bportagem\b': 'pedágio',
        r'\binvólucro\b': 'embalagem',
        r'\bagasalho\b': 'casaco',
        r'\bsandes\b': 'sanduíche',
        r'\btalho\b': 'açougue',
        r'\brelva\b': 'grama',
        r'\btransporte\b': 'transporte',
        r'\bicónico\b': 'icônico',
        r'\bcaldeirada\b': 'ensopado',
        r'\braspadinha\b': 'raspadinha',
        r'\bcriança\b': 'criança',
        r'\bcasa de banho\b': 'banheiro',
        r'\bconcerto\b': 'conserto',
        r'\bvidro\b': 'vidro',
        r'\bvidros\b': 'vidros',
        r'\bcartões?\b': 'cartão',
        r'\bcartões\b': 'cartões',
        r'\bpera\b': 'espera',
        r'\boito\b': 'oito',
        r'\bpetróleo\b': 'petróleo',
        r'\bpiquenique\b': 'piquenique',
        r'\bpiqueniques\b': 'piqueniques',
        r'\bcomputadores?\b': 'computador',
        r'\bcomputadores\b': 'computadores',
        r'\bmoedas?\b': 'moeda',
        r'\bmoedas\b': 'moedas',
        
        # Expressões típicas
        r'\bneste momento\b': 'agora',
        r'\bde facto\b': 'de fato',
        r'\bpor favor\b': 'por favor',
        
        # Palavras com troca de grafias
        r'\bação\b': 'ação',
        r'\bcação\b': 'cação',
        r'\beducação\b': 'educação',
        r'\batividade\b': 'atividade',
        r'\bativa\b': 'ativa',
        r'\bativo\b': 'ativo',
        r'\bexatamente\b': 'exatamente',
        r'\bgênio\b': 'gênio',
        r'\bbiologia\b': 'biologia',
        r'\bfruta\b': 'fruta',
        r'\bpolícia\b': 'polícia',
        
        # Tratamento
        "recebes 100000000 de reais! muitas felicidades!": "recebe 100000000 de reais! muitas felicidades!",
        "muitas felicidades por chegar atж este lugar e por superрr tudo, toma tua recompensa tu mereces": "muitas felicidades por chegar atж este lugar e por superar tudo, toma sua recompensa você merece",
        "vocЖ estр em um lugar desconhecido Para vocЖ": "você está em um lugar desconhecido para você",
    }
    
    # Ler o arquivo original
    try:
        with codecs.open(arquivo_entrada, 'r', encoding='cp1252', errors='replace') as f:
            conteudo = f.read()
            
        # Tamanho original
        tamanho_original = len(conteudo)
        print(f"📊 Tamanho original: {tamanho_original} caracteres")
        
        # Aplicar substituições
        print("🔄 Aplicando padronização PT-BR...")
        for padrao, substituicao in substituicoes.items():
            conteudo = re.sub(padrao, substituicao, conteudo, flags=re.IGNORECASE)
            
        # Salvar o arquivo corrigido
        with codecs.open(arquivo_saida, 'w', encoding='cp1252', errors='replace') as f:
            f.write(conteudo)
            
        print(f"✅ Arquivo padronizado salvo em: {arquivo_saida}")
        print(f"✅ Processo concluído!")
        
    except Exception as e:
        print(f"❌ Erro ao processar arquivo: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    arquivo_entrada = input("Digite o nome do arquivo a ser padronizado: ")
    if os.path.exists(arquivo_entrada):
        nome_base, extensao = os.path.splitext(arquivo_entrada)
        arquivo_saida = nome_base + "_ptbr" + extensao
        padronizar_pt_br(arquivo_entrada, arquivo_saida)
    else:
        print(f"❌ Arquivo não encontrado: {arquivo_entrada}")
