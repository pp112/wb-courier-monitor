import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TARGETS_FILE = BASE_DIR / "targets.txt"

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WB_URL = os.environ["WB_URL"]
AUTH_FILE = BASE_DIR / "auth.json"
WB_HEADERS = json.loads(os.environ["WB_HEADERS"])

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))


def load_targets() -> list[str]:
    if not TARGETS_FILE.exists():
        return []
    lines = TARGETS_FILE.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines]


def load_auth() -> dict | None:
    if AUTH_FILE.exists():
        return json.loads(AUTH_FILE.read_text(encoding="utf-8"))
    return None
