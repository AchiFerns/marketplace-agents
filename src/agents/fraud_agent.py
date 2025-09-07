# src/agents/fraud_agent.py
"""
Fraud/Anomaly Detection Agent
Now independent of asking_price:
- Estimates fair range using neutral baseline.
- Compares seller's asking price to that fair range.
"""

from src.agents.price_agent import suggest_price

# neutral baselines per category
BASELINES = {
    "Mobile": 30000,
    "Laptop": 50000,
    "Furniture": 20000,
    "Electronics": 25000,
    "Camera": 30000,
    "Fashion": 5000,
}

def detect_fraud(product: dict) -> dict:
    # pick neutral baseline instead of seller's asking price
    baseline = BASELINES.get(product.get("category"), 20000)

    # clone product but override asking_price
    neutral_product = {**product, "asking_price": baseline}

    # estimate fair range
    fair_range = suggest_price(neutral_product)
    min_price = fair_range.get("suggested_price_min", 0)
    max_price = fair_range.get("suggested_price_max", 0)

    asking = product.get("asking_price", 0)

    status = "Safe"
    reason = "Asking price is within the expected range."

    if asking < 0.5 * min_price:
        status = "Suspicious"
        reason = f"Asking price ₹{asking} is more than 50% below the fair minimum ₹{min_price}. Possible scam listing."
    elif asking > 2.0 * max_price:
        status = "Suspicious"
        reason = f"Asking price ₹{asking} is more than 200% above the fair maximum ₹{max_price}. Overpriced listing."

    return {
        "status": status,
        "reason": reason,
        "asking_price": asking,
        "suggested_min": min_price,
        "suggested_max": max_price
    }
