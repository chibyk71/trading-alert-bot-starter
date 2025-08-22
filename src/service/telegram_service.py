import logging
import requests
from src.config.setting import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram bot token or chat ID is not set.")

    def send_message(self, message: str):
        if not self.bot_token or not self.chat_id:
            logger.error("Cannot send Telegram message: Missing bot token or chat ID.")
            return False

        try:
            response = requests.post(self.api_url, json={"chat_id": self.chat_id, "text": message})
            response.raise_for_status()
            logger.info(f"Message sent to Telegram: {message}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

telegram_service = TelegramService()
