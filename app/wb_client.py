import logging

import requests

from app import config

log = logging.getLogger(__name__)


class AuthError(Exception):
    pass


def fetch_task_counts() -> dict[str, int]:
    """
    Возвращает {адрес ПВЗ: количество заданий}.
    """
    result: dict[str, int] = {}

    for item in _request_tasks():
        raw_address = item["src_office"]["address_name"]
        address = raw_address.partition("Новосибирск, ")[2] or raw_address
        total_qty = sum(task["qty"] for task in item["tasks"])
        result[address] = total_qty

    return result


def _request_tasks() -> list[dict]:
    r = requests.get(config.WB_URL, headers=_build_headers(), timeout=10)
    if r.status_code in (401, 403):
        raise AuthError(f"Нет доступа ({r.status_code}), возможно истёк токен")
    r.raise_for_status()
    log.info("Запрос к API WB выполнен успешно.")
    return r.json()


def _build_headers() -> dict:
    headers = dict(config.WB_HEADERS)
    headers["Authorization"] = f"Bearer {config.WB_TOKEN}"
    return headers