# Esqueleto do Projeto — Análise Textual de Bios de Matchmaking via Grafos

Este é o gabarito do projeto: toda a estrutura de pastas, todos os imports,
todas as classes e funções já estão definidas com o nome certo e os
parâmetros certos. Falta só preencher o corpo de cada função (onde está
`pass  # Implementar: Nome`).

## Como usar

Cada função tem um comentário `# Implementar: Nome` indicando quem é
responsável por aquela parte. Implemente só as suas, sem mudar a assinatura
(nome da função e dos parâmetros) — isso já está combinado com o resto do
código através dos imports.

## Ordem sugerida pra implementar

1. **grafo/grafo.py** (João Lobo) — a classe `Grafo` é a base de tudo, o resto depende dela.
2. **nlp/preprocessamento.py** (Eric) — pipeline de limpeza de texto.
3. **dados/gerador.py** (Eric) — gera bios fictícias pra testar.
4. **algoritmos/bfs.py** (Paola) — BFS e centralidade.
5. **algoritmos/cliques.py** (Daniel) — Bron-Kerbosch e grau ponderado.
6. **algoritmos/kruskal.py** e **algoritmos/prim.py** (Siqueira) — Union-Find, Kruskal e Prim.
7. **grafo/jaccard.py** (João Lobo) — filtro de Jaccard (depende do grafo já estar pronto).
8. **analise/forca_perfil.py** (João Lobo) — índice de força de perfil (depende de cliques, BFS e grau).
9. **analise/resultados.py** (João Lobo) — funções de print/exibição (depende de tudo acima).
10. **analise/validacao_tecnica.py** (Siqueira) — comparação Kruskal vs Prim.
11. **utils/visualizacao.py** (João Lobo) — gráficos (pode ser feito por último, é só visual).
12. **main.py** (João Lobo) — junta tudo na ordem certa.

## Testando aos poucos

Dá pra testar cada módulo separado antes de integrar tudo no `main.py`.
Por exemplo, depois de implementar `grafo/grafo.py`, já dá pra testar:

```python
from grafo.grafo import Grafo
g = Grafo()
g.construir([{"palavras": ["musica", "viagem"]}, {"palavras": ["musica", "cinema"]}])
print(g.adjacencia)
```

## Instalação

```bash
pip install spacy matplotlib networkx
python -m spacy download pt_core_news_sm
```

## Quando terminar

Depois de preencher tudo, rode `python main.py` e confira se ele executa
sem erro do início ao fim, gerando os prints de análise e os arquivos
`analise/mst.png` e `analise/grafo_coocorrencia.png`.
