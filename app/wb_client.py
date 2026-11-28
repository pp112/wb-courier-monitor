import logging

import requests

from app import config

log = logging.getLogger(__name__)

_rejected_auth = None


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
    global _rejected_auth

    headers, auth = _build_headers()
    r = requests.get(config.WB_URL, headers=headers, timeout=10)
    
    if r.status_code in (401, 403):
        _rejected_auth = auth
        raise AuthError("Данные авторизации устарели. Зайдите в приложение.")
    r.raise_for_status()

    log.info("Запрос к API WB выполнен успешно.")
    return r.json()


def _build_headers() -> tuple[dict, dict]:
    auth = config.load_auth()
    if not auth:
        raise AuthError("Данных авторизации нет. Зайдите в приложение.")
    if auth == _rejected_auth:
        raise AuthError("Данные авторизации устарели. Зайдите в приложение.")
    
    headers = {**config.WB_HEADERS, **auth}
    return headers, auth