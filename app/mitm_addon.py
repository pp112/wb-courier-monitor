import json
from pathlib import Path

from mitmproxy import ctx, http

HOST = "courier.wb.ru"
PATH = "/mobile-api/delivery-api-proxy/api/v2/delivery/find-free-tasks-by-coords"
CAPTURE_HEADERS = ["Authorization", "x-timestamp", "x-signature", "X-Coordinates"]
AUTH_FILE = Path(__file__).parent.parent / "auth.json"

_last = None

def request(flow: http.HTTPFlow) -> None:
    global _last

    req = flow.request
    if req.pretty_host != HOST or not req.path.startswith(PATH):
        return
    if not req.get("Authorization", "").startswith("Bearer "):
        return

    data = {
        h: req.headers[h] for h in CAPTURE_HEADERS if h in req.headers
    }
    if data == _last:
        return

    tmp = AUTH_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
    tmp.replace(AUTH_FILE)

    _last = data
    ctx.log.info("Данные авторизации обновлены в auth.json")
