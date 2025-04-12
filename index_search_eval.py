import pyterrier as pt
import pandas as pd
import json
from pyterrier.measures import MAP, P, Rprec

if not pt.java.started():
    pt.java.init()

corpus = []
for file in ["MB46.json", "MB47.json", "MB48.json", "MB49.json", "MB50.json"]:
    with open(file, "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            corpus.append({
                "docno": tweet["id"],
                "text": tweet["text"]
            })

# 🔁 Convertir en DataFrame
df = pd.DataFrame(corpus)

# ✅ Indexation avec un chemin simple et accessible
indexer = pt.IterDictIndexer("C:/Projet-RI/index", overwrite=True)
index_ref = indexer.index(df.to_dict(orient="records"))

# 🔍 Définir les requêtes
topics = pd.DataFrame([
    {"qid": "MB46", "query": "Gaza children killed"},
    {"qid": "MB47", "query": "Ceasefire Gaza"},
    {"qid": "MB48", "query": "Israel bombing Gaza"},
    {"qid": "MB49", "query": "Gaza genocide"},
    {"qid": "MB50", "query": "Gaza is dying"}
])

# 📥 Charger les jugements de pertinence
qrels = pt.io.read_qrels("qrels.txt")

# 🔍 Modèle de recherche : BM25
bm25 = pt.BatchRetrieve(index_ref, wmodel="BM25")

# 📊 Évaluer les performances
results = bm25.transform(topics)
metrics = pt.Evaluate(
    results,
    qrels,
    metrics=[MAP, P@1, P@5, P@10, Rprec]
)

# ✅ Afficher les résultats
print("\n📊 Résultats BM25 :")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")
