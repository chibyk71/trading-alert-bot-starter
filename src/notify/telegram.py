
import httpx
import logging
from ..config import settings

class TelegramNotifier:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base = f"https://api.telegram.org/bot{self.token}" if self.token else None
        self.logger = logging.getLogger("TelegramNotifier")

    def send_text(self, text: str):
        if not self.base or not self.chat_id:
            self.logger.warning("Telegram not configured; skipping send")
            return
        url = f"{self.base}/sendMessage"
        try:
            httpx.post(url, data={"chat_id": self.chat_id, "text": text}, timeout=10.0)
        except Exception as e:
            self.logger.exception(f"Telegram send failed: {e}")
