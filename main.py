# Responsavel: Joao Lobo

from dados.gerador import carregar_bios
from grafo.grafo import Grafo
from grafo.jaccard import filtrar_grafo_por_jaccard, diagnosticar_distribuicao
from algoritmos.bfs import calcular_centralidade
from algoritmos.cliques import bron_kerbosch, rankear_cliques
from algoritmos.kruskal import kruskal_maximo
from algoritmos.prim import prim_maximo
from algoritmos.grau import calcular_grau_ponderado
from analise.resultados import analisar_filtragem_jaccard, analisar_cliques, analisar_centralidade, analisar_tendencias, analisar_forca_perfis, cruzar_analises
from analise.forca_perfil import analisar_forca_todos_perfis
from analise.validacao_tecnica import validar_consistencia_mst, benchmark_complexidade
from utils.visualizacao import visualizar_mst, visualizar_grafo


def main():
    pass  # Implementar: Joao Lobo


if __name__ == '__main__':
    main()
