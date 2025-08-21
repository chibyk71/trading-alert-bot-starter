
import asyncio
import json
import logging
import websockets

BYBIT_WS_ENDPOINTS = {
    "testnet": "wss://stream-testnet.bybit.com/v5/public/linear",
    "mainnet": "wss://stream.bybit.com/v5/public/linear",
}

class BybitKlineStream:
    def __init__(self, symbols, interval: int, env: str = "testnet"):
        self.symbols = symbols
        self.interval = interval
        self.env = env
        self.logger = logging.getLogger("BybitKlineStream")

    def _topic(self, symbol):
        # unified linear kline topic, e.g. kline.1.BTCUSDT
        return f"kline.{self.interval}.{symbol}"

    async def run(self):
        url = BYBIT_WS_ENDPOINTS[self.env]
        topics = [self._topic(s) for s in self.symbols]
        sub_msg = {
            "op": "subscribe",
            "args": topics
        }
        async for ws in websockets.connect(url, ping_interval=20):
            try:
                await ws.send(json.dumps(sub_msg))
                async for raw in ws:
                    msg = json.loads(raw)
                    # Yield only kline updates that contain 'data'
                    if msg.get("topic", "").startswith("kline.") and "data" in msg:
                        for item in msg["data"]:
                            # Standardize event
                            yield {
                                "symbol": item["symbol"],
                                "interval": item["interval"],
                                "start": int(item["start"]),
                                "end": int(item["end"]),
                                "open": float(item["open"]),
                                "high": float(item["high"]),
                                "low": float(item["low"]),
                                "close": float(item["close"]),
                                "volume": float(item.get("volume", 0)),
                                "confirm": bool(item.get("confirm", False)),
                            }
            except Exception as e:
                self.logger.exception(f"WS error: {e}; reconnecting in 3s")
                await asyncio.sleep(3)
                continue
