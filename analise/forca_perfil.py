# Responsavel: Joao Lobo

def calcular_indice_forca_perfil(palavras_perfil, grafo, centralidade, graus, cliques_rankeados):
    palavras_validas = [p for p in palavras_perfil if p in grafo.adjacencia]

    if not palavras_validas:
        return {
            "cobertura_melhor_clique": 0.0,
            "clique_correspondente": None,
            "centralidade_media": 0.0,
            "grau_ponderado_medio": 0.0,
            "indice_forca": 0.0,
            "classificacao": "fraco"
        }

    melhor_cobertura = 0.0
    melhor_clique = None
    for item in cliques_rankeados:
        clique = item["clique"]
        cobertura = len(set(palavras_validas) & clique) / len(clique) if clique else 0.0
        if cobertura > melhor_cobertura:
            melhor_cobertura = cobertura
            melhor_clique = clique

    centralidades = [centralidade.get(p, 0.0) for p in palavras_validas]
    centralidade_media = sum(centralidades) / len(centralidades)
    centralidade_max = max(centralidade.values()) if centralidade else 1.0
    centralidade_norm = centralidade_media / centralidade_max if centralidade_max > 0 else 0.0

    graus_perfil = [graus.get(p, {}).get("grau_ponderado", 0) for p in palavras_validas]
    grau_medio = sum(graus_perfil) / len(graus_perfil)
    grau_max = max((g["grau_ponderado"] for g in graus.values()), default=1)
    grau_norm = grau_medio / grau_max if grau_max > 0 else 0.0

    indice = round((melhor_cobertura + centralidade_norm + grau_norm) / 3, 4)

    if indice >= 0.5:
        classe = "forte"
    elif indice >= 0.2:
        classe = "medio"
    else:
        classe = "fraco"

    return {
        "cobertura_melhor_clique": round(melhor_cobertura, 4),
        "clique_correspondente": melhor_clique,
        "centralidade_media": round(centralidade_norm, 4),
        "grau_ponderado_medio": round(grau_norm, 4),
        "indice_forca": indice,
        "classificacao": classe
    }


def analisar_forca_todos_perfis(bios, grafo, centralidade, graus, cliques_rankeados):
    resultado = []
    for perfil in bios:
        score = calcular_indice_forca_perfil(
            perfil.get("palavras", []), grafo, centralidade, graus, cliques_rankeados
        )
        resultado.append({
            "id": perfil.get("id"),
            "bio_original": perfil.get("bio_original", ""),
            "indice_forca": score["indice_forca"],
            "classificacao": score["classificacao"],
            "detalhes": score
        })

    resultado.sort(key=lambda x: x["indice_forca"], reverse=True)
    return resultado


def resumo_distribuicao_forca(resultados_perfis):
    total = len(resultados_perfis)
    if total == 0:
        return {"forte": 0, "medio": 0, "fraco": 0, "total": 0}

    contagem = {"forte": 0, "medio": 0, "fraco": 0}
    for r in resultados_perfis:
        contagem[r["classificacao"]] += 1

    return {
        "forte": contagem["forte"],
        "medio": contagem["medio"],
        "fraco": contagem["fraco"],
        "total": total,
        "percentual_forte": round(100 * contagem["forte"] / total, 1),
        "percentual_medio": round(100 * contagem["medio"] / total, 1),
        "percentual_fraco": round(100 * contagem["fraco"] / total, 1),
    }
