# src/llm_client.py
"""
Unified LLM client for Hugging Face and Groq.
"""

import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "none").lower()

if LLM_PROVIDER == "groq":
    from src.groq_client import ask
elif LLM_PROVIDER == "huggingface":
    from src.hf_client import ask   # <- we'll rename your old HF code into hf_client.py
else:
    def ask(prompt: str, model: str = None, max_tokens: int = 120) -> str:
        return "LLM disabled. Set LLM_PROVIDER in .env"
