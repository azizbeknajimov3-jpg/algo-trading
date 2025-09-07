import MetaTrader5 as mt5
from typing import Dict, Any
import os

class ForexBroker:
    def __init__(self):
        self.initialized = self._initialize_mt5()
    
    def _initialize_mt5(self):
        try:
            if not mt5.initialize():
                print("MT5 initialization failed")
                return False
            
            login = os.getenv("MT5_LOGIN")
            password = os.getenv("MT5_PASSWORD")
            server = os.getenv("MT5_SERVER")
            
            if login and password:
                authorized = mt5.login(int(login), password, server)
                if not authorized:
                    print("MT5 login failed")
                    return False
            return True
        except Exception as e:
            print(f"MT5 initialization error: {e}")
            return False
    
    async def place_order(self, symbol: str, side: str, amount: float, order_type: str, price: float = None):
        try:
            if not self.initialized:
                # Mock order for testing
                return {
                    "order_id": f"mt5_mock_{int(datetime.now().timestamp())}",
                    "status": "filled",
                    "symbol": symbol,
                    "side": side,
                    "amount": amount,
                    "filled": amount,
                    "price": price or self.get_current_price(symbol)
                }
            
            order_type = mt5.ORDER_TYPE_BUY if side == "buy" else mt5.ORDER_TYPE_SELL
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": amount,
                "type": order_type,
                "price": price or mt5.symbol_info_tick(symbol).ask if side == "buy" else mt5.symbol_info_tick(symbol).bid,
                "deviation": 20,
                "magic": 234000,
                "comment": "AI-Tradingview-Core",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_FOK,
            }
            
            result = mt5.order_send(request)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                raise Exception(f"MT5 order failed: {result.comment}")
            
            return {
                "order_id": str(result.order),
                "status": "filled",
                "symbol": symbol,
                "side": side,
                "amount": amount,
                "filled": amount,
                "price": result.price
            }
            
        except Exception as e:
            raise Exception(f"Forex order placement failed: {str(e)}")
    
    def get_current_price(self, symbol: str):
        try:
            if self.initialized:
                tick = mt5.symbol_info_tick(symbol)
                return (tick.ask + tick.bid) / 2
            return random.uniform(1.0, 2.0)  # Mock price
        except:
            return random.uniform(1.0, 2.0)