from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Literal, Optional
from ...services.broker_crypto import CryptoBroker
from ...services.broker_forex import ForexBroker
from ...utils.risk_management import validate_order_risk

router = APIRouter()

class OrderRequest(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    amount: float
    exchange: Literal["binance", "bybit", "okx", "mt5"]
    order_type: Literal["market", "limit"]
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class OrderResponse(BaseModel):
    order_id: str
    status: str
    symbol: str
    side: str
    amount: float
    filled: float
    price: Optional[float] = None

@router.post("", response_model=OrderResponse)
async def create_order(order: OrderRequest):
    try:
        # Validate order risk
        risk_validation = validate_order_risk(order)
        if not risk_validation["valid"]:
            raise HTTPException(status_code=400, detail=risk_validation["message"])
        
        # Route to appropriate broker
        if order.exchange in ["binance", "bybit", "okx"]:
            broker = CryptoBroker(order.exchange)
            result = await broker.place_order(
                symbol=order.symbol,
                side=order.side,
                amount=order.amount,
                order_type=order.order_type,
                price=order.price
            )
        elif order.exchange == "mt5":
            broker = ForexBroker()
            result = await broker.place_order(
                symbol=order.symbol,
                side=order.side,
                amount=order.amount,
                order_type=order.order_type,
                price=order.price
            )
        else:
            raise HTTPException(status_code=400, detail="Unsupported exchange")
        
        return OrderResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Order placement failed: {str(e)}")