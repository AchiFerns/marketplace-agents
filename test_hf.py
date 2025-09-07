# test_hf.py — quick Hugging Face connectivity test
import os, requests
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HUGGINGFACE_API_KEY")
model = os.getenv("HF_MODEL", "gpt2")
print("Using token present:", bool(token))
print("Requested HF_MODEL:", model)

if not token:
    print("HUGGINGFACE_API_KEY not set in .env — please add it and rerun.")
    raise SystemExit(1)

url = f"https://api-inference.huggingface.co/models/{model}"
headers = {"Authorization": f"Bearer {token}"}

try:
    resp = requests.get(url, headers=headers, timeout=30)
    print("Status code:", resp.status_code)
    try:
        print("Response JSON (truncated):", resp.json())
    except Exception:
        print("Response text (truncated):", resp.text[:800])
except Exception as e:
    print("Request error:", e)
