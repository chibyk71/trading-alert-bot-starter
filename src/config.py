
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"
    SYMBOLS: str = "BTCUSDT,ETHUSDT"
    INTERVAL: int = 1
    BYBIT_ENV: str = "testnet"  # 'testnet' or 'mainnet'
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    DB_URL: str = "sqlite:///./alerts.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
