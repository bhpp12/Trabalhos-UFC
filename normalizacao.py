import unicodedata
import re

def normalizar_texto(txt):
    # Verifica se o input é vazio ou None, retorna string vazia se for o caso
    if not txt:
        return ""

    # Normaliza o texto removendo acentos
    txt_normalizado = ''.join(
        c for c in unicodedata.normalize('NFKD', txt)
        if not unicodedata.combining(c)
    )

    # Converte o texto normalizado para letras minúsculas
    txt_normalizado_lower = txt_normalizado.lower()

    # Remove caracteres que não sejam letras, números ou espaços
    txt_sem_pontuacao = re.sub(r"[^a-z0-9 ]", " ", txt_normalizado_lower)

    # Remove múltiplos espaços extras
    txt_limpo = " ".join(txt_sem_pontuacao.split())

    return txt_limpo