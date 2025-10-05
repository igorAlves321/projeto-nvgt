import os
import re
import sys
from datetime import datetime

class CorretorArquivos:
    def __init__(self):
        # Dicionário de correções ortográficas e de codificação
        # Inclui problemas comuns de codificação ANSI → UTF-8 → ANSI
        self.correcoes = {
            # Problemas de codificação ANSI e caracteres malformados
            'vocÊ': 'você',
            'vocè': 'você', 
            'Vocè': 'Você',
            'vocÈ': 'você',
            'VocÈ': 'Você',
            'ã§': 'ç',  # Problema comum de codificação
            'ã©': 'é',  # Problema comum de codificação
            'ã¡': 'á',  # Problema comum de codificação
            'ã­': 'í',  # Problema comum de codificação
            'ã³': 'ó',  # Problema comum de codificação
            'ãº': 'ú',  # Problema comum de codificação
            'ã ': 'à',  # Problema comum de codificação
            
            # Caracteres malformados cirílicos/russos → caracteres corretos
            # Baseado na análise real dos arquivos portuguese.lang
            'р': 'á',  # como em crжdito → crédito
            'у': 'ç',   # como em posiусo → posição  
            'ж': 'é',   # como em VocЖ → Você, tambжm → também
            'ь': 'í',   # como em possьvel → possível
            'с': 'ã',   # como em sсo → são
            'з': 'ó',   # como em histзrica → histórica  
            'Ж': 'É',   # VocЖ → Você
            'Щ': 'ú',   # como em Щltimas → últimas
            'Ш': 'ú',   # outros casos
            'Я': 'à',   # para casos específicos
            'Б': 'ó',   
            'Ц': 'ó',   
            'В': 'í',   
            'Г': 'ã',   
            'З': 'ó',   
            'К': 'í',   
            'Л': 'ü',   
            'М': 'é',   
            'Н': 'ã',   
            'П': 'â',   
            'Р': 'Á',   
            'С': 'Ã',   
            'Т': 'É',   
            'Ф': 'í',   
            'Х': 'í',   
            'Ч': 'ú',   
            'Ъ': 'í',   
            'Ы': 'í',   
            'Э': 'í',   
            'Ю': 'ã',   
            'А': 'Á',
            
            # Correções específicas encontradas nos arquivos reais
            'рudio': 'áudio',
            'уevirileri': 'çevirileri', 
            'saьda': 'saída',
            'opushes': 'opções',
            'Configuraushes': 'Configurações',
            'Opushes': 'Opções',
            'verificaусo': 'verificação',
            'confirmaусo': 'confirmação', 
            'interrupусo': 'interrupção',
            'muniусo': 'munição',
            'muniushes': 'munições',
            'nсo': 'não',
            'atribuьdo': 'atribuído',
            'VocЖ': 'Você',  # CRÍTICO
            'vocЖ': 'você',  # CRÍTICO  
            'atж': 'até',    # CRÍTICO
            'tambжm': 'também', # CRÍTICO
            'exploraусo': 'exploração',
            'elevaусo': 'elevação', 
            'histзrica': 'histórica',
            'cemitжrio': 'cemitério',
            'portсo': 'portão',
            'inclinaусo': 'inclinação',
            'expeуa': 'expessa',
            'praуa': 'praça',
            'resquьcios': 'resquícios', 
            'possьvel': 'possível',
            'construусo': 'construção',
            'miЩdas': 'miúdas',
            'Conheуa': 'Conheça',
            'atualizaushes': 'atualizações',
            'versсo': 'versão',
            'atravжs': 'através',
            'tЩmulos': 'túmulos',
            'insuportрvel': 'insuportável',
            'dependЖncias': 'dependências',
            'alguжm': 'alguém',
            'horrьvel': 'horrível', 
            'fumaуa': 'fumaça',
            'incompreensьvel': 'incompreensível',
            'legьtimo': 'legítimo',
            'perfuraushes': 'perfurações',
            'estсo': 'estão',
            'braуo': 'braço',
            'mзvel': 'móvel',
            'Рngulos': 'ângulos',
            'Щnicas': 'únicas',
            'reconhecьveis': 'reconhecíveis',
            'crжdito': 'crédito',
            'cartсo': 'cartão',
            'moжdas': 'moedas',
            'felecidades': 'felicidades',
            'superрr': 'superar',
            'ж': 'é',
            'prЖmio': 'prêmio',
            'sсo': 'são',
            'Щltimas': 'últimas',
            'posiусo': 'posição',
            'жpuca': 'época',
            'deuzes': 'deuses',
            'jр': 'já',
            'forуas': 'forças',
            'descomgelou': 'descongelou',
            'рgua': 'água',
            'furacшes': 'furacões',
            'vulcшes': 'vulcões',
            'oxigЖnio': 'oxigênio',
            'aparЖncia': 'aparência',
            'carрter': 'caráter',
            'lanуaram': 'lançaram',
            'mрgica': 'mágica',
            'possuьam': 'possuíam',
            'mрgicos': 'mágicos',
            'sжculos': 'séculos',
            'irmсos': 'irmãos',
            'espaуo': 'espaço',
            'quando': 'quando',
            'esse': 'esse',
            'lрgrimas': 'lágrimas',
            'fatьdico': 'fatídico',
            'descontrolз': 'descontrolou',
            'atingiram': 'atingiram',
            'furacшes': 'furacões',
            'nunca': 'nunca',
            'vulcшes': 'vulcões',
            'erupусo': 'erupção',
            'cжu': 'céu',
            'descongelada': 'descongelada',
            'ainda': 'ainda',
            'elevada': 'elevada',
            'consequЖncia': 'consequência',
            'milhшes': 'milhões',
            'restantes': 'restantes',
            'milЖnios': 'milênios',
            'devastaусo': 'devastação',
            'enfraquecida': 'enfraquecida',
            'opушes': 'opções',
            'colonizando': 'colonizando',
            'encontraram': 'encontraram',
            'impossьvel': 'impossível',
            'integrar': 'integrar',
            'estaусo': 'estação',
            'comeуou': 'começou',
            'acontecer': 'acontecer',
            'abalou': 'abalou',
            'completamente': 'completamente',
            'doenуas': 'doenças',
            'comeуaram': 'começaram',
            'nave': 'nave',
            'existiam': 'existiam',
            'sobreviventes': 'sobreviventes',
            'comeуaram': 'começaram',
            'pesquisar': 'pesquisar',
            'curas': 'curas',
            'funcionaram': 'funcionaram',
            'essas': 'essas',
            'tinham': 'tinham',
            'mudando': 'mudando',
            'Atж': 'Até',
            'pessoas': 'pessoas',
            'descobriu': 'descobriu',
            'causando': 'causando',
            'alteraушes': 'alterações',
            'divino': 'divino',
            'descobriram': 'descobriram',
            'vinha': 'vinha',
            'norte': 'norte',
            'cрpsulas': 'cápsulas',
            'programadas': 'programadas',
            'chegar': 'chegar',
            'planeta': 'planeta',
            'Apзs': 'Após',
            'destruiусo': 'destruição',
            'Terra': 'Terra',
            'criaram': 'criaram',
            'resistente': 'resistente',
            'poderes': 'poderes',
            'nova': 'nova',
            'raуa': 'raça',
            'humana': 'humana',
            'diferente': 'diferente',
            'forte': 'forte',
            'mais': 'mais',
            'dividiram': 'dividiram',
            'рgua': 'água',
            'tomou': 'tomou',
            'continente': 'continente',
            'meridional': 'meridional',
            'ocidental': 'ocidental',
            'oriental': 'oriental',
            'central': 'central',
            'total': 'total',
            'cresceu': 'cresceu',
            'ofertas': 'ofertas',
            'detinha': 'detinha',
            'bem-vindo': 'bem-vindo',
            'elemental': 'elemental',
            'jogo': 'jogo',
            'anteriormente': 'anteriormente',
            'significa': 'significa',
            'movЖ-lo': 'movê-lo',
            'setas': 'setas',
            'direita': 'direita',
            'esquerda': 'esquerda',
            'pular': 'pular',
            'subir': 'subir',
            'escadas': 'escadas',
            'descer': 'descer',
            'Sabendo': 'Sabendo',
            'agora': 'agora',
            'pode': 'pode',
            'mover-se': 'mover-se',
            'facilidade': 'facilidade',
            'mapas': 'mapas',
            'deixe-me': 'deixe-me',
            'explicar': 'explicar',
            'outras': 'outras',
            'coisas': 'coisas',
            'precisa': 'precisa',
            'saber': 'saber',
            'chamo': 'chamo',
            'boa': 'boa',
            'experiЖncia': 'experiência',
            'letra': 'letra',
            'pode': 'pode',
            'abrir': 'abrir',
            'inventрrio': 'inventário',
            'Nele': 'Nele',
            'armazenarр': 'armazenará',
            'objetos': 'objetos',
            'coletar': 'coletar',
            'caminho': 'caminho',
            'dentro': 'dentro',
            'mover': 'mover',
            'entre': 'entre',
            'seушes': 'seções',
            'para': 'para',
            'cima': 'cima',
            'baixo': 'baixo',
            'move': 'move',
            'shift': 'shift',
            'enter': 'enter',
            'algum': 'algum',
            'objeto': 'objeto',
            'pode': 'pode',
            'leiloр-lo': 'leiloá-lo',
            'ouviu': 'ouviu',
            'outros': 'outros',
            'jogadores': 'jogadores',
            'poderсo': 'poderão',
            'comprar': 'comprar',
            'produtos': 'produtos',
            'desde': 'desde',
            'estejam': 'estejam',
            'possibilidades': 'possibilidades',
            'claro': 'claro',
            'pressionar': 'pressionar',
            'apenas': 'apenas',
            'item': 'item',
            'poderр': 'poderá',
            'dр-lo': 'dá-lo',
            'qualquer': 'qualquer',
            'pessoa': 'pessoa',
            'esteja': 'esteja',
            'perto': 'perto',
            'tiver': 'tiver',
            'ninguжm': 'ninguém',
            'entсo': 'então',
            'vai': 'vai',
            'poder': 'poder',
            'nada': 'nada',
            'certo': 'certo',
            'delet': 'delet',
            'jogarр': 'jogará',
            'chсo': 'chão',
            'possam': 'possam',
            'pegр-lo': 'pegá-lo',
            'mesmo': 'mesmo',
            'pressionando': 'pressionando',
            'espaуo': 'espaço',
            'coordenada': 'coordenada',
            'soltou': 'soltou',
            'coordenadas': 'coordenadas',
            'ver': 'ver',
            'estiverem': 'estiverem',
            'habilitadas': 'habilitadas',
            'mapa': 'mapa',
            'usar': 'usar',
            'itens': 'itens',
            'basta': 'basta',
            'sobre': 'sobre',
            'eles': 'eles',
            'atuarр': 'atuará',
            'funушes': 'funções',
            'Por': 'Por',
            'exemplo': 'exemplo',
            'der': 'der',
            'para': 'para',
            'arma': 'arma',
            'pegarр': 'pegará',
            'terр': 'terá',
            'pronta': 'pronta',
            'luta': 'luta',
            'yeah': 'yeah',
            'nem': 'nem',
            'tudo': 'tudo',
            'estр': 'está',
            'pronto': 'pronto',
            'ainda': 'ainda',
            'sua': 'sua',
            'precisa': 'precisa',
            'recarregр-la': 'recarregá-la',
            'conseguirр': 'conseguirá',
            'isso': 'isso',
            'letra': 'letra',
            'Agora': 'Agora',
            'carregada': 'carregada',
            'uso': 'uso',
            'quiser': 'quiser',
            'atirar': 'atirar',
            'pressiona': 'pressiona',
            'tecla': 'tecla',
            'comtrol': 'control',
            'Para': 'Para',
            'quantos': 'quantos',
            'muniушes': 'munições',
            'tem': 'tem',
            'use': 'use',
            'for': 'for',
            'que': 'que',
            'muniусo': 'munição',
            'simplesmente': 'simplesmente',
            'dirр': 'dirá',
            'nсo': 'não',
            'Se': 'Se',
            'quer': 'quer',
            'ser': 'ser',
            'atirador': 'atirador',
            'experiente': 'experiente',
            'localizar': 'localizar',
            'presa': 'presa',
            'Entсo': 'Então',
            'deve': 'deve',
            'apontр-la': 'apontá-la',
            'VocЖ': 'Você',
            'conseguirр': 'conseguirá',
            'tecla': 'tecla',
            'shift': 'shift',
            'setas': 'setas',
            'Com': 'Com',
            'sair': 'sair',
            'matar': 'matar',
            'estiver': 'estiver',
            'caminho': 'caminho',
            'mais': 'mais',
            'algumas': 'algumas',
            'dicas': 'dicas',
            'explorar': 'explorar',
            'mapas': 'mapas',
            'sem': 'sem',
            'atacar': 'atacar',
            'atacado': 'atacado',
            'pressione': 'pressione',
            'ativa': 'ativa',
            'modo': 'modo',
            'pacifista': 'pacifista',
            'Com': 'Com',
            'este': 'este',
            'modo': 'modo',
            'poderр': 'poderá',
            'atacar': 'atacar',
            'mas': 'mas',
            'poderр': 'poderá',
            'atacр-lo': 'atacá-lo',
            'se': 'se',
            'ativarр': 'ativará',
            'ausente': 'ausente',
            'permitirр': 'permitirá',
            'fique': 'fique',
            'longe': 'longe',
            'computador': 'computador',
            'preocupar': 'preocupar',
            'seu': 'seu',
            'personagem': 'personagem',
            'sofrerр': 'sofrerá',
            'qualquer': 'qualquer',
            'dano': 'dano',
            'sim': 'sim',
            'poderр': 'poderá',
            'realizar': 'realizar',
            'nenhuma': 'nenhuma',
            'aусo': 'ação',
            'enquanto': 'enquanto',
            'estiver': 'estiver',
            'neste': 'neste',
            'Para': 'Para',
            'desativar': 'desativar',
            'pacifista': 'pacifista',
            'auzente': 'ausente',
            'com': 'com',
            'mesmas': 'mesmas',
            'combinaушes': 'combinações',
            'teclas': 'teclas',
            'sсo': 'são',
            'ativados': 'ativados',
            'letra': 'letra',
            'em': 'em',
            'algumas': 'algumas',
            'lojas': 'lojas',
            'exibir': 'exibir',
            'menu': 'menu',
            'compras': 'compras',
            'letra': 'letra',
            'verificar': 'verificar',
            'hora': 'hora',
            'se': 'se',
            'tiver': 'tiver',
            'relзgio': 'relógio',
            'pode': 'pode',
            'verificar': 'verificar',
            'saЩde': 'saúde',
            'mрxima': 'máxima',
            'se': 'se',
            'foi': 'foi',
            'ferido': 'ferido',
            'letra': 'letra',
            'pode': 'pode',
            'que': 'que',
            'roupa': 'roupa',
            'estр': 'está',
            'vestindo': 'vestindo',
            'se': 'se',
            'alguжm': 'alguém',
            'que': 'que',
            'estр': 'está',
            'por': 'por',
            'traz': 'traz',
            'roupas': 'roupas',
            'e': 'e',
            'qual': 'qual',
            'ж': 'é',
            'Alжm': 'Além',
            'disso': 'disso',
            'se': 'se',
            'vocЖ': 'você',
            'pressionar': 'pressionar',
            'letra': 'letra',
            'poderр': 'poderá',
            'verificar': 'verificar',
            'nьvel': 'nível',
            'entre': 'entre',
            'outras': 'outras',
            'estatьsticas': 'estatísticas',
            'de': 'de',
            'seu': 'seu',
            'personagem': 'personagem',
            'com': 'com',
            'alt': 'alt',
            'setas': 'setas',
            'para': 'para',
            'direita': 'direita',
            'para': 'para',
            'esquerda': 'esquerda',
            'para': 'para',
            'cima': 'cima',
            'ou': 'ou',
            'para': 'para',
            'baixo': 'baixo',
            'vocЖ': 'você',
            'pode': 'pode',
            'correr': 'correr',
            'em': 'em',
            'plataformas': 'plataformas',
            'ou': 'ou',
            'escadas': 'escadas',
            'com': 'com',
            'a': 'a',
            'letra': 'letra',
            'vocЖ': 'você',
            'pode': 'pode',
            'se': 'se',
            'sentar': 'sentar',
            'vocЖ': 'você',
            'ouviu': 'ouviu',
            'direito': 'direito',
            'sente-se': 'sente-se',
            'entсo': 'então',
            'vocЖ': 'você',
            'vai': 'vai',
            'descansar': 'descansar',
            'de': 'de',
            'tanto': 'tanto',
            'correr': 'correr',
            'eu': 'eu',
            'acho': 'acho',
            'Se': 'Se',
            'vocЖ': 'você',
            'tem': 'tem',
            'refrigerantes': 'refrigerantes',
            'ao': 'ao',
            'selecionр-los': 'selecioná-los',
            'no': 'no',
            'inventрrio': 'inventário',
            'com': 'com',
            'espaуo': 'espaço',
            'vocЖ': 'você',
            'pode': 'pode',
            'usр-los': 'usá-los',
            'com': 'com',
            'a': 'a',
            'letra': 'letra',
            'fora': 'fora',
            'dele': 'dele',
            'Desta': 'Desta',
            'forma': 'forma',
            'vocЖ': 'você',
            'pode': 'pode',
            'se': 'se',
            'curar': 'curar',
            'dos': 'dos',
            'danos': 'danos',
            'causados': 'causados',
            'pelos': 'pelos',
            'inimigos': 'inimigos',
            'Acho': 'Acho',
            'que': 'que',
            'vocЖ': 'você',
            'estр': 'está',
            'pronto': 'pronto',
            'ж': 'é',
            'hora': 'hora',
            'de': 'de',
            'voltar': 'voltar',
            'ao': 'ao',
            'seu': 'seu',
            'corpo': 'corpo',
            'e': 'e',
            'acordar': 'acordar',
            'cрpsula': 'cápsula',
            'vocЖ': 'você',
            'pode': 'pode',
            'ver': 'ver',
            'pela': 'pela',
            'janela': 'janela',
            'o': 'o',
            'espaуo': 'espaço',
            'sideral': 'sideral',
            'e': 'e',
            'suas': 'suas',
            'maravilhas': 'maravilhas',
            'mas': 'mas',
            'vocЖ': 'você',
            'sabe': 'sabe',
            'que': 'que',
            'se': 'se',
            'vocЖ': 'você',
            'estр': 'está',
            'aqui': 'aqui',
            'ж': 'é',
            'porque': 'porque',
            'uma': 'uma',
            'situaусo': 'situação',
            'de': 'de',
            'emergЖncia': 'emergência',
            'ditou': 'ditou',
            'isso': 'isso',
            'a': 'a',
            'vocЖ': 'você',
            'Oh': 'Oh',
            'VocЖ': 'Você',
            'chegou': 'chegou',
            'Desejo-lhe': 'Desejo-lhe',
            'boa': 'boa',
            'sorte': 'sorte',
            'onde': 'onde',
            'quer': 'quer',
            'que': 'que',
            'tenha': 'tenha',
            'pousado': 'pousado',
            'Apenas': 'Apenas',
            'tenha': 'tenha',
            'cuidado': 'cuidado',
            'vocЖ': 'você',
            'nсo': 'não',
            'sabe': 'sabe',
            'quais': 'quais',
            'perigos': 'perigos',
            'podem': 'podem',
            'estar': 'estar',
            'lр': 'lá',
            'fora': 'fora',
            'grande': 'grande',
            'porta': 'porta',
            'circular': 'circular',
            'que': 'que',
            'conduz': 'conduz',
            'para': 'para',
            'fora': 'fora',
            'deste': 'deste',
            'lugar': 'lugar',
            'claustrofзbico': 'claustrofóbico',
            'alguns': 'alguns',
            'arbustos': 'arbustos',
            'que': 'que',
            'descem': 'descem',
            'um': 'um',
            'pouco': 'pouco',
            'vocЖ': 'você',
            'torce': 'torce',
            'a': 'a',
            'tampa': 'tampa',
            'com': 'com',
            'forуa': 'força',
            'e': 'e',
            'sai': 'sai',
            'da': 'da',
            'cрpsula': 'cápsula',
            'para': 'para',
            'um': 'um',
            'novo': 'novo',
            'mundo': 'mundo',
            'Grama': 'Grama',
            'curta': 'curta',
            'рrvore': 'árvore',
            'grandes': 'grandes',
            'rochas': 'rochas',
            'Decida': 'Descida',
            'a': 'a',
            'um': 'um',
            'lago': 'lago',
            'descida': 'descida',
            'descida': 'descida',
            'atж': 'até',
            'um': 'um',
            'lago': 'lago',
            
            # Erros ortográficos comuns
            'cordenadas': 'coordenadas',
            'precione': 'pressione',
            'oubrigado': 'obrigado',
            'comiga': 'comigo',
            'barios': 'vários',
            'inportante': 'importante',
            'inpresionante': 'impressionante',
            'henormes': 'enormes',
            'comqreto': 'concreto',
            'lomga': 'longa',
            'viajen': 'viagem',
            'si dirige': 'se dirige',
            'cente': 'sente',
            'vomtade': 'vontade',
            'sertamente': 'certamente',
            'alparecer': 'aparentemente',
            'serca': 'cerca',
            'tencuidado': 'tenha cuidado',
            'apartir': 'a partir',
            'anbiente': 'ambiente',
            'comcegue': 'consegue',
            'inpocível': 'impossível',
            'porfín': 'por fim',
            'crusas': 'cruza',
            'buelbes': 'volta',
            'buelvas': 'volte',
            'épuca': 'época',
            'deuzes': 'deuses',
            'se combierte': 'se converte',
            'bebè': 'beber',
            'vè': 'vê',
            'serto': 'certo',
            'ccasa': 'casa',
            'incomdidade': 'incomodidade',
            'quê ': 'que ',
            'porquê ': 'porque ',
            'vocÊ ': 'você ',
            
            # Correções específicas para o contexto do jogo
            'chabe': 'chave',
            'llabe': 'chave',
            'havía': 'havia',
            'havías': 'havias',
            'hicieron': 'fizeram',
        }
        
        # Inicializar dicionários de correções
        self.correcoes_gerais = self.correcoes  # Usar as correções principais como gerais
        self.correcoes_espanhol = self.get_correcoes_espanhol()
        self.correcoes_ingles = self.get_correcoes_ingles()
        
        self.estatisticas = {
            'linhas_processadas': 0,
            'correcoes_aplicadas': 0,
            'caracteres_removidos': 0,
            'detalhes_correcoes': {}
        }

    def get_correcoes_espanhol(self):
        """Retorna o dicionário de correções específicas para arquivos em espanhol"""
        return {
            # Caracteres malformados comuns em espanhol 
            'á': 'á',
            'é': 'é', 
            'í': 'í',
            'ó': 'ó',
            'ú': 'ú',
            'ñ': 'ñ',
            'ü': 'ü',
            '¡': '¡',
            '¿': '¿',
            
            # Correções de caracteres malformados específicos encontrados
            '�': 'í',  # Como em parec�a → parecía
            'parec�a': 'parecía',
            'le�ste': 'leíste',
            'peque�as': 'pequeñas',
            'mi�das': 'pequeñas',
            'constru��o': 'construcción',
            'destrui��o': 'destrucción',
            'at�': 'hasta',
            'voc�': 'tú',
            'Conhe�a': 'Conoce',
            'voltar�o': 'volverán',
            'volver�n': 'volverán',
            'fam�lia': 'familia',
            'Est�': 'Está',
            'ba�o': 'baño',
            'n�o': 'no',
            'da�o': 'daño',
            'H�': 'Hay',
            'h�': 'hay',
            
            # Correções de traduções português → espanhol
            'tijolos': 'ladrillos',
            'qualquer': 'cualquier',
            'outro': 'otro',
            'ler': 'leer',
            'nossa': 'nuestra',
            'Lutas': 'Luchas',
            'morte': 'muerte',
            'uma': 'una',
            'porta': 'puerta',
            'trancada': 'cerrada',
            'lado': 'lado',
            'dela': 'de ella',
            'dizendo': 'que dice',
            'dos': 'de los',
            'das': 'de las',
            'lutas': 'peleas',
            'cantinho': 'esquina',
            'parede': 'pared',
            'pequena': 'pequeña',
            'escrita': 'escrita',
            'com': 'con',
            'sangue': 'sangre',
            'ao': 'al',
            'diz': 'dice',
            'mais': 'más',
            'fazer': 'hacer',
            'mal': 'daño',
            'mim': 'mí',
            'ou': 'ni',
            'minha': 'mi',
            'suas': 'sus',
            'no': 'en el',
            'fogo': 'fuego',
            'do': 'del',
            'inferno': 'infierno',
            'quarto': 'cuarto',
            'pouco': 'poco',
            'mas': 'pero',
            'não': 'no',
            'rastro': 'rastro',
            'podes': 'puedes',
            'sair': 'salir',
            'pela': 'por la',
            'algo': 'algo',
            'na': 'en la',
            'hacerme': 'hacerme',
            'todas': 'todas',
            
            # Correções de codificação específicas
            'reproduсo': 'reproducción',
            'inicializaсo': 'inicialización', 
            'verificaсo': 'verificación',
            'atualizaсo': 'actualización',
            'Bюsqueda': 'Búsqueda',
            'Desativar': 'Desactivar',
            'Ativar': 'Activar',
            'quando': 'cuando',
            'personagem': 'personaje',
            'conectar': 'conectar',
            'desconectar': 'desconectar',
            'conecta': 'se conecta',
            'desconecta': 'se desconecta',
            'início': 'inicio',
            'busca': 'búsqueda',
            'iniciar': 'iniciar'
        }

    def get_correcoes_ingles(self):
        """Retorna o dicionário de correções específicas para arquivos em inglês"""
        return {
            # Caracteres malformados comuns em inglês (? no lugar de acentos)
            'Voc?': 'You',
            'voc?': 'you',
            'est?': 'are',
            'n?o': 'not',
            'at?': 'until',
            'constru??o': 'construction',
            'mi?das': 'small',
            'Conhe?a': 'Meet',
            'port?o': 'gate',
            'pra?a': 'square',
            'corti?a': 'cork',
            'cole??o': 'collection',
            'invent?rio': 'inventory',
            'invent?rios': 'inventories',
            'voc?s': 'you',
            'quest?o': 'question',
            'quest?es': 'questions',
            'op??o': 'option',
            'op??es': 'options',
            'vers?o': 'version',
            'miss?o': 'mission',
            'miss?es': 'missions',
            'decis?o': 'decision',
            'reuni?o': 'meeting',
            'situa??o': 'situation',
            'posi??o': 'position',
            'fun??o': 'function',
            'fun??es': 'functions',
            'informa??o': 'information',
            'informa??es': 'informations',
            'configura??o': 'configuration',
            'configura??es': 'configurations',
            'atualiza??o': 'update',
            'atualiza??es': 'updates',
            'verifica??o': 'verification',
            'instala??o': 'installation',
            'opera??o': 'operation',
            'opera??es': 'operations',
            'localiza??o': 'location',
            'organiza??o': 'organization',
            'cria??o': 'creation',
            'edi??o': 'edition',
            'modifica??o': 'modification',
            'classifica??o': 'classification',
            'administra??o': 'administration',
            'participa??o': 'participation',
            'comunica??o': 'communication',
            'distribui??o': 'distribution',
            'apresenta??o': 'presentation',
            'representa??o': 'representation',
            'concentra??o': 'concentration',
            'separa??o': 'separation',
            'compara??o': 'comparison',
            'prepara??o': 'preparation',
            'repara??o': 'repair',
            'declara??o': 'declaration',
            'observa??o': 'observation',
            'explora??o': 'exploration',
            'forma??o': 'formation',
            'transforma??o': 'transformation',
            'confirma??o': 'confirmation',
            'determina??o': 'determination',
            'imagina??o': 'imagination',
            'combina??o': 'combination',
            'coordena??o': 'coordination',
            'colabora??o': 'collaboration',
            'coopera??o': 'cooperation',
            'corpora??o': 'corporation',
            'demonstra??o': 'demonstration',
            'concentra??o': 'concentration',
            'investiga??o': 'investigation',
            'programa??o': 'programming',
            'documenta??o': 'documentation',
            'implementa??o': 'implementation',
            'especifica??o': 'specification',
            'personaliza??o': 'personalization',
            'otimiza??o': 'optimization',
            'realiza??o': 'realization',
            'utiliza??o': 'utilization',
            'visualiza??o': 'visualization',
            'finaliza??o': 'finalization',
            'inicializa??o': 'initialization',
            'atualiza??o': 'update',
            'sincroniza??o': 'synchronization',
            'autoriza??o': 'authorization',
            'autentica??o': 'authentication',
            'identifica??o': 'identification',
            'notifica??o': 'notification',
            'valida??o': 'validation',
            'ativa??o': 'activation',
            'desativa??o': 'deactivation',
            'conecta??o': 'connection',
            'desconecta??o': 'disconnection',
            'configura??o': 'configuration',
            'restaura??o': 'restoration',
            'exporta??o': 'export',
            'importa??o': 'import',
            'gera??o': 'generation',
            'regenera??o': 'regeneration',
            'degrada??o': 'degradation',
            'corrup??o': 'corruption',
            'interrup??o': 'interruption',
            'prote??o': 'protection',
            'destina??o': 'destination',
            'limita??o': 'limitation',
            'recomenda??o': 'recommendation',
            'compensa??o': 'compensation',
            'representa??o': 'representation',
            'interpreta??o': 'interpretation',
            'tradução': 'translation',
            'tradu??o': 'translation',
            
            # Correções ortográficas específicas do inglês
            'allowd': 'allowed',
            'itens': 'items',
            'colaborate': 'collaborate',
            'colection': 'collection',
            'seperation': 'separation',
            'occured': 'occurred',
            'recieve': 'receive',
            'beleive': 'believe',
            'acheive': 'achieve',
            'definately': 'definitely',
            'seperate': 'separate',
            'neccessary': 'necessary',
            'occassion': 'occasion',
            'accomodate': 'accommodate',
            'embarass': 'embarrass',
            'harrass': 'harass',
            'maintainance': 'maintenance',
            'existance': 'existence',
            'independant': 'independent',
            'tendancy': 'tendency',
            'conscientious': 'conscientious',
            'concious': 'conscious',
            'pronounciation': 'pronunciation',
            'recomend': 'recommend',
            'diferent': 'different',
            'enviroment': 'environment',
            'goverment': 'government',
            'developement': 'development',
            'managment': 'management',
            'arguement': 'argument',
            'judgement': 'judgment',
            'acknowlegment': 'acknowledgment',
            'priviledge': 'privilege',
            'knowlegde': 'knowledge',
            'withdrawl': 'withdrawal',
            'skillful': 'skillful',
            'fulfil': 'fulfill',
            'untill': 'until',
            'successfull': 'successful',
            'gratefull': 'grateful',
            'peacefull': 'peaceful',
            'powerfull': 'powerful',
            'wonderfull': 'wonderful',
            'beautifull': 'beautiful',
            'carefull': 'careful',
            'usefull': 'useful',
            'harmfull': 'harmful',
            'helpfull': 'helpful',
            'hopefull': 'hopeful',
            'meaningfull': 'meaningful',
            'successfull': 'successful',
            'stressfull': 'stressful',
            'resourcefull': 'resourceful',
            'respectfull': 'respectful',
            'forgetfull': 'forgetful',
            'regretfull': 'regretful',
            'resentfull': 'resentful',
            'revengefull': 'revengeful',
            'spitfull': 'spiteful',
            'wastefull': 'wasteful',
            'sinful': 'sinful',
            'joyfull': 'joyful',
            'painfull': 'painful',
            'faithfull': 'faithful',
            'playfull': 'playful',
            'restfull': 'restful',
            'peacefull': 'peaceful',
            'colorful': 'colorful',
            'flavorfull': 'flavorful',
            'insightfull': 'insightful',
            'delightfull': 'delightful',
            'thoughtfull': 'thoughtful',
            'awfull': 'awful',
            'fulltime': 'full-time',
            'halftime': 'half-time',
            
            # Traduções português → inglês (correções mais específicas)
            'personagem': 'character',
            'conectar': 'connect',
            'desconectar': 'disconnect',
            'configuração': 'configuration',
            'configurações': 'configurations',
            'atualização': 'update',
            'atualizações': 'updates',
            'verificação': 'verification',
            'ativar': 'enable',
            'desativar': 'disable',
            'selecionar': 'select',
            'cancelar': 'cancel',
            'confirmar': 'confirm',
            'continuar': 'continue',
            'parar': 'stop',
            'começar': 'start',
            'terminar': 'finish',
            'completar': 'complete',
            'iniciar': 'start',
            'finalizar': 'finish',
            'salvar': 'save',
            'carregar': 'load',
            'baixar': 'download',
            'enviar': 'send',
            'receber': 'receive',
            'processar': 'process',
            'calcular': 'calculate',
            'verificar': 'verify',
            'validar': 'validate',
            'autorizar': 'authorize',
            'autenticar': 'authenticate',
            'identificar': 'identify',
            'notificar': 'notify',
            'avisar': 'warn',
            'alertar': 'alert',
            'informar': 'inform',
            'comunicar': 'communicate',
            'transmitir': 'transmit',
            'transferir': 'transfer',
            'importar': 'import',
            'exportar': 'export',
            'sincronizar': 'synchronize',
            'atualizar': 'update',
            'modificar': 'modify',
            'alterar': 'change',
            'editar': 'edit',
            'deletar': 'delete',
            'remover': 'remove',
            'adicionar': 'add',
            'inserir': 'insert',
            'incluir': 'include',
            'excluir': 'exclude',
            'substituir': 'replace',
            'restaurar': 'restore',
            'recuperar': 'recover',
            'reparar': 'repair',
            'corrigir': 'correct',
            'consertar': 'fix',
            'resolver': 'solve',
            'executar': 'execute',
            'implementar': 'implement',
            'instalar': 'install',
            'desinstalar': 'uninstall',
            'configurar': 'configure',
            'personalizar': 'customize',
            'otimizar': 'optimize',
            'melhorar': 'improve',
            'desenvolver': 'develop',
            'criar': 'create',
            'construir': 'build',
            'projetar': 'design',
            'planejar': 'plan',
            'organizar': 'organize',
            'gerenciar': 'manage',
            'administrar': 'administrate',
            'controlar': 'control',
            'monitorar': 'monitor',
            'observar': 'observe',
            'examinar': 'examine',
            'analisar': 'analyze',
            'avaliar': 'evaluate',
            'testar': 'test',
            'experimentar': 'experiment',
            'demonstrar': 'demonstrate',
            'apresentar': 'present',
            'mostrar': 'show',
            'exibir': 'display',
            'visualizar': 'visualize',
            'representar': 'represent',
            'simular': 'simulate',
            'emular': 'emulate',
            'imitar': 'imitate',
            'copiar': 'copy',
            'clonar': 'clone',
            'duplicar': 'duplicate',
            'replicar': 'replicate',
            'reproduzir': 'reproduce',
            'gerar': 'generate',
            'produzir': 'produce',
            'fabricar': 'manufacture',
            'compilar': 'compile',
            'interpretar': 'interpret',
            'traduzir': 'translate',
            'converter': 'convert',
            'transformar': 'transform',
            'adaptar': 'adapt',
            'ajustar': 'adjust',
            'calibrar': 'calibrate',
            'equilibrar': 'balance',
            'normalizar': 'normalize',
            'padronizar': 'standardize',
            'formatar': 'format',
            'estruturar': 'structure',
            'organizar': 'organize',
            'classificar': 'classify',
            'categorizar': 'categorize',
            'agrupar': 'group',
            'separar': 'separate',
            'dividir': 'divide',
            'combinar': 'combine',
            'mesclar': 'merge',
            'unir': 'unite',
            'conectar': 'connect',
            'ligar': 'link',
            'associar': 'associate',
            'relacionar': 'relate',
            'comparar': 'compare',
            'contrastar': 'contrast',
            'diferenciar': 'differentiate',
            'distinguir': 'distinguish',
            'identificar': 'identify',
            'reconhecer': 'recognize',
            'detectar': 'detect',
            'localizar': 'locate',
            'encontrar': 'find',
            'buscar': 'search',
            'procurar': 'look for',
            'pesquisar': 'research',
            'investigar': 'investigate',
            'explorar': 'explore',
            'descobrir': 'discover',
            'revelar': 'reveal',
            'expor': 'expose',
            'divulgar': 'disclose',
            'publicar': 'publish',
            'compartilhar': 'share',
            'distribuir': 'distribute',
            'espalhar': 'spread',
            'propagar': 'propagate',
            'expandir': 'expand',
            'aumentar': 'increase',
            'diminuir': 'decrease',
            'reduzir': 'reduce',
            'minimizar': 'minimize',
            'maximizar': 'maximize',
            'limitar': 'limit',
            'restringir': 'restrict',
            'permitir': 'allow',
            'autorizar': 'authorize',
            'habilitar': 'enable',
            'desabilitar': 'disable',
            'bloquear': 'block',
            'desbloquear': 'unblock',
            'proteger': 'protect',
            'defender': 'defend',
            'atacar': 'attack',
            'danificar': 'damage',
            'destruir': 'destroy',
            'eliminar': 'eliminate',
            'exterminar': 'exterminate',
            'aniquilar': 'annihilate',
            'devastar': 'devastate',
            'arruinar': 'ruin',
            'quebrar': 'break',
            'corromper': 'corrupt',
            'infectar': 'infect',
            'contaminar': 'contaminate',
            'poluir': 'pollute',
            'sujar': 'dirty',
            'limpar': 'clean',
            'purificar': 'purify',
            'filtrar': 'filter',
            'separar': 'separate',
            'isolar': 'isolate',
            'quarentena': 'quarantine',
            'conter': 'contain',
            'confinar': 'confine',
            'restringir': 'restrict',
            'encapsular': 'encapsulate'
        }

    def aplicar_correcoes_espanhol(self, texto, nome_arquivo=""):
        """Aplica correções específicas para textos em espanhol"""
        if not texto:
            return texto
            
        correcoes = self.get_correcoes_espanhol()
        texto_corrigido = texto
        
        # Aplicar correções diretas
        for erro, correcao in correcoes.items():
            if erro in texto_corrigido:
                ocorrencias = texto_corrigido.count(erro)
                texto_corrigido = texto_corrigido.replace(erro, correcao)
                
                # Atualizar estatísticas
                if erro not in self.estatisticas['detalhes_correcoes']:
                    self.estatisticas['correcoes_aplicadas'] += 1
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': ocorrencias
                    }
        
        # Aplicar correções com regex para problemas de palavra completa
        # Caracteres malformados isolados
        texto_corrigido = re.sub(r'\b�\b', 'í', texto_corrigido)
        texto_corrigido = re.sub(r'�+', 'ó', texto_corrigido)
        
        return texto_corrigido

    def verificar_problemas_codificacao(self, texto):
        """Verifica se há caracteres malformados no texto"""
        import re
        
        # Padrão para caracteres cirílicos/russos malformados
        caracteres_malformados = re.compile(r'[рушежьсзЖЩШЯБЦВГЗКЛМНПРСТФХЧЪЫЭЮА]+')
        
        # Padrão para caracteres malformados comuns (�, ��, etc.)
        caracteres_malformados_genericos = re.compile(r'[�]+')
        
        problemas1 = caracteres_malformados.findall(texto)
        problemas2 = caracteres_malformados_genericos.findall(texto)
        
        if problemas1 or problemas2:
            print(f"⚠️  Encontrados {len(problemas1 + problemas2)} grupos de caracteres malformados")
            if problemas1:
                print("🔍 Cirílicos:", list(set(problemas1))[:5])
            if problemas2:
                print("🔍 Genéricos:", list(set(problemas2))[:5])
            return True
        return False

    def verificar_arquivo_existe(self, nome_arquivo):
        """Verifica se o arquivo existe na pasta atual"""
        return os.path.isfile(nome_arquivo)

    def detectar_codificacao(self, nome_arquivo):
        """Tenta detectar a codificação do arquivo (prioriza ANSI)"""
        # Priorizar codificações ANSI
        codificacoes = ['cp1252', 'latin-1', 'iso-8859-1', 'utf-8']
        
        for codificacao in codificacoes:
            try:
                with open(nome_arquivo, 'r', encoding=codificacao) as arquivo:
                    # Ler apenas uma pequena amostra para teste
                    arquivo.read(1024)
                print(f"✅ Codificação detectada: {codificacao}")
                if codificacao in ['cp1252', 'latin-1', 'iso-8859-1']:
                    print("📝 Arquivo já está em codificação ANSI/Windows")
                return codificacao
            except UnicodeDecodeError:
                continue
        
        return 'cp1252'  # Padrão ANSI se não conseguir detectar

    def limpar_formatacao(self, texto):
        """Remove caracteres de formatação problemáticos"""
        # Remove caracteres \r
        caracteres_removidos = texto.count('\r')
        texto_limpo = texto.replace('\r', '')
        
        # Remove espaços extras no final das linhas
        linhas = texto_limpo.split('\n')
        linhas_limpas = [linha.rstrip() for linha in linhas]
        texto_limpo = '\n'.join(linhas_limpas)
        
        self.estatisticas['caracteres_removidos'] += caracteres_removidos
        return texto_limpo

    def aplicar_correcoes(self, texto):
        """Aplica as correções ortográficas e de codificação"""
        texto_corrigido = texto
        
        for erro, correcao in self.correcoes.items():
            # Para caracteres especiais, usar substituição direta sem word boundaries
            if any(char in erro for char in 'рушежьсзЖЩШЯБЦВГЗКЛМНПРСТФХЧЪЫЭЮА'):
                # Substituição direta para caracteres malformados
                ocorrencias = texto_corrigido.count(erro)
                if ocorrencias > 0:
                    texto_corrigido = texto_corrigido.replace(erro, correcao)
                    self.estatisticas['correcoes_aplicadas'] += ocorrencias
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': ocorrencias
                    }
            else:
                # Para palavras normais, usar regex com word boundaries
                padrao = r'\b' + re.escape(erro) + r'\b'
                ocorrencias = len(re.findall(padrao, texto_corrigido, re.IGNORECASE))
                
                if ocorrencias > 0:
                    texto_corrigido = re.sub(padrao, correcao, texto_corrigido, flags=re.IGNORECASE)
                    self.estatisticas['correcoes_aplicadas'] += ocorrencias
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': ocorrencias
                    }
        
        return texto_corrigido

    def aplicar_correcoes_espanhol(self, texto, nome_arquivo=""):
        """Aplica correções específicas para arquivos em espanhol"""
        print("🇪🇸 Aplicando correções específicas para espanhol...")
        
        # Aplicar correções específicas do espanhol
        correcoes = self.get_correcoes_espanhol()
        texto_corrigido = texto
        
        # Aplicar correções diretas
        for erro, correcao in correcoes.items():
            if erro in texto_corrigido:
                ocorrencias = texto_corrigido.count(erro)
                texto_corrigido = texto_corrigido.replace(erro, correcao)
                
                # Atualizar estatísticas
                if erro not in self.estatisticas['detalhes_correcoes']:
                    self.estatisticas['correcoes_aplicadas'] += 1
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': ocorrencias
                    }
        
        # Correções adicionais específicas para espanhol
        correcoes_extras = {
            'Configuraci?n': 'Configuración',
            'Informaci?n': 'Información',
            'Animaci?n': 'Animación',
            'Posici?n': 'Posición',
            'Direcci?n': 'Dirección',
            'Creaci?n': 'Creación',
            'Operaci?n': 'Operación',
            'Descripci?n': 'Descripción',
            'Clasificaci?n': 'Clasificación',
            'Autenticaci?n': 'Autenticación',
            'Modificaci?n': 'Modificación',
            'Verificaci?n': 'Verificación',
            'Notificaci?n': 'Notificación',
            'Comunicaci?n': 'Comunicación',
            'Participaci?n': 'Participación',
            'Organizaci?n': 'Organización',
            'Generaci?n': 'Generación',
            'Instalaci?n': 'Instalación',
            'Presentaci?n': 'Presentación',
            'Distribuci?n': 'Distribución',
            'Administraci?n': 'Administración',
            'Configuraci�n': 'Configuración',
            'Informaci�n': 'Información',
            'Animaci�n': 'Animación',
            'Posici�n': 'Posición',
            'Direcci�n': 'Dirección',
            'Creaci�n': 'Creación',
            'Operaci�n': 'Operación',
            'Descripci�n': 'Descripción',
            'Clasificaci�n': 'Clasificación',
            'Autenticaci�n': 'Autenticación',
            'Modificaci�n': 'Modificación',
            'Verificaci�n': 'Verificación',
            'Notificaci�n': 'Notificación',
            'Comunicaci�n': 'Comunicación',
            'Participaci�n': 'Participación',
            'Organizaci�n': 'Organización',
            'Generaci�n': 'Generación',
            'Instalaci�n': 'Instalación',
            'Presentaci�n': 'Presentación',
            'Distribuci�n': 'Distribución',
            'Administraci�n': 'Administración'
        }
        
        # Aplicar correções extras
        for erro, correcao in correcoes_extras.items():
            if erro in texto_corrigido:
                texto_corrigido = texto_corrigido.replace(erro, correcao)
                if erro not in self.estatisticas['detalhes_correcoes']:
                    self.estatisticas['caracteres_corrigidos'] += 1
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': texto_corrigido.count(correcao)
                    }
        
        return texto_corrigido

    def aplicar_correcoes_ingles(self, texto, nome_arquivo=""):
        """Aplica correções específicas para textos em inglês"""
        print("🇺🇸 Aplicando correções específicas para inglês...")
        
        # Aplicar correções específicas do inglês
        correcoes = self.get_correcoes_ingles()
        texto_corrigido = texto
        
        # Aplicar correções diretas
        for erro, correcao in correcoes.items():
            if erro in texto_corrigido:
                ocorrencias = texto_corrigido.count(erro)
                texto_corrigido = texto_corrigido.replace(erro, correcao)
                
                # Atualizar estatísticas
                if erro not in self.estatisticas['detalhes_correcoes']:
                    self.estatisticas['correcoes_aplicadas'] += 1
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': ocorrencias
                    }
        
        # Correções adicionais específicas para inglês
        correcoes_extras = {
            # Correções de gramática e ortografia específicas
            'precione': 'press',
            'preciona': 'press',
            'pressionr': 'press',
            'pressionaer': 'press',
            'pressionar': 'press',
            'pressiona': 'press',
            'preicona': 'press',
            'preicone': 'press',
            'preicionar': 'press',
            'preiconar': 'press',
            'proicionar': 'press',
            'proiciona': 'press',
            'proicione': 'press',
            'proicona': 'press',
            'enconrar': 'encounter',
            'encontarar': 'encounter',
            'encontrar': 'encounter',
            'encontre': 'find',
            'encontrou': 'found',
            'encontra': 'finds',
            'encontrara': 'will find',
            'encontraram': 'found',
            'encontrado': 'found',
            'encontrada': 'found',
            'encontradas': 'found',
            'encontrados': 'found',
            'encontrando': 'finding',
            'inecontrar': 'encounter',
            'inecontrou': 'encountered',
            'inecontra': 'encounters',
            'cordenadas': 'coordinates',
            'coordenadas': 'coordinates',
            'cordenada': 'coordinate',
            'coordenada': 'coordinate',
            'oubrigado': 'thank you',
            'obrigado': 'thank you',
            'brigado': 'thank you',
            'brigada': 'thank you',
            'obriagdo': 'thank you',
            'obriagda': 'thank you',
            'obrgiado': 'thank you',
            'obrgiada': 'thank you',
            'comiga': 'with me',
            'comigo': 'with me',
            'comgio': 'with me',
            'comgio': 'with me',
            'barios': 'various',
            'varios': 'various',
            'vários': 'various',
            'bario': 'various',
            'vario': 'various',
            'inportante': 'important',
            'importante': 'important',
            'inporatnte': 'important',
            'inporatne': 'important',
            'inporatnte': 'important',
            'inpresionante': 'impressive',
            'impressionante': 'impressive',
            'inpresioannte': 'impressive',
            'inpresionanate': 'impressive',
            'henormes': 'enormous',
            'enormes': 'enormous',
            'henorme': 'enormous',
            'enorme': 'enormous',
            'comqreto': 'concrete',
            'concreto': 'concrete',
            'lomga': 'long',
            'longa': 'long',
            'viajen': 'journey',
            'viagem': 'journey',
            'viajem': 'journey',
            'viaje': 'journey',
            'si dirige': 'heads',
            'se dirige': 'heads',
            'cente': 'feel',
            'sente': 'feel',
            'vomtade': 'will',
            'vontade': 'will',
            'sertamente': 'certainly',
            'certamente': 'certainly',
            'alparecer': 'apparently',
            'aparentemente': 'apparently',
            'serca': 'fence',
            'cerca': 'fence',
            'tencuidado': 'be careful',
            'tenha cuidado': 'be careful',
            'apartir': 'from',
            'a partir': 'from',
            'anbiente': 'environment',
            'ambiente': 'environment',
            'comcegue': 'get',
            'consegue': 'get',
            'inpocível': 'impossible',
            'impossível': 'impossible',
            'porfín': 'finally',
            'por fim': 'finally',
            'crusas': 'cross',
            'cruza': 'cross',
            'buelbes': 'return',
            'volta': 'return',
            'buelvas': 'return',
            'volte': 'return',
            'épuca': 'era',
            'época': 'era',
            'deuzes': 'gods',
            'deuses': 'gods',
            'se combierte': 'becomes',
            'se converte': 'becomes',
            'bebè': 'drink',
            'beber': 'drink',
            'vè': 'see',
            'vê': 'see',
            'serto': 'certain',
            'certo': 'certain',
            'ccasa': 'house',
            'casa': 'house',
            'incomdidade': 'discomfort',
            'incomodidade': 'discomfort'
        }
        
        # Aplicar correções extras
        for erro, correcao in correcoes_extras.items():
            if erro in texto_corrigido:
                texto_corrigido = texto_corrigido.replace(erro, correcao)
                if erro not in self.estatisticas['detalhes_correcoes']:
                    self.estatisticas['correcoes_aplicadas'] += 1
                    self.estatisticas['detalhes_correcoes'][erro] = {
                        'correcao': correcao,
                        'ocorrencias': texto_corrigido.count(correcao)
                    }
        
        return texto_corrigido

    def processar_arquivo(self, nome_arquivo):
        """Processa o arquivo aplicando todas as correções"""
        print(f"🔍 Processando arquivo: {nome_arquivo}")
        
        # Detectar codificação
        codificacao = self.detectar_codificacao(nome_arquivo)
        print(f"📝 Codificação detectada: {codificacao}")
        
        try:
            # Ler arquivo
            with open(nome_arquivo, 'r', encoding=codificacao) as arquivo:
                conteudo_original = arquivo.read()
            
            print(f"📊 Tamanho original: {len(conteudo_original)} caracteres")
            
            # Contar linhas
            linhas = conteudo_original.split('\n')
            self.estatisticas['linhas_processadas'] = len(linhas)
            
            # Verificar problemas de codificação
            print("🔍 Verificando problemas de codificação...")
            self.verificar_problemas_codificacao(conteudo_original)
            
            # Aplicar correções baseadas no idioma
            print("🔧 Aplicando correções...")
            conteudo_limpo = self.limpar_formatacao(conteudo_original)
            
            # Detectar idioma e aplicar correções específicas
            if 'spanish' in nome_arquivo.lower() or 'español' in nome_arquivo.lower() or 'espanol' in nome_arquivo.lower():
                conteudo_corrigido = self.aplicar_correcoes_espanhol(conteudo_limpo, nome_arquivo)
            elif 'english' in nome_arquivo.lower() or 'ingles' in nome_arquivo.lower() or 'inglês' in nome_arquivo.lower():
                conteudo_corrigido = self.aplicar_correcoes_ingles(conteudo_limpo, nome_arquivo)
            elif 'portuguese' in nome_arquivo.lower() or 'portugues' in nome_arquivo.lower():
                conteudo_corrigido = self.aplicar_correcoes(conteudo_limpo)
            else:
                # Usar correções gerais para outros idiomas
                conteudo_corrigido = self.aplicar_correcoes(conteudo_limpo)
            
            # Gerar nome do arquivo corrigido
            nome_base, extensao = os.path.splitext(nome_arquivo)
            nome_corrigido = f"{nome_base}_corrigido{extensao}"
            
            # Salvar arquivo corrigido em ANSI
            codificacao_saida = 'cp1252'  # ANSI padrão do Windows
            print(f"💾 Salvando em codificação: {codificacao_saida} (ANSI)")
            
            try:
                with open(nome_corrigido, 'w', encoding=codificacao_saida) as arquivo:
                    arquivo.write(conteudo_corrigido)
                print(f"✅ Arquivo corrigido salvo como: {nome_corrigido}")
            except UnicodeEncodeError as e:
                # Se houver problema com ANSI, tentar latin-1
                print("⚠️ Problema com cp1252, tentando latin-1...")
                codificacao_saida = 'latin-1'
                with open(nome_corrigido, 'w', encoding=codificacao_saida) as arquivo:
                    arquivo.write(conteudo_corrigido)
                print(f"✅ Arquivo corrigido salvo como: {nome_corrigido} (latin-1)")
            
            print(f"📊 Tamanho final: {len(conteudo_corrigido)} caracteres")
            
            return nome_corrigido
            
        except Exception as e:
            print(f"❌ Erro ao processar arquivo: {e}")
            return None

    def exibir_estatisticas(self):
        """Exibe estatísticas detalhadas das correções"""
        print("\n" + "="*50)
        print("📈 RELATÓRIO DE CORREÇÕES")
        print("="*50)
        print(f"📄 Linhas processadas: {self.estatisticas['linhas_processadas']}")
        print(f"🔧 Total de correções: {self.estatisticas['correcoes_aplicadas']}")
        print(f"🧹 Caracteres removidos: {self.estatisticas['caracteres_removidos']}")
        
        if self.estatisticas['detalhes_correcoes']:
            print("\n🔍 DETALHES DAS CORREÇÕES:")
            print("-" * 30)
            for erro, info in self.estatisticas['detalhes_correcoes'].items():
                print(f"  '{erro}' → '{info['correcao']}' ({info['ocorrencias']}x)")
        
        print(f"\n⏰ Processamento concluído em: {datetime.now().strftime('%H:%M:%S')}")
        print(f"🔤 Codificação de saída: ANSI (cp1252/latin-1)")
        print("✅ Arquivo compatível com jogos antigos e BGT")
        
        if self.estatisticas['correcoes_aplicadas'] == 0:
            print("ℹ️  Nenhuma correção necessária - arquivo já estava correto!")
        else:
            print(f"🎯 Arquivo corrigido com sucesso!")
            
        print("="*50)

