# 🛒 Marketplace Agents – AI Intern Project

An **AI-powered backend service** for a second-hand marketplace.  
This project uses **LLMs + rule-based agents** to help buyers and sellers with pricing, moderation, and fraud detection.  

✨ Built with **FastAPI**, structured as modular **agents**, and enhanced with **Groq LLaMA-3.1** for human-friendly explanations.

---

## 🚀 Features

- 💰 **Price Suggestor Agent** → Suggests a fair resale price range.  
- 🛡 **Chat Moderation Agent** → Detects abuse, spam, phone numbers.  
- 🔍 **Fraud Detection Agent** → Flags suspicious underpriced/overpriced listings.  
- 🤝 **Negotiation Agent** → Simulates buyer–seller negotiation to reach a deal.  
- 📝 **Logging** → Saves all price suggestions into `reports/price_suggestions.csv`.  
- 🔗 **FastAPI API** → Exposes endpoints (`/negotiate`, `/moderate`, `/fraud-check`, `/negotiate-deal`).  

---

## 📂 Project Structure

marketplace-agents/
├── data/
│ ├── products.csv
│ └── cleaned_products.csv
├── reports/
│ ├── data_profile.json
│ └── price_suggestions.csv
├── src/
│ ├── agents/
│ │ ├── price_agent.py
│ │ ├── moderation_agent.py
│ │ ├── fraud_agent.py
│ │ └── negotiation_agent.py
│ ├── api.py
│ ├── preprocess.py
│ ├── llm_client.py
│ ├── groq_client.py
│ └── save_report.py
├── examples/
│ ├── test_api_with_key.py
│ └── test_creative_agents.py
├── tests/
│ └── test_moderation.py
├── .env.example
├── requirements.txt
└── README.md

yaml
---

## ⚙️ Setup

### 1. Clone & create environment
```bash
git clone <your-repo-url>
cd marketplace-agents

conda create -n marketplace-agents python=3.11 -y
conda activate marketplace-agents

2. Install dependencies
pip install -r requirements.txt

3. Configure .env
Create a .env file in project root:
API_KEY=supersecret123
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
USE_LLM=true
GROQ_MODEL=llama-3.1-8b-instant

▶️ Run the API
Start FastAPI server:
uvicorn src.api:app --reload
Open docs: 👉 http://127.0.0.1:8000/docs

📌 API Endpoints
🔹 Health Check
GET /
Response:
{ "status": "ok", "project": "marketplace-agents" }

🔹 Price Suggestor (/negotiate)
Request
POST /negotiate
x-api-key: supersecret123
Content-Type: application/json
json
Copy code
{
  "title": "iPhone 12",
  "category": "Mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": 24,
  "asking_price": 35000,
  "location": "Mumbai"
}
Response

{
  "suggested_price_min": 22994,
  "suggested_price_max": 29266,
  "reason": "The asking price of ₹35,000 for an iPhone 12 (2 years old, good condition) seems high. A fair range is ₹22,994–₹29,266, based on age, condition, and Apple’s brand value.",
  "llm_provider": "groq",
  "llm_model": "llama-3.1-8b-instant"
}

🔹 Chat Moderation (/moderate)
Request
{ "message": "Call me at 9876543210 for details!" }
Response
{
  "status": "PhoneDetected",
  "reason": "Contains phone number or numeric contact info.",
  "labels": ["phone"],
  "confidence": 0.7
}

🔹 Fraud Detection (/fraud-check)
Request 
{
  "title": "iPhone 12",
  "category": "Mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": 24,
  "asking_price": 2000,
  "location": "Mumbai"
}

Response
{
  "status": "Suspicious",
  "reason": "Asking price ₹2000 is more than 50% below the fair minimum ₹22994. Possible scam listing.",
  "asking_price": 2000,
  "suggested_min": 22994,
  "suggested_max": 29266
}

🔹 Negotiation (/negotiate-deal)
Request
{
  "title": "Dell Inspiron Laptop",
  "category": "Laptop",
  "brand": "Dell",
  "condition": "Good",
  "age_months": 36,
  "asking_price": 80000,
  "location": "Pune"
}
Response

{
  "seller_initial": 80000,
  "buyer_offer": 26500,
  "final_agreed_price": 53250,
  "suggested_range": "24000 - 29000"
}

📝 Logging (Bonus)
All /negotiate calls are logged into:
reports/price_suggestions.csv

Example row:
2025-09-07T15:51:06.052111,iPhone 12,Apple,24,35000,22994,29266,"The suggested price range...",groq,llama-3.1-8b-instant

✅ Testing
Run example scripts:

python -m examples.test_api_with_key
python -m examples.test_creative_agents

Run unit tests:
pytest -q

📦 Deliverables
Agents implemented (src/agents/).

Exposed via FastAPI endpoints.

Dataset + cleaned data included.

LLM integration (Groq).

Logging system (reports/).

README with setup, usage, and examples.

🎯 Evaluation Criteria Mapping
Agent Implementation → Modular agents in src/agents/.

Correctness → Price ranges & moderation are realistic.

Code Quality → Modular, .env, logging, tests, clear README.

Practicality → Useful in real-world marketplaces.

Creativity → Fraud detection + multi-agent negotiation.

🔮 Future Improvements
Fraud clustering with ML anomaly detection.

Recommendation system (related products).


