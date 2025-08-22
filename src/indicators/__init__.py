import pandas_ta as ta

def add_indicators(df):
    """
    Adds key technical indicators to the DataFrame:
    - RSI (14)
    - MACD (12, 26, 9)
    - EMA (50, 200)
    - Bollinger Bands (20, 2)
    - ATR (14)
    """
    df["rsi"] = ta.rsi(df["close"], length=14)

    macd = ta.macd(df["close"], fast=12, slow=26, signal=9)
    if macd is not None:
        df["macd"] = macd["MACD_12_26_9"]
        df["macd_signal"] = macd["MACDs_12_26_9"]
        df["macd_hist"] = macd["MACDh_12_26_9"]
    else:
        df["macd"] = None
        df["macd_signal"] = None
        df["macd_hist"] = None

    df["ema_50"] = ta.ema(df["close"], length=50)
    df["ema_200"] = ta.ema(df["close"], length=200)

    bb = ta.bbands(df["close"], length=20, std=2)
    if bb is not None:
        df["bb_upper"] = bb["BBU_20_2.0"]
        df["bb_middle"] = bb["BBM_20_2.0"]
        df["bb_lower"] = bb["BBL_20_2.0"]
    else:
        df["bb_upper"] = None
        df["bb_middle"] = None
        df["bb_lower"] = None

    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)

    return df
