# Responsavel: Daniel
# Cliques (Bron-Kerbosch) e grau ponderado.
#
# Um clique e um grupo de palavras onde TODAS estao ligadas entre si.
# No nosso caso isso representa um nicho de interesse bem coeso (ex:
# musica, show, banda, festival formando um clique = nicho musical).
#
# Grau ponderado e a soma dos pesos das arestas de uma palavra - mostra
# o quanto ela e "forte" no vocabulario (nao so com quantas palavras
# ela aparece, mas com que frequencia).


def bron_kerbosch(grafo, R, P, X, cliques):
    if not P and not X:
        if len(R) >= 2:
            cliques.append(frozenset(R))
        return

    # pega o vertice de P ou X que tem mais vizinhos em P (pivo), isso
    # reduz a quantidade de chamadas recursivas
    pivo = max(P | X, key=lambda v: len(set(grafo.vizinhos(v).keys()) & P))
    vizinhos_pivo = set(grafo.vizinhos(pivo).keys())

    for v in list(P - vizinhos_pivo):
        viz_v = set(grafo.vizinhos(v).keys())
        bron_kerbosch(grafo, R | {v}, P & viz_v, X & viz_v, cliques)
        P = P - {v}
        X = X | {v}


def peso_medio_clique(grafo, clique):
    palavras = list(clique)
    pesos = []

    for i in range(len(palavras)):
        for j in range(i + 1, len(palavras)):
            p = grafo.peso(palavras[i], palavras[j])
            if p > 0:
                pesos.append(p)

    return round(sum(pesos) / len(pesos), 4) if pesos else 0.0


def rankear_cliques(grafo, cliques, top_n=10):
    resultado = []
    for c in cliques:
        resultado.append({
            "clique": c,
            "tamanho": len(c),
            "peso_medio": peso_medio_clique(grafo, c)
        })

    resultado.sort(key=lambda x: x["peso_medio"], reverse=True)
    return resultado[:top_n]


def calcular_grau_ponderado(grafo):
    resultado = {}
    for palavra, vizinhos in grafo.adjacencia.items():
        resultado[palavra] = {
            "grau_ponderado": sum(vizinhos.values()),
            "grau_simples": len(vizinhos)
        }
    return dict(sorted(resultado.items(), key=lambda x: x[1]["grau_ponderado"], reverse=True))


def palavras_nicho_intenso(graus, top_n=10):
    # alto grau ponderado mas baixo grau simples = aparece com poucas
    # palavras mas com muita forca (nicho restrito e intenso)
    resultado = []
    for p, v in graus.items():
        gs, gp = v["grau_simples"], v["grau_ponderado"]
        if gs > 0:
            resultado.append((p, gp, gs, gp / gs))

    resultado.sort(key=lambda x: x[3], reverse=True)
    return [(p, gp, gs) for p, gp, gs, _ in resultado[:top_n]]


def palavras_interesse_generico(graus, top_n=10):
    # o oposto: aparece com muitas palavras mas com pouca forca cada
    resultado = []
    for p, v in graus.items():
        gs, gp = v["grau_simples"], v["grau_ponderado"]
        if gp > 0:
            resultado.append((p, gp, gs, gs / gp))

    resultado.sort(key=lambda x: x[3], reverse=True)
    return [(p, gp, gs) for p, gp, gs, _ in resultado[:top_n]]
