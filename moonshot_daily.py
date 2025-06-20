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
Heute ist der {datetime.datetime.now().strftime('%d. %B %Y')}. Gib mir ausschließlich aktuelle Empfehlungen basierend auf diesem Datum.

Du bist ein spezialisierter Börsen-Analyst mit Fokus auf spekulative Small- und Micro-Cap-Aktien unter 20 USD. Deine Aufgabe ist es, täglich bis zu drei potenzielle Moonshot-Aktien zu identifizieren, die heute interessant für manuelles Trading über Trade Republic sein könnten.

Nutze ausschließlich öffentlich verfügbare, belegbare Informationen – keine Annahmen, keine Spekulation. Verwende ausschließlich das heutige Datum als Grundlage für alle Informationen – egal ob Charttechnik, Nachrichten oder Volumen.

🔎 Voraussetzung: Nur Aktien, bei denen **alle folgenden 7 Kriterien gleichzeitig erfüllt sind**:

1. Preis unter 20 USD (optimal: 2–15 USD)  
2. Technisches Kaufsignal (z. B. EMA-Crossover, Breakout, hohes Volumen)  
3. Positive Nachrichten **aus den letzten 7 Tagen**  
4. Analysten-Empfehlung oder Kursziel-Anhebung **aus den letzten 5 Handelstagen**  
5. Positiver Social Media/Reddit-Hype **aus den letzten 48 Stunden**  
6. Spekulatives Momentum **innerhalb der letzten 3 Tage**  
7. Relevanz zu einem der folgenden Trendthemen:  
– Künstliche Intelligenz (AI)  
– Quantencomputing  
– Biotechnologie  
– Cybersecurity  
– Erneuerbare Energien  
– Raumfahrt / Satellitentechnik  
– Fintech

⚠️ Falls **keine Aktie alle 7 Kriterien erfüllt**, gib **keine Empfehlung** aus.

📎 Wenn es keine Empfehlung gibt, gib bitte optional eine kurze Info, woran es konkret gescheitert ist.

📊 Format der Ausgabe (Slack-kompatibel, mit Emojis und Absätzen):

📅 *Erstellt am {datetime.datetime.now().strftime('%d.%m.%Y – %H:%M')}*

Für jede Aktie:

1. 🔹 **Name + Ticker**  
2. 💵 **Letzter Kurs (geschätzt oder letzter Schlusskurs)**  
3. 🎯 **Einstieg bis maximal X USD**  
4. 📊 **Begründung für die Auswahl**  
5. 🧭 **Handlungsempfehlung**

🟩 Falls außergewöhnliche Stärke vorliegt (z. B. +300 % Volumen, mehrere Analysten, viraler Reddit-Hype):  
„🟩 Starkes Setup – außergewöhnliche Datenlage“

🚨 Hinweis: Diese Empfehlungen sind spekulativ. Handle auf eigene Verantwortung (DYOR).
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