import os
import datetime
import requests
from dotenv import load_dotenv
import openai
from typing import List, Dict, Optional

# .env laden
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

if not OPENAI_API_KEY or not SLACK_WEBHOOK_URL:
    raise EnvironmentError("OPENAI_API_KEY und SLACK_WEBHOOK_URL müssen in der .env-Datei gesetzt sein.")

openai.api_key = OPENAI_API_KEY

def get_moonshot_recommendation():
    prompt = f"""
Heute ist der {datetime.datetime.now().strftime('%d. %B %Y')}. Gib mir ausschließlich aktuelle Empfehlungen basierend auf diesem Datum.

Du bist ein spezialisierter Börsen-Analyst mit Fokus auf spekulative Small- und Micro-Cap-Aktien unter 20 USD. Deine Aufgabe ist es, täglich bis zu drei potenzielle Moonshot-Aktien zu identifizieren, die heute interessant für manuelles Trading über Trade Republic sein könnten.

Nutze ausschließlich öffentlich verfügbare, belegbare Informationen – keine Annahmen, keine Spekulation. Verwende ausschließlich das heutige Datum als Grundlage für alle Informationen – egal ob Charttechnik, Nachrichten oder Volumen.

🔎 Gib **nur Aktien aus**, bei denen mindestens **4 der folgenden 5 Hauptkriterien erfüllt** sind. Zusätzlich sollten **möglichst viele der Bonuskriterien** erfüllt sein.

### Hauptkriterien (mind. 4 erforderlich):
1. Preis unter 20 USD (optimal: 2–15 USD)  
2. Technisches Kaufsignal (z. B. EMA-Crossover, Breakout, starkes Volumen)  
3. Positiver Social Media/Reddit-Hype (innerhalb der letzten 48 h)  
4. Spekulatives Momentum (innerhalb der letzten 3 Tage)  
5. Relevanz zu einem der folgenden Trendthemen:  
– Künstliche Intelligenz (AI)  
– Quantencomputing  
– Biotechnologie  
– Cybersecurity  
– Erneuerbare Energien  
– Raumfahrt / Satellitentechnik  
– Fintech

### Bonuskriterien:
6. Positive Nachrichten in den letzten 7 Tagen  
7. Analysten-Empfehlung oder Kursziel-Anhebung in den letzten 5 Handelstagen

📊 Gib maximal drei Aktien aus, die diese Kriterien möglichst gut erfüllen. Auch wenn nicht alle erfüllt sind, nenne den Titel **sofern mindestens 4 Hauptkriterien erfüllt sind**, und liste transparent auf, **welche erfüllt** und **welche nicht erfüllt** wurden.

⚠️ Falls keine Aktie diese Mindestkriterien erfüllt, gib bitte eine kurze Übersicht, woran es heute gescheitert ist.

---

### 📤 Ausgabeformat (Slack-kompatibel, mit Finviz-Link & Buy-Button):

🗓 *Erstellt am {datetime.datetime.now().strftime('%d.%m.%Y – %H:%M')}*

🚀 *Heute identifizierte potenzielle Moonshots:*

Für jede Aktie:

---

🔹 **Name + Ticker**  
🔗 [Finviz öffnen](https://finviz.com/quote.ashx?t=TICKER)  
💵 **Letzter Kurs:** XX,XX USD  
🎯 **Einstieg bis max.:** XX,XX USD  

📊 **Erfüllte Kriterien:**  
✅ Preis unter 20 USD  
✅ Technisches Kaufsignal  
✅ Social Media/Reddit-Hype  
✅ Relevanz zu Trendthema: AI  

❌ **Nicht erfüllt:**  
– Keine Nachrichten in den letzten 7 Tagen  
– Keine Analysten-Empfehlung

🧱 **Handlungsempfehlung:**  
> Beobachten oder bei Pullback einsteigen. Volumen und Hype sprechen für kurzfristiges Momentum.

🟩 *Klick hier, um automatisch über deinen Trading-Bot zu kaufen:*  
```json
{{
  "symbol": "TICKER",
  "action": "buy",
  "strategy": "smartentry",
  "timeframe": "1D",
  "note": "🚀 SmartEntry aktiviert: Trade für TICKER bei letztem Schlusskurs via Slack-Buy-Button."
}}
```
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=900,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Fehler beim Abrufen der Empfehlung: {e}"

def send_to_slack(message):
    payload = {"text": message}
    try:
        resp = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Fehler beim Senden an Slack: {e}")
        return False
    return True

def main():
    print(f"[INFO] Starte Moonshot-Notifier am {datetime.datetime.now().isoformat()}")
    recommendation = get_moonshot_recommendation()
    if send_to_slack(recommendation):
        print("[INFO] Empfehlung erfolgreich an Slack gesendet.")
    else:
        print("[ERROR] Fehler beim Senden an Slack.")

if __name__ == "__main__":
    main()
