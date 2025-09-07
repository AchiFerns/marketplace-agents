# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Shopping%20Cart.png" width="35" height="35" /> Marketplace Agents – AI Intern Project

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LLaMA](https://img.shields.io/badge/Groq_LLaMA_3.1-8B-5E5CE6?style=for-the-badge&logo=meta&logoColor=white)

**🤖 AI-Powered Backend Service for Second-Hand Marketplaces**

An intelligent backend that uses **LLMs + rule-based agents** to help buyers and sellers with pricing, moderation, and fraud detection.

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 💰 **Price Suggestor Agent**
Suggests a fair resale price range

### 🔒 **Chat Moderation Agent**
Detects abuse, spam, phone numbers

### ⚠️ **Fraud Detection Agent**
Flags suspicious underpriced/overpriced listings

</td>
<td width="50%">

### 🤝 **Negotiation Agent**
Simulates buyer-seller negotiation to reach a deal

### 📝 **Logging System**
Saves all price suggestions into CSV

### ⚡ **FastAPI Integration**
RESTful API with Swagger documentation

</td>
</tr>
</table>

## 📂 Project Structure

```
marketplace-agents/
├── 📊 data/                    # Dataset
│   ├── products.csv
│   └── cleaned_products.csv
├── 📈 reports/                 # Logs & profiling
│   ├── data_profile.json
│   └── price_suggestions.csv
├── 🧠 src/                     # Source code
│   ├── agents/                # Agents
│   │   ├── price_agent.py
│   │   ├── moderation_agent.py
│   │   ├── fraud_agent.py
│   │   └── negotiation_agent.py
│   ├── api.py
│   ├── llm_client.py
│   ├── save_report.py
│   └── preprocess.py
├── 🧪 tests/                   # Unit tests
│   └── test_moderation.py
├── 📝 examples/                # Example scripts
│   ├── test_api_with_key.py
│   └── test_creative_agents.py
├── .env.example               # Environment config
├── requirements.txt
└── README.md
```

## ⚙️ Setup

### **1. Clone & Create Environment**

```bash
# Clone the repository
git clone https://github.com/AchiFerns/marketplace-agents.git
cd marketplace-agents

# Create conda environment
conda create -n marketplace-agents python=3.11 -y
conda activate marketplace-agents

# Install dependencies
pip install -r requirements.txt
```

### **2. Configure .env**

Create a `.env` file in project root:

```env
API_KEY=supersecret123
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
USE_LLM=true
GROQ_MODEL=llama-3.1-8b-instant
```

### **3. Run the API**

```bash
uvicorn src.api:app --reload
```

📍 Open: http://127.0.0.1:8000/docs

## 🚀 API Endpoints

### ✅ **Health Check**
```http
GET /
```
**Response:**
```json
{ 
  "status": "ok", 
  "project": "marketplace-agents" 
}
```

---

### 💰 **Price Suggestor** `/negotiate`

<details>
<summary><b>View Request/Response</b></summary>

**Request:**
```json
{
  "title": "iPhone 12",
  "category": "Mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": 24,
  "asking_price": 35000,
  "location": "Mumbai"
}
```

**Response:**
```json
{
  "suggested_price_min": 22994,
  "suggested_price_max": 29266,
  "reason": "The asking price of ₹35,000 seems high...",
  "llm_provider": "groq",
  "llm_model": "llama-3.1-8b-instant"
}
```
</details>

---

### 🔒 **Chat Moderation** `/moderate`

<details>
<summary><b>View Request/Response</b></summary>

**Request:**
```json
{ 
  "message": "Call me at 9876543210 for details!" 
}
```

**Response:**
```json
{
  "status": "PhoneDetected",
  "reason": "Contains phone number or numeric contact info.",
  "labels": ["phone"],
  "confidence": 0.7
}
```
</details>

---

### ⚠️ **Fraud Detection** `/fraud-check`

<details>
<summary><b>View Request/Response</b></summary>

**Request:**
```json
{
  "title": "iPhone 12",
  "category": "Mobile",
  "brand": "Apple",
  "condition": "Good",
  "age_months": 24,
  "asking_price": 2000,
  "location": "Mumbai"
}
```

**Response:**
```json
{
  "status": "Suspicious",
  "reason": "Asking price ₹2000 is more than 50% below the fair minimum ₹22994. Possible scam listing.",
  "suggested_min": 22994,
  "suggested_max": 29266
}
```
</details>

---

### 🤝 **Negotiation** `/negotiate-deal`

<details>
<summary><b>View Request/Response</b></summary>

**Request:**
```json
{
  "title": "Dell Inspiron Laptop",
  "category": "Laptop",
  "brand": "Dell",
  "condition": "Good",
  "age_months": 36,
  "asking_price": 80000,
  "location": "Pune"
}
```

**Response:**
```json
{
  "seller_initial": 80000,
  "buyer_offer": 25000,
  "final_agreed_price": 53250,
  "suggested_range": "24000 - 29000"
}
```
</details>

## 📝 Logging

All `/negotiate` calls are logged into:

```bash
reports/price_suggestions.csv
```

**Example row:**
```csv
2025-09-07T15:51:06.052111,iPhone 12,Apple,24,35000,22994,29266,"The suggested price range...",groq,llama-3.1-8b-instant
```

## ✅ Testing

### **Run Example Scripts**
```bash
python -m examples.test_api_with_key
python -m examples.test_creative_agents
```

### **Run Unit Tests**
```bash
pytest -q
```

## 📦 Deliverables

| Component | Description |
|-----------|-------------|
| ✅ **Agents** | Modular agents implemented in `src/agents/` |
| ✅ **API** | FastAPI endpoints exposed and documented |
| ✅ **Dataset** | Products data + cleaned version included |
| ✅ **LLM Integration** | Groq LLaMA-3.1 integration |
| ✅ **Logging** | Comprehensive logging in `reports/` |
| ✅ **Documentation** | Setup, usage, and examples |

## 📊 Evaluation Criteria Mapping

<div align="center">

| Criteria | Implementation |
|----------|---------------|
| **Agent Implementation** | → Modular agents in `src/agents/` |
| **Correctness** | → Price ranges & moderation realistic |
| **Code Quality** | → Modular, `.env`, logging, tests, clear README |
| **Practicality** | → Useful in real-world marketplaces |
| **Creativity** | → Fraud detection + multi-agent negotiation |

</div>

## 🔮 Future Improvements

- 🎯 Fraud clustering with ML anomaly detection
- 🌐 Multi-language support
- 🚀 Performance optimization
- 📊 Advanced analytics dashboard

---

<div align="center">

### 👉 Built with **FastAPI** + **Groq LLaMA-3.1**

[![GitHub](https://img.shields.io/badge/GitHub-AchiFerns-181717?style=flat-square&logo=github)](https://github.com/AchiFerns)

**⭐ Star this repo if you find it helpful!**

</div>
