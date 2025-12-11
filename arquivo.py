import pandas as pd
from trabalho import Trabalho

def carregar_dataset(caminho):
    # Lê o arquivo CSV usando pandas, assumindo que os delimitadores são ponto e vírgula
    df = pd.read_csv(caminho, delimiter=';', encoding='utf-8')
    trabalhos = []

    for _, row in df.iterrows():
        trabalho = Trabalho(
            row.get("NM_PROGRAMA", "").strip(),          # Programa do trabalho
            row.get("NM_ORIENTADOR", "").strip(),        # Nome do orientador
            row.get("NM_GRANDE_AREA_CONHECIMENTO", "").strip(),  # Grande área
            row.get("NM_AREA_CONHECIMENTO", "").strip(),          # Área específica
            row.get("NM_PRODUCAO", "").strip(),         # Título do trabalho
        )
        trabalhos.append(trabalho) # Adiciona o objeto à lista

    return trabalhos   # Retorna a lista completa de objetos Trabalho