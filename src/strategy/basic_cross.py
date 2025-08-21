
from .base import Strategy, SignalOut

class BasicCrossStrategy(Strategy):
    """
    Example logic (tweak as desired):
    - Bullish if close > ema20 > ema50 and RSI rising from < 40 to > 50
    - Bearish if close < ema20 < ema50 and RSI falling from > 60 to < 50
    - Else FLAT
    """
    def on_candle(self, df):
        if len(df) < 60:
            return None
        row = df.iloc[-1]
        prev = df.iloc[-2]

        # Guards
        if row[['ema20','ema50','rsi']].isna().any():
            return None

        bull_stack = row['close'] > row['ema20'] > row['ema50']
        bear_stack = row['close'] < row['ema20'] < row['ema50']

        rsi_up = prev['rsi'] < 40 and row['rsi'] > 50
        rsi_down = prev['rsi'] > 60 and row['rsi'] < 50

        macd_cross_up = prev['macd'] <= prev['macd_signal'] and row['macd'] > row['macd_signal']
        macd_cross_dn = prev['macd'] >= prev['macd_signal'] and row['macd'] < row['macd_signal']

        if bull_stack and (rsi_up or macd_cross_up):
            return SignalOut('LONG', 'Bull stack + momentum up')
        if bear_stack and (rsi_down or macd_cross_dn):
            return SignalOut('SHORT', 'Bear stack + momentum down')
        return SignalOut('FLAT', 'No clear edge')
