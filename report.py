# report.py — Rapport quotidien Telegram à 23h59

import requests, json, os
from datetime import date
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, DATA_FILE

TG = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send(text: str):
    try:
        requests.post(TG, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }, timeout=15)
    except Exception as e:
        print(f"[TG ERROR] {e}")

def send_rapport(resultats: list, strategie: str, wallet: str):
    today = date.today().strftime("%d/%m/%Y")
    articles_publies = [r for r in resultats if r.get("url")]
    erreurs = [r for r in resultats if not r.get("url")]

    # Ligne articles
    lignes = ""
    for r in articles_publies:
        lignes += f"✅ *{r['titre'][:50]}*\n🔗 {r['url']}\n💰 {r.get('liens_count', 0)} lien(s) affiliation\n\n"

    for r in erreurs:
        lignes += f"❌ *{r.get('titre', '?')}* — erreur\n\n"

    rapport = f"""
📊 *RAPPORT QUOTIDIEN — {today}*
━━━━━━━━━━━━━━━━━━━━━

🧠 *Stratégie :*
_{strategie}_

📝 *Articles publiés ({len(articles_publies)}/{len(resultats)}) :*

{lignes}
🪙 *Wallet de collecte :*
`{wallet}`

_Les commissions d'affiliation sont versées sur ton compte Amazon Associates, puis tu transfères vers le wallet._
━━━━━━━━━━━━━━━━━━━━━
🤖 _Agent autonome — actif 24h/24_
""".strip()

    send(rapport)

    # Sauvegarde
    data = {}
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            data = json.load(f)
    rapports = data.get("rapports", [])
    rapports.append({
        "date": today,
        "articles": len(articles_publies),
        "urls": [r.get("url") for r in articles_publies]
    })
    data["rapports"] = rapports
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
