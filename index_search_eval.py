import pyterrier as pt
import pandas as pd
import json
import os

# 🧠 Initialiser PyTerrier
if not pt.started():
    pt.init()

# 📁 Charger les tweets depuis tous les fichiers
all_docs = []
for topic in ["MB01", "MB02", "MB03"]:
    with open(f"{topic}.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            all_docs.append({"docno": tweet["id"], "text": tweet["text"]})

# 🧱 Créer le DataFrame
df = pd.DataFrame(all_docs)

# 🔨 Construire l’index
indexer = pt.DFIndexer("./index", overwrite=True)
index_ref = indexer.index(df["text"], df["docno"])

# 🔍 Définir les requêtes (topics)
topics = pd.DataFrame([
    {"qid": "MB01", "query": "Gaza children killed"},
    {"qid": "MB02", "query": "Israeli airstrikes on Gaza"},
    {"qid": "MB03", "query": "Hospitals bombed in Gaza"}
])

# 🛠️ Chargement du modèle BM25
bm25 = pt.BatchRetrieve(index_ref, wmodel="BM25")

# ⚙️ Évaluer avec qrels
qrels = pt.io.read_qrels("qrels.txt")
eval = pt.Utils.evaluate(bm25.transform(topics), qrels, metrics=["map", "P@1", "P@5", "P@10", "Rprec"])

# ✅ Afficher les résultats
print("Résultats BM25 :")
for k, v in eval.items():
    print(f"{k}: {v:.4f}")
