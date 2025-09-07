# src/agents/price_agent.py
"""
Price Suggestor Agent (Rule-based + optional LLM explanation)
Includes LLM provider/model info in output when USE_LLM=true.
"""

import os
from src.llm_client import ask

def _get_llm_info():
    prov = os.getenv("LLM_PROVIDER", "none")
    # Groq uses GROQ_MODEL, HF uses HF_MODEL
    if prov == "groq":
        model = os.getenv("GROQ_MODEL", "")
    elif prov == "huggingface":
        model = os.getenv("HF_MODEL", "")
    else:
        model = ""
    return prov, model

def suggest_price(product: dict) -> dict:
    base = float(product.get("asking_price", 0))
    age = int(product.get("age_months", 0))
    condition = product.get("condition", "Good")
    category = product.get("category", "Other")
    brand = product.get("brand", "").lower()

    rates = {
        "Mobile": 0.012,
        "Laptop": 0.009,
        "Furniture": 0.005,
        "Electronics": 0.008,
        "Fashion": 0.015,
        "Camera": 0.009,
    }
    rate = rates.get(category, 0.01)
    depreciated = base * ((1 - rate) ** age)
    condition_mult = {"Like New": 1.05, "Good": 0.95, "Fair": 0.80}
    adjusted = depreciated * condition_mult.get(condition, 1.0)
    if brand in ["apple", "sony", "nike", "adidas"]:
        adjusted *= 1.05

    low = int(adjusted * 0.88)
    high = int(adjusted * 1.12)

    reason = (
        f"Suggested based on asking price {base}, "
        f"category {category} (rate {rate*100:.2f}%/month), "
        f"age {age} months, condition {condition}, brand {brand.title()}."
    )

    llm_used = None
    if os.getenv("USE_LLM", "false").lower() in ("1", "true", "yes"):
        prov, model = _get_llm_info()
        prompt = f"""
Product details: {product}
Suggested price range: ₹{low} - ₹{high}.
Write 2 short friendly sentences explaining why this range is fair (mention age, condition, brand).
"""
        try:
            llm_text = ask(prompt)
            reason = llm_text.strip() if llm_text else reason
        except Exception:
            # fallback to rule-based reason
            pass
        llm_used = {"provider": prov, "model": model}

    out = {
        "suggested_price_min": low,
        "suggested_price_max": high,
        "reason": reason
    }
    if llm_used:
        out["llm_provider"] = llm_used["provider"]
        out["llm_model"] = llm_used["model"]
    return out

if __name__ == "__main__":
    sample = {
        "title": "iPhone 12",
        "category": "Mobile",
        "brand": "Apple",
        "condition": "Good",
        "age_months": 24,
        "asking_price": 35000,
        "location": "Mumbai"
    }
    print(suggest_price(sample))
