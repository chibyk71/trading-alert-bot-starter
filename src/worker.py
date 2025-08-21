
import asyncio
import logging
import pandas as pd
from collections import defaultdict
from .config import settings
from .exchanges.bybit_ws import BybitKlineStream
from .indicators import compute_indicators
from .strategy.basic_cross import BasicCrossStrategy
from .notify.telegram import TelegramNotifier
from .storage import create_db_and_tables, Candle, Signal, get_session

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL, "INFO"))
log = logging.getLogger("worker")

async def main():
    create_db_and_tables()
    symbols = [s.strip() for s in settings.SYMBOLS.split(",") if s.strip()]
    stream = BybitKlineStream(symbols, settings.INTERVAL, env=settings.BYBIT_ENV)
    notifier = TelegramNotifier()
    strategy = BasicCrossStrategy()

    # Keep a small rolling dataframe per symbol
    frames = defaultdict(lambda: pd.DataFrame(columns=[
        "open","high","low","close","volume","start","end","confirm"
    ]))

    async for ev in stream.run():
        sym = ev["symbol"]
        df = frames[sym]

        # upsert by candle 'end' timestamp
        if (df["end"] == ev["end"]).any():
            df.loc[df["end"] == ev["end"], ["open","high","low","close","volume","start","confirm"]] = [
                ev["open"], ev["high"], ev["low"], ev["close"], ev["volume"], ev["start"], ev["confirm"]
            ]
        else:
            df.loc[len(df)] = [ev["open"], ev["high"], ev["low"], ev["close"], ev["volume"], ev["start"], ev["end"], ev["confirm"]]

        # Keep last N candles to limit memory
        frames[sym] = df.tail(600).reset_index(drop=True)
        df_ind = compute_indicators(frames[sym].copy())

        # Only act on confirmed candle closes
        if bool(ev["confirm"]):
            sig = strategy.on_candle(df_ind)
            if sig:
                msg = f"[{sym} {settings.INTERVAL}m] {sig.side} — {sig.reason} @ close={ev['close']:.2f}"
                log.info(msg)
                notifier.send_text(msg)
                # persist
                with get_session() as s:
                    s.add(Signal(symbol=sym, interval=settings.INTERVAL, side=sig.side, reason=sig.reason, ts=ev["end"]))
                    s.commit()

            # also persist candle (optional)
            with get_session() as s:
                s.add(Candle(symbol=sym, interval=settings.INTERVAL, start=ev["start"], end=ev["end"],
                             open=ev["open"], high=ev["high"], low=ev["low"], close=ev["close"],
                             volume=ev["volume"], confirm=ev["confirm"]))
                s.commit()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
