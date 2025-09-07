from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter()

class BacktestRequest(BaseModel):
    strategy: str
    symbol: str
    timeframe: str
    start_date: str
    end_date: str
    initial_balance: float
    parameters: Optional[dict] = None

class BacktestResult(BaseModel):
    total_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    trades: int
    final_balance: float
    equity_curve: List[dict]

@router.post("", response_model=BacktestResult)
async def run_backtest(request: BacktestRequest):
    try:
        # Mock backtest results - integrate with backtrader or jesse in production
        mock_result = {
            "total_return": 15.5,
            "sharpe_ratio": 1.8,
            "max_drawdown": -8.2,
            "win_rate": 65.3,
            "trades": 42,
            "final_balance": request.initial_balance * 1.155,
            "equity_curve": generate_mock_equity_curve(request)
        }
        return BacktestResult(**mock_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")

def generate_mock_equity_curve(request: BacktestRequest):
    # Generate mock equity curve data
    curve = []
    start_balance = request.initial_balance
    current_balance = start_balance
    
    for i in range(100):
        current_balance *= (1 + random.uniform(-0.02, 0.03))
        curve.append({
            "timestamp": int((datetime.datetime.now() - datetime.timedelta(days=100-i)).timestamp() * 1000),
            "balance": round(current_balance, 2)
        })
    
    return curve