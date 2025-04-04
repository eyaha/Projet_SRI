import json
import pandas as pd

# 📁 Liste des fichiers JSON
files = ["MB01.json", "MB02.json", "MB03.json" , "MB04.json", "MB05.json"]

# 📦 Liste pour stocker tous les tweets
all_tweets = []

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        tweets = json.load(f)
        for tweet in tweets:
            all_tweets.append({
                "docno": tweet["id"],      # identifiant du tweet
                "text": tweet["text"]      # contenu textuel
            })

# 🧱 Création du DataFrame
df = pd.DataFrame(all_tweets)

# 💾 Sauvegarde en CSV si tu veux l'utiliser plus tard
df.to_csv("tweets_dataframe.csv", index=False)

# ✅ Aperçu
print(df.head())
