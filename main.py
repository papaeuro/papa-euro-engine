# main.py — Version GitHub Actions (run once)

import threading
from datetime import datetime

from config import GROQ_API_KEY
from wallet import create_or_load_wallet
from trends import get_trending_topics, get_best_niches
from brain import plan_day, generate_article
from publisher import publish
from report import send, send_rapport

def run_task(tache: dict, resultats: list):
    sujet = tache.get("sujet", "")
    niche = tache.get("niche", "")
    mots_cles = tache.get("mots_cles", [])
    print(f"[TACHE] {sujet}")
    try:
        article = generate_article(sujet, mots_cles, niche)
        url = publish(article)
        print(f"[OK] {url}")
        resultats.append({
            "titre": article.get("titre", sujet),
            "url": url,
            "liens_count": len(article.get("liens_affiliation", []))
        })
    except Exception as e:
        print(f"[ERR] {e}")
        resultats.append({"titre": sujet, "url": None})

def main():
    print(f"[AGENT] {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    wallet = create_or_load_wallet()
    send(f"🤖 *Agent démarré*\n🕐 {datetime.now().strftime('%H:%M')}\n🪙 `{wallet['address']}`\n_Analyse en cours..._")

    niches = get_best_niches()
    plan = plan_day(niches[:3])
    taches = plan.get("taches", [])
    strategie = plan.get("strategie", "Contenu multi-niche")

    print(f"[PLAN] {strategie} — {len(taches)} taches")
    send(f"🧠 *Plan :* _{strategie}_\n📋 {len(taches)} articles")

    resultats = []
    threads = [threading.Thread(target=run_task, args=(t, resultats)) for t in taches]
    for t in threads: t.start()
    for t in threads: t.join()

    send_rapport(resultats, strategie, wallet["address"])
    print("[DONE]")

if __name__ == "__main__":
    main()
