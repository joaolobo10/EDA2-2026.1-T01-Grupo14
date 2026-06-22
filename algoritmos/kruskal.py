# Responsavel: Siqueira

import time


class UnionFind:
    def __init__(self, elementos):
        self.pai = {e: e for e in elementos}
        self.rank = {e: 0 for e in elementos}

    def find(self, x):
        if self.pai[x] != x:
            self.pai[x] = self.find(self.pai[x])
        return self.pai[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)

        if rx == ry:
            return False  

        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx

        self.pai[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

        return True

    def mesmo_conjunto(self, x, y):
        return self.find(x) == self.find(y)


def kruskal_maximo(grafo):
    inicio = time.time()

    vertices = grafo.vertices()
    arestas = sorted(grafo.arestas(), key=lambda x: x[2], reverse=True)

    uf = UnionFind(vertices)
    mst = []
    peso_total = 0

    for a, b, peso in arestas:
        if uf.union(a, b):
            mst.append((a, b, peso))
            peso_total += peso

        if len(mst) == len(vertices) - 1:
            break

    return {
        "arestas": mst,
        "peso_total": peso_total,
        "tempo_execucao": round(time.time() - inicio, 6),
        "num_vertices": len(vertices),
        "num_arestas": len(mst)
    }