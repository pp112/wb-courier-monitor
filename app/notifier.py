import logging

import requests

from app import config

log = logging.getLogger(__name__)


def send(text: str) -> None:
    """
    Отправляет уведомление в telegram-бот
    """
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text},
            timeout=15,
        )
        if not r.ok:
            log.error("Telegram %s: %s", r.status_code, r.text)
    except requests.RequestException:
        log.exception("Ошибка отправки в Telegram")
