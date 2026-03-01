import os

def converter_extensoes(direcao):
    pasta_atual = os.getcwd()

    if direcao == "1":
        origem = ".nvgt"
        destino = ".txt"
        acao = "convertidos"
    elif direcao == "2":
        origem = ".txt"
        destino = ".nvgt"
        acao = "convertidos"
    else:
        print("Opção inválida.")
        return

    contador = 0

    for nome_arquivo in os.listdir(pasta_atual):
        if nome_arquivo.lower().endswith(origem):
            nome_base = os.path.splitext(nome_arquivo)[0]
            novo_nome = nome_base + destino

            caminho_antigo = os.path.join(pasta_atual, nome_arquivo)
            caminho_novo = os.path.join(pasta_atual, novo_nome)

            os.rename(caminho_antigo, caminho_novo)
            contador += 1

    print(f"Operação concluída. {contador} arquivo(s) {acao}.")

def apagar_bgt():
    pasta_atual = os.getcwd()
    contador = 0

    for nome_arquivo in os.listdir(pasta_atual):
        if nome_arquivo.lower().endswith(".bgt"):
            caminho = os.path.join(pasta_atual, nome_arquivo)
            os.remove(caminho)
            contador += 1

    print(f"{contador} arquivo(s) .bgt apagado(s).")

def main():
    print("Escolha uma opção:")
    print("1 - Converter de NVGT para TXT")
    print("2 - Converter de TXT para NVGT")
    print("3 - Apagar todos os arquivos .bgt")

    escolha = input("Digite 1, 2 ou 3: ").strip()

    if escolha in ("1", "2"):
        converter_extensoes(escolha)
    elif escolha == "3":
        apagar_bgt()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()
