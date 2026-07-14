# ✈️ TravelMate AI

> **Your Intelligent Agentic AI Travel Planning Assistant**

TravelMate AI is an Agentic AI-powered travel planning assistant built on **IBM watsonx Orchestrate**. It collects your travel preferences through a clean Streamlit interface, builds a structured travel request, and forwards it to the watsonx Orchestrate agent to generate a fully personalised, end-to-end itinerary.

---

## 🛠️ Technology Stack

| Technology | Role |
|---|---|
| **IBM watsonx Orchestrate** | Agentic AI backbone — orchestrates all planning tools and sub-agents |
| **IBM Cloud** | Scalable enterprise cloud hosting the AI services |
| **IBM Bob** | AI developer assistant used to build and iterate on TravelMate AI |
| **RAG Knowledge Base** | Retrieval-Augmented Generation for contextual travel knowledge |
| **Exa Web Search** | Real-time web search for up-to-date travel information *(when available)* |
| **Streamlit** | Python-based frontend framework |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/travelmate-ai.git
cd travelmate-ai
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (never commit this file):

```env
WATSONX_AGENT_URL=https://your-watsonx-orchestrate-endpoint
WATSONX_API_KEY=your_api_key_here
```

> ⚠️ **Never hardcode API keys or secrets in source code.**  
> Use environment variables or [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) (`st.secrets`) for all credentials.

### 5. Run the application

```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 📋 Features

- **Destination & Origin** — specify where you're going and where you're starting from
- **Trip Duration** — number of days for the trip
- **Travelers** — total headcount
- **Budget & Currency** — full budget with currency selector (INR, USD, EUR, GBP, JPY, AUD, Other)
- **Travel Type** — Solo / Couple / Family / Friends / Student / Business
- **Travel Style** — Budget / Moderate / Luxury / Adventure / Relaxation / Cultural / Eco-friendly
- **Travel Interests** — multi-select from 12 interest categories
- **Special Requirements** — free-text for accessibility, dietary needs, or any custom requests
- **Input Validation** — clear error messages for missing or invalid inputs
- **Structured Request Generation** — produces a formatted request string ready for the agent API

---

## 🗂️ Project Structure

```
travelmate-ai/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .env                # Local secrets (⚠️ do NOT commit)
```

---

## 🔗 API Integration (Coming Soon)

The generated travel request is already structured for forwarding to the IBM watsonx Orchestrate agent. When the API is ready, uncomment and configure the relevant section in [`app.py`](app.py):

```python
import os, requests

api_url = os.environ.get("WATSONX_AGENT_URL")
api_key = os.environ.get("WATSONX_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}
payload = {"message": travel_request}
response = requests.post(api_url, json=payload, headers=headers)
st.write(response.json())
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> Built with IBM watsonx Orchestrate, IBM Cloud, IBM Bob, and Streamlit.
