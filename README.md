# world-cuisine-connections

A similarity graph over world cuisines built from what they cook with. Each
cuisine is a node, edges are cosine similarity between ingredient vectors, and
the output is an interactive network you can open in a browser
(`connection_map.html`).

The point of the repo is that "which cuisines are similar" depends entirely on
how you vectorize, so it does it three ways and keeps all three:

| file | representation |
|---|---|
| `look.csv` | raw shared-ingredient counts |
| `look_TFIDF.csv` | TF-IDF weighted, so common ingredients stop dominating |
| `look_bert.csv` | BERT sentence embeddings |

`fuzz_model_compare.py` puts the three side by side.

## The rest of the pipeline

- `cuisine_reweightings.py` — scrapes the AllRecipes cuisine index, since a
  cuisine with more recipes scraped looks artificially broader without a
  correction
- `groupings.py` — collapses cuisine name variants using PolyFuzz over
  multilingual BERT embeddings
- `graph.py` — builds the network, applies population weighting from
  `pop_weights.csv`, and writes the pyvis output

## Running

    pip install networkx pandas matplotlib numpy pyvis scikit-learn scipy
    python graph.py

Then open `connection_map.html`.
