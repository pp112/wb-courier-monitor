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

    try:
        while True:
            try:
                snapshot = monitor.process(
                    wb_client.fetch_task_counts(), snapshot
                )
            except wb_client.AuthError as e:
                log.error(e)
                notifier.send(f"⚠️ {e}")
                break

            time.sleep(config.POLL_INTERVAL)
    finally:
        notifier.send("Мониторинг остановлен")
        log.info("Программа завершена")


if __name__ == "__main__":
    main()