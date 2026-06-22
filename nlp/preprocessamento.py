# Responsavel: Daniel

import re

try:
    import spacy
    nlp = spacy.load("pt_core_news_sm")
    USAR_SPACY = True
except Exception:
    USAR_SPACY = False
    print("[AVISO] spacy nao encontrado, usando normalizacao mais simples")


# stopwords que a gente foi adicionando na mao conforme via palavra
STOPWORDS_EXTRAS = {
    "gosto", "adoro", "amo", "curto", "gosta", "muito", "sempre", "também",
    "todo", "toda", "todos", "todas", "meu", "minha", "meus", "minhas",
    "seu", "sua", "seus", "suas", "nosso", "nossa", "um", "uma", "uns",
    "umas", "ser", "ter", "fazer", "ir", "vir", "dar", "ver", "saber",
    "querer", "poder", "dever", "ficar", "falar", "achar", "deixar",
    "passar", "ainda", "já", "mais", "bem", "aqui", "lá", "sim", "não",
    "nas", "nos", "num", "numa", "pelo", "pela", "pelos", "pelas",
    "quando", "como", "onde", "porque", "que", "qual", "quais",
    "por", "para", "com", "sem", "sob", "sobre", "entre", "até",
    "desde", "perante", "após", "ante", "contra", "durante",
    "mediante", "salvo", "exceto", "conforme", "segundo",
    "sou", "são", "é", "era", "eram", "foi", "foram", "será", "serão",
    "estou", "está", "estão", "estava", "estavam",
    "posso", "pode", "podem", "podia", "podiam",
    "faço", "faz", "fazem", "fazia", "faziam",
    "vou", "vai", "vão", "ia", "iam",
    "tenho", "tem", "têm", "tinha", "tinham",
    "toco", "toca", "tocam", "tocava", "tocavam",
    "fico", "fica", "ficam", "ficava", "ficavam",
    "eu", "ele", "ela", "eles", "elas", "nós", "vós", "isso", "isto",
    "aquilo", "este", "esta", "esse", "essa", "aquele", "aquela",
    "se", "te", "me", "lhe", "lhes", "nas", "no", "na", "do", "da",
    "dos", "das", "ao", "aos", "à", "às", "o", "a", "os", "as",
    "e", "ou", "mas", "porém", "contudo", "entretanto", "logo",
    "assim", "então", "pois", "mesmo", "tão", "tal", "cada",
}


def tokenizar(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-záàãâéêíóôõúüçñ\s]", " ", texto)
    return texto.split()


def lematizar_spacy(tokens):
    doc = nlp(" ".join(tokens))
    return [t.lemma_ for t in doc if not t.is_stop and not t.is_space]


def normalizar_sem_spacy(tokens):
    # versao mais simples sem o spacy, so tira plural basico
    # nao e perfeita mas resolve a maioria dos casos
    resultado = []
    for t in tokens:
        if t.endswith("ões"):
            t = t[:-3] + "ão"
        elif t.endswith("ais"):
            t = t[:-2] + "l"
        elif t.endswith("is") and len(t) > 4:
            t = t[:-1]
        elif t.endswith("es") and len(t) > 4:
            t = t[:-2]
        elif t.endswith("s") and len(t) > 4:
            t = t[:-1]
        resultado.append(t)
    return resultado


def preprocessar(texto):
    if not texto or not texto.strip():
        return []

    tokens = tokenizar(texto)
    tokens = [t for t in tokens if len(t) >= 3]

    if USAR_SPACY:
        tokens = lematizar_spacy(tokens)
    else:
        tokens = normalizar_sem_spacy(tokens)

    tokens = [t for t in tokens if t not in STOPWORDS_EXTRAS]

    # tira repetidas mantendo a ordem
    vistos = set()
    resultado = []
    for t in tokens:
        if t not in vistos and len(t) >= 3:
            vistos.add(t)
            resultado.append(t)

    return resultado
