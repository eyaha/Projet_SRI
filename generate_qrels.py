import json
import os

topics = ["MB46", "MB47", "MB48" , "MB49", "MB50"]
qrels = []

for topic in topics:
    with open(f"{topic}.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for i, tweet in enumerate(tweets):
            relevance = 1 if i < 30 else 0
            line = f"{topic} 0 {tweet['id']} {relevance}"
            qrels.append(line)

# Écriture du fichier
with open("qrels.txt", "w") as f:
    f.write("\n".join(qrels))

print("✅ Fichier qrels.txt généré.")
