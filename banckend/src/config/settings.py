from pydantic import BaseSettings
from typing import List
import yaml
import os

class Settings(BaseSettings):
    # API Settings
    APP_NAME: str = "AI-Tradingview-Core"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    DISABLE_AUTH: bool = os.getenv("DISABLE_AUTH", "false").lower() == "true"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://frontend:3000"]
    
    # Trading Settings
    ALLOWED_SYMBOLS: List[str] = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "EUR/USD", "GBP/USD"]
    DEFAULT_EXCHANGE: str = "binance"
    MAX_ORDER_AMOUNT: float = 10000.0
    TESTNET: bool = os.getenv("TESTNET", "true").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Load YAML config if exists
def load_yaml_config():
    config_path = os.path.join(os.path.dirname(__file__), "settings.yaml")
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)
    return {}

yaml_config = load_yaml_config()