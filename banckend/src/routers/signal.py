from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
from ...services.ai_predictor import AIPredictor

router = APIRouter()

class SignalResponse(BaseModel):
    prediction: Literal["buy", "sell", "hold"]
    confidence: float
    symbol: str
    timestamp: int

@router.get("/{symbol}")
async def get_signal(symbol: str):
    try:
        predictor = AIPredictor()
        signal = await predictor.get_prediction(symbol)
        return SignalResponse(**signal)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching signal: {str(e)}")