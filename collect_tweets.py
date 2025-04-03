import tweepy
import json

API_KEY = "kDbeg6E2u7DCUJy9IC4q4gNAQ"
API_SECRET = "48bKyKKDxg2In7VFJTY6bH6g73YunJD5fQ8nDofsE6suyX1TJQ"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAJl90QEAAAAAVVx8NT1v9GcGy5odeZiFlPpJ1uc%3DQhSprJOMbdu0qJM72mfmnqHbGGk41sGoZANg8tJUQTVGZNBsmm"

client = tweepy.Client(bearer_token=BEARER_TOKEN)

query = "Israel bombing Gaza -is:retweet lang:en"

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
with open("MB03.json", "w", encoding="utf-8") as f:
    json.dump(tweets_data, f, indent=4, ensure_ascii=False)

print("✅ Fichier MB03.json généré avec succès.")
