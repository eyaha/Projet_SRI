import pyterrier as pt
if not pt.started():
    pt.init()
import pandas as pd
import os
import json
from pyterrier.measures import MAP, P
from pyterrier import terrier

with open("tweets.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

corpus = [{"docno": tweet["id"], "text": tweet["text"]} for tweet in tweets]
tweets_df = pd.DataFrame(corpus)

# Ensure all index directories exist and are valid
os.makedirs("/content/indices/lex", exist_ok=True)
os.makedirs("/content/indices/stem", exist_ok=True)
os.makedirs("/content/indices/lemma", exist_ok=True)

# Index without stemming
indexer_lex = pt.IterDictIndexer("/content/indices/lex", overwrite=True)
index_lex = indexer_lex.index(tweets_df.to_dict(orient="records"))

# Index with stemming
indexer_stem = pt.IterDictIndexer("/content/indices/stem", overwrite=True, stemmer="porter")
index_stem = indexer_stem.index(tweets_df.to_dict(orient="records"))

# Index with lemmatization
import spacy
nlp = spacy.load("en_core_web_sm")
tweets_df["text_lemma"] = tweets_df["text"].apply(lambda t: " ".join([token.lemma_ for token in nlp(t)]))

indexer_lemma = pt.IterDictIndexer("/content/indices/lemma", overwrite=True)
index_lemma = indexer_lemma.index(
    tweets_df[["docno", "text_lemma"]].rename(columns={"text_lemma": "text"}).to_dict(orient="records")
)

topics = pt.io.read_topics("topics.xml", format="trec")
qrels   = pt.io.read_qrels("qrels.txt")

topics["qid"] = topics["qid"].str.strip()
qrels["qid"]  = qrels["qid"].str.strip()

print("Topics QIDs:", sorted(topics["qid"].unique()))
print("Qrels  QIDs:", sorted(qrels["qid"].unique()))


models = {
    "bm25_lex": pt.BatchRetrieve(index_lex, wmodel="BM25"),
    "tfidf_lex": pt.BatchRetrieve(index_lex, wmodel="TF_IDF"),
    "bm25_stem": pt.BatchRetrieve(index_stem, wmodel="BM25"),
    "dph_stem": pt.BatchRetrieve(index_stem, wmodel="DPH"),
    "bm25_lemma": pt.BatchRetrieve(index_lemma, wmodel="BM25"),
    "pl2_lemma": pt.BatchRetrieve(index_lemma, wmodel="PL2"),
}

results = {}
for name, model in models.items():
    res = pt.Experiment(
        [model],
        topics,
        qrels,
        eval_metrics=[MAP, P@1, P@5, P@10, "Rprec"],  # correct parameter name
        names=[name]
    )
    results[name] = res

# 1. Concatenate the results into a single DataFrame
eval_df = pd.concat(results.values())

# 2. Rename columns to match desired plot labels
eval_df = eval_df.rename(columns={
    "AP": "map",
    "P@1": "P_1",
    "P@5": "P_5",
    "P@10": "P_10"
})

print(eval_df)

# 3. Plot
import matplotlib.pyplot as plt

metrics = ["map", "P_1", "P_5", "P_10", "Rprec"]
eval_df.set_index("name")[metrics].plot.bar(
    figsize=(12, 6),
    title="Comparaison des modèles et traitements"
)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
