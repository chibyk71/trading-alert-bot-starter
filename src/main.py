import asyncio
from dotenv import load_dotenv
from alerts import send_telegram_alert
from indicators import simple_moving_average

# later you’ll plug in live broker data instead of dummy candles
import random

load_dotenv()

async def main():
    print("📈 Trading bot started...")

    # Dummy loop to simulate price data
    candles = [random.randint(90, 110) for _ in range(20)]

    # Example: calculate SMA(5)
    sma = simple_moving_average(candles, period=5)
    print(f"SMA(5): {sma}")

    # Example alert
    await send_telegram_alert("🚨 Example alert: SMA(5) calculated.")

if __name__ == "__main__":
    asyncio.run(main())
