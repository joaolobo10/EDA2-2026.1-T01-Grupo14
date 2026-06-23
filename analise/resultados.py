# Responsavel: Joao Lobo

from algoritmos.cliques import rankear_cliques, palavras_nicho_intenso, palavras_interesse_generico
from analise.forca_perfil import resumo_distribuicao_forca


def analisar_filtragem_jaccard(stats):
    print("\n" + "=" * 60)
    print("  FILTRAGEM ESTRUTURAL - INDICE DE JACCARD")
    print("=" * 60)

    print(f"\n  Parametros usados: limiar_jaccard={stats.get('limiar_jaccard_usado')} | "
          f"proporcao_minima_bios={stats.get('proporcao_minima_bios_usada')}")
    print(f"  (proporcao_minima_bios e relativa ao total de bios, nao precisa")
    print(f"   recalibrar quando o tamanho do dataset mudar)")

    print(f"\n  Vertices antes do filtro:  {stats['vertices_antes']}")
    print(f"  Vertices depois do filtro: {stats['vertices_depois']} "
          f"(-{stats['vertices_isolados_removidos']} isolados)")
    print(f"\n  Arestas antes do filtro:   {stats['arestas_antes']}")
    print(f"  Arestas depois do filtro:  {stats['arestas_depois']}")
    print(f"  Arestas removidas:         {stats['arestas_removidas']} ({stats['percentual_removido']}%)")
    print(f"\n  Jaccard medio das arestas mantidas:  {stats['jaccard_medio_mantidas']}")
    print(f"  Jaccard medio das arestas removidas: {stats['jaccard_medio_removidas']}")

    print(f"\n  Interpretacao: a filtragem tirou coocorrencias com baixo apoio")
    print(f"  estrutural (sem vizinhos em comum) e peso baixo, reduzindo ruido")
    print(f"  antes de rodar cliques, MST e centralidade.")


def analisar_cliques(cliques, grafo, top_n=10):
    print("\n" + "=" * 60)
    print("  ANALISE 1 - NICHOS DE INTERESSE (CLIQUES)")
    print("=" * 60)

    if not cliques:
        print("  Nenhum clique de tamanho >= 3 encontrado.")
        print("  Sugestao: reduzir o filtro de frequencia minima.")
        return

    ranking = rankear_cliques(grafo, cliques, top_n=top_n)

    print(f"\n  Total de cliques maximais (tamanho >= 3): {len(cliques)}")
    print(f"\n  Top {min(top_n, len(ranking))} nichos mais fortes:\n")

    for i, item in enumerate(ranking, 1):
        palavras = sorted(item["clique"])
        print(f"  #{i:02d} | Tamanho: {item['tamanho']} | Peso medio: {item['peso_medio']:.2f}")
        print(f"       Palavras: {', '.join(palavras)}")

    print("\n  Distribuicao de tamanho dos cliques:")
    contagem = {}
    for c in cliques:
        contagem[len(c)] = contagem.get(len(c), 0) + 1
    for tamanho in sorted(contagem):
        print(f"    Tamanho {tamanho}: {contagem[tamanho]} clique(s)")


def analisar_centralidade(centralidade, top_n=20):
    print("\n" + "=" * 60)
    print("  ANALISE 2 - CENTRALIDADE DAS PALAVRAS (BFS)")
    print("=" * 60)

    if not centralidade:
        print("  Nenhum dado de centralidade disponivel.")
        return

    top = list(centralidade.items())[:top_n]
    bottom = list(centralidade.items())[-10:]

    print(f"\n  Top {min(top_n, len(top))} palavras mais CENTRAIS")
    print("  (interesses universais, conectam varios nichos):\n")
    for i, (p, v) in enumerate(top, 1):
        print(f"  #{i:02d} | {p:<20} centralidade: {v:.6f}")

    print(f"\n  Top 10 palavras mais PERIFERICAS")
    print("  (interesses de nicho, pouco conectadas ao vocabulario geral):\n")
    for i, (p, v) in enumerate(bottom, 1):
        print(f"  #{i:02d} | {p:<20} centralidade: {v:.6f}")


def analisar_tendencias(graus, top_n=20):
    print("\n" + "=" * 60)
    print("  ANALISE 3 - PALAVRAS EM TENDENCIA (GRAU PONDERADO)")
    print("=" * 60)

    top = list(graus.items())[:top_n]
    print(f"\n  Top {min(top_n, len(top))} palavras em TENDENCIA")
    print("  (alto grau ponderado, aparecem muito e com forca):\n")
    for i, (p, v) in enumerate(top, 1):
        print(f"  #{i:02d} | {p:<20} grau ponderado: {v['grau_ponderado']:>6} | grau simples: {v['grau_simples']:>4}")

    nicho = palavras_nicho_intenso(graus, top_n=10)
    print("\n  Palavras de NICHO INTENSO (poucas conexoes mas fortes):\n")
    for i, (p, gp, gs) in enumerate(nicho, 1):
        print(f"  #{i:02d} | {p:<20} ponderado: {gp:>6} | simples: {gs:>4}")

    generico = palavras_interesse_generico(graus, top_n=10)
    print("\n  Palavras de INTERESSE GENERICO (muitas conexoes mas fracas):\n")
    for i, (p, gp, gs) in enumerate(generico, 1):
        print(f"  #{i:02d} | {p:<20} ponderado: {gp:>6} | simples: {gs:>4}")


