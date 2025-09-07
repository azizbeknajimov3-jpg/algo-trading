from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import datetime
import random

router = APIRouter()

class OHLCVData(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float

def generate_mock_ohlcv(symbol: str, timeframe: str = "1h", limit: int = 100):
    base_price = random.uniform(100, 1000)
    data = []
    current_time = int(datetime.datetime.now().timestamp() * 1000)
    
    for i in range(limit):
        timestamp = current_time - (i * 3600000)  # 1 hour intervals
        open_price = base_price * (1 + random.uniform(-0.02, 0.02))
        high_price = open_price * (1 + random.uniform(0, 0.03))
        low_price = open_price * (1 - random.uniform(0, 0.03))
        close_price = (high_price + low_price) / 2 * (1 + random.uniform(-0.01, 0.01))
        volume = random.uniform(100, 1000)
        
        data.append({
            "timestamp": timestamp,
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": round(volume, 2)
        })
    
    return data[::-1]  # Return oldest first

@router.get("/{symbol}", response_model=List[OHLCVData])
async def get_chart_data(
    symbol: str,
    timeframe: str = Query("1h", regex="^(1m|5m|15m|1h|4h|1d)$"),
    limit: int = Query(100, ge=1, le=1000)
):
    try:
        # In production, this would fetch from exchange or database
        data = generate_mock_ohlcv(symbol, timeframe, limit)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chart data: {str(e)}")