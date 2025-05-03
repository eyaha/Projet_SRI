import json
import os

topics = ["MB46", "MB47", "MB48", "MB49", "MB50"]

for topic in topics:
    qrels = []
    with open(f"{topic}.json", "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for i, tweet in enumerate(tweets):
            relevance = 1 if i < 30 else 0
            line = f"{topic} 0 {tweet['id']} {relevance}"
            qrels.append(line)
    
    # Créer un fichier qrels séparé pour chaque topic
    with open(f"{topic}_qrels.txt", "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(qrels))

    print(f"✅ Fichier {topic}_qrels.txt généré.")
