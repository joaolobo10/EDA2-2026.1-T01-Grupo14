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
    pass  

if __name__ == '__main__':
    main()

from dados.gerador import carregar_bios
from grafo.grafo import Grafo
from grafo.jaccard import filtrar_grafo_por_jaccard, diagnosticar_distribuicao
from algoritmos.bfs import calcular_centralidade
from algoritmos.cliques import bron_kerbosch, rankear_cliques
from algoritmos.kruskal import kruskal_maximo
from algoritmos.prim import prim_maximo
from algoritmos.grau import calcular_grau_ponderado
from analise.resultados import (
    analisar_filtragem_jaccard,
    analisar_cliques,
    analisar_centralidade,
    analisar_tendencias,
    analisar_forca_perfis,
    cruzar_analises
)
from analise.forca_perfil import analisar_forca_todos_perfis
from analise.validacao_tecnica import validar_consistencia_mst, benchmark_complexidade
from utils.visualizacao import visualizar_mst, visualizar_grafo


def main():
    print("=" * 60)
    print("  ANALISE TEXTUAL DE BIOS DE MATCHMAKING VIA GRAFOS")
    print("=" * 60)

    print("\n[1/7] Carregando e pre-processando bios...")
    bios = carregar_bios("dados/bios.json")
    print(f"      {len(bios)} perfis carregados.")

    print("\n[2/7] Construindo grafo de coocorrencia...")
    grafo_bruto = Grafo()
    grafo_bruto.construir(bios, frequencia_minima=2)
    print(f"      Vertices: {grafo_bruto.num_vertices()} | Arestas: {grafo_bruto.num_arestas()}")

    print("\n[3/7] Aplicando filtragem estrutural (Jaccard)...")
    diagnostico = diagnosticar_distribuicao(grafo_bruto, total_bios=len(bios))
    if diagnostico:
        pp = diagnostico["peso_proporcional"]
        jc = diagnostico["jaccard"]
        print(f"      Diagnostico (peso proporcional ao total de bios):")
        print(f"        p10={pp['p10']} p25={pp['p25']} mediana={pp['p50_mediana']} p75={pp['p75']} p90={pp['p90']} max={pp['max']}")
        print(f"      Diagnostico (Jaccard de vizinhanca):")
        print(f"        p10={jc['p10']} p25={jc['p25']} mediana={jc['p50_mediana']} p75={jc['p75']} p90={jc['p90']} max={jc['max']}")

    grafo, estatisticas_jaccard = filtrar_grafo_por_jaccard(
        grafo_bruto, total_bios=len(bios), limiar_jaccard=0.15, proporcao_minima_bios=0.04
    )
    print(f"      Arestas: {estatisticas_jaccard['arestas_antes']} -> "
          f"{estatisticas_jaccard['arestas_depois']} (-{estatisticas_jaccard['percentual_removido']}%)")

    print("\n[4/7] Executando algoritmos sobre o grafo filtrado...")

    print("      -> Calculando centralidade via BFS...")
    centralidade = calcular_centralidade(grafo)

    print("      -> Identificando cliques maximais...")
    vertices = list(grafo.adjacencia.keys())
    cliques = []
    bron_kerbosch(grafo, set(), set(vertices), set(), cliques)
    cliques = [c for c in cliques if len(c) >= 3]
    print(f"         {len(cliques)} cliques de tamanho >= 3 encontrados.")

    print("      -> Calculando grau ponderado...")
    graus = calcular_grau_ponderado(grafo)

    print("      -> Calculando MST via Kruskal...")
    mst_kruskal = kruskal_maximo(grafo)

    print("      -> Calculando MST via Prim...")
    mst_prim = prim_maximo(grafo)

    print("\n[5/7] Analisando dados...")

    analisar_filtragem_jaccard(estatisticas_jaccard)

    cliques_rankeados = rankear_cliques(grafo, cliques, top_n=len(cliques))

    analisar_cliques(cliques, grafo)
    analisar_centralidade(centralidade)
    analisar_tendencias(graus)

    resultados_forca = analisar_forca_todos_perfis(bios, grafo, centralidade, graus, cliques_rankeados)
    analisar_forca_perfis(resultados_forca)

    cruzar_analises(centralidade, graus, cliques, mst_kruskal)

    print("\n[6/7] Validacao tecnica (Kruskal vs Prim)...")
    validar_consistencia_mst(mst_kruskal, mst_prim)
    benchmark_complexidade(grafo)

    print("\n[7/7] Gerando visualizacoes...")
    visualizar_mst(mst_kruskal, titulo="Árvore Geradora Máxima — Kruskal (grafo filtrado)")
    visualizar_grafo(grafo, titulo="Grafo de Coocorrência Filtrado (Jaccard)")

    print("\n" + "=" * 60)
    print("  ANALISE CONCLUIDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
