# trends.py — Recherche les tendances du jour via SerpAPI

import requests
from config import SERPAPI_KEY

def get_trending_topics(niche: str = "make money online") -> list:
    """Cherche les sujets tendance sur Google pour une niche donnée."""
    try:
        r = requests.get("https://serpapi.com/search", params={
            "q": niche,
            "api_key": SERPAPI_KEY,
            "hl": "fr",
            "gl": "fr",
            "num": 10
        }, timeout=20)
        results = r.json().get("organic_results", [])
        topics = [res.get("title", "") for res in results[:5] if res.get("title")]
        return topics
    except Exception as e:
        print(f"[SERPAPI ERROR] {e}")
        return [niche]

def get_best_niches() -> list:
    """Trouve les niches les plus rentables du moment."""
    try:
        r = requests.get("https://serpapi.com/search", params={
            "q": "most profitable online niches 2025",
            "api_key": SERPAPI_KEY,
            "hl": "en",
            "gl": "us",
            "num": 10
        }, timeout=20)
        results = r.json().get("organic_results", [])
        niches = [res.get("title", "") for res in results[:5]]
        return niches if niches else ["finance", "health", "tech", "gaming", "crypto"]
    except:
        return ["finance", "health", "tech", "gaming", "crypto"]
