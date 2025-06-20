# moonshot_notifier

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

`moonshot_notifier` is an automated daily Slack notifier that uses ChatGPT to identify up to three potential **moonshot stock candidates** under $20 USD, based on strict criteria. The notifier runs every weekday at 10:00 (CET) via GitHub Actions and sends the recommendations to a specified Slack channel.

It is designed for manual trading using brokers like Trade Republic.

---

## 🔍 Strategy & Criteria

Every weekday, the notifier asks ChatGPT (GPT-4o) to select **up to 3 stocks** that fulfill all **7 strict criteria**:

1. **Price under $20** (ideally $2–$15)
2. **Technical Buy Signal** (e.g., EMA crossover, breakout, unusual volume)
3. **Positive News** within the **last 7 days**
4. **Analyst Buy Ratings** or upgrades within the **last 5 trading days**
5. **Reddit or Social Media Hype** within the **last 48 hours**
6. **Speculative Momentum** in the **last 3 days**
7. **Relevance to a trending theme**:
   - Artificial Intelligence (AI)
   - Quantum Computing
   - Biotechnology
   - Cybersecurity
   - Renewable Energy
   - Space / Satellite
   - Fintech

⚠️ **If no stock meets all 7 conditions**, the bot **does not send a recommendation**.

---

## 💬 Example Output

```markdown
📅 *Created on 18 June 2025 – 10:00*

🔹 **Stock Name (TICKER)**
💵 Last price: $4.67  
🎯 Entry: up to $5.20  
📊 Reason: EMA crossover, +350% volume, news from June 16 (new contract), Buy rating from JP Morgan, strong Reddit activity, biotech-related  
🧭 Action: Watch for breakout above $5.20. 🟩 Strong Setup – exceptional data


⸻

⚙️ Tech Stack
	•	GitHub Actions with CRON scheduler (Mon–Fri, 10:00 CET)
	•	ChatGPT-4o for generating the output
	•	Slack Webhook for sending the message

⸻

🔐 Secrets (required in GitHub repo settings)
	•	OPENAI_API_KEY – your OpenAI API key
	•	SLACK_WEBHOOK_URL – your Slack Incoming Webhook URL

⸻

🧪 Local Development

To run the script locally:

python3 notifier.py

Make sure you have a .env file in your root directory with:

OPENAI_API_KEY=your_openai_key
SLACK_WEBHOOK_URL=your_webhook_url


⸻

📜 License

This project is licensed under the MIT License.
