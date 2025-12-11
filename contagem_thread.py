import threading
from normalizacao import normalizar_texto

class ContadorThread(threading.Thread):
    def __init__(self, bloco_de_trabalhos, stopwords, resultados_parciais, indice):
        super().__init__()
        self.bloco_de_trabalhos = bloco_de_trabalhos  # Sublista de trabalhos para esta thread
        self.stopwords = stopwords                     # Conjunto de stopwords
        self.resultados_parciais = resultados_parciais # Lista compartilhada para resultados
        self.indice = indice                           # Índice desta thread na lista de resultados

    def run(self):
        contagem_local = {}  # Dicionário local da thread

        for trabalho in self.bloco_de_trabalhos:
            titulo_normalizado = normalizar_texto(trabalho.titulo)  # Normaliza o título

            for palavra in titulo_normalizado.split():  # Itera sobre cada palavra
                if len(palavra) <= 3:                   # Ignora palavras curtas
                    continue
                if palavra in self.stopwords:           # Ignora stopwords
                    continue

                contagem_local[palavra] = contagem_local.get(palavra, 0) + 1

        self.resultados_parciais[self.indice] = contagem_local  # Armazena resultado da thread
