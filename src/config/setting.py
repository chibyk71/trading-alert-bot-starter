import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    EXCHANGE_API_KEY: str = os.getenv("EXCHANGE_API_KEY", "")
    EXCHANGE_API_SECRET: str = os.getenv("EXCHANGE_API_SECRET", "")
    SYMBOL: str = os.getenv("SYMBOL", "BTCUSDT")
    TIMEFRAME: str = os.getenv("TIMEFRAME", "1m")

settings = Settings()
# --- IGNORE ---