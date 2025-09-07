import requests
from typing import Dict, Any
import os
from ..config.settings import settings

class AIPredictor:
    def __init__(self):
        self.ai_service_url = os.getenv("AI_SERVICE_URL", "http://ai-service:5000")
    
    async def get_prediction(self, symbol: str) -> Dict[str, Any]:
        try:
            # Try to get prediction from AI service
            response = requests.get(f"{self.ai_service_url}/predict", params={"symbol": symbol})
            if response.status_code == 200:
                return response.json()
            
            # Fallback to mock prediction if AI service is unavailable
            return self._generate_mock_prediction(symbol)
            
        except Exception:
            return self._generate_mock_prediction(symbol)
    
    def _generate_mock_prediction(self, symbol: str) -> Dict[str, Any]:
        import random
        predictions = ["buy", "sell", "hold"]
        prediction = random.choice(predictions)
        
        return {
            "prediction": prediction,
            "confidence": round(random.uniform(0.5, 0.99), 2),
            "symbol": symbol,
            "timestamp": int(datetime.datetime.now().timestamp() * 1000)
        }