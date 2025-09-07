# examples/test_api_with_key.py
"""
Test script for Marketplace Agents API with API key + CSV logging.
- Calls /negotiate with a sample product
- Calls /moderate with a sample chat message
- Saves negotiation results into reports/price_suggestions.csv
"""

import requests, json
from src.save_report import save_suggestion   # logging helper

BASE = "http://127.0.0.1:8000"
headers = {"x-api-key": "supersecret123", "Content-Type": "application/json"}

# -------- Sample product --------
product = {
    "title": "iPhone 12",
    "category": "Mobile",
    "brand": "Apple",
    "condition": "Good",
    "age_months": 24,
    "asking_price": 35000,
    "location": "Mumbai"
}

# -------- Call /negotiate --------
print("== Calling /negotiate ==")
r = requests.post(f"{BASE}/negotiate", json=product, headers=headers, timeout=30)
print("status:", r.status_code)
result = r.json()
print(json.dumps(result, indent=2, ensure_ascii=False))

# Save to CSV
print("\n== Saving result to reports/price_suggestions.csv ==")
save_suggestion(product, result)

# -------- Call /moderate --------
print("\n== Calling /moderate ==")
msg = {"message": "Call me at 9876543210 for more info!"}
r2 = requests.post(f"{BASE}/moderate", json=msg, headers=headers, timeout=30)
print("status:", r2.status_code)
print(json.dumps(r2.json(), indent=2, ensure_ascii=False))

print("\n✅ Done. Check reports/price_suggestions.csv for a new log entry.")
