# moonshot_notifier

Täglicher Versand von ChatGPT-generierten Aktien-Empfehlungen an Slack.

## Setup

1. Python 3 installieren
2. Repository klonen
3. `.env` Datei mit OpenAI- und Slack-Webhook-Token anlegen (siehe `.env` Beispiel)
4. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
5. Skript testen:
   ```bash
   python moonshot_daily.py
   ```

## Automatisierung (Cronjob)

Füge folgenden Eintrag zu deinem Crontab hinzu, um das Skript täglich um 09:00 Uhr auszuführen:

```
0 9 * * * /usr/bin/python3 /path/to/moonshot_notifier/moonshot_daily.py >> /var/log/moonshot.log 2>&1
```

Passe `/path/to/moonshot_notifier/` ggf. an deinen Installationspfad an. 