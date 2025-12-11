def contar_por_chave(lista, funcao_chave):
    # Cria um dicionário para armazenar contagem de cada chave
    contagem = {}
    for trabalho in lista:
        chave = funcao_chave(trabalho)  # Extrai a chave (ex: programa, orientador)
        if chave:                       # Ignora valores vazios
            contagem[chave] = contagem.get(chave, 0) + 1  # Incrementa contagem
    return contagem