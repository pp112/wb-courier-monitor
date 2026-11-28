import logging
import time

from app import config, monitor, wb_client, notifier


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

def main():
    log.info("Программа запущена")
    snapshot = None
    auth_notified = False
    try:
        while True:
            try:
                snapshot = monitor.process(
                    wb_client.fetch_task_counts(), snapshot
                )
                if auth_notified:
                    notifier.send("✅ Токен WB получен.")
                    auth_notified = False
                time.sleep(config.POLL_INTERVAL)
            except wb_client.AuthError as e:
                log.error(e)
                if not auth_notified:
                    notifier.send(f"⚠️ {e}")
                    auth_notified = True
                time.sleep(2)
    except Exception as e:
        log.error(f"Ошибка: {e}")
        notifier.send("Мониторинг остановлен")
        log.info("Программа завершена")


if __name__ == "__main__":
    main()