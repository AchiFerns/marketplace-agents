# src/groq_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
BASE_URL = "https://api.groq.com/openai/v1"

def ask(prompt: str, model: str = None, max_tokens: int = 200) -> str:
    if not GROQ_KEY:
        return "No GROQ_API_KEY found in .env"

    url = f"{BASE_URL}/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}"}
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        if resp.status_code != 200:
            return f"Groq API error {resp.status_code}: {resp.text}"
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Groq request failed: {e}"
