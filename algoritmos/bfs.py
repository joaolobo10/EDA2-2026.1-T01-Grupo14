# Responsavel: Paola

from collections import deque


def bfs(grafo, origem):
    if origem not in grafo.adjacencia:
        return {}

    dist = {origem: 0}
    fila = deque([origem])

    while fila:
        atual = fila.popleft()
        for vizinho in grafo.vizinhos(atual):
            if vizinho not in dist:
                dist[vizinho] = dist[atual] + 1
                fila.append(vizinho)

    return dist


def distancia_entre(grafo, origem, destino):
    dist = bfs(grafo, origem)
    return dist.get(destino, -1)


def calcular_centralidade(grafo):
    # centralidade(palavra) = 1 / distancia media ate as outras palavras
    #quanto menor a distancia media, mais "central" ela é no vocabulario
    vertices = grafo.vertices()
    centralidade = {}

    for palavra in vertices:
        dist = bfs(grafo, palavra)
        distancias = [d for v, d in dist.items() if v != palavra and d > 0]

        if not distancias:
            centralidade[palavra] = 0.0
        else:
            media = sum(distancias) / len(distancias)
            centralidade[palavra] = round(1.0 / media, 6) if media > 0 else 0.0

    return dict(sorted(centralidade.items(), key=lambda x: x[1], reverse=True))



def componentes_conexos(grafo):
    visitados = set()
    componentes = []

    for v in grafo.vertices():
        if v not in visitados:
            dist = bfs(grafo, v)
            comp = set(dist.keys())
            componentes.append(comp)
            visitados |= comp

    return componentes

