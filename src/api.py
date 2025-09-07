# src/api.py
"""
FastAPI app exposing multiple agents:
- GET /               -> health check
- POST /negotiate     -> price suggestion
- POST /moderate      -> chat moderation
- POST /fraud-check   -> fraud/anomaly detection
- POST /negotiate-deal -> buyer-seller negotiation

Protected with a simple API key header:
  x-api-key: <API_KEY>
"""

import os
import logging
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from fastapi.concurrency import run_in_threadpool

# Agents
from src.agents.price_agent import suggest_price
from src.agents.moderation_agent import moderate_message
from src.agents.fraud_agent import detect_fraud
from src.agents.negotiation_agent import negotiate_price

# --- API key setup ---
API_KEY = os.getenv("API_KEY", "devkey123")

async def check_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

# --- Logging setup ---
logger = logging.getLogger("marketplace-agents")
logging.basicConfig(level=logging.INFO)

# --- FastAPI app ---
app = FastAPI(title="Marketplace Agents API", version="0.2")

# --- Pydantic Models ---
class ProductIn(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    condition: Optional[str] = None
    age_months: Optional[int] = Field(default=0, ge=0)
    asking_price: Optional[float] = Field(default=0.0, ge=0.0)
    location: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


class PriceOut(BaseModel):
    suggested_price_min: int
    suggested_price_max: int
    reason: str
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None


class ModerateIn(BaseModel):
    message: str


class ModerateOut(BaseModel):
    status: str
    reason: str
    labels: Optional[list] = []
    confidence: Optional[float] = None
    llm_status: Optional[str] = None
    llm_reason: Optional[str] = None
    llm_labels: Optional[list] = None

# --- Endpoints ---

@app.get("/", summary="Health check")
async def root():
    return {"status": "ok", "project": "marketplace-agents"}


@app.post("/negotiate", response_model=PriceOut)
async def negotiate(product: ProductIn, _=Depends(check_api_key)):
    """Suggest a price range for a product."""
    try:
        result = await run_in_threadpool(suggest_price, product.dict())
    except Exception as e:
        logger.exception("Error in negotiate")
        raise HTTPException(status_code=500, detail=str(e))

    if "suggested_price_min" not in result or "suggested_price_max" not in result:
        raise HTTPException(status_code=500, detail="Agent returned invalid response")

    return result


@app.post("/moderate", response_model=ModerateOut)
async def moderate(payload: ModerateIn, _=Depends(check_api_key)):
    """Moderate a chat message."""
    try:
        res = await run_in_threadpool(moderate_message, payload.message)
    except Exception as e:
        logger.exception("Error in moderate")
        raise HTTPException(status_code=500, detail=str(e))

    if "status" not in res:
        raise HTTPException(status_code=500, detail="Moderation agent returned invalid response")

    return res


@app.post("/fraud-check")
async def fraud_check(product: ProductIn, _=Depends(check_api_key)):
    """Check if the asking price looks suspicious compared to fair range."""
    try:
        result = await run_in_threadpool(detect_fraud, product.dict())
        return result
    except Exception as e:
        logger.exception("Error in fraud_check")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/negotiate-deal")
async def negotiate_deal(product: ProductIn, _=Depends(check_api_key)):
    """Simulate buyer-seller negotiation."""
    try:
        result = await run_in_threadpool(negotiate_price, product.dict())
        return result
    except Exception as e:
        logger.exception("Error in negotiate_deal")
        raise HTTPException(status_code=500, detail=str(e))


