import requests

import config


def send(text: str) -> None:
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": config.TELEGRAM_CHAT_ID, "text": text},
            timeout=15,
        )
        if not r.ok:
            print("Telegram %s: %s", r.status_code, r.text)
    except requests.RequestException:
        print("Ошибка отправки в Telegram")
