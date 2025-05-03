import json
import pandas as pd

# Initialize an empty list for the full corpus
corpus = []

# Loop through all MB01 to MB60 files
for i in range(1, 61):
    filename = f"MB{i:02}.json"
    with open(filename, "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            corpus.append({
                "docno": tweet["id"],
                "text": tweet["text"]
            })

# Convert to DataFrame if needed for indexing
df_corpus = pd.DataFrame(corpus)

# Show the number of documents loaded
print(f"✅ Total tweets loaded: {len(df_corpus)}")
