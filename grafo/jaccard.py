# Responsavel: Joao Lobo

def jaccard_vizinhanca(grafo, a, b):
    viz_a = set(grafo.vizinhos(a).keys())
    viz_b = set(grafo.vizinhos(b).keys())

    uniao = viz_a | viz_b
    intersecao = viz_a & viz_b

    if not uniao:
        return 0.0

    return round(len(intersecao) / len(uniao), 6)


def calcular_jaccard_todas_arestas(grafo):
    resultado = {}
    for a, b, _ in grafo.arestas():
        resultado[(a, b)] = jaccard_vizinhanca(grafo, a, b)
    return resultado


def diagnosticar_distribuicao(grafo, total_bios):
    arestas = grafo.arestas()
    if not arestas or total_bios == 0:
        return {}

    pesos_prop = sorted(peso / total_bios for _, _, peso in arestas)
    jaccards = sorted(calcular_jaccard_todas_arestas(grafo).values())

    def percentil(lista, p):
        if not lista:
            return 0.0
        i = min(len(lista) - 1, max(0, int(p / 100 * (len(lista) - 1))))
        return round(lista[i], 5)

    return {
        "total_arestas": len(arestas),
        "peso_proporcional": {
            "p10": percentil(pesos_prop, 10),
            "p25": percentil(pesos_prop, 25),
            "p50_mediana": percentil(pesos_prop, 50),
            "p75": percentil(pesos_prop, 75),
            "p90": percentil(pesos_prop, 90),
            "max": round(pesos_prop[-1], 5),
        },
        "jaccard": {
            "p10": percentil(jaccards, 10),
            "p25": percentil(jaccards, 25),
            "p50_mediana": percentil(jaccards, 50),
            "p75": percentil(jaccards, 75),
            "p90": percentil(jaccards, 90),
            "max": round(jaccards[-1], 5),
        },
    }


def filtrar_grafo_por_jaccard(grafo, total_bios, limiar_jaccard=0.15, proporcao_minima_bios=0.04):
    # remove uma aresta se ela tiver jaccard baixo E peso proporcional
    # baixo ao mesmo tempo. Se uma das duas condicoes for forte, mantem
    # (protege arestas que sao fortes so pela frequencia, mesmo com
    # vizinhanca diferente)
    from grafo.grafo import Grafo

    arestas_originais = grafo.arestas()
    jaccard_arestas = calcular_jaccard_todas_arestas(grafo)

    novo_grafo = Grafo()
    novo_grafo.frequencia_palavra = dict(grafo.frequencia_palavra)

    mantidas = 0
    removidas = 0
    soma_jaccard_mantidas = 0.0
    soma_jaccard_removidas = 0.0

    for a, b, peso in arestas_originais:
        j = jaccard_arestas.get((a, b), 0.0)
        peso_prop = peso / total_bios if total_bios > 0 else 0.0

        manter = (j >= limiar_jaccard) or (peso_prop >= proporcao_minima_bios)

        if manter:
            novo_grafo._add_aresta(a, b, peso)
            mantidas += 1
            soma_jaccard_mantidas += j
        else:
            removidas += 1
            soma_jaccard_removidas += j

    # tira vertices que ficaram sem nenhuma aresta depois do filtro
    isolados = [v for v in novo_grafo.adjacencia if len(novo_grafo.adjacencia[v]) == 0]
    for v in isolados:
        del novo_grafo.adjacencia[v]

    total = len(arestas_originais)
    stats = {
        "arestas_antes": total,
        "arestas_depois": mantidas,
        "arestas_removidas": removidas,
        "percentual_removido": round(100 * removidas / total, 2) if total else 0.0,
        "jaccard_medio_mantidas": round(soma_jaccard_mantidas / mantidas, 4) if mantidas else 0.0,
        "jaccard_medio_removidas": round(soma_jaccard_removidas / removidas, 4) if removidas else 0.0,
        "vertices_isolados_removidos": len(isolados),
        "vertices_antes": grafo.num_vertices(),
        "vertices_depois": novo_grafo.num_vertices(),
        "proporcao_minima_bios_usada": proporcao_minima_bios,
        "limiar_jaccard_usado": limiar_jaccard,
    }

    return novo_grafo, stats
