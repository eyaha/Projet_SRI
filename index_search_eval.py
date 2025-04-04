import pyterrier as pt
import pandas as pd
import json
from pyterrier.measures import MAP, P, Rprec

# ✅ Initialisation PyTerrier
if not pt.java.started():
    pt.java.init()

# 📄 Charger les fichiers JSON (MB01 à MB03)
corpus = []
for file in ["MB01.json", "MB02.json", "MB03.json"]:
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
    {"qid": "MB01", "query": "Gaza children killed"},
    {"qid": "MB02", "query": "Ceasefire Gaza"},
    {"qid": "MB03", "query": "Israel bombing Gaza"}
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
