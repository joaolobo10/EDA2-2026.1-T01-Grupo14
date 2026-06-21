# Análise Textual de Bios de Matchmaking via Grafos

Trabalho da disciplina de Estruturas de Dados / Algoritmos em Grafos.

## Integrantes

- João Lobo — Estrutura do grafo, construção, análise e integração
- Eric — Pipeline de pré-processamento NLP
- Paola — BFS e centralidade das palavras
- Daniel — Cliques (Bron-Kerbosch) e grau ponderado
- Siqueira — Union-Find, Kruskal e Prim (MST)

---

## Estrutura de Pastas

```
matchmaking_textual/
│
├── main.py                      # Ponto de entrada — executa o pipeline completo
│
├── dados/
│   ├── gerador.py               # Gerador de bios fictícias e carregador de JSON
│   └── bios.json                # Arquivo de bios (gerado automaticamente se não existir)
│
├── nlp/
│   └── preprocessamento.py     # Tokenização, stopwords, lematização (spaCy/nltk)
│
├── grafo/
│   └── grafo.py                 # Estrutura do grafo de coocorrência (dicionário de adjacência)
│
├── algoritmos/
│   ├── bfs.py                   # BFS + centralidade
│   ├── cliques.py               # Bron-Kerbosch (cliques) + grau ponderado
│   ├── kruskal.py               # Union-Find + Kruskal (MST máximo)
│   ├── prim.py                  # Prim com heap (MST máximo) + comparação de complexidade
│   └── grau.py                  # Reexporta funções de grau ponderado
│
├── analise/
│   └── resultados.py            # Rankings, exibição e cruzamento entre análises
│
└── utils/
    └── visualizacao.py          # Visualizações com matplotlib e networkx (só renderização)
```

---

## Instalação

```bash
pip install spacy nltk matplotlib networkx
python -m spacy download pt_core_news_sm
```

Se o spaCy não estiver disponível, o sistema usa um fallback simples de normalização.

---

## Execução

```bash
cd matchmaking_textual
python main.py
```

Na primeira execução sem o arquivo `dados/bios.json`, o sistema gera automaticamente
50 bios fictícias para teste. Substitua o arquivo pelas bios reais quando disponíveis.

---

## Formato do arquivo de bios (bios.json)

```json
[
  {
    "id": 1,
    "bio_original": "Amo música e viajo sempre que posso.",
    "palavras": []
  },
  ...
]
```

O campo `palavras` pode estar vazio — o sistema faz o pré-processamento automaticamente.

---

## O que o sistema analisa

| Análise | Algoritmo | O que responde |
|---|---|---|
| Nichos de interesse | Bron-Kerbosch (cliques) | Quais grupos de palavras formam temas coesos? |
| Palavras centrais | BFS + centralidade | Quais palavras conectam mais nichos? |
| Esqueleto semântico | Kruskal / Prim (MST) | Quais são as relações mais fortes do vocabulário? |
| Palavras em tendência | Grau ponderado | Quais palavras aparecem mais e com maior intensidade? |
| Cruzamento | Todos | O que as análises revelam em conjunto? |

---

## Uso de LLM no desenvolvimento

- Geração das bios fictícias: ChatGPT / Claude (prompts documentados nos slides)
- Apoio no planejamento e estruturação do projeto
- Os algoritmos de grafos foram inteiramente implementados pelo grupo

---

## Notas técnicas e limitações conhecidas (importante revisar antes da entrega)

**Parâmetros do filtro de Jaccard precisam de recalibração por tamanho de dataset.**
Em `main.py`, `filtrar_grafo_por_jaccard` usa `limiar_jaccard=0.15` e
`peso_minimo_absoluto=2`. Esses valores foram calibrados para um teste com
50 bios. Quando o dataset crescer para 200-500 bios, os pesos das arestas
tendem a aumentar proporcionalmente, e esses limiares podem voltar a
remover poucas ou nenhuma aresta — o programa agora avisa automaticamente
no terminal quando isso acontece ("[AVISO] Filtro removeu menos de 1%...").
Se aparecer esse aviso, aumentem `limiar_jaccard` (ex: 0.2-0.3) ou
diminuam `peso_minimo_absoluto` até o filtro voltar a ter efeito visível
(idealmente removendo entre 5% e 20% das arestas — nem pouco a ponto de
ser inócuo, nem tanto a ponto de fragmentar demais o grafo).

**Complexidade de `calcular_centralidade` (BFS).**
Roda um BFS a partir de cada vértice do grafo — O(V·(V+E)). Para o
vocabulário esperado com 200-500 bios isso deve rodar em segundos, mas
se o vocabulário crescer muito (milhares de palavras únicas), pode ficar
perceptivelmente lento. Não é um bug, é uma escolha consciente de
simplicidade de implementação; se precisar otimizar, dá para limitar o
cálculo de centralidade a uma amostra de vértices em vez de todos.

**Complexidade de `calcular_indice_forca_perfil`.**
Para cada perfil (bio), itera por todos os cliques rankeados —
O(bios × cliques). Com 500 bios e dezenas de cliques isso ainda roda
rápido, mas é outro ponto de trade-off consciente entre simplicidade e
desempenho, bom para mencionar na seção de "complexidade e adequação"
da apresentação.

**Visualizações: layout com espaçamento geometricamente garantido.**
Os layouts de `utils/visualizacao.py` (circular por cluster e radial por
árvore) calculam o raio de cada camada/cluster com base no tamanho real
dos nós (convertido de pontos do matplotlib para unidades de dados), não
apenas na quantidade de nós. Isso evita sobreposição mesmo com zoom ou
em telas com DPI diferente. O efeito colateral é que a figura fica mais
espaçada (mais "vazio" entre clusters/galhos) — é intencional, prioriza
legibilidade sobre compacidade.