def cruzar_analises(centralidade, graus, cliques, mst, top_n=10):
    print("\n" + "=" * 60)
    print("  CRUZAMENTO ENTRE ANALISES")
    print("=" * 60)

    top_centrais = set(list(centralidade.keys())[:top_n])
    top_tendencia = set(list(graus.keys())[:top_n])

    grau_mst = {}
    for a, b, _ in mst["arestas"]:
        grau_mst[a] = grau_mst.get(a, 0) + 1
        grau_mst[b] = grau_mst.get(b, 0) + 1
    top_hubs = set(sorted(grau_mst, key=grau_mst.get, reverse=True)[:top_n])

    inter1 = top_hubs & top_centrais
    print(f"\n  [1] Palavras hub da MST que tambem sao centrais (BFS): {len(inter1)}/{top_n}\n")
    for p in sorted(inter1):
        print(f"    -> {p}")
    if len(inter1) > top_n // 2:
        print("\n  Interpretacao: alta coincidencia, o esqueleto da MST reflete bem a centralidade real.")
    else:
        print("\n  Interpretacao: baixa coincidencia, MST e BFS capturam aspectos diferentes do grafo.")

    palavras_em_cliques = set()
    for c in cliques:
        palavras_em_cliques |= c
    inter2 = top_tendencia & palavras_em_cliques
    print(f"\n  [2] Palavras em tendencia que pertencem a algum clique: {len(inter2)}/{top_n}\n")
    for p in sorted(inter2):
        print(f"    -> {p}")
    if len(inter2) > top_n // 2:
        print("\n  Interpretacao: palavras populares tendem a formar nichos coesos.")
    else:
        print("\n  Interpretacao: palavras populares sao genericas, nao formam nichos especificos.")

    inter3 = top_centrais & top_tendencia
    print(f"\n  [3] Palavras centrais que tambem sao tendencia: {len(inter3)}/{top_n}\n")
    for p in sorted(inter3):
        print(f"    -> {p}")
    if len(inter3) > top_n // 2:
        print("\n  Interpretacao: centralidade e popularidade se reforcam.")
    else:
        print("\n  Interpretacao: centralidade e popularidade divergem.")


def analisar_forca_perfis(resultados_perfis, top_n=10):
    print("\n" + "=" * 60)
    print("  ANALISE 4 - INDICE DE FORCA DE PERFIL (POPULARIDADE)")
    print("=" * 60)

    if not resultados_perfis:
        print("  Nenhum perfil para analisar.")
        return

    resumo = resumo_distribuicao_forca(resultados_perfis)
    print(f"\n  Distribuicao geral do dataset ({resumo['total']} perfis):")
    print(f"    Forte: {resumo['forte']} ({resumo['percentual_forte']}%)")
    print(f"    Medio: {resumo['medio']} ({resumo['percentual_medio']}%)")
    print(f"    Fraco: {resumo['fraco']} ({resumo['percentual_fraco']}%)")

    print(f"\n  Top {top_n} perfis MAIS FORTES:\n")
    for i, r in enumerate(resultados_perfis[:top_n], 1):
        clique_txt = ""
        if r["detalhes"]["clique_correspondente"]:
            clique_txt = f" | clique: {{{', '.join(sorted(r['detalhes']['clique_correspondente']))}}}"
        print(f"  #{i:02d} | ID {r['id']:<4} | forca: {r['indice_forca']:.4f} ({r['classificacao']}){clique_txt}")
        bio_curta = r['bio_original'][:80] + ("..." if len(r['bio_original']) > 80 else "")
        print(f"       \"{bio_curta}\"")

    print(f"\n  Top {top_n} perfis MAIS FRACOS:\n")
    for i, r in enumerate(resultados_perfis[-top_n:][::-1], 1):
        print(f"  #{i:02d} | ID {r['id']:<4} | forca: {r['indice_forca']:.4f} ({r['classificacao']})")
        bio_curta = r['bio_original'][:80] + ("..." if len(r['bio_original']) > 80 else "")
        print(f"       \"{bio_curta}\"")

    print(f"\n  Interpretacao: perfis fortes concentram palavras que estao em")
    print(f"  cliques de peso alto, sao centrais e tem grau ponderado alto.")
    print(f"  Isso responde a pergunta: um clique forte gera perfil popular?")
    print(f"  Gera, mas so pra quem cobre bem aquele clique.")
