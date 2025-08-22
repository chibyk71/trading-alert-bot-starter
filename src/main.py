import time
from src.config.setting import settings
from src.service.telegram_service import TelegramService
from src.service.exchange_service import ExchangeService
from src.analysis.signal_generator import generate_signals
from src.utils.logger import logger

def main():
    logger.info("Starting Trading Bot...")

    telegram = TelegramService()
    exchange = ExchangeService()

    while True:
        try:
            # Fetch latest market data
            df = exchange.get_ohlcv(settings.SYMBOLS, settings.TIMEFRAME)

            if df.empty:
                logger.warning("No data received from exchange.")
                time.sleep(int(settings.TIMEFRAME) * 60)
                continue

            # Generate trading signal
            signal = generate_signals(df)
            logger.info(f"Signal for {settings.SYMBOLS}: {signal}")

            # Notify via Telegram if signal is strong
            if signal in ["STRONG_BUY", "STRONG_SELL"]:
                message = f"🚨 {settings.SYMBOLS} Signal: {signal}\nLast Price: {df['close'].iloc[-1]}"
                telegram.send_message(message)
                logger.info(f"Sent Telegram alert: {message}")

        except Exception as e:
            logger.error(f"Error in main loop: {e}")

        # Wait before polling again
        time.sleep(int(settings.TIMEFRAME) * 60)


if __name__ == "__main__":
    main()
