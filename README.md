# SENTINEL: Autonomous Incident Response for Splunk

![SENTINEL Dashboard](https://via.placeholder.com/1200x600.png?text=SENTINEL+Dashboard+Preview)

SENTINEL is a production-grade, autonomous incident response system built for the **Splunk Agentic Ops Hackathon**. It intercepts alerts from your Splunk instance, orchestrates AI agents to triage, investigate, and simulate remediations using **Splunk Hosted Models (Foundation-Sec)** and real-time Threat Intelligence.

## 🚀 Quick Start (5 Minutes to Demo)

### Prerequisites
- Docker and Docker Compose installed.
- (Optional) A `.env` file with your Splunk and API credentials for live data.

### 1. Setup Environment
Clone the repository and copy the example environment file:
```bash
git clone https://github.com/yourusername/SENTINEL.git
cd SENTINEL
cp .env.example .env
```
*(Open `.env` and add your Splunk URL, Token, and Hosted Models API key if testing with real data. If not, the system will fall back to realistic mock responses).*

### 2. Launch the Stack
Start the Backend (FastAPI), Celery workers, Redis broker, and Frontend (Next.js) using Docker Compose:
```bash
docker-compose up --build -d
```

### 3. View the Dashboard
Navigate to `http://localhost:3000` in your browser. You will see the live SENTINEL dashboard connecting to the backend.

### 4. Trigger an Alert
To simulate an alert coming from Splunk into the webhook receiver:
```bash
curl -X POST http://localhost:8000/api/v1/webhook/splunk \
  -H "Content-Type: application/json" \
  -d '{"result": {"src_ip": "192.168.1.100", "dest_ip": "10.0.0.5", "action": "failed_login", "user": "admin"}}'
```
Watch the Dashboard update in real-time as the agents orchestrate the investigation!

## 🧠 Architecture

Our architecture guarantees high performance, scalability, and seamless integration:

1. **Splunk Instance:** Forward alerts via Webhook to our API.
2. **FastAPI Webhook Server:** Receives alerts and drops them into a Redis message broker.
3. **Celery Orchestration Engine:** Manages an async pipeline of autonomous agents.
4. **Autonomous Agents:**
   - **Triage Agent:** Uses `Foundation-Sec-1.1-8B` to score severity.
   - **Investigate Agent:** Queries VirusTotal/AlienVault and runs correlation SPL queries via `splunk-sdk`.
   - **Remediate Agent:** Determines the playbook and executes actions.
5. **Next.js Dashboard:** A premium, dark-themed UI that pulls real-time updates.

## 🏆 Hackathon Tracks
- **Security:** End-to-end autonomous IR.
- **Platform & Developer Experience:** Built using Splunk Python SDK and standard webhooks.
- **Bonus:** Leverages Splunk Hosted Models for generative AI event scoring.

## 📄 License
This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
