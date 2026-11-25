import time

import requests

import config


class AuthError(Exception):
    pass


def fetch_offices():
    headers = config.WB_HEADERS
    headers["x-timestamp"] = int(time.time())

    r = requests.get(config.WB_URL, headers=headers, timeout=10)
    if r.status_code in (401, 403):
        raise AuthError(f"Нет доступа ({r.status_code}), возможно истёк токен")
    r.raise_for_status()

    result = {}
    for item in r.json():
        address_name = item["src_office"]["address_name"]
        qty = item["tasks"]
