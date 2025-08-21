
import pandas as pd
import pandas_ta as ta

def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expects columns: ['open','high','low','close','volume']
    Returns df with RSI, EMA 20/50 and MACD columns appended.
    """
    out = df.copy()
    out['rsi'] = ta.rsi(out['close'], length=14)
    out['ema20'] = ta.ema(out['close'], length=20)
    out['ema50'] = ta.ema(out['close'], length=50)
    macd = ta.macd(out['close'])
    out['macd'] = macd['MACD_12_26_9']
    out['macd_signal'] = macd['MACDs_12_26_9']
    out['macd_hist'] = macd['MACDh_12_26_9']
    return out
