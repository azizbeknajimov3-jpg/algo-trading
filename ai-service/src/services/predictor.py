import numpy as np
import pandas as pd
from typing import Dict, Any, List
import random
from ..models.lstm_model import LSTMModel
from ..models.transformer_model import TransformerModel

class Predictor:
    def __init__(self):
        self.models = {}
        self.current_model_type = "mock"  # Can be "lstm", "transformer", or "mock"
    
    def predict(self, symbol: str) -> Dict[str, Any]:
        if self.current_model_type == "mock":
            return self._mock_prediction(symbol)
        
        # For real models, ensure we have a trained model for this symbol
        if symbol not in self.models:
            self._train_model(symbol)
        
        # Placeholder for real prediction logic
        return self.models[symbol].predict(symbol)
    
    def train(self, symbol: str, data: List[Dict] = None):
        """Train model for a specific symbol"""
        if not data:
            data = self._generate_training_data()
        
        if self.current_model_type == "lstm":
            self.models[symbol] = LSTMModel()
        elif self.current_model_type == "transformer":
            self.models[symbol] = TransformerModel()
        
        self.models[symbol].train(data)
    
    def _mock_prediction(self, symbol: str) -> Dict[str, Any]:
        """Generate mock predictions for testing"""
        predictions = ["buy", "sell", "hold"]
        prediction = random.choice(predictions)
        
        return {
            "prediction": prediction,
            "confidence": round(random.uniform(0.5, 0.99), 2),
            "symbol": symbol,
            "timestamp": int(pd.Timestamp.now().timestamp() * 1000)
        }
    
    def _generate_training_data(self):
        """Generate mock training data"""
        # This would be replaced with real data loading in production
        return []