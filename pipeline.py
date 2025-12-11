from arquivo import carregar_dataset
from contagem import contar_por_chave
from contagem_thread import ContadorThread
import sys
from carregar_stopwords import carregar_stopwords_de_listas, stopwords_pt, stopwords_en


#1. Divisão da lista para processamento concorrente
def dividir_lista(lista_completa, quantidade_blocos):
    tamanho_total = len(lista_completa)
    tamanho_base = tamanho_total // quantidade_blocos  # Tamanho de cada bloco
    sobra = tamanho_total % quantidade_blocos         # Elementos restantes

    blocos = []
    inicio = 0

    for i in range(quantidade_blocos):
        if i < sobra:
            resto = 1  # Distribui 1 elemento extra para os primeiros blocos
        else:
            resto = 0
        fim = inicio + tamanho_base + resto
        blocos.append(lista_completa[inicio:fim])
        inicio = fim

    return blocos


#2. Geração do ranking a partir de um dicionário de frequências, Ordena primeiro pela contagem decrescente (-x[1])
# Depois alfabeticamente para desempate (x[0])
def gerar_ranking(dicionario, top_n=10):
    return sorted(dicionario.items(), key=lambda x: (-x[1], x[0]))[:top_n]

#3. Função principal
def main(caminho_dataset):
   
    trabalhos = carregar_dataset(caminho_dataset)
    print(f"Total de trabalhos carregados: {len(trabalhos)}")
    
    stopwords = carregar_stopwords_de_listas(stopwords_pt, stopwords_en)
    
    num_threads = 4
    blocos = dividir_lista(trabalhos, num_threads)
    
    resultados_parciais = [None] * num_threads
    
    threads = []
    for i in range(num_threads):
        t = ContadorThread(blocos[i], stopwords, resultados_parciais, i)
        threads.append(t)
        t.start()
        
    #Esperar threads terminarem
    for t in threads:
        t.join()
        
    #Agregar resultados das threads
    frequencia_total = {}
    for parcial in resultados_parciais:
        if parcial is None:
            continue
        for palavra, contagem in parcial.items():
            frequencia_total[palavra] = frequencia_total.get(palavra, 0) + contagem

    
    #4. Rankings
    ranking_programas = gerar_ranking(contar_por_chave(trabalhos, lambda t: t.programa))
    ranking_orientadores = gerar_ranking(contar_por_chave(trabalhos, lambda t: t.orientador))
    ranking_areas = gerar_ranking(contar_por_chave(trabalhos, lambda t: t.grande_area))
    ranking_palavras = gerar_ranking(frequencia_total, top_n=20)
    
    #5. Exibir resultados
    print("\nTop 10 Programas com mais trabalhos:")
    for prog, count in ranking_programas:
        print(f"{prog}: {count}")
        
    print("\nTop 10 Orientadores com mais trabalhos:")
    for orientador, count in ranking_orientadores:
        print(f"{orientador}: {count}")

    print("\nTop 10 Grandes Áreas + Áreas de Conhecimento:")
    for area, count in ranking_areas:
        print(f"{area}: {count}")

    print("\nTop 20 palavras mais recorrentes nos títulos:")
    for palavra, count in ranking_palavras:
        print(f"{palavra}: {count}")

#6. Execução direta via terminal
if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        caminho_dataset = "ap2-capes-ufc-2021.csv"
    else:
        caminho_dataset = sys.argv[1]

    main(caminho_dataset)
    
