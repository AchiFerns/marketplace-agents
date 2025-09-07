# src/agents/negotiation_agent.py
"""
Negotiation Agent
Now independent of asking_price:
- Uses neutral baseline to estimate fair range.
- Buyer offers midpoint of fair range.
- Seller starts at their asking price.
- Final agreed price = midpoint between buyer offer and seller offer.
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

def negotiate_price(product: dict) -> dict:
    # choose a neutral baseline
    baseline = BASELINES.get(product.get("category"), 20000)

    # clone product but override asking_price for fair range calc
    neutral_product = {**product, "asking_price": baseline}

    # estimate fair range
    fair_range = suggest_price(neutral_product)
    min_price = fair_range.get("suggested_price_min", 0)
    max_price = fair_range.get("suggested_price_max", 0)

    asking = product.get("asking_price", 0)

    # buyer offer = midpoint of fair range
    buyer_offer = int((min_price + max_price) / 2)

    # seller starts with their asking price
    seller_offer = asking

    # final deal = midpoint between seller and buyer
    agreed_price = int((buyer_offer + seller_offer) / 2)

    return {
        "seller_initial": seller_offer,
        "buyer_offer": buyer_offer,
        "final_agreed_price": agreed_price,
        "suggested_range": f"{min_price} - {max_price}"
    }
