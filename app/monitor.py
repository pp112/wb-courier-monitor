import logging

from app import config, notifier

log = logging.getLogger(__name__)


def process(
    tasks_count: dict[str, int], 
    previous: dict[str, int] | None,
) -> dict[str, int]:
    """
    Сравнивает текущее состояние с прошлым снимком и шлёт уведомления.
    """
    current = _filter_targets(tasks_count, config.load_targets())
    
    if previous is None:
        notifier.send(f"Мониторинг запущен. ПВЗ с заказами сейчас: {len(current)}")
        return current

    lines = []
    for address, qty in current.items():
        old_qty = previous.get(address, 0)
        if qty > old_qty:
            lines.append(f"📍 {address}: +{qty - old_qty} (всего {qty})")

    if lines:
        notifier.send("🆕 Новые задания:\n" + "\n".join(lines))
        log.info("Уведомление отправлено, ПВЗ: %s", len(lines))

    return current



def _filter_targets(task_counts: dict[str, int], targets: list[str]) -> dict[str, int]:
    if not targets:
        return task_counts
    return {
        addr: qty
        for addr, qty in task_counts.items()
        if any(t.lower() in addr.lower() for t in targets)
    }
