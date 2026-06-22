# Responsavel: Siqueira
# Prim usando heap (heapq do python) pra achar a MST de MAIOR peso.
#
# A diferenca pro Kruskal: o Prim cresce a arvore a partir de UM
# vertice, sempre pegando a aresta de maior peso que liga um vertice
# que ja ta na arvore com um que ainda nao ta. O Kruskal olha pra
# TODAS as arestas do grafo de uma vez.
#
# Como o heapq do python e uma heap MINIMA e a gente quer sempre pegar
# o MAIOR peso, colocamos os pesos negativos na heap (truque comum).

import heapq
import time


def prim_maximo(grafo, vertice_inicial=None):
    inicio = time.time()
    vertices = grafo.vertices()

    if not vertices:
        return {"arestas": [], "peso_total": 0, "tempo_execucao": 0,
                "num_vertices": 0, "num_arestas": 0}

    if vertice_inicial is None or vertice_inicial not in grafo.adjacencia:
        vertice_inicial = vertices[0]

    visitados = set()
    mst = []
    peso_total = 0
    heap = []

    def expandir(palavra):
        visitados.add(palavra)
        for vizinho, peso in grafo.vizinhos(palavra).items():
            if vizinho not in visitados:
                heapq.heappush(heap, (-peso, palavra, vizinho))

    expandir(vertice_inicial)

    while heap and len(mst) < len(vertices) - 1:
        peso_neg, a, b = heapq.heappop(heap)

        if b in visitados:
            continue  # ja foi visitado por outro caminho, ignora

        peso = -peso_neg
        mst.append((a, b, peso))
        peso_total += peso
        expandir(b)

    return {
        "arestas": mst,
        "peso_total": peso_total,
        "tempo_execucao": round(time.time() - inicio, 6),
        "num_vertices": len(vertices),
        "num_arestas": len(mst)
    }


def comparar_kruskal_prim(grafo, subsets=None):
    # roda kruskal e prim em pedacos do grafo de tamanhos diferentes
    # pra comparar o tempo de execucao dos dois
    from grafo.grafo import Grafo
    from algoritmos.kruskal import kruskal_maximo

    vertices_todos = grafo.vertices()
    total = len(vertices_todos)

    if subsets is None:
        subsets = sorted(set([
            max(10, total // 4),
            max(20, total // 2),
            max(30, 3 * total // 4),
            total
        ]))

    resultados = []

    for tamanho in subsets:
        vertices_sub = vertices_todos[:tamanho]
        vset = set(vertices_sub)

        subgrafo = Grafo()
        for v in vertices_sub:
            subgrafo.adjacencia[v] = {}
        for v in vertices_sub:
            for viz, peso in grafo.vizinhos(v).items():
                if viz in vset:
                    subgrafo.adjacencia[v][viz] = peso

        res_k = kruskal_maximo(subgrafo)
        res_p = prim_maximo(subgrafo)

        resultados.append({
            "tamanho": tamanho,
            "tempo_kruskal": res_k["tempo_execucao"],
            "tempo_prim": res_p["tempo_execucao"],
            "peso_total_kruskal": res_k["peso_total"],
            "peso_total_prim": res_p["peso_total"]
        })

    return resultados
