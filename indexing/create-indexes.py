import pyterrier as pt
if not pt.started():
    pt.init()

import pandas as pd
import os
from pyterrier.measures import MAP, P, Rprecision

# ---------------------- Étape 1 : Charger le corpus ----------------------
corpus = []
for i in range(1, 61):
    with open(f"MB{i:02}.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            corpus.append({"docno": tweet["id"], "text": tweet["text"]})
tweets_df = pd.DataFrame(corpus)

# ---------------------- Étape 2 : Indexation ----------------------
os.makedirs("indices", exist_ok=True)

indexer_lex = pt.IterDictIndexer("indices/lex", overwrite=True)
index_lex = indexer_lex.index(tweets_df.to_dict(orient="records"))

indexer_stem = pt.IterDictIndexer("indices/stem", overwrite=True)
index_stem = indexer_stem.index(tweets_df.to_dict(orient="records"), stemmer="porter")

import spacy
nlp = spacy.load("en_core_web_sm")
tweets_df["text_lemma"] = tweets_df["text"].apply(lambda t: " ".join([token.lemma_ for token in nlp(t)]))
indexer_lemma = pt.IterDictIndexer("indices/lemma", overwrite=True)
index_lemma = indexer_lemma.index(tweets_df[["docno", "text_lemma"]].rename(columns={"text_lemma": "text"}).to_dict(orient="records"))

# ---------------------- Étape 3 : Topics & Qrels ----------------------
topics = pt.io.read_topics("topics_MB01-60.xml", format="trec-xml")
qrels = pt.io.read_qrels("qrels_MB01-60.txt")

# ---------------------- Étape 4 : Recherche ----------------------
models = {
    "bm25_lex": pt.BatchRetrieve(index_lex, wmodel="BM25"),
    "tfidf_lex": pt.BatchRetrieve(index_lex, wmodel="TF_IDF"),
    "bm25_stem": pt.BatchRetrieve(index_stem, wmodel="BM25"),
    "dph_stem": pt.BatchRetrieve(index_stem, wmodel="DPH"),
    "bm25_lemma": pt.BatchRetrieve(index_lemma, wmodel="BM25"),
    "pl2_lemma": pt.BatchRetrieve(index_lemma, wmodel="PL2"),
}

# ---------------------- Étape 5 : Évaluation ----------------------
results = {}
for name, model in models.items():
    res = pt.Experiment(
        [model],
        topics,
        qrels,
        eval_measures=[MAP, P@1, P@5, P@10, Rprecision],
        names=[name]
    )
    results[name] = res

eval_df = pd.concat(results.values())
print(eval_df)

# ---------------------- Visualisation ----------------------
import matplotlib.pyplot as plt
eval_df.set_index("name")[["map", "P_1", "P_5", "P_10", "Rprec"]].plot.bar(
    figsize=(12, 6), title="Comparaison des modèles et traitements")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
