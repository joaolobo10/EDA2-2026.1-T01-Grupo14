# Responsavel: Siqueira
# Essa parte e validacao TECNICA, nao e analise de dados/NLP. Serve pra
# provar que Kruskal e Prim estao implementados corretamente (batem no
# mesmo resultado) e pra comparar a complexidade pratica dos dois.
# Por isso fica separada das analises principais (cliques, centralidade,
# tendencias, forca de perfil).

from algoritmos.prim import comparar_kruskal_prim


def validar_consistencia_mst(mst_kruskal, mst_prim):
    print("\n" + "=" * 60)
    print("  VALIDACAO TECNICA - CONSISTENCIA KRUSKAL vs PRIM")
    print("=" * 60)
    print("  (validacao de implementacao, nao e analise de dados)")

    print(f"\n  Kruskal -> peso total: {mst_kruskal['peso_total']} | tempo: {mst_kruskal['tempo_execucao']:.6f}s")
    print(f"  Prim    -> peso total: {mst_prim['peso_total']} | tempo: {mst_prim['tempo_execucao']:.6f}s")

    if mst_kruskal["peso_total"] == mst_prim["peso_total"]:
        print("\n  OK - as duas implementacoes chegam no mesmo peso total.")
    else:
        print("\n  ATENCAO - pesos diferentes, revisar a implementacao.")


def benchmark_complexidade(grafo, subsets=None):
    print("\n" + "-" * 60)
    print("  Benchmark de complexidade (Kruskal vs Prim)")
    print("-" * 60)

    resultados = comparar_kruskal_prim(grafo, subsets=subsets)

    print(f"\n  {'Vertices':<10}{'Tempo Kruskal (s)':<20}{'Tempo Prim (s)':<18}{'Mais rapido'}")
    for r in resultados:
        mais_rapido = "Kruskal" if r["tempo_kruskal"] < r["tempo_prim"] else "Prim"
        print(f"  {r['tamanho']:<10}{r['tempo_kruskal']:<20.6f}{r['tempo_prim']:<18.6f}{mais_rapido}")

    print(f"\n  Obs: grafos de coocorrencia tendem a ser mais esparsos com")
    print(f"  vocabulario pequeno e mais densos conforme o dataset cresce,")
    print(f"  entao o resultado relativo entre os dois pode mudar com o tamanho.")

    return resultados
