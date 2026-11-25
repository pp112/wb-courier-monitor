import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
TARGETS_FILE = BASE_DIR / "targets.txt"
SNAPSHOT_FILE = BASE_DIR / "data" / "snapshot.json"

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WB_URL = os.environ["WB_URL"]
WB_HEADERS = json.loads(os.environ["WB_HEADERS"])

POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))


def load_targets() -> list[str]:
    if not TARGETS_FILE.exists():
        return []
    lines = TARGETS_FILE.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines]
