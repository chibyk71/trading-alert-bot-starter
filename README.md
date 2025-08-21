
# Trading Analysis Alert Bot (Starter)

An opinionated Python starter for a real-time trading analysis bot that:
- Subscribes to Bybit unified-contract **kline** WebSocket (default: 1m candles).
- Computes indicators (RSI, EMA, MACD) with `pandas` + `pandas-ta`.
- Generates simple, configurable signals.
- Sends alerts to Telegram.
- Exposes a small FastAPI endpoint to check health and push manual test signals.

> ⚠️ Educational starter. Not financial advice. Trade at your own risk.

## Features
- Async consumer per symbol/timeframe
- Pluggable strategies (see `src/strategy/basic_cross.py`)
- Exchange abstraction to add Binance/OANDA/Alpaca later
- Minimal persistence with SQLite (via SQLModel) for signals & candles
- `.env` configuration
- Ready to run on Bybit **testnet** by default

## Quickstart
1. **Python 3.11+** recommended
2. Install system deps (on Debian/Ubuntu):
   ```bash
   sudo apt-get update && sudo apt-get install -y python3-dev build-essential
   ```
3. Create venv & install:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -U pip
   pip install -r requirements.txt
   ```
4. Copy env and edit:
   ```bash
   cp .env.example .env
   # set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, etc.
   ```
5. Run the API (optional) and the worker:
   ```bash
   uvicorn src.api:app --reload --port 8080
   python -m src.worker
   ```

## Project Structure
```text
src/
  api.py                # FastAPI app
  config.py             # settings loader
  exchanges/
    bybit_ws.py         # Bybit WebSocket client (kline)
  indicators.py         # Indicator helpers (RSI, EMA, MACD)
  strategy/
    base.py             # Interface
    basic_cross.py      # Example strategy
  notify/
    telegram.py         # Telegram notifier
  storage.py            # SQLModel setup for candles & signals
  worker.py             # Orchestrates everything
```

## Extending
- Add more indicators in `indicators.py`
- Create new strategies in `src/strategy/`
- To support another broker, add a new client under `src/exchanges/` and plug it in `worker.py`

## License
MIT
