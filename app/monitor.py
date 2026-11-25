import json

import config
import telegram_notifier


def process(current: dict):
    """Сравнивает текущее состояние с прошлым снимком и шлёт уведомления."""
    previous = _load_snapshot()

    if previous is None:
        _save_snapshot(current)
        telegram_notifier.send(
            f"Мониторинг запущен. ПВЗ с заказами сейчас: {len(current)}"
        )
        return
# убрать лишние пвз до цикла чтобы не считать их заказы
    offices = []
    targets = config.load_targets()
    for office, qty in current.items():
        old_qty = previous.get(office, 0)
        diff = qty - old_qty
        if diff > 0:
            offices.append(office)
    
    telegram_notifier.send(
        "🆕 Новые заказы:"
        f"{'\n'.join(offices)}"
    )

    _save_snapshot(current)


def _load_snapshot() -> dict | None:
    if not config.SNAPSHOT_FILE.exists():
        return None
    return json.loads(config.SNAPSHOT_FILE.read_text(encoding="utf-8"))


def _save_snapshot(offices: dict) -> None:
    config.SNAPSHOT_FILE.write_text(
        json.dumps(offices, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )