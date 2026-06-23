# Responsavel: Joao Lobo

import math


def _diametro_no_em_unidades_dados(tamanho_pontos, polegadas_por_unidade):
    raio_pontos = math.sqrt(tamanho_pontos / math.pi)
    raio_polegadas = raio_pontos / 72.0
    raio_dados = raio_polegadas / polegadas_por_unidade if polegadas_por_unidade > 0 else raio_polegadas
    return 2 * raio_dados


def _layout_circular_por_cluster(G, graus, tamanho_base=260, tamanho_por_grau=260,
                                   polegadas_por_unidade=0.55, margem_seguranca=1.5):
    import networkx as nx

    componentes = sorted(nx.connected_components(G), key=len, reverse=True)
    n_clusters = len(componentes)
    colunas = max(1, math.ceil(math.sqrt(n_clusters)))

    def diametro_no(no):
        tamanho = tamanho_base + graus.get(no, 0) * tamanho_por_grau
        return _diametro_no_em_unidades_dados(tamanho, polegadas_por_unidade)

    pos = {}
    raios_cluster = {}

    for indice, componente in enumerate(componentes):
        nos = list(componente)
        k = len(nos)
        graus_locais = {n: graus.get(n, 0) for n in nos}
        nos_ordenados = sorted(nos, key=lambda n: graus_locais[n], reverse=True)

        if k == 1:
            raios_cluster[indice] = diametro_no(nos[0]) / 2
            info = (indice, nos_ordenados, graus_locais, None)
        else:
            hub = nos_ordenados[0]
            resto = nos_ordenados[1:]
            usar_hub_central = graus_locais[hub] >= 2 * (sum(graus_locais.values()) / k) and k > 4

            anel = resto if usar_hub_central else nos_ordenados
            m = len(anel)

            if m == 0:
                raios_cluster[indice] = diametro_no(hub) / 2
                info = (indice, [hub], graus_locais, None)
            else:
                diametro_max_anel = max(diametro_no(n) for n in anel)
                dist_minima = diametro_max_anel * margem_seguranca

                if m == 1:
                    raio_anel = diametro_max_anel
                else:
                    raio_anel = dist_minima / (2 * math.sin(math.pi / m))

                raio_minimo_centro = diametro_max_anel * 3.0
                raio_anel = max(raio_anel, raio_minimo_centro)

                if usar_hub_central:
                    raio_min_hub = (diametro_no(hub) + diametro_max_anel) / 2 * margem_seguranca
                    raio_anel = max(raio_anel, raio_min_hub)

                raios_cluster[indice] = raio_anel
                info = (indice, nos_ordenados, graus_locais, (hub if usar_hub_central else None, anel))

        pos[f"__info_{indice}"] = info

    diametro_max_geral = 0.0
    for componente in componentes:
        for no in componente:
            d = diametro_no(no)
            if d > diametro_max_geral:
                diametro_max_geral = d

    raio_maximo = max(raios_cluster.values()) if raios_cluster else 1.0
    espacamento_cluster = max(2.5, 2 * (raio_maximo + diametro_max_geral) * margem_seguranca)

    pos_final = {}
    for indice in range(n_clusters):
        linha = indice // colunas
        coluna = indice % colunas
        centro_x = coluna * espacamento_cluster
        centro_y = -linha * espacamento_cluster

        _, nos_ordenados, graus_locais, extra = pos[f"__info_{indice}"]

        if extra is None:
            pos_final[nos_ordenados[0]] = (centro_x, centro_y)
            continue

        hub, anel = extra
        if hub is not None:
            pos_final[hub] = (centro_x, centro_y)

        raio = raios_cluster[indice]
        m = len(anel)
        for i, no in enumerate(anel):
            angulo = 2 * math.pi * i / max(m, 1)
            pos_final[no] = (centro_x + raio * math.cos(angulo), centro_y + raio * math.sin(angulo))

    return pos_final


