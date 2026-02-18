# Unified AI Observability Platform

A production-ready observability platform designed to monitor both **Traditional ML Models** and **Generative AI (LLM) Applications** in a single pane of glass.

![Dashboard Preview](https://github.com/user-attachments/assets/placeholder)

## 🚀 Features

### 1. Traditional ML Monitoring
-   **Drift Detection**: Real-time calculation of **Population Stability Index (PSI)** to detect distribution shifts.
-   **Performance Tracking**: Monitor prediction accuracy and latency.
-   **Risk Scoring**: Composite risk score based on drift magnitude and model confidence.

### 2. Generative AI (LLM) Observability
-   **Hallucination Detection**: Heuristic-based detection of uncertainty markers in LLM responses.
-   **Cost Tracking**: Real-time calculation of token usage and estimated cost using OpenAI pricing models.
-   **Latency Monitoring**: Track response times for every LLM interaction.

### 3. Unified Dashboard
-   **Real-time Visualization**: Built with **Next.js**, **Recharts**, and **Tailwind CSS**.
-   **Live Logs**: Stream incoming ML and LLM events via WebSocket/API polling.
-   **Alerting System**: Centralized alerts for high drift, hallucinations, or latency spikes.

---

## 🛠️ Tech Stack

-   **Frontend**: Next.js 14 (App Router), Tailwind CSS, Recharts, Lucide React
-   **Backend**: FastAPI (Python), Pydantic
-   **Processing**: Python Worker (Drift/Risk Engine)
-   **Database**: PostgreSQL
-   **Message Broker**: Redis (Pub/Sub for ingestion)
-   **Infrastructure**: Docker & Docker Compose

---

## 🏗️ Architecture

The system follows a microservices event-driven architecture:

1.  **Ingestion API (FastAPI)**: Receives `POST /log-ml` and `POST /log-llm` requests and pushes them to Redis.
2.  **Worker Service**: Subscribes to Redis channels, processes events (calculates drift/risk), and writes to PostgreSQL.
3.  **PostgreSQL**: Stores raw logs, computed metrics, and alerts.
4.  **Frontend**: Fetches aggregated metrics and live logs from the API for visualization.

---

## ⚡ Getting Started

### Prerequisites
-   Docker & Docker Compose
-   Node.js 18+ (for local frontend dev)
-   Python 3.9+ (for local testing)

### 1. Clone the Repository
```bash
git clone https://github.com/VedantSawant616/tcet.git
cd tcet
```

### 2. Start the Backend Infrastructure
Launch API, Worker, Database, and Redis:
```bash
docker-compose up -d api worker postgres redis
```
*Wait for a few seconds for the database to initialize.*

### 3. Start the Frontend (Local)
*Note: We run the frontend locally for the best development experience.*
```bash
cd frontend
npm install
npm run dev
```
Access the dashboard at **http://localhost:3000**.

### 4. Generate Test Traffic
Simulate real-world ML and LLM traffic using the included script:
```bash
# In a new terminal window
pip install requests
python test_traffic.py
```
You should see live data appearing on the dashboard!

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/log-ml` | Log a traditional ML model prediction |
| `POST` | `/log-llm` | Log an LLM interaction (prompt/response) |
| `GET` | `/metrics` | Retrieve time-series metrics |
| `GET` | `/alerts` | Get active alerts |
| `GET` | `/events/llm` | Get recent LLM transaction logs |

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
