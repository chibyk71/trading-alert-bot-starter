import pandas as pd
import requests
from src.utils.logger import logger

class ExchangeService:
    BASE_URL = "https://api.binance.com/api/v3"

    def get_klines(self, symbol: str, interval: str, limit: int = 100):
        url = f"{self.BASE_URL}/klines"
        params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to fetch klines: {e}")
            return []

    def get_ohlcv(self, symbol: str, interval: str, limit: int = 100) -> pd.DataFrame:
        """
        Returns OHLCV data as a pandas DataFrame with columns:
        [timestamp, open, high, low, close, volume]
        """
        data = self.get_klines(symbol, interval, limit)
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades", 
            "taker_buy_base", "taker_buy_quote", "ignore"
        ])

        df = df[["open_time", "open", "high", "low", "close", "volume"]].copy()
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        return df.rename(columns={"open_time": "timestamp"})
