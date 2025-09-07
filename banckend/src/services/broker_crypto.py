import ccxt
from typing import Dict, Any
import os
from ..config.settings import settings

class CryptoBroker:
    def __init__(self, exchange: str):
        self.exchange_name = exchange
        self.exchange = self._initialize_exchange(exchange)
    
    def _initialize_exchange(self, exchange_name: str):
        exchange_class = getattr(ccxt, exchange_name)
        config = {
            'apiKey': os.getenv(f"{exchange_name.upper()}_API_KEY"),
            'secret': os.getenv(f"{exchange_name.upper()}_SECRET"),
            'sandbox': os.getenv("TESTNET", "true").lower() == "true",
            'enableRateLimit': True
        }
        return exchange_class(config)
    
    async def place_order(self, symbol: str, side: str, amount: float, order_type: str, price: float = None):
        try:
            # Mock order placement for testing
            if not self.exchange.apiKey:
                return {
                    "order_id": f"mock_{int(datetime.now().timestamp())}",
                    "status": "filled",
                    "symbol": symbol,
                    "side": side,
                    "amount": amount,
                    "filled": amount,
                    "price": price or await self.get_current_price(symbol)
                }
            
            order_params = {
                'symbol': symbol,
                'type': order_type,
                'side': side,
                'amount': amount
            }
            
            if order_type == 'limit' and price:
                order_params['price'] = price
            
            order = await self.exchange.create_order(**order_params)
            return order
            
        except Exception as e:
            raise Exception(f"Order placement failed: {str(e)}")
    
    async def get_current_price(self, symbol: str):
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            return ticker['last']
        except:
            # Return mock price if API not available
            return random.uniform(100, 1000)