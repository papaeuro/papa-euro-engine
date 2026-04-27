# publisher.py — Publication automatique sur Telegra.ph

import requests, json, os
from config import DATA_FILE

TELEGRAPH_URL = "https://api.telegra.ph"

def _get_or_create_account() -> dict:
    """Crée un compte Telegra.ph une seule fois et le réutilise."""
    data = _load()
    if "telegraph" in data:
        return data["telegraph"]

    r = requests.post(f"{TELEGRAPH_URL}/createAccount", json={
        "short_name": "AgentBot",
        "author_name": "Agent Autonome",
        "author_url": ""
    }, timeout=15)
    account = r.json()["result"]
    data["telegraph"] = account
    _save(data)
    return account

def build_content(article: dict) -> list:
    """Convertit l'article en format Telegra.ph (Node list)."""
    nodes = []

    # Intro
    if article.get("intro"):
        nodes.append({"tag": "p", "children": [article["intro"]]})

    # Sections
    for section in article.get("sections", []):
        nodes.append({"tag": "h3", "children": [section.get("titre", "")]})
        nodes.append({"tag": "p", "children": [section.get("contenu", "")]})

    # Liens affiliation
    liens = article.get("liens_affiliation", [])
    if liens:
        nodes.append({"tag": "h3", "children": ["🛒 Produits recommandés"]})
        for lien in liens:
            nodes.append({
                "tag": "p",
                "children": [
                    f"➡️ {lien.get('produit', '')} — {lien.get('prix_estime', '')} : ",
                    {"tag": "a", "attrs": {"href": lien.get("url", "#")}, "children": ["Voir sur Amazon"]}
                ]
            })

    # Conclusion
    if article.get("conclusion"):
        nodes.append({"tag": "h3", "children": ["Conclusion"]})
        nodes.append({"tag": "p", "children": [article["conclusion"]]})

    return nodes

def publish(article: dict) -> str:
    """Publie un article sur Telegra.ph et retourne l'URL."""
    account = _get_or_create_account()
    access_token = account["access_token"]
    content = build_content(article)

    r = requests.post(f"{TELEGRAPH_URL}/createPage", json={
        "access_token": access_token,
        "title": article.get("titre", "Article"),
        "author_name": "Agent Autonome",
        "content": content,
        "return_content": False
    }, timeout=15)

    result = r.json()
    if result.get("ok"):
        url = "https://telegra.ph/" + result["result"]["path"]
        return url
    else:
        raise Exception(f"Telegra.ph error: {result}")

def _load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {}

def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