def main():
    print("🚀 CORRETOR DE ARQUIVOS (ANSI)")
    print("="*35)
    print("Este script corrige erros ortográficos e de codificação em arquivos ANSI.")
    print("📝 Lê arquivos em ANSI e salva o resultado também em ANSI.")
    print()
    
    # Verificar se foi passado argumento na linha de comando
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
        # Se for caminho absoluto, extrair apenas o nome do arquivo
        if os.path.sep in nome_arquivo:
            diretorio = os.path.dirname(nome_arquivo)
            nome_arquivo = os.path.basename(nome_arquivo)
            os.chdir(diretorio)
        print(f"📁 Processando arquivo: {nome_arquivo}")
    else:
        # Solicitar nome do arquivo
        nome_arquivo = input("📝 Digite o nome do arquivo a ser corrigido: ").strip()
    
    if not nome_arquivo:
        print("❌ Nome de arquivo não pode estar vazio!")
        return
    
    # Criar instância do corretor
    corretor = CorretorArquivos()
    
    # Verificar se arquivo existe
    if not corretor.verificar_arquivo_existe(nome_arquivo):
        print(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta atual!")
        print(f"📁 Pasta atual: {os.getcwd()}")
        print("\n📋 Arquivos disponíveis:")
        arquivos = [f for f in os.listdir('.') if os.path.isfile(f)]
        for arquivo in sorted(arquivos)[:10]:  # Mostrar apenas os 10 primeiros
            print(f"  - {arquivo}")
        return
    
    # Processar arquivo
    arquivo_corrigido = corretor.processar_arquivo(nome_arquivo)
    
    if arquivo_corrigido:
        # Exibir estatísticas
        corretor.exibir_estatisticas()
        
        # Opção de visualizar diferenças
        resposta = input("\n🔍 Deseja ver algumas das diferenças encontradas? (s/n): ").lower()
        if resposta in ['s', 'sim', 'y', 'yes']:
            print("\n📋 EXEMPLOS DE CORREÇÕES APLICADAS:")
            print("-" * 40)
            count = 0
            for erro, info in list(corretor.estatisticas['detalhes_correcoes'].items())[:5]:
                print(f"  ✏️  '{erro}' → '{info['correcao']}'")
                count += 1
            
            if len(corretor.estatisticas['detalhes_correcoes']) > 5:
                print(f"  ... e mais {len(corretor.estatisticas['detalhes_correcoes']) - 5} correções")
    
    print("\n🎉 Processo finalizado! Obrigado por usar o Corretor de Arquivos.")
    print("💡 O arquivo foi salvo em codificação ANSI, compatível com jogos antigos.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Processo interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    input("\nPressione Enter para sair...")