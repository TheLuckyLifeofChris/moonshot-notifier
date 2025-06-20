# Moonshot-Notifier

![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

Ein automatisierter Aktien-Screener, der täglich bis zu drei spekulative US-Aktien per Slack empfiehlt – basierend auf 7 klaren Kriterien.




# 🌙 Moonshot-Notifier

Der **Moonshot Notifier** ist ein automatisierter GitHub Actions Workflow, der werktags um 10:00 Uhr (UTC) ausgeführt wird. Er generiert mithilfe von ChatGPT täglich bis zu drei spekulative Aktienempfehlungen und sendet sie direkt an einen definierten Slack-Channel.

---

## 🚀 Features

- ⏰ Automatisierter Cron-Job: Montag bis Freitag um 10:00 Uhr (UTC)
- 🧠 Nutzung von GPT-4o zur Generierung von Aktienempfehlungen
- 💬 Direkte Slack-Benachrichtigung über Webhook
- 🧾 Strikter Kriterienkatalog für Empfehlungen (Preis, News, Momentum, Social Media etc.)

---

## 📦 Setup

### 1. 🔑 GitHub Secrets

Folgende Secrets müssen in den Repository-Einstellungen gesetzt werden:

| Secret Name        | Beschreibung                                 |
|--------------------|----------------------------------------------|
| `OPENAI_API_KEY`   | Dein OpenAI API Key                          |
| `SLACK_WEBHOOK_URL`| Webhook-URL des Ziel-Slack-Channels          |

> ⚙️ → Repository → Settings → Secrets → Actions → `New repository secret`

---

### 2. 🔁 Automatisierung via GitHub Actions

Der Workflow liegt unter:

```bash
.github/workflows/moonshot-notifier.yml
