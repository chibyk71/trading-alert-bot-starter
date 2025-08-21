
from abc import ABC, abstractmethod
from typing import Optional

class SignalOut:
    def __init__(self, side: str, reason: str):
        self.side = side  # 'LONG' | 'SHORT' | 'FLAT'
        self.reason = reason

    def __repr__(self):
        return f"SignalOut(side={self.side}, reason={self.reason})"

class Strategy(ABC):
    @abstractmethod
    def on_candle(self, df) -> Optional[SignalOut]:
        ...
