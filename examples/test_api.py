# examples/test_api.py
import requests
import json

BASE = "http://127.0.0.1:8000"

# --- Price request
product = {
    "title": "iPhone 12",
    "category": "Mobile",
    "brand": "Apple",
    "condition": "Good",
    "age_months": 24,
    "asking_price": 35000,
    "location": "Mumbai"
}

try:
    r = requests.post(f"{BASE}/negotiate", json=product, timeout=30)
    print("negotiate status", r.status_code)
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except Exception:
        print("negotiate response text:", r.text)
except Exception as e:
    print("negotiate request error:", e)

# --- Moderation request
try:
    r2 = requests.post(f"{BASE}/moderate", json={"message":"Call me at 9876543210"}, timeout=30)
    print("\nmoderate status", r2.status_code)
    try:
        print(json.dumps(r2.json(), indent=2, ensure_ascii=False))
    except Exception:
        print("moderate response text:", r2.text)
except Exception as e:
    print("moderate request error:", e)
