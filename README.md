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
cd EDA2-2026.1-T01-Grupo14
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

