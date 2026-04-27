import requests, json, re
from config import GROQ_API_KEY, GROQ_MODEL

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM = "Tu es un agent IA expert en génération de revenus en ligne. Réponds UNIQUEMENT en JSON valide, sans texte autour, sans markdown."

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

def parse_json(text: str) -> dict:
    text = re.sub(r"```json|```", "", text).strip()
    try:
        return json.loads(text)
    except:
        return {}

def plan_day(niches: list) -> dict:
    prompt = f"""Niches tendance : {niches[:3]}

Retourne exactement ce JSON avec 3 taches :
{{"strategie": "description courte", "taches": [{{"niche": "finance", "sujet": "Comment gagner de l argent en ligne en 2026", "type": "article", "mots_cles": ["argent", "revenus"]}}, {{"niche": "tech", "sujet": "Les meilleurs outils IA gratuits en 2026", "type": "guide", "mots_cles": ["IA", "outils"]}}, {{"niche": "crypto", "sujet": "Debutant en crypto que faire en 2026", "type": "liste", "mots_cles": ["crypto", "bitcoin"]}}]}}"""
    
    result = parse_json(ask(prompt))
    if not result.get("taches"):
        return {
            "strategie": "Contenu multi-niche finance tech crypto",
            "taches": [
                {"niche": "finance", "sujet": "Comment gagner de l'argent en ligne en 2026", "type": "article", "mots_cles": ["argent", "revenus"]},
                {"niche": "tech", "sujet": "Les meilleurs outils IA gratuits en 2026", "type": "guide", "mots_cles": ["IA", "gratuit"]},
                {"niche": "crypto", "sujet": "Débuter en crypto en 2026 guide complet", "type": "liste", "mots_cles": ["crypto", "bitcoin"]}
            ]
        }
    return result

def generate_article(sujet: str, mots_cles: list, niche: str) -> dict:
    prompt = f"""Génère un article de 400 mots en français sur : {sujet}
Niche : {niche}, Mots-clés : {mots_cles}

Retourne exactement ce JSON :
{{"titre": "titre de l article", "intro": "introduction de 2 phrases", "sections": [{{"titre": "titre section 1", "contenu": "contenu long de 100 mots"}}, {{"titre": "titre section 2", "contenu": "contenu long de 100 mots"}}, {{"titre": "titre section 3", "contenu": "contenu long de 100 mots"}}], "conclusion": "conclusion de 2 phrases", "liens_affiliation": [{{"produit": "nom produit", "url": "https://amazon.fr/dp/B08N5WRWNW", "prix_estime": "29 euros"}}]}}"""
    
    result = parse_json(ask(prompt))
    if not result.get("titre"):
        return {
            "titre": sujet,
            "intro": f"Découvrez tout sur {sujet}.",
            "sections": [{"titre": "Introduction", "contenu": f"Guide complet sur {sujet} pour 2026."}],
            "conclusion": "Commencez dès aujourd'hui !",
            "liens_affiliation": []
        }
    return result
