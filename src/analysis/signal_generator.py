import pandas as pd

def generate_signals(df: pd.DataFrame) -> str:
    """
    Generate simple Buy/Sell/Neutral signals based on:
    - RSI (<30 = Buy, >70 = Sell)
    - MACD crossover
    - EMA trend confirmation (close > EMA50 > EMA200 = bullish)
    """

    if df.empty or len(df) < 200:
        return "NEUTRAL"

    latest = df.iloc[-1]

    # --- RSI Signal ---
    rsi_signal = "BUY" if latest["rsi"] < 30 else "SELL" if latest["rsi"] > 70 else "NEUTRAL"

    # --- MACD Signal ---
    macd_signal = (
        "BUY" if latest["macd"] > latest["macd_signal"]
        else "SELL" if latest["macd"] < latest["macd_signal"]
        else "NEUTRAL"
    )

    # --- EMA Trend ---
    ema_trend = (
        "BULLISH" if latest["close"] > latest["ema_50"] > latest["ema_200"]
        else "BEARISH" if latest["close"] < latest["ema_50"] < latest["ema_200"]
        else "NEUTRAL"
    )

    # --- Final Signal Logic ---
    if rsi_signal == "BUY" and macd_signal == "BUY" and ema_trend == "BULLISH":
        return "STRONG_BUY"
    elif rsi_signal == "SELL" and macd_signal == "SELL" and ema_trend == "BEARISH":
        return "STRONG_SELL"
    else:
        return "NEUTRAL"
