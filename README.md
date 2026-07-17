# ✈️ TravelMate AI
### Your Intelligent Agentic AI Travel Planning Assistant

TravelMate AI is an **Agentic AI-powered travel planning assistant** built using **IBM watsonx Orchestrate**, **IBM Cloud**, **Python**, and **Streamlit**. It allows users to generate personalized travel itineraries by providing travel details such as destination, origin, duration, budget, travel style, interests, and special requirements.

The application securely communicates with a deployed **IBM watsonx Orchestrate Agent** using the official **IBM watsonx Orchestrate ADK**, which intelligently generates complete travel plans including accommodation suggestions, transportation guidance, local food recommendations, budget estimation, safety tips, and hidden gems.

---

# 🛠️ Technology Stack

| Technology | Role |
|------------|------|
| IBM watsonx Orchestrate | Agentic AI engine for intelligent itinerary generation |
| IBM Cloud | Cloud platform hosting watsonx Orchestrate services |
| IBM watsonx Orchestrate ADK | Official SDK for securely invoking the TravelMate AI Agent |
| IBM Bob | AI developer assistant used during development |
| Python | Backend application logic |
| Streamlit | Interactive web application frontend |
| GitHub | Source code management and version control |
| Streamlit Community Cloud | Public deployment platform |

---

# 🚀 Live Demo

### 🌐 Public Application

https://travelmateaiibm.streamlit.app

### 💻 GitHub Repository

https://github.com/amith-0609/IBM_TravelAgent

---

# 🚀 Getting Started

## Prerequisites

- Python 3.9 or higher
- pip

---

## 1. Clone the repository

```bash
git clone https://github.com/amith-0609/IBM_TravelAgent.git

cd IBM_TravelAgent
```

---

## 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure IBM watsonx Orchestrate

Create either a `.env` file (for local development) or configure **Streamlit Secrets** when deploying.

```env
WATSONX_ORCHESTRATE_API_KEY=your_api_key

WATSONX_ORCHESTRATE_URL=https://your-instance-url

WATSONX_ORCHESTRATE_AGENT_ID=your_agent_id
```

> ⚠️ Never hardcode API keys or secrets into the source code.
>
> Use **environment variables** or **Streamlit Secrets** for secure credential management.

---

## 5. Run the application

```bash
streamlit run app.py
```

The application opens at:

```
http://localhost:8501
```

---

# 📋 Features

✅ Personalized travel itinerary generation

✅ IBM watsonx Orchestrate Agent integration

✅ Destination and Origin selection

✅ Trip duration planning

✅ Budget-aware recommendations

✅ Multiple travel styles

- Budget
- Moderate
- Luxury
- Adventure
- Relaxation
- Cultural
- Eco-friendly

✅ Travel types

- Solo
- Couple
- Family
- Friends
- Student
- Business

✅ Interest-based itinerary generation

- Local Food
- Culture
- Beaches
- Adventure
- Nature
- Shopping
- Nightlife
- History
- Wildlife
- Wellness
- Photography
- Festivals

✅ Special requirements support

✅ Day-by-day itinerary

✅ Morning, Afternoon & Evening activities

✅ Accommodation suggestions

✅ Local transportation guidance

✅ Restaurant recommendations

✅ Budget estimation

✅ Practical travel tips

✅ Safety considerations

✅ Hidden gems

---

# 🗂️ Project Structure

```
IBM_TravelAgent/

│── app.py                 # Main Streamlit application

│── requirements.txt       # Python dependencies

│── README.md              # Project documentation

│── .gitignore

│── assets/                # Images and screenshots (optional)

└── screenshots/           # Application screenshots (optional)
```

---

# 🤖 IBM watsonx Orchestrate Integration

TravelMate AI is fully integrated with **IBM watsonx Orchestrate** using the official **IBM watsonx Orchestrate ADK**.

Application workflow:

```
User
   │
   ▼
TravelMate AI (Streamlit)
   │
   ▼
Travel Request Builder
   │
   ▼
IBM watsonx Orchestrate ADK
   │
   ▼
TravelMate AI Agent
   │
   ▼
Personalized Travel Itinerary
   │
   ▼
User
```

The TravelMate AI agent processes traveler preferences and generates:

- Trip overview
- Day-by-day itinerary
- Accommodation recommendations
- Local transportation guidance
- Food recommendations
- Budget estimation
- Practical travel tips
- Safety considerations
- Hidden gems

---

# 📈 Future Enhancements

- Live flight API integration
- Hotel booking APIs
- Weather forecasting
- Google Maps integration
- Voice-enabled travel assistant
- Multi-agent collaboration
- Real-time booking support
- Offline itinerary downloads
- Multi-language support

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Please feel free to open an issue or submit a pull request.

---

# 📄 License

This project is intended for educational and demonstration purposes as part of the **IBM University Engagement Program**.

---

## 👨‍💻 Developed By

**Amith Yakkala**

IBM University Engagement Project

TravelMate AI — Intelligent Agentic AI Travel Planning Assistant

---

### ⭐ Built with IBM watsonx Orchestrate, IBM Cloud, IBM Bob, Python, Streamlit, and GitHub.
