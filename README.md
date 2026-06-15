# GUARDIAN: Autonomous Incident Response for Splunk

GUARDIAN is a production-grade, autonomous incident response system built for the **Splunk Agentic Ops Hackathon**. It intercepts alerts from your Splunk instance and orchestrates a pipeline of multi-agent AI to triage, investigate, and remediate threats autonomously in real-time.

## 🏆 Hackathon Track
This project strictly falls under the **Security** track (specifically Security Operations, SOAR, and Threat Intelligence), while heavily utilizing the **Platform & Developer Experience** track via the Splunk Webhook ecosystem.

---

## ✅ Submission Checklist Fulfilled
1. **Clear README documentation:** Yes, provided below.
2. **Setup and run instructions:** Yes, detailed Cloud Deployment guide.
3. **Any required dependencies:** Yes, standard Python & Node packages.
4. **Example configurations/datasets:** Yes, we provide the exact mock Ransomware payload to trigger the pipeline via cURL.

---

## 🚀 Quick Start (Cloud Deployment)

GUARDIAN is designed to be completely cloud-native, entirely bypassing local Docker constraints for a flawless 24/7 autonomous pipeline.

### 1. Deploy the Backend (Render)
GUARDIAN uses FastAPI and built-in asynchronous `BackgroundTasks` to process threats without needing a heavy Celery worker.
1. Connect your GitHub repository to Render as a **Web Service**.
2. Set Root Directory to `backend` and Dockerfile Path to `./Dockerfile`.
3. Set the following Environment Variables:
   - `SPLUNK_HOST`
   - `SPLUNK_TOKEN`
   - `AZURE_OPENAI_API_KEY` (Our production failover for AI triage)
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_DEPLOYMENT` (e.g., `gpt-5.4`)
   - `AZURE_OPENAI_API_VERSION`
   - `VIRUSTOTAL_API_KEY`
   - `ALIENVAULT_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

### 2. Deploy the Frontend Command Center (Vercel)
1. Connect your GitHub repository to Vercel.
2. Set the Root Directory to `frontend`.
3. Add the `NEXT_PUBLIC_API_URL` environment variable pointing to your deployed Render URL (e.g., `https://sentinel-backend-xxxx.onrender.com`).
4. Click Deploy.

### 3. Run the Simulation (Example Dataset)
You don't need a live Splunk instance to test the AI. You can trigger a live Ransomware attack simulation directly from the integrated terminal on the Next.js Vercel dashboard. Alternatively, use this cURL payload:

```bash
curl -X POST https://your-render-url.onrender.com/api/v1/webhook/splunk \
  -H "Content-Type: application/json" \
  -d '{
    "sid": "DEMO-9999",
    "search_name": "Ransomware Behavior Detected",
    "app": "search",
    "owner": "admin",
    "results_link": "https://prd-p-3icdn.splunkcloud.com",
    "result": {
      "src_ip": "185.156.73.14",
      "dest_ip": "10.0.1.55",
      "user": "system",
      "action": "multiple_file_encryptions"
    }
  }'
```

---

## 🧠 Architecture

Our architecture guarantees zero mock data. The entire pipeline runs on live API integrations.
1. **Splunk Webhook:** Forwards logs directly to our FastAPI endpoint.
2. **FastAPI `BackgroundTasks`:** Instantly queues the alert so Splunk doesn't timeout.
3. **Multi-Agent Pipeline:**
   - **Triage Agent:** Uses AI models to score severity and filter false positives.
   - **Investigate Agent:** Queries live Threat Intel (VirusTotal, AlienVault OTX) for IOCs.
   - **Remediate Agent:** Determines the playbook and instantly messages the Security Team via Telegram.
4. **Next.js Dashboard:** A premium, dark-themed UI that visualizes the autonomous agent actions in real-time.