def _layout_radial_arvore(G, graus, raiz=None, tamanho_base=260, tamanho_por_grau=220,
                            polegadas_por_unidade=0.45, margem_seguranca=1.3):
    import networkx as nx
    from collections import deque

    if raiz is None:
        raiz = max(G.degree, key=lambda x: x[1])[0]

    def diametro_no(no):
        tamanho = tamanho_base + graus.get(no, 0) * tamanho_por_grau
        return _diametro_no_em_unidades_dados(tamanho, polegadas_por_unidade)

    nivel = {raiz: 0}
    pai = {raiz: None}
    ordem_bfs = [raiz]
    fila = deque([raiz])
    visitados = {raiz}

    while fila:
        atual = fila.popleft()
        for vizinho in G.neighbors(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                nivel[vizinho] = nivel[atual] + 1
                pai[vizinho] = atual
                ordem_bfs.append(vizinho)
                fila.append(vizinho)

    filhos = {n: [] for n in G.nodes()}
    for n in ordem_bfs[1:]:
        filhos[pai[n]].append(n)

    tamanho_subarvore = {n: 1 for n in G.nodes()}
    for n in reversed(ordem_bfs):
        if pai[n] is not None:
            tamanho_subarvore[pai[n]] += tamanho_subarvore[n]

    nos_por_nivel = {}
    for n, niv in nivel.items():
        nos_por_nivel.setdefault(niv, []).append(n)

    angulo_centro = {raiz: 0.0}
    angulo_inicial = {raiz: 0.0}
    angulo_final = {raiz: 2 * math.pi}

    fila = deque([raiz])
    while fila:
        atual = fila.popleft()
        ini = angulo_inicial[atual]
        fim = angulo_final[atual]
        total_filhos = sum(tamanho_subarvore[f] for f in filhos[atual])

        cursor = ini
        for f in filhos[atual]:
            fatia = (fim - ini) * (tamanho_subarvore[f] / total_filhos) if total_filhos else 0
            ang_meio = cursor + fatia / 2
            angulo_centro[f] = ang_meio
            angulo_inicial[f] = cursor
            angulo_final[f] = cursor + fatia
            cursor += fatia
            fila.append(f)

    raio_minimo_nivel = {0: 0.0}
    for niv, nos_nivel in nos_por_nivel.items():
        if niv == 0:
            continue
        diametro_max = max(diametro_no(n) for n in nos_nivel)
        dist_minima = diametro_max * margem_seguranca

        if len(nos_nivel) == 1:
            raio_minimo_nivel[niv] = diametro_max
            continue

        angulos_nivel = sorted(angulo_centro[n] for n in nos_nivel)
        menor_delta = min(
            (angulos_nivel[i + 1] - angulos_nivel[i] for i in range(len(angulos_nivel) - 1)),
            default=2 * math.pi
        )
        fechamento = (angulos_nivel[0] + 2 * math.pi) - angulos_nivel[-1]
        menor_delta = max(min(menor_delta, fechamento), 1e-6)

        raio_minimo_nivel[niv] = dist_minima / (2 * math.sin(min(menor_delta, math.pi) / 2))

    niveis_ordenados = sorted(raio_minimo_nivel.keys())
    raio_acumulado = {0: 0.0}
    for i in range(1, len(niveis_ordenados)):
        niv = niveis_ordenados[i]
        niv_anterior = niveis_ordenados[i - 1]
        diametro_max_niv = max(diametro_no(n) for n in nos_por_nivel[niv])
        diametro_max_ant = max((diametro_no(n) for n in nos_por_nivel.get(niv_anterior, [raiz])), default=diametro_no(raiz))
        incremento = (diametro_max_niv + diametro_max_ant) / 2 * margem_seguranca
        candidato = raio_acumulado[niv_anterior] + max(incremento, 0.8)
        raio_acumulado[niv] = max(candidato, raio_minimo_nivel[niv])

    pos = {raiz: (0.0, 0.0)}
    for no in G.nodes():
        if no == raiz:
            continue
        raio = raio_acumulado[nivel[no]]
        ang = angulo_centro[no]
        pos[no] = (raio * math.cos(ang), raio * math.sin(ang))

    return pos


def _tamanho_figura(n_nos):
    lado = max(14, min(40, 8 + n_nos * 0.18))
    return (lado, lado)


def visualizar_mst(mst, titulo="Árvore Geradora Máxima — Kruskal"):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import matplotlib.cm as cm
    except ImportError:
        print("[AVISO] matplotlib ou networkx nao instalados.")
        return

    if not mst["arestas"]:
        print("[AVISO] MST vazia, nada pra desenhar.")
        return

    G = nx.Graph()
    for a, b, peso in mst["arestas"]:
        G.add_edge(a, b, weight=peso)

    graus = dict(G.degree())
    grau_max = max(graus.values()) if graus else 1
    grau_min = min(graus.values()) if graus else 1

    pos = _layout_radial_arvore(G, graus, tamanho_base=260, tamanho_por_grau=220)

    pesos_arestas = [G[u][v]["weight"] for u, v in G.edges()]
    peso_max = max(pesos_arestas) if pesos_arestas else 1

    cmap_nos = cm.get_cmap("RdYlGn")
    norm_nos = mcolors.Normalize(vmin=grau_min, vmax=grau_max)
    cores_nos = [cmap_nos(norm_nos(graus[n])) for n in G.nodes()]

    tamanhos = [260 + graus[n] * 220 for n in G.nodes()]
    larguras = [0.7 + 3.5 * (G[u][v]["weight"] / peso_max) for u, v in G.edges()]

    cmap_arestas = cm.get_cmap("Greys")
    cores_arestas = [cmap_arestas(0.35 + 0.6 * (G[u][v]["weight"] / peso_max)) for u, v in G.edges()]

    figsize = _tamanho_figura(G.number_of_nodes())
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for (u, v), larg, cor in zip(G.edges(), larguras, cores_arestas):
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color=cor, linewidth=larg, zorder=1, solid_capstyle="round")

    xs = [pos[n][0] for n in G.nodes()]
    ys = [pos[n][1] for n in G.nodes()]
    ax.scatter(xs, ys, s=tamanhos, c=cores_nos, zorder=3, edgecolors="#222222", linewidths=0.9)

    for no in G.nodes():
        x, y = pos[no]
        fontsize = 6.5 if graus[no] < 3 else (8.5 if graus[no] < 6 else 10.5)
        fontweight = "normal" if graus[no] < 4 else "bold"
        ax.text(x, y, no, fontsize=fontsize, fontweight=fontweight, color="black", ha="center", va="center", zorder=4)

    arestas_ordenadas = sorted([(G[u][v]["weight"], u, v) for u, v in G.edges()], reverse=True)
    limiar = peso_max * 0.55
    for peso, u, v in arestas_ordenadas:
        if peso < limiar:
            break
        mx = (pos[u][0] + pos[v][0]) / 2
        my = (pos[u][1] + pos[v][1]) / 2
        ax.text(mx, my, str(peso), fontsize=6, color="#222222", ha="center", va="center", zorder=5,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#999999", linewidth=0.6))

    linhas_tabela = [f"  {u} — {v}: {p}" for p, u, v in arestas_ordenadas[:20]]
    tabela_texto = "Top arestas (peso):\n" + "\n".join(linhas_tabela)
    ax.text(1.01, 0.99, tabela_texto, transform=ax.transAxes, fontsize=6.5, va="top", ha="left",
            family="monospace", color="#222222",
            bbox=dict(boxstyle="round,pad=0.5", fc="#F5F5F5", ec="#CCCCCC", linewidth=0.8))

    sm = plt.cm.ScalarMappable(cmap=cmap_nos, norm=norm_nos)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.35, pad=0.01, location="left")
    cbar.set_label("Grau do vértice na MST", fontsize=9)

    ax.set_title(titulo, fontsize=15, fontweight="bold", pad=18, color="#111111")
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("analise/mst.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.show()
    print("      Visualizacao salva em: analise/mst.png")


def visualizar_grafo(grafo, titulo="Grafo de Coocorrência", top_arestas=60):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import matplotlib.cm as cm
    except ImportError:
        print("[AVISO] matplotlib ou networkx nao instalados.")
        return

    arestas_top = sorted(grafo.arestas(), key=lambda x: x[2], reverse=True)[:top_arestas]

    if not arestas_top:
        print("[AVISO] Grafo vazio, nada pra desenhar.")
        return

    G = nx.Graph()
    for a, b, peso in arestas_top:
        G.add_edge(a, b, weight=peso)

    G.remove_nodes_from(list(nx.isolates(G)))

    graus = dict(G.degree())
    grau_max = max(graus.values()) if graus else 1
    grau_min = min(graus.values()) if graus else 1

    pos = _layout_circular_por_cluster(G, graus, tamanho_base=260, tamanho_por_grau=260)

    pesos_arestas = [G[u][v]["weight"] for u, v in G.edges()]
    peso_max = max(pesos_arestas) if pesos_arestas else 1

    cmap_nos = cm.get_cmap("plasma")
    norm_nos = mcolors.Normalize(vmin=grau_min, vmax=grau_max)
    cores_nos = [cmap_nos(norm_nos(graus[n])) for n in G.nodes()]

    tamanhos = [260 + graus[n] * 260 for n in G.nodes()]
    larguras = [0.5 + 3.2 * (G[u][v]["weight"] / peso_max) for u, v in G.edges()]
    cores_arestas = [plt.cm.Blues(0.35 + 0.6 * (G[u][v]["weight"] / peso_max)) for u, v in G.edges()]

    figsize = _tamanho_figura(G.number_of_nodes())
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for (u, v), larg, cor in zip(G.edges(), larguras, cores_arestas):
        x = [pos[u][0], pos[v][0]]
        y = [pos[u][1], pos[v][1]]
        ax.plot(x, y, color=cor, linewidth=larg, zorder=1, solid_capstyle="round")

    xs = [pos[n][0] for n in G.nodes()]
    ys = [pos[n][1] for n in G.nodes()]
    ax.scatter(xs, ys, s=tamanhos, c=cores_nos, zorder=3, edgecolors="#222222", linewidths=0.9)

    for no in G.nodes():
        x, y = pos[no]
        fontsize = 6.5 if graus[no] < 2 else (8.5 if graus[no] < 4 else 10.5)
        fontweight = "normal" if graus[no] < 3 else "bold"
        ax.text(x, y, no, fontsize=fontsize, fontweight=fontweight, color="black", ha="center", va="center", zorder=4)

    arestas_ordenadas = sorted([(G[u][v]["weight"], u, v) for u, v in G.edges()], reverse=True)
    limiar = peso_max * 0.6
    for peso, u, v in arestas_ordenadas:
        if peso < limiar:
            break
        mx = (pos[u][0] + pos[v][0]) / 2
        my = (pos[u][1] + pos[v][1]) / 2
        ax.text(mx, my, str(peso), fontsize=6, color="#111111", ha="center", va="center", zorder=5,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#AAAAAA", linewidth=0.6))

    linhas = [f"  {u} — {v}: {p}" for p, u, v in arestas_ordenadas[:20]]
    tabela = "Top arestas (peso):\n" + "\n".join(linhas)
    ax.text(1.01, 0.99, tabela, transform=ax.transAxes, fontsize=6.5, va="top", ha="left",
            family="monospace", color="#222222",
            bbox=dict(boxstyle="round,pad=0.5", fc="#F5F5F5", ec="#CCCCCC", linewidth=0.8))

    sm = plt.cm.ScalarMappable(cmap=cmap_nos, norm=norm_nos)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, shrink=0.35, pad=0.01, location="left")
    cbar.set_label("Grau do vértice", fontsize=9)

    ax.set_title(f"{titulo} — top {top_arestas} arestas por peso", fontsize=15, fontweight="bold", pad=18, color="#111111")
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig("analise/grafo_coocorrencia.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.show()
    print("      Visualizacao salva em: analise/grafo_coocorrencia.png")


def visualizar_comparacao_mst(resultados_comparacao):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("[AVISO] matplotlib nao instalado.")
        return

    if not resultados_comparacao:
        return

    tamanhos = [r["tamanho"] for r in resultados_comparacao]
    tempos_k = [r["tempo_kruskal"] for r in resultados_comparacao]
    tempos_p = [r["tempo_prim"] for r in resultados_comparacao]

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ax.plot(tamanhos, tempos_k, "o-", label="Kruskal", color="#2471A3", linewidth=2.5, markersize=8)
    ax.plot(tamanhos, tempos_p, "s-", label="Prim", color="#E74C3C", linewidth=2.5, markersize=8)

    ax.set_xlabel("Número de vértices no grafo", fontsize=11)
    ax.set_ylabel("Tempo de execução (segundos)", fontsize=11)
    ax.set_title("Comparação de Complexidade: Kruskal vs Prim", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, alpha=0.25, color="#AAAAAA")
    ax.legend(fontsize=10)

    plt.tight_layout()
    plt.savefig("analise/comparacao_kruskal_prim.png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.show()
    print("      Visualizacao salva em: analise/comparacao_kruskal_prim.png")
