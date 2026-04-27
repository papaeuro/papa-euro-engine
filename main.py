# main.py — Agent autonome complet

import threading, schedule, time
from datetime import datetime

from config import REPORT_HOUR, REPORT_MINUTE
from wallet import create_or_load_wallet, get_address
from trends import get_trending_topics, get_best_niches
from brain import plan_day, generate_article
from publisher import publish
from report import send, send_rapport

def run_task(tache: dict, resultats: list):
    """Exécute une tâche : génère + publie un article."""
    sujet = tache.get("sujet", "")
    niche = tache.get("niche", "")
    mots_cles = tache.get("mots_cles", [])

    print(f"[TACHE] Génération : {sujet}")
    try:
        article = generate_article(sujet, mots_cles, niche)
        print(f"[TACHE] Publication : {article.get('titre', '?')}")
        url = publish(article)
        print(f"[TACHE] Publié → {url}")
        resultats.append({
            "titre": article.get("titre", sujet),
            "url": url,
            "liens_count": len(article.get("liens_affiliation", []))
        })
    except Exception as e:
        print(f"[TACHE ERROR] {sujet}: {e}")
        resultats.append({"titre": sujet, "url": None, "erreur": str(e)})

def run_agent():
    """Cycle complet d'une journée."""
    print(f"\n{'='*50}")
    print(f"[AGENT] Démarrage — {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    # 1. Wallet
    wallet = create_or_load_wallet()
    print(f"[WALLET] {wallet['address']}")

    # 2. Notification démarrage
    send(
        f"🤖 *Agent démarré*\n"
        f"🕐 {datetime.now().strftime('%H:%M')}\n"
        f"🪙 `{wallet['address']}`\n"
        f"_Analyse des tendances en cours..._"
    )

    # 3. Tendances du jour
    print("[TRENDS] Recherche des niches...")
    niches = get_best_niches()
    topics = get_trending_topics(niches[0] if niches else "make money online")
    print(f"[TRENDS] Niches : {niches[:3]}")

    # 4. Planification
    print("[BRAIN] Planification...")
    plan = plan_day(niches[:3])
    strategie = plan.get("strategie", "Contenu multi-niche")
    taches = plan.get("taches", [])
    print(f"[BRAIN] {strategie} — {len(taches)} tâches")

    send(f"🧠 *Plan du jour :*\n_{strategie}_\n📋 {len(taches)} articles à publier")

    # 5. Exécution parallèle
    resultats = []
    threads = [
        threading.Thread(target=run_task, args=(t, resultats))
        for t in taches
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()

    print(f"[AGENT] {len(resultats)} tâches terminées")

    # 6. Rapport final
    send_rapport(resultats, strategie, wallet["address"])
    print("[RAPPORT] ✓ Envoyé sur Telegram")

def main():
    print("🤖 Agent PapaEuro — Démarrage")
    print("Ctrl+C pour arrêter\n")

    # Cycle immédiat au démarrage
    run_agent()

    # Programme le cycle quotidien
    heure = f"{REPORT_HOUR:02d}:{REPORT_MINUTE:02d}"
    schedule.every().day.at(heure).do(run_agent)
    print(f"[SCHEDULER] Prochain cycle programmé à {heure}")

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main()
