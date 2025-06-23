import os
import datetime
import requests
from dotenv import load_dotenv
import openai

# .env laden
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')

if not OPENAI_API_KEY or not SLACK_WEBHOOK_URL:
    raise EnvironmentError("OPENAI_API_KEY und SLACK_WEBHOOK_URL müssen in der .env-Datei gesetzt sein.")

openai.api_key = OPENAI_API_KEY

def get_moonshot_recommendation():
    prompt = f"""
Heute ist der {datetime.datetime.now().strftime('%d. %B %Y')}. Gib mir eine fiktive, aber realistische tägliche Übersicht über maximal drei spekulative US-Aktien unter 20 USD mit starkem Momentum, die gut zu einer Moonshot-Strategie passen könnten.

Simuliere aktuelle Nachrichten, Kursmuster und Stimmungen so, wie ein Börsenanalyst es typischerweise einschätzen würde. Verwende reale Ticker und plausible Kursangaben. Hinweis: Diese Daten sind hypothetisch und dienen als Inspiration zur manuellen Analyse durch den Nutzer.

🔎 Gib **nur Aktien aus**, bei denen mindestens **4 der folgenden 5 Hauptkriterien erfüllt** sind. Zusätzlich sollten möglichst viele Bonuskriterien erfüllt sein.

### Hauptkriterien (mind. 4 erforderlich):
1. Preis unter 20 USD (optimal: 2–15 USD)  
2. Technisches Kaufsignal (EMA-Crossover, Breakout, starkes Volumen)  
3. Positiver Social Media/Reddit-Hype (letzte 48 h)  
4. Spekulatives Momentum (letzte 3 Tage)  
5. Relevanz zu einem Trendthema: AI, Quantencomputing, Biotech, Cybersecurity, Erneuerbare Energien, Raumfahrt, Fintech

### Bonuskriterien:
6. Positive Nachrichten (letzte 7 Tage)  
7. Analysten-Empfehlung oder Kursziel-Anhebung (letzte 5 Handelstage)

⚠️ Falls keine Aktie diese Kriterien erfüllt, gib eine kurze Begründung.

---

### 📤 Ausgabeformat (Slack-kompatibel):

🗓 *Erstellt am {datetime.datetime.now().strftime('%d.%m.%Y – %H:%M')}*

🚀 *Heute identifizierte potenzielle Moonshots:*

Für jede Aktie:

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
– Keine Analysten-Empfehlung

🧭 **Handlungsempfehlung:**  
> Beobachten oder bei Pullback einsteigen.
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