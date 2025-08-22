import logging
import requests
from src.config.setting import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExchangeService:
    BASE_URL = "https://api.binance.com/api/v3"

    from typing import Optional

    def __init__(self, symbol: Optional[str] = None, timeframe: Optional[str] = None):
        self.symbol = symbol or settings.SYMBOL
        self.timeframe = timeframe or settings.TIMEFRAME

    def get_klines(self, limit: int = 100):
        """
        Fetch candlestick (OHLCV) data.
        :param limit: Number of candles to retrieve.
        :return: List of candlestick data.
        """
        url = f"{self.BASE_URL}/klines"
        params = {"symbol": self.symbol.upper(), "interval": self.timeframe, "limit": limit}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Fetched {len(data)} candles for {self.symbol} ({self.timeframe})")
            return data
        except requests.RequestException as e:
            logger.error(f"Error fetching candlestick data: {e}")
            return []

    def get_current_price(self):
        """
        Fetch the latest market price.
        :return: Current price as float or None if failed.
        """
        url = f"{self.BASE_URL}/ticker/price"
        params = {"symbol": self.symbol.upper()}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            price = float(response.json()["price"])
            logger.info(f"Current price of {self.symbol}: {price}")
            return price
        except requests.RequestException as e:
            logger.error(f"Error fetching current price: {e}")
            return None

exchange_service = ExchangeService()
