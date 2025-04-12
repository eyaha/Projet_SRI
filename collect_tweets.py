import tweepy
import json

API_KEY = "0dDtkoya6TylruN2PSF4FMjZK"
API_SECRET = "7J2TfvvCeHEkrEy6IMjuyV4BeIlOoRbloKFCp26gXVbJoH6sNl"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAANSQ0QEAAAAA732rSVcyLm1A%2Bh3hDu9WE%2BkF5co%3DuJHqKYpkxLwsibQ2XoA1utcPhmdTyWkhpiOX5BrE3feavlKseo"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "Gaza is dying -is:retweet lang:en"

response = client.search_recent_tweets(
    query=query,
    max_results=100,
    tweet_fields=["created_at", "lang", "public_metrics"]
)

tweets_data = []
for tweet in response.data:
    tweets_data.append({
        "id": str(tweet.id),
        "timestamp": tweet.created_at.isoformat(),
        "user": "anonymous",
        "text": tweet.text,
        "lang": tweet.lang,
        "retweets": tweet.public_metrics.get("retweet_count", 0),
        "likes": tweet.public_metrics.get("like_count", 0)
    })

# 💾 Sauvegarde du fichier
with open("MB50.json", "w", encoding="utf-8") as f:
    json.dump(tweets_data, f, indent=4, ensure_ascii=False)

print("✅ Fichier MB05.json généré avec succès.")
