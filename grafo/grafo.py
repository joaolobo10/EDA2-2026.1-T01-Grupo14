# Responsavel: Joao Lobo
# Estrutura do grafo de coocorrencia de palavras.
# Cada palavra e um vertice, e a aresta entre duas palavras tem peso

from itertools import combinations


class Grafo:
    def __init__(self):
        # adjacencia[palavra] = {vizinho: peso, ...}
        self.adjacencia = {}
        self.frequencia_palavra = {}

    def construir(self, bios, frequencia_minima=2):
        # primeiro conta a frequencia de cada palavra e monta o grafo
        # bruto (sem filtro), depois remove as palavras que aparecem
        # pouco (frequencia_minima)
        grafo_bruto = {}
        freq = {}

        for perfil in bios:
            palavras = perfil.get("palavras", [])
            palavras_unicas = list(set(palavras))

            for p in palavras_unicas:
                freq[p] = freq.get(p, 0) + 1

            for a, b in combinations(palavras_unicas, 2):
                # ordena pra (a,b) e (b,a) caírem na mesma chave
                x, y = sorted([a, b])
                if x not in grafo_bruto:
                    grafo_bruto[x] = {}
                if y not in grafo_bruto[x]:
                    grafo_bruto[x][y] = 0
                grafo_bruto[x][y] += 1

        self.frequencia_palavra = freq
        palavras_validas = set(p for p in freq if freq[p] >= frequencia_minima)

        for a in grafo_bruto:
            if a not in palavras_validas:
                continue
            for b, peso in grafo_bruto[a].items():
                if b not in palavras_validas:
                    continue
                self._add_aresta(a, b, peso)

    def _add_aresta(self, a, b, peso):
        if a not in self.adjacencia:
            self.adjacencia[a] = {}
        if b not in self.adjacencia:
            self.adjacencia[b] = {}
        self.adjacencia[a][b] = peso
        self.adjacencia[b][a] = peso

    def vertices(self):
        return list(self.adjacencia.keys())

    def vizinhos(self, palavra):
        return self.adjacencia.get(palavra, {})

    def peso(self, a, b):
        return self.adjacencia.get(a, {}).get(b, 0)

    def tem_aresta(self, a, b):
        return b in self.adjacencia.get(a, {})

    def arestas(self):
        vistas = set()
        resultado = []
        for a, vizinhos in self.adjacencia.items():
            for b, peso in vizinhos.items():
                chave = tuple(sorted([a, b]))
                if chave not in vistas:
                    vistas.add(chave)
                    resultado.append((a, b, peso))
        return resultado

    def num_vertices(self):
        return len(self.adjacencia)

    def num_arestas(self):
        return len(self.arestas())

    def grau(self, palavra):
        return len(self.adjacencia.get(palavra, {}))

    def __repr__(self):
        return f"Grafo({self.num_vertices()} vertices, {self.num_arestas()} arestas)"
