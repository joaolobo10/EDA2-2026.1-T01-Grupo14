# Responsavel: Siqueira
# Union-Find (disjoint set) e Kruskal para achar a MST de MAIOR peso.
#
# Union-Find e a estrutura de dados extra que o trabalho pede alem do
# grafo. Ela serve pra responder rapido se dois vertices ja estao no
# mesmo "grupo" (componente), o que o Kruskal usa pra nao formar ciclo.
#
# Kruskal normal acha a arvore de MENOR peso. Pra pegar a de MAIOR
# peso a gente so ordena as arestas do maior pro menor em vez do
# menor pro maior (e o resto do algoritmo fica igual).

import time


class UnionFind:
    def __init__(self, elementos):
        self.pai = {e: e for e in elementos}
        self.rank = {e: 0 for e in elementos}

    def find(self, x):
        # path compression: depois de achar a raiz, aponta x direto pra ela
        if self.pai[x] != x:
            self.pai[x] = self.find(self.pai[x])
        return self.pai[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)

        if rx == ry:
            return False  # ja estao no mesmo grupo, juntar formaria ciclo

        # une o menor embaixo do maior (union by rank)
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