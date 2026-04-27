# brain.py — Cerveau Groq LLaMA

import requests, json
from config import GROQ_API_KEY, GROQ_MODEL

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM = """Tu es un agent IA autonome expert en génération de revenus légitimes en ligne.
Tu génères du contenu de haute qualité, des articles, des stratégies d'affiliation.
Réponds toujours en JSON valide uniquement, sans texte autour."""

def ask(prompt: str) -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=HEADERS, json=payload, timeout=40
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return json.dumps({"error": str(e)})

def plan_day(niches: list) -> dict:
    prompt = f"""
    Les niches tendance aujourd'hui sont : {niches}
    
    Planifie 3 tâches de génération de contenu pour aujourd'hui.
    Chaque tâche doit cibler une niche différente.
    
    Réponds en JSON :
    {{
      "strategie": "une phrase résumant le plan",
      "taches": [
        {{"niche": "...", "sujet": "...", "type": "article|guide|liste", "mots_cles": ["k1","k2"]}}
      ]
    }}
    """
    try:
        return json.loads(ask(prompt))
    except:
        return {"strategie": "Contenu multi-niche", "taches": [
            {"niche": n, "sujet": n, "type": "article", "mots_cles": [n]}
            for n in niches[:3]
        ]}

def generate_article(sujet: str, mots_cles: list, niche: str) -> dict:
    prompt = f"""
    Génère un article complet en français sur : "{sujet}"
    Niche : {niche}
    Mots-clés à inclure : {mots_cles}
    
    L'article doit :
    - Faire 500 mots minimum
    - Être bien structuré avec des titres
    - Inclure naturellement 2-3 recommandations de produits Amazon avec des liens fictifs
    - Avoir un appel à l'action final
    
    Réponds en JSON :
    {{
      "titre": "...",
      "intro": "...",
      "sections": [
        {{"titre": "...", "contenu": "..."}}
      ],
      "conclusion": "...",
      "liens_affiliation": [
        {{"produit": "...", "url": "https://amazon.fr/dp/EXEMPLE", "prix_estime": "..."}}
      ]
    }}
    """
    try:
        return json.loads(ask(prompt))
    except:
        return {"titre": sujet, "intro": sujet, "sections": [], "conclusion": "", "liens_affiliation": []}
