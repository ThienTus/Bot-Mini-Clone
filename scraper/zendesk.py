import requests

BASE_URL = "https://support.optisigns.com/api/v2/help_center/articles.json"

def fetch_articles(limit=30):
    articles = []
    url = BASE_URL

    while url and len(articles) < limit:
        res = requests.get(url).json()
        articles.extend(res["articles"])
        url = res["next_page"]

    return articles[:limit]
